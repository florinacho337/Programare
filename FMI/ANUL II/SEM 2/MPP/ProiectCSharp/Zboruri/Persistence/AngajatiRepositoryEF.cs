using log4net;
using Model;

namespace Persistence;

public class AngajatiRepositoryEF: IAngajatiRepository
{
    private static readonly ILog Logger = LogManager.GetLogger("AngajatiRepositoryEF");
    private readonly ZboruriDbContext _dbContext;

    public AngajatiRepositoryEF(ZboruriDbContext dbContext)
    {
        Logger.Info("Initializing AngajatiRepositoryEF");
        _dbContext = dbContext;
    }

    public void Save(Angajat entity)
    {
    }

    public void Update(string id, Angajat update)
    {
    }

    public Angajat FindOne(string id)
    {
        return null;
    }

    public IEnumerable<Angajat> FindAll()
    {
        return null;
    }

    public void Delete(string id)
    {
    }

    public Angajat? FindByUsernameAndPass(string username, string password)
    {
        Logger.InfoFormat("finding angajat with username {0}", username);
        var angajat = _dbContext.Angajati.FirstOrDefault(a => a.Username == username && a.Parola == password);
        Logger.InfoFormat("Exiting findOne with value {0}", angajat);
        return angajat;
    }
}