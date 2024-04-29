package ro.mpp2024.network.jsonprotocol;


import ro.mpp2024.domain.Angajat;
import ro.mpp2024.domain.Zbor;

import java.util.List;

public class Request {
    private RequestType Type;
    private Angajat Angajat;
    private int MinSeats;
    private String Destination;
    private String Date;
    private String Client, Tara, Oras;
    private List<String> Turisti;
    private int NrLocuri;
    private Zbor Zbor;

    public Zbor getZbor() {
        return Zbor;
    }

    public void setZbor(Zbor zbor) {
        this.Zbor = zbor;
    }

    @Override
    public String toString() {
        return "Request{" +
                "type=" + Type +
                ", angajat=" + Angajat +
                ", minSeats=" + MinSeats +
                ", destination='" + Destination + '\'' +
                ", date=" + Date +
                ", client='" + Client + '\'' +
                ", tara='" + Tara + '\'' +
                ", oras='" + Oras + '\'' +
                ", turisti=" + Turisti +
                ", nrLocuri=" + NrLocuri +
                ", zbor=" + Zbor +
                '}';
    }

    public int getNrLocuri() {
        return NrLocuri;
    }

    public void setNrLocuri(int nrLocuri) {
        this.NrLocuri = nrLocuri;
    }

    public List<String> getTuristi() {
        return Turisti;
    }

    public void setTuristi(List<String> turisti) {
        this.Turisti = turisti;
    }

    public String getOras() {
        return Oras;
    }

    public void setOras(String oras) {
        this.Oras = oras;
    }

    public String getTara() {
        return Tara;
    }

    public void setTara(String tara) {
        this.Tara = tara;
    }

    public String getClient() {
        return Client;
    }

    public void setClient(String client) {
        this.Client = client;
    }

    public Request(){}
    public RequestType getType() {
        return Type;
    }

    public void setType(RequestType type) {
        this.Type = type;
    }

    public Angajat getAngajat() {
        return Angajat;
    }

    public void setAngajat(Angajat angajat) {
        this.Angajat = angajat;
    }

    public int getMinSeats() {
        return MinSeats;
    }

    public void setMinSeats(int minSeats) {
        this.MinSeats = minSeats;
    }

    public String getDestination() {
        return Destination;
    }

    public void setDestination(String destination) {
        this.Destination = destination;
    }

    public String getDate() {
        return Date;
    }

    public void setDate(String date) {
        this.Date = date;
    }
}
