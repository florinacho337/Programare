using log4net;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Model;

namespace Persistence;

public class BileteRepositoryEF: IBileteRepository
{
    private static readonly ILog Logger = LogManager.GetLogger("BileteRepositoryEF");
    private readonly ZboruriDbContext _dbContext;

    public BileteRepositoryEF(ZboruriDbContext dbContext)
    {
        Logger.Info("Initializing BileteRepositoryEF");
        _dbContext = dbContext;
    }

    public void Save(Bilet entity)
    {
        Logger.InfoFormat("saving bilet {0}", entity);
        var zbor = _dbContext.Zboruri.AsNoTracking().FirstOrDefault(z => z.Id == entity.Zbor.Id);

        if (zbor != null)
        {
            _dbContext.Zboruri.Attach(zbor);
            _dbContext.Entry(zbor).State = EntityState.Unchanged;
            
            _dbContext.Bilete.Add(entity);
            var result = _dbContext.SaveChanges();
            
            if (result == 0)
            {
                Logger.Error("No tickets saved!");
                throw new RepositoryException("No tickets saved!");
            }
            else
            {
                Logger.InfoFormat("Saved {0} tickets", result);
            }
        }
        else
        {
            Logger.Error("No zbor found!");
            throw new RepositoryException("No zbor found!");
        }
    }

    public void Update(int id, Bilet update)
    {
    }

    public Bilet FindOne(int id)
    {
        return null;
    }

    public IEnumerable<Bilet> FindAll()
    {
        return null;
    }

    public void Delete(int id)
    {
    }
}