using Model;

namespace Services;

public interface IZboruriObserver
{
    void TicketBought(Zbor oldZbor, Zbor zbor);
}