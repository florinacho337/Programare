package ro.mpp2024.domain;

public class Angajat extends Entity<String> {
    private String Username;
    private String Nume;
    private String Parola;

    public Angajat(String username, String parola) {
        this(username, "", parola);
    }

    public Angajat(String username, String nume, String parola) {
        this.Username = username;
        this.Nume = nume;
        this.Parola = parola;
    }

    public String getUsername() {
        return Username;
    }

    public void setUsername(String username) {
        this.Username = username;
    }

    public String getNume() {
        return Nume;
    }

    public void setNume(String nume) {
        this.Nume = nume;
    }

    public String getParola() {
        return Parola;
    }

    public void setParola(String parola) {
        this.Parola = parola;
    }

    @Override
    public String toString() {
        return "Angajat{" +
                "username='" + Username + '\'' +
                ", nume='" + Nume + '\'' +
                ", parola='" + Parola + '\'' +
                '}';
    }
}
