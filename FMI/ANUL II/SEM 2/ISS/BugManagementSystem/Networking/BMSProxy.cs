using System.Net.Sockets;
using Google.Protobuf;
using Services;

namespace Networking;

public class BMSProxy(string host, int port) : IBmsServices
{
    private IBmsObserver _client;

    private NetworkStream _stream;

    private TcpClient _connection;

    private readonly Queue<Response> _responses = new();
    private volatile bool _finished;
    private EventWaitHandle _waitHandle;

    public virtual List<Model.Employee> GetAllEmployees()
    {
        Request request = ProtoUtils.CreateGetEmployeesRequest();
        SendRequest(request);
        Response response = ReadResponse();
        if (response.Type == Response.Types.Type.Error)
        {
            throw new BmsException(response.Message);
        }

        return ProtoUtils.GetEmployees(response);
    }

    public virtual void AddEmployee(Model.Employee employee)
    {
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

// ---- New methods ----
    public virtual List<Model.Bug> GetAllBugs()
    {
        Request request = ProtoUtils.CreateGetBugsRequest();
        SendRequest(request);
        Response response = ReadResponse();
        if (response.Type == Response.Types.Type.Error)
        {
            throw new BmsException(response.Message);
        }

        return ProtoUtils.GetBugs(response);
    }

    public virtual Model.Employee LogIn(Model.Employee employee, IBmsObserver client)
    {
        InitializeConnection();
        Request request = ProtoUtils.CreateLoginRequest(employee);
        SendRequest(request);
        Response response = ReadResponse();
        if (response.Type == Response.Types.Type.Error)
        {
            CloseConnection();
            throw new BmsException(response.Message);
        }

        _client = client;
        return ProtoUtils.GetEmployee(response);
    }

    public virtual void LogOut(Model.Employee employee)
    {
        Request req = ProtoUtils.CreateLogoutRequest(employee);
        SendRequest(req);
        Response response = ReadResponse();
        CloseConnection();
        if (response.Type == Response.Types.Type.Error)
            throw new BmsException(response.Message);
    }

    public virtual void AddBug(Model.Bug bug)
    {
        var req = ProtoUtils.CreateAddBugRequest(bug);
        SendRequest(req);
        var response = ReadResponse();
        if (response.Type == Response.Types.Type.Error)
            throw new BmsException(response.Message);
    }

    public virtual void UpdateBug(Model.Bug bug)
    {
        var req = ProtoUtils.CreateUpdateBugRequest(bug);
        SendRequest(req);
        var response = ReadResponse();
        if (response.Type == Response.Types.Type.Error)
            throw new BmsException(response.Message);
    }

    public void RemoveBug(Model.Bug bug)
    {
        var req = ProtoUtils.CreateRemoveBugRequest(bug);
        SendRequest(req);
        var response = ReadResponse();
        if (response.Type == Response.Types.Type.Error)
            throw new BmsException(response.Message);
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
                // Monitor.Wait(_responses); 
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
        return response.Type is Response.Types.Type.AddBug or Response.Types.Type.UpdateBug or Response.Types.Type.RemoveBug;
    }

    private void HandleUpdate(Response update)
    {
        try
        {
            switch (update.Type)
            {
                case Response.Types.Type.AddBug:
                    var bug = ProtoUtils.GetBug(update);
                    _client.BugAdded(bug);
                    break;
                case Response.Types.Type.UpdateBug:
                    bug = ProtoUtils.GetBug(update);
                    _client.BugUpdated(bug);
                    break;
                case Response.Types.Type.RemoveBug:
                    bug = ProtoUtils.GetBug(update);
                    _client.BugRemoved(bug);
                    break;
            }
        }
        catch (Exception e)
        {
            Console.WriteLine(e.StackTrace);
        }
    }

    protected virtual void Run()
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