using System.Configuration;
using Gtk;
using Networking;
using Services;

namespace Client;

public static class StartClient
{
    private static int DEFAULT_PORT=55556;
    private static String DEFAULT_IP="127.0.0.1";

    public static void Main(string[] args)
    {
        Application.Init();
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

        Console.WriteLine("Using  server on IP {0} and port {1}", ip, port);
        IBmsServices server = new BMSProxy(ip, port);
        var ctrl = new ClientCtrl(server);
        Window w = new LoginWindow(ctrl);
        w.ShowAll();
        Application.Run();
    }
}