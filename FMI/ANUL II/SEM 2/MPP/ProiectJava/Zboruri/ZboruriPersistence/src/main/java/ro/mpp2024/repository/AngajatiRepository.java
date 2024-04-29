package ro.mpp2024.repository;

import ro.mpp2024.domain.Angajat;

public interface AngajatiRepository extends Repository<String, Angajat> {
    Angajat findByUsernameAndPass(String username, String password);
}
