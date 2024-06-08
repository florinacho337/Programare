using Model;

namespace Networking;

public class Response
{
    public ResponseType Type { get; set; }
    public String ErrorMessage { get; set; }
    public List<Zbor> Flights { get; set; }
    public Zbor Zbor { get; set; }
    public Zbor OldZbor { get; set; }
    public Zbor Found { get; set; }

    public override string ToString()
    {
        return
            $"{nameof(Type)}: {Type}, {nameof(ErrorMessage)}: {ErrorMessage}, {nameof(Flights)}: {Flights}, {nameof(Zbor)}: {Zbor}, {nameof(OldZbor)}: {OldZbor}";
    }
}