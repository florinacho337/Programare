package ro.mpp2024.server;

import ro.mpp2024.domain.Angajat;
import ro.mpp2024.domain.Bilet;
import ro.mpp2024.domain.Zbor;
import ro.mpp2024.repository.*;
import ro.mpp2024.services.ZboruriException;
import ro.mpp2024.services.ZboruriObserver;
import ro.mpp2024.services.ZboruriServices;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.StreamSupport;

public class Service implements ZboruriServices {
    private final AngajatiRepository repoAngajati;
    private final BileteRepository repoBilete;
    private final ZboruriRepository repoZboruri;
    private final Map<String, ZboruriObserver> loggedEmployees;

    public Service(AngajatiRepository repoAngajati, BileteRepository repoBilete, ZboruriRepository repoZboruri) {
        this.repoAngajati = repoAngajati;
        this.repoBilete = repoBilete;
        this.repoZboruri = repoZboruri;
        this.loggedEmployees = new HashMap<>();
    }

    @Override
    public synchronized void login(Angajat angajat, ZboruriObserver observer) throws ZboruriException {
        Angajat angajatR = repoAngajati.findByUsernameAndPass(angajat.getUsername(), angajat.getParola());
        if (angajatR == null) {
            throw new ZboruriException("Username or password is incorrect.");
        }

        if (loggedEmployees.get(angajat.getUsername()) != null) {
            throw new ZboruriException("User already logged in.");
        }
        loggedEmployees.put(angajat.getUsername(), observer);
    }

    @Override
    public synchronized void logout(Angajat angajat, ZboruriObserver observer) throws ZboruriException {
        ZboruriObserver localClient = loggedEmployees.remove(angajat.getUsername());
        if (localClient == null) {
            throw new ZboruriException("Angajat " + angajat.getUsername() + " not logged in.");
        }
    }

    @Override
    public synchronized List<Zbor> findZboruriDestDateAndMinSeats(String dest, LocalDateTime date, int min) {
        return repoZboruri.findAllByDestDateAndMinimumSeats(dest, date, min);
    }

    @Override
    public synchronized List<Zbor> findZboruri() {
        return StreamSupport.stream(repoZboruri.findAll().spliterator(), false).toList();
    }

    @Override
    public synchronized void cumparaBilet(String client, String tara, String oras, List<String> turisti, int nrLocuri, Zbor zbor) {
        Zbor newZbor = new Zbor(zbor.getAeroport(), zbor.getDestinatie(), zbor.getPlecare(), zbor.getNrLocuri() - nrLocuri);
        newZbor.setId(zbor.getId());
        repoZboruri.update(newZbor.getId(), newZbor);
        Bilet bilet = new Bilet(client, oras, tara, turisti, nrLocuri, newZbor);
        repoBilete.save(bilet);
        notifyAngajati(zbor, newZbor);
    }

    private void notifyAngajati(Zbor oldZbor, Zbor zbor) {
        ExecutorService executor= Executors.newFixedThreadPool(5);
        for(var angajat :loggedEmployees.keySet()) {
            ZboruriObserver angajatClient = loggedEmployees.get(angajat);
            if (angajatClient != null)
                executor.execute(() -> {
                    try {
                        System.out.println("Notifying [" + angajat + "] a ticket was bought.");
                        angajatClient.ticketBought(oldZbor, zbor);
                    } catch (ZboruriException e) {
                        System.err.println("Error notifying angajat " + e);
                    }
                });
        }
    }
}