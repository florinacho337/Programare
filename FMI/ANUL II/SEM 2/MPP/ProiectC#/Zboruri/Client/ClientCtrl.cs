using System.Collections;
using Model;
using Services;

namespace Client;

public class ClientCtrl: IZboruriObserver
{
    public event EventHandler<ZboruriAngajatEventArgs> updateEvent;
    private readonly IZboruriServices _server;
    private Angajat _currentAngajat;

    public ClientCtrl(IZboruriServices server)
    {
        this._server = server;
        _currentAngajat = null;
    }

    public void TicketBought(Zbor oldZbor, Zbor zbor)
    {
        ZboruriAngajatEventArgs userArgs=new ZboruriAngajatEventArgs(ZboruriAngajatEvent.TicketBought, zbor);
        Console.WriteLine("Ticket bought!");
        OnUserEvent(userArgs);
    }

    public void Login(string username, string password)
    {
        Angajat angajat = new Angajat(username, password);
        angajat.Id = username;
        _server.Login(angajat, this);
        Console.WriteLine("Login succeeded ....");
        _currentAngajat = angajat;
        Console.WriteLine("Current angajat {0}", angajat);
    }

    public void Logout()
    {
        Console.WriteLine("Ctrl logout");
        _server.Logout(_currentAngajat, this);
        _currentAngajat = null;
    }

    public IList<Zbor> FindZboruri()
    {
        IList<Zbor> zboruri = new List<Zbor>();
        foreach (var zbor in _server.FindZboruri())
        {
            zboruri.Add(zbor);
        }

        return zboruri;
    }

    public IList<Zbor> FindZboruriDestDateAndMinSeats(string destination, DateTime date, int min)
    {
        IList<Zbor> zboruri = new List<Zbor>();
        foreach (var zbor in _server.FindZboruriDestDateAndMinSeats(destination, date, min))
        {
            zboruri.Add(zbor);
        }

        return zboruri;
    }

    public Zbor FindZbor(int id)
    {
        Zbor zbor = _server.FindZbor(id);
        return zbor;
    }

    public void CumparaBilet(string client, string city, string country, List<TuristBilet> turisti, int nrLocuri, Zbor zbor)
    {
        Zbor newZbor = new Zbor(zbor.Destinatie, zbor.Plecare, zbor.Aeroport, zbor.NrLocuri)
        {
            Id = zbor.Id
        };
        ZboruriAngajatEventArgs angajatArgs =
            new ZboruriAngajatEventArgs(ZboruriAngajatEvent.TicketBought, newZbor);
        OnUserEvent(angajatArgs);
        _server.CumparaBilet(client, country, city, turisti, nrLocuri, zbor);
    }
    
    protected virtual void OnUserEvent(ZboruriAngajatEventArgs e)
    {
        if (updateEvent == null) return;
        updateEvent(this, e);
        Console.WriteLine("Update Event called");
    }
}