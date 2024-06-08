using Model;
using Persistence;
using Services;

namespace Server.Service;

public class Service(
    IAngajatiRepository angajatiRepository,
    IBileteRepository bileteRepository,
    IZboruriRepository zboruriRepository)
    : IZboruriServices
{
    private readonly IDictionary<string, IZboruriObserver> _loggedClients = new Dictionary<string, IZboruriObserver>();

    public void Login(Angajat angajat, IZboruriObserver client)
    {
        Angajat? angajatR = angajatiRepository.FindByUsernameAndPass(angajat.Username, angajat.Parola);
        if (angajatR == null)
            throw new ZboruriException("Username or password is incorrect.");
        if (!_loggedClients.TryAdd(angajatR.Username, client))
            throw new ZboruriException("User already logged in.");
    }

    public void Logout(Angajat angajat, IZboruriObserver client)
    {
        IZboruriObserver localClient = _loggedClients[angajat.Username];
        if (localClient == null)
            throw new ZboruriException("Angajat " + angajat.Username + " not logged in.");
        _loggedClients.Remove(angajat.Username);
    }

    public List<Zbor> FindZboruriDestDateAndMinSeats(string dest, DateTime data, int min)
    {
        return zboruriRepository.FindAllByDestDateAndMinimumSeats(dest, data, min).Where(z => z.NrLocuri > 0).ToList();
    }

    public List<Zbor> FindZboruri()
    {
        return zboruriRepository.FindAll().Where(z => z.NrLocuri > 0).ToList();
    }

    public void CumparaBilet(string client, string tara, string oras, List<TuristBilet> turisti, int nrLocuri, Zbor zbor)
    {
        Zbor newZbor = new Zbor(zbor.Destinatie, zbor.Plecare, zbor.Aeroport, zbor.NrLocuri - nrLocuri)
        {
            Id = zbor.Id
        };
        zboruriRepository.Update(newZbor.Id, newZbor);
        Bilet bilet = new Bilet(client, oras, tara, turisti, nrLocuri, newZbor);
        bileteRepository.Save(bilet);
        NotifyAngajati(zbor, newZbor);
    }

    private void NotifyAngajati(Zbor zbor, Zbor newZbor)
    {
        foreach (var angajat in _loggedClients.Keys)
        {
            IZboruriObserver angajatClient = _loggedClients[angajat];
            Task.Run(() => angajatClient.TicketBought(zbor, newZbor));
        }
    }

    public Zbor FindZbor(int id)
    {
        return zboruriRepository.FindOne(id);
    }
}