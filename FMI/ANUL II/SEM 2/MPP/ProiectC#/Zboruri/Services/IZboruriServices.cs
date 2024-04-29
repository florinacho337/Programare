using Model;

namespace Services;

public interface IZboruriServices
{
    void Login(Angajat angajat, IZboruriObserver client);
    void Logout(Angajat angajat, IZboruriObserver client);
    List<Zbor> FindZboruriDestDateAndMinSeats(string dest, DateTime data, int min);
    List<Zbor> FindZboruri();
    void CumparaBilet(string client, string tara, string oras, List<TuristBilet> turisti, int nrLocuri, Zbor zbor);
    Zbor FindZbor(int id);
}