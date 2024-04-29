using Model;

namespace Persistence
{
    public interface IAngajatiRepository: IRepository<string, Angajat>
    {
        Angajat? FindByUsernameAndPass(string username, string password);
    }
}