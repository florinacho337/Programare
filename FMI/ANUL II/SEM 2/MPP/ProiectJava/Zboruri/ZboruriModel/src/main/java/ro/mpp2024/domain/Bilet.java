package ro.mpp2024.domain;

import java.util.List;

public class Bilet extends Entity<Integer> {
    private String Client;
    private String Oras;
    private String Tara;
    private List<String> Turisti;
    private int NrLocuri;
    private Zbor Zbor;

    public Bilet(String client, String oras, String tara, List<String> turisti, int nrLocuri, Zbor zbor) {
        this.Client = client;
        this.Oras = oras;
        this.Tara = tara;
        this.Turisti = turisti;
        this.NrLocuri = nrLocuri;
        this.Zbor = zbor;
    }

    public String getClient() {
        return Client;
    }

    public void setClient(String client) {
        this.Client = client;
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

    public List<String> getTuristi() {
        return Turisti;
    }

    public void setTuristi(List<String> turisti) {
        this.Turisti = turisti;
    }

    public int getNrLocuri() {
        return NrLocuri;
    }

    public void setNrLocuri(int nrLocuri) {
        this.NrLocuri = nrLocuri;
    }

    public Zbor getZbor() {
        return Zbor;
    }

    public void setZbor(Zbor zbor) {
        this.Zbor = zbor;
    }

    @Override
    public String toString() {
        return "Bilet{" +
                "client='" + Client + '\'' +
                ", turisti=" + Turisti +
                ", nrLocuri=" + NrLocuri +
                ", zbor=" + Zbor +
                '}';
    }
}
