using System.Data;
using log4net;
using Model;

namespace Persistence
{
    public class BileteDbRepository: IBileteRepository
    {
        private static readonly ILog Logger = LogManager.GetLogger("BileteDbRepository");
        private readonly IDictionary<string, string> _props = new SortedList<string, string>();

        public BileteDbRepository(IDictionary<string, string> props)
        {
            Logger.Info("Initializing BileteDBRepository");
            _props["ConnectionString"] = "URI=" + props["ConnectionString"] + ", Version=3";
        }

        public void Save(Bilet entity)
        {
            Logger.InfoFormat("saving bilet {0}", entity);
            var con = DbUtils.GetConnection(_props);
            using var comm = con.CreateCommand();
            comm.CommandText = "insert into bilete(Client, Oras, Tara, NrLocuri, Zbor) values (@client, @oras, @tara, @nr_locuri, @zbor)";
            IDbDataParameter paramClient = comm.CreateParameter();
            IDbDataParameter paramOras = comm.CreateParameter();
            IDbDataParameter paramTara = comm.CreateParameter();
            IDbDataParameter paramNrLocuri = comm.CreateParameter();
            IDbDataParameter paramZbor = comm.CreateParameter();
            paramClient.ParameterName = "@client";
            paramOras.ParameterName = "@oras";
            paramTara.ParameterName = "@tara";
            paramNrLocuri.ParameterName = "@nr_locuri";
            paramZbor.ParameterName = "@zbor";
            paramClient.Value = entity.Client;
            paramOras.Value = entity.Oras;
            paramTara.Value = entity.Tara;
            paramNrLocuri.Value = entity.NrLocuri;
            paramZbor.Value = entity.Zbor.Id;
            comm.Parameters.Add(paramClient);
            comm.Parameters.Add(paramOras);
            comm.Parameters.Add(paramTara);
            comm.Parameters.Add(paramNrLocuri);
            comm.Parameters.Add(paramZbor);

            int result = comm.ExecuteNonQuery();
            if (result == 0)
            {
                Logger.Error("No tickets saved!");
                throw new RepositoryException("No tickets saved!");
            }
            else
            {
                SaveTuristi(entity.Turisti);
                Logger.InfoFormat("Saved {0} tickets", result);
            }
        }

        private void SaveTuristi(List<TuristBilet> entityTuristi)
        { 
            
            IDbConnection con = DbUtils.GetConnection(_props);
            Logger.Info("saving turisti");
            using var comm = con.CreateCommand();
            comm.CommandText = "select max(Id) as \"id\" from bilete";
            using var dataR = comm.ExecuteReader();
            if (dataR.Read())
                foreach (var turist in entityTuristi)
                    SaveTurist(con, dataR.GetInt32(0), turist.Turist);
        }

        private void SaveTurist(IDbConnection con, int id, string turist)
        {
            Logger.InfoFormat("saving turist {0}", turist);
            using var com = con.CreateCommand();
            com.CommandText = "insert into turisti_bilet (BiletId, Turist) values (@id_bilet, @turist)";
            IDbDataParameter paramIdBilet = com.CreateParameter();
            IDbDataParameter paramTurist = com.CreateParameter();
            paramIdBilet.ParameterName = "@id_bilet";
            paramTurist.ParameterName = "@turist";
            paramIdBilet.Value = id;
            paramTurist.Value = turist;
            com.Parameters.Add(paramIdBilet);
            com.Parameters.Add(paramTurist);

            int result = com.ExecuteNonQuery();
            if (result == 0)
            {
                Logger.Error("No Turist saved!");
                throw new RepositoryException("No Turist saved!");
            }
            else
                Logger.InfoFormat("Turist {0} saved", turist);
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
}