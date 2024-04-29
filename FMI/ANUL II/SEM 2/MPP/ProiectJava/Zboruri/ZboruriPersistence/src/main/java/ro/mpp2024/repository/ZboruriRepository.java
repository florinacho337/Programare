package ro.mpp2024.repository;

import ro.mpp2024.domain.Zbor;

import java.time.LocalDateTime;
import java.util.List;

public interface ZboruriRepository extends Repository<Integer, Zbor> {
    List<Zbor> findAllByDestDateAndMinimumSeats(String destination, LocalDateTime date, int min);
}
