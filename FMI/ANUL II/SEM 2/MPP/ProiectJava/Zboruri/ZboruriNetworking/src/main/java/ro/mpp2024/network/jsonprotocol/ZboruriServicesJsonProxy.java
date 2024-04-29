package ro.mpp2024.network.jsonprotocol;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import ro.mpp2024.domain.Zbor;
import ro.mpp2024.domain.Angajat;
import ro.mpp2024.services.ZboruriException;
import ro.mpp2024.services.ZboruriObserver;
import ro.mpp2024.services.ZboruriServices;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.time.LocalDateTime;
import java.util.List;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

public class ZboruriServicesJsonProxy implements ZboruriServices {
    private final String host;
    private final int port;

    private ZboruriObserver client;

    private BufferedReader input;
    private PrintWriter output;
    private Gson gsonFormatter;
    private Socket connection;

    private final BlockingQueue<Response> qresponses;
    private volatile boolean finished;

    public ZboruriServicesJsonProxy(String host, int port) {
        this.host = host;
        this.port = port;
        qresponses = new LinkedBlockingQueue<>();
    }

    private void closeConnection() {
        finished = true;
        try {
            input.close();
            output.close();
            connection.close();
            client = null;
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    private void sendRequest(Request request) throws ZboruriException {
        String reqLine = gsonFormatter.toJson(request);
        try {
            output.println(reqLine);
            output.flush();
        } catch (Exception e) {
            throw new ZboruriException("Error sending object " + e);
        }

    }

    private Response readResponse() {
        Response response = null;
        try {

            response = qresponses.take();

        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return response;
    }

    private void initializeConnection() {
        try {
            gsonFormatter = new GsonBuilder()
                    .registerTypeAdapter(LocalDateTime.class, new LocalDateTimeTypeAdapter())
                    .registerTypeAdapter(ResponseType.class, new ResponseTypeAdapter())
                    .create();
            connection = new Socket(host, port);
            output = new PrintWriter(connection.getOutputStream());
            output.flush();
            input = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            finished = false;
            startReader();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void startReader() {
        Thread tw = new Thread(new ReaderThread());
        tw.start();
    }


    private void handleUpdate(Response response) {
        if (response.getType() == ResponseType.BuyTicket) {
            Zbor oldZbor = response.getOldZbor();
            Zbor newZbor = response.getZbor();
            System.out.println("Ticket bought!");
            try {
                client.ticketBought(oldZbor, newZbor);
            } catch (ZboruriException e) {
                e.printStackTrace();
            }
        }
    }

    private boolean isUpdate(Response response) {
        return response.getType() == ResponseType.BuyTicket;
    }

    @Override
    public void login(Angajat angajat, ZboruriObserver client) throws ZboruriException {
        initializeConnection();

        Request req = JsonProtocolUtils.createLoginRequest(angajat);
        sendRequest(req);
        Response response = readResponse();
        if (response.getType() == ResponseType.Error) {
            String err = response.getErrorMessage();
            closeConnection();
            throw new ZboruriException(err);
        }
        this.client = client;
    }

    @Override
    public void logout(Angajat angajat, ZboruriObserver client) throws ZboruriException {
        Request req = JsonProtocolUtils.createLogoutRequest(angajat);
        sendRequest(req);
        Response response = readResponse();
        closeConnection();
        if (response.getType() == ResponseType.Error) {
            String err = response.getErrorMessage();
            throw new ZboruriException(err);
        }
    }

    @Override
    public List<Zbor> findZboruriDestDateAndMinSeats(String dest, LocalDateTime date, int min) throws ZboruriException {
        Request req = JsonProtocolUtils.createGetFlightsDestDateSeatsRequest(dest, date, min);
        sendRequest(req);
        Response response = readResponse();
        if (response.getType() == ResponseType.Error) {
            String err = response.getErrorMessage();
            throw new ZboruriException(err);
        }
        return response.getFlights();
    }

    @Override
    public List<Zbor> findZboruri() throws ZboruriException {
        Request req = JsonProtocolUtils.createGetAllFlightsRequest();
        sendRequest(req);
        Response response = readResponse();
        if (response.getType() == ResponseType.Error) {
            String err = response.getErrorMessage();
            throw new ZboruriException(err);
        }
        return response.getFlights();
    }

    @Override
    public void cumparaBilet(String client, String tara, String oras, List<String> turisti, int nrLocuri, Zbor zbor) throws ZboruriException {
        Request req = JsonProtocolUtils.createBuyTicketRequest(client, tara, oras, turisti, nrLocuri, zbor);
        sendRequest(req);
        Response response = readResponse();
        if (response.getType() == ResponseType.Error) {
            String err = response.getErrorMessage();
            throw new ZboruriException(err);
        }
    }

    private class ReaderThread implements Runnable {
        public void run() {
            while (!finished) {
                try {
                    String responseLine = input.readLine();
                    System.out.println("response received " + responseLine);
                    Response response = gsonFormatter.fromJson(responseLine, Response.class);
                    if (response == null)
                        return;
                    if (isUpdate(response)) {
                        handleUpdate(response);
                    } else {

                        try {
                            qresponses.put(response);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }
                } catch (IOException e) {
                    System.out.println("Reading error " + e);
                }
            }
        }
    }
}
