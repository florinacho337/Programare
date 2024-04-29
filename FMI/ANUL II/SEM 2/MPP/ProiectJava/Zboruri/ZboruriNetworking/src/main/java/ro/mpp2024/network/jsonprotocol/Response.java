package ro.mpp2024.network.jsonprotocol;

import ro.mpp2024.domain.Zbor;

import java.io.Serializable;
import java.util.List;


public class Response implements Serializable {
    private ResponseType Type;
    private String ErrorMessage;
    private List<Zbor> Flights;
    private Zbor Zbor;
    private Zbor OldZbor;

    public Response() {
    }

    public ResponseType getType() {
        return Type;
    }

    public void setType(ResponseType type) {
        this.Type = type;
    }

    public String getErrorMessage() {
        return ErrorMessage;
    }

    public void setErrorMessage(String errorMessage) {
        this.ErrorMessage = errorMessage;
    }

    public List<Zbor> getFlights() {
        return Flights;
    }

    public void setFlights(List<Zbor> flights) {
        this.Flights = flights;
    }

    public void setZbor(Zbor zbor) {
        this.Zbor = zbor;
    }

    public Zbor getZbor() {
        return Zbor;
    }

    public void setOldZbor(Zbor oldZbor) {
        this.OldZbor = oldZbor;
    }

    public Zbor getOldZbor() {
        return OldZbor;
    }
}
