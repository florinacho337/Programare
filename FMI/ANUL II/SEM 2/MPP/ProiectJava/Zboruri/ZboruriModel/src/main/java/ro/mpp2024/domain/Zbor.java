package ro.mpp2024.domain;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.time.LocalDateTime;

public class Zbor extends Entity<Integer> {
    private String Aeroport;
    private String Destinatie;
    private LocalDateTime Plecare;
    private int NrLocuri;

    public Zbor(){

    }

    public Zbor(String aeroport, String destinatie, LocalDateTime plecare, int nrLocuri) {
        this.Aeroport = aeroport;
        this.Destinatie = destinatie;
        this.Plecare = plecare;
        this.NrLocuri = nrLocuri;
    }

    public String getAeroport() {
        return Aeroport;
    }

    public void setAeroport(String aeroport) {
        this.Aeroport = aeroport;
    }

    public String getDestinatie() {
        return Destinatie;
    }

    public void setDestinatie(String destinatie) {
        this.Destinatie = destinatie;
    }

    public LocalDateTime getPlecare() {
        return Plecare;
    }

    public void setPlecare(LocalDateTime plecare) {
        this.Plecare = plecare;
    }

    public int getNrLocuri() {
        return NrLocuri;
    }

    public void setNrLocuri(int nrLocuri) {
        this.NrLocuri = nrLocuri;
    }

    @Override
    public String toString() {
        return "Zbor{" +
                "aeroport='" + Aeroport + '\'' +
                ", destinatie='" + Destinatie + '\'' +
                ", plecare=" + Plecare +
                ", nrLocuri=" + NrLocuri +
                '}';
    }
}
