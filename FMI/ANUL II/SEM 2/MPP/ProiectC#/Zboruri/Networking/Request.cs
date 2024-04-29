using Model;

namespace Networking;

public class Request
{
    public RequestType Type { get; set; }
    public Angajat Angajat { get; set; }
    public int MinSeats { get; set; }
    public string Destination { get; set; }
    public DateTime Date { get; set; }
    public string Client { get; set; }
    public string Tara { get; set; }
    public string Oras { get; set; }
    public List<string> Turisti { get; set; }
    public int NrLocuri { get; set; }
    public Zbor Zbor { get; set; }
    public int Id { get; set; }

    public override string ToString()
    {
        return
            $"{nameof(Type)}: {Type}, {nameof(Angajat)}: {Angajat}, {nameof(MinSeats)}: {MinSeats}, {nameof(Destination)}: {Destination}, {nameof(Date)}: {Date}, {nameof(Client)}: {Client}, {nameof(Tara)}: {Tara}, {nameof(Oras)}: {Oras}, {nameof(Turisti)}: {Turisti}, {nameof(NrLocuri)}: {NrLocuri}, {nameof(Zbor)}: {Zbor}";
    }
}