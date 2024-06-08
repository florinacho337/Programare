using Model;

namespace Networking;

public class JsonProtocolUtils
{
    public static Response CreateOkResponse(){
        Response resp=new Response
        {
            Type = ResponseType.Ok
        };
        return resp;
    }
    
    public static Response CreateErrorResponse(String errorMessage){
        Response resp=new Response
        {
            Type = ResponseType.Error,
            ErrorMessage = errorMessage
        };
        return resp;
    }
    
    public static Request CreateLoginRequest(Angajat angajat)
    {
        var req = new Request
        {
            Type = RequestType.Login,
            Angajat = angajat
        };
        return req;
    }

    public static Request CreateLogoutRequest(Angajat angajat)
    {
        var req = new Request
        {
            Type = RequestType.Logout,
            Angajat = angajat
        };
        return req;
    }

    public static Response CreateGetAllFlightsResponse(List<Zbor> flights)
    {
        var resp = new Response
        {
            Type = ResponseType.GetFlights,
            Flights = flights
        };
        return resp;
    }

    public static Response CreateGetFlightsDestDateSeatsResponse(List<Zbor> flights)
    {
        var resp = new Response
        {
            Type = ResponseType.GetFlightsSeatsDestDate,
            Flights = flights
        };
        return resp;
    }

    public static Request CreateGetFlightsDestDateSeatsRequest(string dest, DateTime date, int min)
    {
        var req = new Request
        {
            Type = RequestType.GetFlightsSeatsDestDate,
            Destination = dest,
            Date = date,
            MinSeats = min
        };
        return req;
    }

    public static Request CreateGetAllFlightsRequest()
    {
        var req = new Request
        {
            Type = RequestType.GetAllFlights
        };
        return req;
    }

    public static Request CreateBuyTicketRequest(string client, string tara, string oras, List<TuristBilet> turisti, int nrLocuri, Zbor zbor)
    {
        var req = new Request
        {
            Type = RequestType.BuyTicket,
            Client = client,
            Tara = tara,
            Oras = oras,
            Turisti = turisti.Select(t => t.Turist).ToList(),
            NrLocuri = nrLocuri,
            Zbor = zbor
        };
        return req;
    }

    public static Response CreateBuyTicketResponse(Zbor oldZbor, Zbor zbor)
    {
        var resp = new Response
        {
            Type = ResponseType.BuyTicket,
            Zbor = zbor,
            OldZbor = oldZbor
        };
        return resp;
    }

    public static Request CreateFindZborRequest(int id)
    {
        var req = new Request
        {
            Type = RequestType.FindZbor,
            Id = id
        };
        return req;
    }

    public static Response CreateFindZborResponse(Zbor zbor)
    {
        var resp = new Response
        {
            Type = ResponseType.FindZbor,
            Found = zbor
        };
        return resp;
    }
}