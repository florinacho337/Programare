using System.Net.Sockets;
using System.Text;
using Model;
using Services;
using Newtonsoft.Json;

namespace Networking
{
    public class ZboruriServerProxy(string host, int port) : IZboruriServices
    {
        private IZboruriObserver _client;

        private NetworkStream _stream;
        
        private TcpClient _connection;

        private readonly Queue<Response> _responses = new();
        private volatile bool _finished;
        private EventWaitHandle _waitHandle;


        public virtual void Login(Angajat angajat, IZboruriObserver client1)
        {
            InitializeConnection();
            Request req = JsonProtocolUtils.CreateLoginRequest(angajat);
            SendRequest(req);
            Response response = ReadResponse();
            Console.WriteLine(response.Type);
            if (response.Type is ResponseType.Error)
            {
                CloseConnection();
                throw new ZboruriException(response.ErrorMessage);
            }

            this._client = client1;
        }

        public virtual void Logout(Angajat angajat, IZboruriObserver client)
        {
            Request req = JsonProtocolUtils.CreateLogoutRequest(angajat);
            SendRequest(req);
            Response response = ReadResponse();
            CloseConnection();
            if (response.Type is ResponseType.Error)
                throw new ZboruriException(response.ErrorMessage);
        }

        public virtual List<Zbor> FindZboruriDestDateAndMinSeats(string dest, DateTime data, int min)
        {
            Request req = JsonProtocolUtils.CreateGetFlightsDestDateSeatsRequest(dest, data, min);
            SendRequest(req);
            Response response = ReadResponse();
            if (response.Type is ResponseType.Error)
                throw new ZboruriException(response.ErrorMessage);
            return response.Flights;
        }

        public virtual List<Zbor> FindZboruri()
        {
            Request req = JsonProtocolUtils.CreateGetAllFlightsRequest();
            SendRequest(req);
            Response response = ReadResponse();
            if (response.Type is ResponseType.Error)
                throw new ZboruriException(response.ErrorMessage);
            return response.Flights;
            
        }

        public virtual void CumparaBilet(string client, string tara, string oras, List<TuristBilet> turisti, int nrLocuri, Zbor zbor)
        {
            Request req = JsonProtocolUtils.CreateBuyTicketRequest(client, tara, oras, turisti, nrLocuri, zbor);
            SendRequest(req);
            Response response = ReadResponse();
            if (response.Type is ResponseType.Error)
                throw new ZboruriException(response.ErrorMessage);
        }

        public virtual Zbor FindZbor(int id)
        {
            Request req = JsonProtocolUtils.CreateFindZborRequest(id);
            SendRequest(req);
            Response response = ReadResponse();
            if (response.Type is ResponseType.Error)
                throw new ZboruriException(response.ErrorMessage);
            return response.Found;
        }

        private void CloseConnection()
        {
            _finished = true;
            try
            {
                _stream.Close();

                _connection.Close();
                _waitHandle.Close();
                _client = null;
            }
            catch (Exception e)
            {
                Console.WriteLine(e.StackTrace);
            }
        }

        private void SendRequest(Request request)
        {
            try
            {
                string requestJson = JsonConvert.SerializeObject(request);
                requestJson += '\n';
                byte[] buffer = Encoding.UTF8.GetBytes(requestJson);
                _stream.Write(buffer, 0, buffer.Length);
                _stream.Flush();
            }
            catch (Exception e)
            {
                throw new ZboruriException("Error sending object " + e);
            }
        }

        private Response ReadResponse()
        {
            Response response = null;
            try
            {
                _waitHandle.WaitOne();
                lock (_responses)
                {
                    //Monitor.Wait(responses); 
                    response = _responses.Dequeue();
                }
            }
            catch (Exception e)
            {
                Console.WriteLine(e.StackTrace);
            }

            return response;
        }

        private void InitializeConnection()
        {
            try
            {
                _connection = new TcpClient(host, port);
                _stream = _connection.GetStream();
                _finished = false;
                _waitHandle = new AutoResetEvent(false);
                StartReader();
            }
            catch (Exception e)
            {
                Console.WriteLine(e.StackTrace);
            }
        }

        private void StartReader()
        {
            Thread tw = new Thread(Run);
            tw.Start();
        }
        
        private bool IsUpdate(Response response) {
            return response.Type is ResponseType.BuyTicket;
        }

        private void HandleUpdate(Response update)
        {
            if (update.Type is ResponseType.BuyTicket)
            {
                try
                {
                    _client.TicketBought(update.OldZbor, update.Zbor);
                }
                catch (ZboruriException e)
                {
                    Console.WriteLine(e.StackTrace);
                }
            }
        }
        
        private string ReadLine()
        {
            using (MemoryStream ms = new MemoryStream())
            {
                int byteRead;
                while ((byteRead = _stream.ReadByte()) != '\n')
                {
                    if (byteRead == -1)
                        throw new EndOfStreamException("End of stream reached before newline character was found.");
                    ms.WriteByte((byte)byteRead);
                }
                return Encoding.ASCII.GetString(ms.ToArray());
            }
        }

        public virtual void Run()
        {
            while (!_finished)
            {
                try
                {
                    string responseJson = ReadLine();
                    responseJson = responseJson.Trim();
                    Response response = JsonConvert.DeserializeObject<Response>(responseJson);
                    Console.WriteLine("response received " + response);
                    if (IsUpdate(response))
                    {
                        HandleUpdate(response);
                    }
                    else
                    {
                        lock (_responses)
                        {
                            _responses.Enqueue(response);
                        }

                        _waitHandle.Set();
                    }
                }
                catch (Exception e)
                {
                    Console.WriteLine("Reading error " + e);
                }
            }
        }
    }
}