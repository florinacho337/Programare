package ro.mpp2024.services;

import ro.mpp2024.domain.Zbor;

public interface ZboruriObserver {
    void ticketBought(Zbor oldZbor, Zbor zbor) throws ZboruriException;
}
