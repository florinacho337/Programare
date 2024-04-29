using System.Net.Sockets;
using Google.Protobuf;
using Services;

namespace Networking;

public class BmsWorker : IbmsObserver
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
}