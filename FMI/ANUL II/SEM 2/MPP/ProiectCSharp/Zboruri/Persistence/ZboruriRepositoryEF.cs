using System.Globalization;
using log4net;
using Model;
using Utils;

namespace Persistence;

public class ZboruriRepositoryEF: IZboruriRepository
{
    private static readonly ILog Logger = LogManager.GetLogger("ZboruriRepositoryEF");
    private readonly ZboruriDbContext _dbContext;

    public ZboruriRepositoryEF(ZboruriDbContext dbContext)
    {
        Logger.Info("Initializing ZboruriRepositoryEF");
        _dbContext = dbContext;
    }

    public void Save(Zbor entity)
    {
    }

    public void Update(int id, Zbor update)
    {
        Logger.InfoFormat("updating zbor with id {0}", id);
        var zbor = _dbContext.Zboruri.Find(id);
        if (zbor == null)
        {
            Logger.Error("No flight found!");
            throw new RepositoryException("No flight found!");
        }
        _dbContext.Entry(zbor).CurrentValues.SetValues(update);
        int result = _dbContext.SaveChanges();
        if (result == 0)
        {
            Logger.Error("No flights updated!");
            throw new RepositoryException("No flights updated!");
        }
        else
        {
            Logger.InfoFormat("Updated {0} instances", result);
        }
    }

    public Zbor FindOne(int id)
    {
        Logger.InfoFormat("finding zbor with id {0}", id);
        var zbor = _dbContext.Zboruri.Find(id);
        if (zbor != null)
        {
            const string format = Constants.DateTimeFormatter;
            zbor.Plecare = DateTime.ParseExact(zbor.Plecare.ToString(format), format, CultureInfo.InvariantCulture);
        }
        Logger.InfoFormat("Exiting findOne with value {0}", zbor);
        return zbor;
    }

    public IEnumerable<Zbor> FindAll()
    {
        Logger.InfoFormat("finding flights");
        var zboruri = _dbContext.Zboruri.ToList();
        foreach (var zbor in zboruri)
        {
            var formatter = Constants.DateTimeFormatter;
            zbor.Plecare = DateTime.ParseExact(zbor.Plecare.ToString(formatter), formatter, CultureInfo.InvariantCulture);
        }
        Logger.InfoFormat("Found {0} instances", zboruri.Count);
        return zboruri;
    }

    public void Delete(int id)
    {
    }

    public List<Zbor> FindAllByDestDateAndMinimumSeats(string destination, DateTime data, int min)
    {
        Logger.InfoFormat("finding flights with destination {0} from {1} with minimum {2} seats", destination, data, min);
        var zboruri = _dbContext.Zboruri.Where(z => z.Destinatie == destination && z.Plecare.Date == data.Date && z.NrLocuri >= min).ToList();
        foreach (var zbor in zboruri)
        {
            var formatter = Constants.DateTimeFormatter;
            zbor.Plecare = DateTime.ParseExact(zbor.Plecare.ToString(formatter), formatter, CultureInfo.InvariantCulture);
        }
        Logger.InfoFormat("Found {0} instances", zboruri.Count);
        return zboruri;
    }
}