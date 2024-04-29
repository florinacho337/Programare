using System.Net.Sockets;
using Google.Protobuf;
using Services;

namespace Networking;

public class BMSProxy(string host, int port): IBmsServices
{
    private IbmsObserver _client;

    private NetworkStream _stream;
        
    private TcpClient _connection;

    private readonly Queue<Response> _responses = new();
    private volatile bool _finished;
    private EventWaitHandle _waitHandle;
    public virtual List<Model.Employee> GetAllEmployees()
    {
        InitializeConnection();
        Request request = ProtoUtils.CreateGetEmployeesRequest();
        SendRequest(request);
        Response response = ReadResponse();
        if (response.Type == Response.Types.Type.Error)
        {
            throw new BmsException(response.Message);
        }
        return ProtoUtils.GetEmployees(response);
    }

    public void Close()
    {
        CloseConnection();
    }
    public virtual void AddEmployee(Model.Employee employee)
    {
        InitializeConnection();
        Request request = ProtoUtils.CreateAddEmployeeRequest(employee);
        SendRequest(request);
        Response response = ReadResponse();
        if (response.Type == Response.Types.Type.Error)
        {
            throw new BmsException(response.Message);
        }
    }

    public virtual void RemoveEmployee(string username)
    {
        InitializeConnection();
        Request request = ProtoUtils.CreateRemoveEmployeeRequest(username);
        SendRequest(request);
        Response response = ReadResponse();
        if (response.Type == Response.Types.Type.Error)
        {
            throw new BmsException(response.Message);
        }
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
                request.WriteDelimitedTo(_stream);
                _stream.Flush();
            }
            catch (Exception e)
            {
                throw new BmsException("Error sending object " + e);
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

        private bool IsUpdate(Response response)
        {
            return false;
        }

        private void HandleUpdate(Response update)
        {
        }
        public virtual void Run()
        {
            while (!_finished)
            {
                try
                {
                    Response response = Response.Parser.ParseDelimitedFrom(_stream);
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