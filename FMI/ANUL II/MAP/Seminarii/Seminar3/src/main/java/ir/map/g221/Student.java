package ir.map.g221;

import java.util.Comparator;
import java.util.Objects;

public class Student {
    private String nume;
    private float medie;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Student student = (Student) o;
        return Float.compare(medie, student.medie) == 0 && Objects.equals(nume, student.nume);
    }

    @Override
    public int hashCode() {
        return Objects.hash(nume, medie);
    }

    @Override
    public String toString() {
        return "Student{" +
                "nume='" + nume + '\'' +
                ", medie=" + medie +
                '}';
    }

    public void setNume(String nume) {
        this.nume = nume;
    }

    public void setMedie(float medie) {
        this.medie = medie;
    }

    public String getNume() {
        return nume;
    }

    public float getMedie() {
        return medie;
    }

    public Student(String nume, float medie) {
        this.nume = nume;
        this.medie = medie;
    }
}
