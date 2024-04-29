using System.Configuration;
using System.Net.Sockets;
using log4net.Config;
using Networking;
using Persistence;
using Services;

namespace Server;

public static class StartServer
{
    private static readonly int DEFAULT_PORT = 55556;
    private static readonly String DEFAULT_IP = "127.0.0.1";
    
    private static void Main()
    {
        XmlConfigurator.Configure(new System.IO.FileInfo("../../log4net.config"));
        Console.WriteLine("Reading properties from app.config ...");
        int port = DEFAULT_PORT;
        String ip = DEFAULT_IP;
        String portS = ConfigurationManager.AppSettings["port"];
        if (portS == null)
        {
            Console.WriteLine("Port property not set. Using default value " + DEFAULT_PORT);
        }
        else
        {
            bool result = Int32.TryParse(portS, out port);
            if (!result)
            {
                Console.WriteLine("Port property not a number. Using default value " + DEFAULT_PORT);
                port = DEFAULT_PORT;
                Console.WriteLine("Portul " + port);
            }
        }

        String ipS = ConfigurationManager.AppSettings["ip"];

        if (ipS == null)
        {
            Console.WriteLine("Port property not set. Using default value " + DEFAULT_IP);
        }

        Console.WriteLine("Configuration Settings for database {0}", GetConnectionStringByName("zboruriDB"));
        // IDictionary<String, string> props = new SortedList<String, String>();
        // props.Add("ConnectionString", GetConnectionStringByName("zboruriDB"));
        // IAngajatiRepository angajatiRepository = new AngajatiDbRepository(props);
        // IZboruriRepository zboruriRepository = new ZboruriDbRepository(props);
        // IBileteRepository bileteRepository = new BileteDbRepository(props);
        ZboruriDbContext zboruriDbContext = new ZboruriDbContext();
        IAngajatiRepository angajatiRepository = new AngajatiRepositoryEF(zboruriDbContext);
        IBileteRepository bileteRepository = new BileteRepositoryEF(zboruriDbContext);
        IZboruriRepository zboruriRepository = new ZboruriRepositoryEF(zboruriDbContext);
        IZboruriServices service = new Service.Service(angajatiRepository, bileteRepository, zboruriRepository);


        Console.WriteLine("Starting server on IP {0} and port {1}", ip, port);
        SerialZboruriServer server = new SerialZboruriServer(ip, port, service);
        server.Start();
        Console.WriteLine("Server started ...");
        Console.ReadLine();
    }


    static string GetConnectionStringByName(string name)
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

public class SerialZboruriServer : ConcurrentServer
{
    private readonly IZboruriServices _server;
    private ZboruriClientWorker _worker;

    public SerialZboruriServer(string host, int port, IZboruriServices server) : base(host, port)
    {
        this._server = server;
        Console.WriteLine("SerialZboruriServer...");
    }

    protected override Thread CreateWorker(TcpClient client)
    {
        _worker = new ZboruriClientWorker(_server, client);
        return new Thread(_worker.Run);
    }
}