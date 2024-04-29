package ro.mpp2024;

import ro.mpp2024.network.utils.ServerException;
import ro.mpp2024.network.utils.AbstractServer;
import ro.mpp2024.network.utils.ZboruriJsonConcurrentServer;
import ro.mpp2024.repository.AngajatiDBRepository;
import ro.mpp2024.repository.BileteDBRepository;
import ro.mpp2024.repository.ZboruriDBRepository;
import ro.mpp2024.server.Service;
import ro.mpp2024.services.ZboruriServices;

import java.io.IOException;
import java.util.Properties;

public class StartJsonServer {

    public static void main(String[] args) {
        Properties serverProps=new Properties();
        try {
            serverProps.load(StartJsonServer.class.getResourceAsStream("/zboruriserver.properties"));
            System.out.println("Server properties set. ");
            serverProps.list(System.out);
        } catch (IOException e) {
            System.err.println("Cannot find zboruriserver.properties "+e);
            return;
        }
        AngajatiDBRepository repoAngajati = new AngajatiDBRepository(serverProps);
        ZboruriDBRepository repoZboruri = new ZboruriDBRepository(serverProps);
        BileteDBRepository repoBilete = new BileteDBRepository(serverProps);
        ZboruriServices service = new Service(repoAngajati, repoBilete, repoZboruri);
        int defaultPort = 55555;
        int zboruriServerPort= defaultPort;
        try {
            zboruriServerPort = Integer.parseInt(serverProps.getProperty("zboruri.server.port"));
        }catch (NumberFormatException nef){
            System.err.println("Wrong  Port Number"+nef.getMessage());
            System.err.println("Using default port "+ defaultPort);
        }
        System.out.println("Starting server on port: "+zboruriServerPort);
        AbstractServer server = new ZboruriJsonConcurrentServer(zboruriServerPort, service);
        try {
            server.start();
        } catch (ServerException e) {
            System.err.println("Error starting the server" + e.getMessage());
        }
    }
}
