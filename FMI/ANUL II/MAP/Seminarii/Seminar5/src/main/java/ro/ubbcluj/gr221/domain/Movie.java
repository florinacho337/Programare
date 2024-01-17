package ro.ubbcluj.gr221.domain;

public class Movie extends Entity<Long> {
    private int idRegizor;
    private String name;
    private String gen;

    public Movie(int idRegizor, String name, String gen) {
        this.idRegizor = idRegizor;
        this.name = name;
        this.gen = gen;
    }

    public int getIdRegizor() {
        return idRegizor;
    }

    public void setIdRegizor(int idRegizor) {
        this.idRegizor = idRegizor;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getGen() {
        return gen;
    }

    public void setGen(String gen) {
        this.gen = gen;
    }
}
