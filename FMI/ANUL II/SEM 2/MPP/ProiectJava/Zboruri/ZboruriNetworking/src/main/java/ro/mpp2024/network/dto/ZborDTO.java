package ro.mpp2024.network.dto;

import java.io.Serializable;

public class ZborDTO implements Serializable, Comparable<ZborDTO> {
    private String aeroport;
    private String destinatie;
    private String plecare;
    private int nrLocuri;
    private String oraPlecare;
    private Integer id;

    @Override
    public String toString() {
        return "ZborDTO{" +
                "aeroport='" + aeroport + '\'' +
                ", destinatie='" + destinatie + '\'' +
                ", plecare='" + plecare + '\'' +
                ", nrLocuri=" + nrLocuri +
                ", oraPlecare=" + oraPlecare +
                ", id=" + id +
                '}';
    }

    public void setAeroport(String aeroport) {
        this.aeroport = aeroport;
    }

    public void setDestinatie(String destinatie) {
        this.destinatie = destinatie;
    }

    public void setPlecare(String plecare) {
        this.plecare = plecare;
    }

    public void setNrLocuri(int nrLocuri) {
        this.nrLocuri = nrLocuri;
    }

    public void setOraPlecare(String oraPlecare) {
        this.oraPlecare = oraPlecare;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public ZborDTO(String aeroport, String destinatie, String plecare, int nrLocuri, String oraPlecare, Integer id) {
        this.aeroport = aeroport;
        this.destinatie = destinatie;
        this.plecare = plecare;
        this.nrLocuri = nrLocuri;
        this.oraPlecare = oraPlecare;
        this.id = id;
    }

    public String getAeroport() {
        return aeroport;
    }

    public String getDestinatie() {
        return destinatie;
    }

    public String getPlecare() {
        return plecare;
    }

    public int getNrLocuri() {
        return nrLocuri;
    }

    public String getOraPlecare() {
        return oraPlecare;
    }

    public Integer getId() {
        return id;
    }

    @Override
    public int compareTo(ZborDTO o) {
        return id.compareTo(o.id);
    }

    @Override
    public boolean equals(Object obj) {
        if (obj instanceof ZborDTO zborDTO) {
            return id.equals(zborDTO.id);
        }
        return false;
    }

    @Override
    public int hashCode() {
        return id != null ? id.hashCode() : 0;
    }
}
