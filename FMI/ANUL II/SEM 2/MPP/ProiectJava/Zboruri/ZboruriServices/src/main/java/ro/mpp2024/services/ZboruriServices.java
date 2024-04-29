package ro.mpp2024.services;

import ro.mpp2024.domain.Angajat;
import ro.mpp2024.domain.Zbor;

import java.time.LocalDateTime;
import java.util.List;

public interface ZboruriServices {
    void login(Angajat angajat, ZboruriObserver client) throws ZboruriException;
    void logout(Angajat angajat, ZboruriObserver client) throws ZboruriException;
    List<Zbor> findZboruriDestDateAndMinSeats(String dest, LocalDateTime date, int min) throws ZboruriException;
    List<Zbor> findZboruri() throws ZboruriException;
    void cumparaBilet(String client, String tara, String oras, List<String> turisti, int nrLocuri, Zbor zbor) throws ZboruriException;
}
