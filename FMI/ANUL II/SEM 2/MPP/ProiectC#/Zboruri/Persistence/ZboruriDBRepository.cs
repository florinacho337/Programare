using System.Data;
using System.Globalization;
using log4net;
using Model;
using Utils;

namespace Persistence
{
    public class ZboruriDbRepository: IZboruriRepository
    {
        private static readonly ILog Logger = LogManager.GetLogger("ZboruriDbRepository");
        private readonly IDictionary<string, string> _props = new SortedList<string, string>();

        public ZboruriDbRepository(IDictionary<string, string> props)
        {
            Logger.Info("Initializing ZboruriDBRepository");
            _props["ConnectionString"] = "URI=" + props["ConnectionString"] + ", Version=3";
        }

        public void Save(Zbor entity)
        {
        }

        public void Update(int id, Zbor update)
        {
            Logger.InfoFormat("updating zbor with id {0}", id);
            IDbConnection con = DbUtils.GetConnection(_props);
            using var comm = con.CreateCommand();
            comm.CommandText =
                "update zboruri set Destinatie=@destinatie, Plecare=@plecare, Aeroport=@aeroport, NrLocuri=@nr_locuri where Id=@id";
            IDbDataParameter paramDest = comm.CreateParameter();
            IDbDataParameter paramPlecare = comm.CreateParameter();
            IDbDataParameter paramAeroport = comm.CreateParameter();
            IDbDataParameter paramNrLocuri = comm.CreateParameter();
            IDbDataParameter paramId = comm.CreateParameter();
            paramDest.ParameterName = "@destinatie";
            paramPlecare.ParameterName = "@plecare";
            paramAeroport.ParameterName = "@aeroport";
            paramNrLocuri.ParameterName = "@nr_locuri";
            paramId.ParameterName = "@id";
            paramDest.Value = update.Destinatie;
            paramPlecare.Value = update.Plecare.ToString(Constants.DateTimeFormatter);
            paramAeroport.Value = update.Aeroport;
            paramNrLocuri.Value = update.NrLocuri;
            paramId.Value = id;
            comm.Parameters.Add(paramDest);
            comm.Parameters.Add(paramPlecare);
            comm.Parameters.Add(paramAeroport);
            comm.Parameters.Add(paramNrLocuri);
            comm.Parameters.Add(paramId);

            int result = comm.ExecuteNonQuery();
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
            IDbConnection con = DbUtils.GetConnection(_props);
            using (var comm = con.CreateCommand())
            {
                comm.CommandText = "select Id, Destinatie, Plecare, Aeroport, NrLocuri from zboruri where Id=@id";
                IDbDataParameter paramId = comm.CreateParameter();
                paramId.ParameterName = "@id";
                paramId.Value = id;
                comm.Parameters.Add(paramId);

                using (var dataR = comm.ExecuteReader())
                {
                    if (dataR.Read())
                    {
                        Zbor zbor = CreateZbor(dataR);
                        Logger.InfoFormat("Exiting findOne with value {0}", zbor);
                        return zbor;
                    }
                }
            }
            Logger.InfoFormat("Exiting findOne with value {0}", null);
            return null;
        }

        private Zbor CreateZbor(IDataReader dataR)
        {
            int idV = dataR.GetInt32(0);
            string destinatie = dataR.GetString(1);
            DateTime plecare = DateTime.ParseExact(dataR.GetString(2), Constants.DateTimeFormatter, CultureInfo.InvariantCulture);
            string aeroport = dataR.GetString(3);
            int nrLocuri = dataR.GetInt32(4);
            Zbor zbor = new Zbor(destinatie, plecare, aeroport, nrLocuri)
            {
                Id = idV
            };
            return zbor;
        }

        public IEnumerable<Zbor> FindAll()
        {
            Logger.InfoFormat("finding flights");
            List<Zbor> zboruri = new List<Zbor>();
            IDbConnection con = DbUtils.GetConnection(_props);
            using (var comm = con.CreateCommand())
            {
                comm.CommandText = "select Id, Destinatie, Plecare, Aeroport, NrLocuri from zboruri";

                using (var dataR = comm.ExecuteReader())
                {
                    while (dataR.Read())
                    {
                        Zbor zbor = CreateZbor(dataR);
                        zboruri.Add(zbor);
                    }
                }
                Logger.InfoFormat("Found {0} instances", zboruri.Count);
            }
            Logger.InfoFormat("Exiting findAllByDestAndDate with value {0}", null);
            return zboruri;
        }

        public void Delete(int id)
        {
        }

        public List<Zbor> FindAllByDestDateAndMinimumSeats(string destination, DateTime data, int min)
        {
            Logger.InfoFormat("finding flights with destination {0} from {1} with minimum {2} seats", destination, data, min);
            List<Zbor> zboruri = new List<Zbor>();
            IDbConnection con = DbUtils.GetConnection(_props);
            using (var comm = con.CreateCommand())
            {
                comm.CommandText = "select Id, Destinatie, Plecare, Aeroport, NrLocuri from zboruri where Destinatie=@destinatie and Plecare like @data || '%' and NrLocuri >= @minimum";
                IDbDataParameter paramDest = comm.CreateParameter();
                IDbDataParameter paramData = comm.CreateParameter();
                IDbDataParameter paramLocuri = comm.CreateParameter();
                paramDest.ParameterName = "@destinatie";
                paramData.ParameterName = "@data";
                paramLocuri.ParameterName = "@minimum";
                paramDest.Value = destination;
                paramData.Value = data.ToString(Constants.DateFormatter);
                paramLocuri.Value = min;
                comm.Parameters.Add(paramDest);
                comm.Parameters.Add(paramData);
                comm.Parameters.Add(paramLocuri);

                using (var dataR = comm.ExecuteReader())
                {
                    while (dataR.Read())
                    {
                        Zbor zbor = CreateZbor(dataR);
                        zboruri.Add(zbor);
                    }
                }
                Logger.InfoFormat("Found {0} instances", zboruri.Count);
            }
            Logger.InfoFormat("Exiting findAllByDestAndDate with value {0}", null);
            return zboruri;
        }
    }
}