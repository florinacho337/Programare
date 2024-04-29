using System.Configuration;
using System.Net.Sockets;
using Data;
using Networking;
using Services;

namespace Server;

public static class StartServer
{
    private static readonly int DEFAULT_PORT = 55556;
    private static readonly string DEFAULT_IP = "127.0.0.1";
    
    private static void Main()
    {
        Console.WriteLine("Reading properties from app.config ...");
        var port = DEFAULT_PORT;
        var ip = DEFAULT_IP;
        var portS = ConfigurationManager.AppSettings["port"];
        if (portS == null)
        {
            Console.WriteLine("Port property not set. Using default value " + DEFAULT_PORT);
        }
        else
        {
            var result = int.TryParse(portS, out port);
            if (!result)
            {
                Console.WriteLine("Port property not a number. Using default value " + DEFAULT_PORT);
                port = DEFAULT_PORT;
                Console.WriteLine("Portul " + port);
            }
        }

        var ipS = ConfigurationManager.AppSettings["ip"];

        if (ipS == null)
        {
            Console.WriteLine("Port property not set. Using default value " + DEFAULT_IP);
        }

        string connectionString = GetConnectionStringByName("BmsDb");
        var dbContext = new BugManagementSystemDbContext(connectionString);
        var service = new Service(dbContext);


        Console.WriteLine("Starting server on IP {0} and port {1}", ip, port);
        var server = new SerialServer(ip, port, service);
        server.Start();
        Console.WriteLine("Server started ...");
        Console.ReadLine();
    }
    
    private static string GetConnectionStringByName(string name)
    {
        // Assume failure.
        string returnValue = null;

        // Look for the name in the connectionStrings section.
        ConnectionStringSettings settings = ConfigurationManager.ConnectionStrings[name];

        // If found, return the connection string.
        if (settings != null)
            returnValue = settings.ConnectionString;

        return returnValue;
    }
}
public class SerialServer : ConcurrentServer
{
    private readonly IBmsServices _server;
    private BmsWorker _worker;

    public SerialServer(string host, int port, IBmsServices server) : base(host, port)
    {
        this._server = server;
        Console.WriteLine("SerialServer...");
    }

    protected override Thread CreateWorker(TcpClient client)
    {
        _worker = new BmsWorker(_server, client);
        return new Thread(_worker.Run);
    }
}