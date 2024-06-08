using System.Net.Sockets;
using System.Text;
using Model;
using Services;
using Newtonsoft.Json;

namespace Networking
{
    public sealed class ZboruriClientWorker : IZboruriObserver
    {
        private readonly IZboruriServices _server;
        private readonly TcpClient _connection;

        private readonly NetworkStream _stream;
        private volatile bool _connected;
        
        public ZboruriClientWorker(IZboruriServices server, TcpClient connection)
        {
            this._server = server;
            this._connection = connection;
            try
            {
                _stream = connection.GetStream();
                _connected = true;
                Console.WriteLine("S-a creat worker-ul");
            }
            catch (Exception e)
            {
                Console.WriteLine(e.StackTrace);
            }
        }

        private string ReadLine()
        {
            using MemoryStream ms = new MemoryStream();
            int byteRead;
            while ((byteRead = _stream.ReadByte()) != '\n')
            {
                if (byteRead == -1)
                    throw new EndOfStreamException("End of stream reached before newline character was found.");
                ms.WriteByte((byte)byteRead);
            }
            return Encoding.ASCII.GetString(ms.ToArray());
        }

        public void Run()
        {
            while (_connected)
            {
                try
                {
                    string reqLine = ReadLine();
                    Console.WriteLine(reqLine);
                    Request request = JsonConvert.DeserializeObject<Request>(reqLine);
                    Console.WriteLine("Am primit requestul {0}", request);
                    object response = HandleRequest(request);
                    if (response != null)
                    {
                        SendResponse((Response)response);
                    }
                }
                catch (Exception e)
                {
                    Console.WriteLine(e.StackTrace);
                }

                try
                {
                    Thread.Sleep(1000);
                }
                catch (Exception e)
                {
                    Console.WriteLine(e.StackTrace);
                }
            }

            try
            {
                _stream.Close();
                _connection.Close();
            }
            catch (Exception e)
            {
                Console.WriteLine("Error " + e);
            }
        }

        private static readonly Response OkResponse = JsonProtocolUtils.CreateOkResponse();
        
        private Response HandleRequest(Request request)
        {
            if (request.Type is RequestType.Login)
            {
                Console.WriteLine("Login request ...");
                Angajat angajat = request.Angajat;
                try
                {
                    lock (_server)
                    {
                        _server.Login(angajat, this);
                    }

                    return OkResponse;
                }
                catch (ZboruriException e)
                {
                    _connected = false;
                    return JsonProtocolUtils.CreateErrorResponse(e.Message);
                }
            }

            if (request.Type is RequestType.Logout)
            {
                Console.WriteLine("Logout request");
                var angajat = request.Angajat;
                try
                {
                    lock (_server)
                    {
                        _server.Logout(angajat, this);
                    }

                    _connected = false;
                    return OkResponse;
                }
                catch (ZboruriException e)
                {
                    return JsonProtocolUtils.CreateErrorResponse(e.Message);
                }
            }

            if (request.Type is RequestType.GetFlightsSeatsDestDate)
            {
                Console.WriteLine("GetFlightsDestDateSeatsRequest ...");
                string dest = request.Destination;
                DateTime date = request.Date;
                int min = request.MinSeats;
                try
                {
                    List<Zbor> zboruri;
                    lock (_server)
                    {
                        zboruri = _server.FindZboruriDestDateAndMinSeats(dest, date, min);
                    }

                    return JsonProtocolUtils.CreateGetFlightsDestDateSeatsResponse(zboruri);
                }
                catch (ZboruriException e)
                {
                    return JsonProtocolUtils.CreateErrorResponse(e.Message);
                }
            }
            

            if (request.Type is RequestType.BuyTicket)
            {
                Console.WriteLine("BuyTicketRequest ...");
                string client = request.Client;
                string tara = request.Tara;
                string oras = request.Oras;
                List<TuristBilet> turisti = request.Turisti.Select(t => new TuristBilet {Turist = t}).ToList();
                int nrLocuri = request.NrLocuri;
                Zbor zbor = request.Zbor;
                
                try
                {
                    lock (_server)
                    {
                        _server.CumparaBilet(client, tara, oras, turisti, nrLocuri, zbor);
                    }

                    return OkResponse;
                }
                catch (ZboruriException e)
                {
                    return JsonProtocolUtils.CreateErrorResponse(e.Message);
                }
            }

            if (request.Type is RequestType.GetAllFlights)
            {
                Console.WriteLine("GetAllFlightsRequest ...");
                try
                {
                    List<Zbor> zboruri;
                    lock (_server)
                    {
                        zboruri = _server.FindZboruri();
                    }

                    return JsonProtocolUtils.CreateGetAllFlightsResponse(zboruri);
                }
                catch (ZboruriException e)
                {
                    return JsonProtocolUtils.CreateErrorResponse(e.Message);
                }
            }

            if (request.Type is RequestType.FindZbor)
            {
                Console.WriteLine("FindZborRequest ...");
                try
                {
                    Zbor zbor;
                    lock (_server)
                    {
                        zbor = _server.FindZbor(request.Id);
                    }

                    return JsonProtocolUtils.CreateFindZborResponse(zbor);
                }
                catch (ZboruriException e)
                {
                    return JsonProtocolUtils.CreateErrorResponse(e.Message);
                }
            }

            return null;
        }

        private void SendResponse(Response response)
        {
            Console.WriteLine("sending response " + response);
            string responseJson = JsonConvert.SerializeObject(response);
            responseJson += '\n';
            byte[] buffer = Encoding.UTF8.GetBytes(responseJson);
            lock (_stream)
            {
                _stream.Write(buffer, 0, buffer.Length);
                _stream.Flush();
            }
        }

        public void TicketBought(Zbor oldZbor, Zbor zbor)
        {
            Response response = JsonProtocolUtils.CreateBuyTicketResponse(oldZbor, zbor);
            Console.WriteLine("Ticket bought!");
            try
            {
                SendResponse(response);
            }
            catch (Exception e)
            {
                Console.WriteLine(e.StackTrace);
            }
        }
    }
}