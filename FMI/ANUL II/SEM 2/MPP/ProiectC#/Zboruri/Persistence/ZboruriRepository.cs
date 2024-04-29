using Model;

namespace Persistence
{
    public interface IZboruriRepository: IRepository<int, Zbor>
    {
        List<Zbor> FindAllByDestDateAndMinimumSeats(String destination, DateTime data, int min);
    }
}