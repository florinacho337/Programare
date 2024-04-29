package ro.mpp2024.network.jsonprotocol;

import ro.mpp2024.domain.Zbor;
import ro.mpp2024.domain.Angajat;
import ro.mpp2024.utils.Constants;

import java.time.LocalDateTime;
import java.util.List;


public class JsonProtocolUtils {

    public static Response createOkResponse(){
        Response resp=new Response();
        resp.setType(ResponseType.Ok);
        return resp;
    }

    public static Response createErrorResponse(String errorMessage){
        Response resp=new Response();
        resp.setType(ResponseType.Error);
        resp.setErrorMessage(errorMessage);
        return resp;
    }

    public static Request createLoginRequest(Angajat angajat){
        Request req=new Request();
        req.setType(RequestType.Login);
        req.setAngajat(angajat);
        return req;
    }

    public static Request createLogoutRequest(Angajat angajat){
        Request req=new Request();
        req.setType(RequestType.Logout);
        req.setAngajat(angajat);
        return req;
    }

    public static Response createGetAllFlightsResponse(List<Zbor> flights) {
        Response resp=new Response();
        resp.setType(ResponseType.GetFlights);
        resp.setFlights(flights);
        return resp;
    }

    public static Response createGetFlightsDestDateSeatsResponse(List<Zbor> flights) {
        Response resp=new Response();
        resp.setType(ResponseType.GetFlightsSeatsDestDate);
        resp.setFlights(flights);
        return resp;
    }

    public static Request createGetFlightsDestDateSeatsRequest(String dest, LocalDateTime date, int min) {
        Request req=new Request();
        req.setType(RequestType.GetFlightsSeatsDestDate);
        req.setDestination(dest);
        req.setDate(date.format(Constants.DATE_TIME_FORMATTER));
        req.setMinSeats(min);
        return req;
    }

    public static Request createGetAllFlightsRequest() {
        Request req=new Request();
        req.setType(RequestType.GetAllFlights);
        return req;
    }

    public static Request createBuyTicketRequest(String client, String tara, String oras, List<String> turisti, int nrLocuri, Zbor zbor) {
        Request req=new Request();
        req.setType(RequestType.BuyTicket);
        req.setClient(client);
        req.setTara(tara);
        req.setOras(oras);
        req.setTuristi(turisti);
        req.setNrLocuri(nrLocuri);
        req.setZbor(zbor);
        return req;
    }

    public static Response createBuyTicketResponse(Zbor oldZbor, Zbor zbor) {
        Response resp=new Response();
        resp.setType(ResponseType.BuyTicket);
        resp.setZbor(zbor);
        resp.setOldZbor(oldZbor);
        return resp;
    }
}
