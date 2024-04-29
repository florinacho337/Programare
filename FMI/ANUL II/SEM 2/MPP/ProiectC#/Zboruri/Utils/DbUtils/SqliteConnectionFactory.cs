using System.Data;
using Mono.Data.Sqlite;

namespace Utils.DbUtils
{
	public class SqliteConnectionFactory : ConnectionFactory
	{
		public override IDbConnection CreateConnection(IDictionary<string,string> props)
		{
			//Mono Sqlite Connection
			
			String connectionString = props["ConnectionString"];
			Console.WriteLine("SQLite ---Se deschide o conexiune la  ... {0}", connectionString);
			return new SqliteConnection(connectionString);
			
		}
	}
}
