using System.Net.Sockets;
using Google.Protobuf;
using Services;

namespace Networking;

public class BmsWorker : IBmsObserver
{
    private readonly IBmsServices _server;
    private readonly TcpClient _connection;

    private readonly NetworkStream _stream;
    private volatile bool _connected;

    public BmsWorker(IBmsServices server, TcpClient connection)
    {
        this._server = server;
        this._connection = connection;
        try
        {
            _stream = connection.GetStream();
            _connected = true;
        }
        catch (Exception e)
        {
            Console.WriteLine(e.StackTrace);
        }
    }

    public virtual void Run()
    {
        while (_connected)
        {
            try
            {
                Request request = Request.Parser.ParseDelimitedFrom(_stream);
                Response response = HandleRequest(request);
                if (response != null)
                {
                    SendResponse(response);
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

    private Response HandleRequest(Request request)
    {
        Request.Types.Type reqType = request.Type;
        switch (reqType)
        {
            case Request.Types.Type.AddEmployee:
            {
                Console.WriteLine("AddEmployee request ...");
                var employee = ProtoUtils.GetEmployee(request);
                try
                {
                    lock (_server)
                    {
                        _server.AddEmployee(employee);
                    }

                    return ProtoUtils.CreateOkResponse();
                }
                catch (BmsException e)
                {
                    return ProtoUtils.CreateErrorResponse(e.Message);
                }
            }
            case Request.Types.Type.GetEmployees:
            {
                Console.WriteLine("GetEmployees request ...");
                try
                {
                    List<Model.Employee> employees;
                    lock (_server)
                    {
                        employees = _server.GetAllEmployees();
                    }

                    return ProtoUtils.CreateGetEmployeesResponse(employees);
                }
                catch (BmsException e)
                {
                    return ProtoUtils.CreateErrorResponse(e.Message);
                }
            }
            case Request.Types.Type.RemoveEmployee:
            {
                Console.WriteLine("RemoveEmployee request ...");
                string username = request.Username;
                try
                {
                    lock (_server)
                    {
                        _server.RemoveEmployee(username);
                    }

                    return ProtoUtils.CreateOkResponse();
                }
                catch (BmsException e)
                {
                    return ProtoUtils.CreateErrorResponse(e.Message);
                }
            }
            case Request.Types.Type.GetBugs:
            {
                Console.WriteLine("GetBugs request ...");
                try
                {
                    List<Model.Bug> bugs;
                    lock (_server)
                    {
                        bugs = _server.GetAllBugs();
                    }

                    return ProtoUtils.CreateGetBugsResponse(bugs);
                }
                catch (BmsException e)
                {
                    return ProtoUtils.CreateErrorResponse(e.Message);
                }
            }
            case Request.Types.Type.Login:
            {
                Console.WriteLine("Login request ...");
                var employee = ProtoUtils.GetEmployee(request);
                Model.Employee foundEmployee;
                try
                {
                    lock (_server)
                    {
                        foundEmployee = _server.LogIn(employee, this);
                    }

                    return ProtoUtils.CreateSuccessfulLoginResponse(foundEmployee);
                }
                catch (BmsException e)
                {
                    _connected = false;
                    return ProtoUtils.CreateErrorResponse(e.Message);
                }
            }
            case Request.Types.Type.Logout:
            {
                Console.WriteLine("Logout request ...");
                var employee = ProtoUtils.GetEmployee(request);
                try
                {
                    lock (_server)
                    {
                        _server.LogOut(employee);
                    }

                    _connected = false;
                    return ProtoUtils.CreateOkResponse();
                }
                catch (BmsException e)
                {
                    return ProtoUtils.CreateErrorResponse(e.Message);
                }
            }
            case Request.Types.Type.AddBug:
            {
                Console.WriteLine("AddBug request ...");
                var bug = ProtoUtils.GetBug(request);
                try
                {
                    lock (_server)
                    {
                        _server.AddBug(bug);
                    }

                    return ProtoUtils.CreateOkResponse();
                }
                catch (BmsException e)
                {
                    return ProtoUtils.CreateErrorResponse(e.Message);
                }
            }
            case Request.Types.Type.UpdateBug:
            {
                Console.WriteLine("UpdateBug request ...");
                var bug = ProtoUtils.GetBug(request);
                try
                {
                    lock (_server)
                    {
                        _server.UpdateBug(bug);
                    }

                    return ProtoUtils.CreateOkResponse();
                }
                catch (BmsException e)
                {
                    return ProtoUtils.CreateErrorResponse(e.Message);
                }
            }
            case Request.Types.Type.RemoveBug:
            {
                Console.WriteLine("RemoveBug request ...");
                var bug = ProtoUtils.GetBug(request);
                try
                {
                    lock (_server)
                    {
                        _server.RemoveBug(bug);
                    }

                    return ProtoUtils.CreateOkResponse();
                }
                catch (BmsException e)
                {
                    return ProtoUtils.CreateErrorResponse(e.Message);
                }
            }
        }

        return null;
    }

    private void SendResponse(Response response)
    {
        Console.WriteLine("sending response " + response);
        lock (_stream)
        {
            response.WriteDelimitedTo(_stream);
            _stream.Flush();
        }
    }

    // ----------------------------------------- NEW -----------------------------------------
    public void BugAdded(Model.Bug bugREntity)
    {
        Response response = ProtoUtils.CreateBugAddedResponse(bugREntity);
        try
        {
            SendResponse(response);
        }
        catch (Exception e)
        {
            Console.WriteLine(e.StackTrace);
        }
    }

    public void BugUpdated(Model.Bug newBug)
    {
        Response response = ProtoUtils.CreateBugUpdatedResponse(newBug);
        try
        {
            SendResponse(response);
        }
        catch (Exception e)
        {
            Console.WriteLine(e.StackTrace);
        }
    }

    public void BugRemoved(Model.Bug bug)
    {
        Response response = ProtoUtils.CreateBugRemovedResponse(bug);
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