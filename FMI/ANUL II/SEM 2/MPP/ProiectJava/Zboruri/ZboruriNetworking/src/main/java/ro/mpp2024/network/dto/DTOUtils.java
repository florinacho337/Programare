package ro.mpp2024.network.dto;

import ro.mpp2024.domain.Angajat;
import ro.mpp2024.domain.Zbor;
import ro.mpp2024.utils.Constants;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;


public class DTOUtils {
    public static Zbor getFromDTO(ZborDTO zborDTO){
        String aeroport = zborDTO.getAeroport();
        String destinatie = zborDTO.getDestinatie();
        LocalDateTime plecare = LocalDateTime.parse(zborDTO.getPlecare(), Constants.DATE_TIME_FORMATTER);
        int nrLocuri = zborDTO.getNrLocuri();
        Zbor zbor = new Zbor(aeroport, destinatie, plecare, nrLocuri);
        zbor.setId(zborDTO.getId());
        return zbor;
    }

    public static ZborDTO getDTO(Zbor zbor){
        String aeroport = zbor.getAeroport();
        String destinatie = zbor.getDestinatie();
        LocalDateTime plecare = zbor.getPlecare();
        int nrLocuri = zbor.getNrLocuri();
        int id = zbor.getId();
        return new ZborDTO(aeroport, destinatie, plecare.format(Constants.DATE_TIME_FORMATTER), nrLocuri, plecare.toLocalTime().toString(), id);
    }
}
