using System.Data;
using log4net;
using Model;

namespace Persistence;

public class AngajatiDbRepository : IAngajatiRepository
{
    private static readonly ILog Logger = LogManager.GetLogger("AngajatiDbRepository");
    private readonly IDictionary<string, string> _props = new SortedList<string, string>();

    public AngajatiDbRepository(IDictionary<string, string> props)
    {
        Logger.Info("Initializing AngajatiDBRepository");
        this._props["ConnectionString"] = "URI=" + props["ConnectionString"] + ", Version=3";
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

    public Angajat? FindByUsernameAndPass(string user, string password)
    {
        Logger.InfoFormat("finding angajat with username {0}", user);
        IDbConnection con = DbUtils.GetConnection(_props);
        using (var comm = con.CreateCommand())
        {
            comm.CommandText = "select Username, Parola, Nume from angajati where Username=@user and Parola=@pass";
            IDbDataParameter paramUser = comm.CreateParameter();
            IDbDataParameter paramPass = comm.CreateParameter();
            paramUser.ParameterName = "@user";
            paramPass.ParameterName = "@pass";
            paramUser.Value = user;
            paramPass.Value = password;
            comm.Parameters.Add(paramUser);
            comm.Parameters.Add(paramPass);
        
            using (var dataR = comm.ExecuteReader())
            {
                if (dataR.Read())
                {
                    string username = dataR.GetString(0);
                    string parola = dataR.GetString(1);
                    string nume = dataR.GetString(2);
                    Angajat angajat = new Angajat(username, nume, parola)
                    {
                        Id = username
                    };
                    Logger.InfoFormat("Exiting findOne with value {0}", angajat);
                    return angajat;
                }
            }
        }
        
        Logger.InfoFormat("Exiting findOne with value {0}", null);
        return null;
    }
}