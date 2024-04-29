package ro.mpp2024.network.utils;

import ro.mpp2024.network.jsonprotocol.ZboruriClientJsonWorker;
import ro.mpp2024.services.ZboruriServices;

import java.net.Socket;

public class ZboruriJsonConcurrentServer extends AbsConcurrentServer{
    private ZboruriServices zboruriServer;
    public ZboruriJsonConcurrentServer(int port, ZboruriServices zboruriServer) {
        super(port);
        this.zboruriServer = zboruriServer;
        System.out.println("Zboruri - ZboruriJsonConcurrentServer");
    }

    @Override
    protected Thread createWorker(Socket client) {
        ZboruriClientJsonWorker worker=new ZboruriClientJsonWorker(zboruriServer, client);

        Thread tw=new Thread(worker);
        return tw;
    }
}
