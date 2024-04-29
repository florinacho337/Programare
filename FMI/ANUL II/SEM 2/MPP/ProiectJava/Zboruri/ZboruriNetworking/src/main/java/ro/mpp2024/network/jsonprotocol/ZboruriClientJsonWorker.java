package ro.mpp2024.network.jsonprotocol;

import com.google.gson.*;
import ro.mpp2024.domain.Zbor;
import ro.mpp2024.domain.Angajat;
import ro.mpp2024.services.ZboruriException;
import ro.mpp2024.services.ZboruriObserver;
import ro.mpp2024.services.ZboruriServices;
import ro.mpp2024.utils.Constants;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.time.LocalDateTime;
import java.util.List;

public class ZboruriClientJsonWorker implements Runnable, ZboruriObserver {
    private final ZboruriServices server;
    private final Socket connection;

    private BufferedReader input;
    private PrintWriter output;
    private final Gson gsonFormatter;
    private volatile boolean connected;

    public ZboruriClientJsonWorker(ZboruriServices server, Socket connection) {
        this.server = server;
        this.connection = connection;
        gsonFormatter = new GsonBuilder()
                .registerTypeAdapter(LocalDateTime.class, new LocalDateTimeTypeAdapter())
                .create();
        try {
            output = new PrintWriter(connection.getOutputStream());
            input = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            connected = true;
        } catch (IOException e) {
            e.printStackTrace();
        }
   }

    public void run() {
        while (connected) {
            try {
                String requestLine = input.readLine();
                Request request = gsonFormatter.fromJson(requestLine, Request.class);
                Response response = handleRequest(request);
                if (response != null) {
                    sendResponse(response);
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        try {
            input.close();
            output.close();
            connection.close();
        } catch (IOException e) {
            System.out.println("Error " + e);
        }
    }

    private static final Response okResponse = JsonProtocolUtils.createOkResponse();

    private Response handleRequest(Request request) {
        if (request.getType() == RequestType.Login) {
            System.out.println("Login request ..." + request.getType());
            Angajat angajat = request.getAngajat();
            try {
                server.login(angajat, this);
                return okResponse;
            } catch (ZboruriException e) {
                connected = false;
                return JsonProtocolUtils.createErrorResponse(e.getMessage());
            }
        }
        if (request.getType() == RequestType.Logout) {
            System.out.println("Logout request");

            Angajat angajat = request.getAngajat();
            try {
                server.logout(angajat, this);
                connected = false;
                return okResponse;

            } catch (ZboruriException e) {
                return JsonProtocolUtils.createErrorResponse(e.getMessage());
            }
        }

        if (request.getType() == RequestType.GetAllFlights) {
            System.out.println("GetAllFlights request ...");
            try {
                List<Zbor> zboruri = server.findZboruri();
                return JsonProtocolUtils.createGetAllFlightsResponse(zboruri);
            } catch (ZboruriException e) {
                return JsonProtocolUtils.createErrorResponse(e.getMessage());
            }
        }

        if (request.getType() == RequestType.GetFlightsSeatsDestDate) {
            System.out.println("GetFlightsSeatsDestDate request ...");
            String dest = request.getDestination();
            LocalDateTime date = LocalDateTime.parse(request.getDate(), Constants.DATE_TIME_FORMATTER);
            int min = request.getMinSeats();
            try {
                List<Zbor> zboruri = server.findZboruriDestDateAndMinSeats(dest, date, min);
                return JsonProtocolUtils.createGetFlightsDestDateSeatsResponse(zboruri);
            } catch (ZboruriException e) {
                return JsonProtocolUtils.createErrorResponse(e.getMessage());
            }
        }

        if (request.getType() == RequestType.BuyTicket) {
            System.out.println("BuyTicket request ...");
            String client = request.getClient();
            String tara = request.getTara();
            String oras = request.getOras();
            List<String> turisti = request.getTuristi();
            int nrLocuri = request.getNrLocuri();
            Zbor zbor = request.getZbor();
            try {
                server.cumparaBilet(client, tara, oras, turisti, nrLocuri, zbor);
                return okResponse;
            } catch (ZboruriException e) {
                return JsonProtocolUtils.createErrorResponse(e.getMessage());
            }
        }

        return null;
    }

    private void sendResponse(Response response) throws IOException {
        String responseLine = gsonFormatter.toJson(response);
        System.out.println("sending response " + responseLine);
        synchronized (output) {
            output.println(responseLine);
            output.flush();
        }
    }

    @Override
    public void ticketBought(Zbor oldZbor, Zbor zbor) throws ZboruriException {
        Response resp= JsonProtocolUtils.createBuyTicketResponse(oldZbor, zbor);
        System.out.println("Bought ticket!");
        try {
            sendResponse(resp);
        } catch (IOException e) {
            throw new ZboruriException("Sending error: "+e);
        }
    }
}
