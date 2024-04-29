using System.Configuration;
using System.Data;
using Microsoft.EntityFrameworkCore;
using Model;
using Utils.DbUtils;

namespace Persistence
{
    public class DbUtils
    {
        private static IDbConnection _instance;


        public static IDbConnection GetConnection(IDictionary<string, string> props)
        {
            if (_instance == null || _instance.State == ConnectionState.Closed)
            {
                _instance = GetNewConnection(props);
                _instance.Open();
            }

            return _instance;
        }

        private static IDbConnection GetNewConnection(IDictionary<string, string> props)
        {
            return ConnectionFactory.getInstance().CreateConnection(props);
        }
    }

    public class ZboruriDbContext(string connectionString) : DbContext(GetOptions(connectionString))
    {
        public DbSet<Angajat> Angajati { get; set; }
        public DbSet<Zbor> Zboruri { get; set; }
        public DbSet<Bilet> Bilete { get; set; }
        public DbSet<TuristBilet> BileteTuristi { get; set; }

        public ZboruriDbContext() : this(GetConnectionStringByName("zboruriDB"))
        {
        }
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Angajat>(entity =>
            {
                entity.HasKey(e => e.Username);
                entity.Property(e => e.Username).ValueGeneratedNever();
                entity.ToTable("angajati");
            });

            modelBuilder.Entity<Zbor>(entity =>
            {
                entity.Property(e => e.Plecare)
                    .HasConversion(
                        v => v.ToString("s"),
                        v => DateTime.Parse(v)
                    );
                entity.ToTable("zboruri");
            });

            modelBuilder.Entity<TuristBilet>(entity =>
            {
                entity.Property<int>("BiletId"); // Shadow property
                entity.Property<string>("Turist");
                
                entity.HasKey("BiletId", "Turist");
                
                entity.HasOne(e => e.Bilet)
                    .WithMany(e => e.Turisti)
                    .HasForeignKey("BiletId");

                entity.Property("BiletId").IsRequired();
                entity.Property("Turist").IsRequired();
                
                entity.ToTable("turisti_bilet");
            });

            modelBuilder.Entity<Bilet>(entity =>
            {
                entity.HasMany(e => e.Turisti)
                    .WithOne(e => e.Bilet)
                    .HasForeignKey("BiletId");
                entity.ToTable("bilete");
            });
        }

        private static DbContextOptions GetOptions(string connectionString)
        {
            var optionsBuilder = new DbContextOptionsBuilder();
            optionsBuilder.UseSqlite(connectionString);
            return optionsBuilder.Options;
        }
        
        private static string GetConnectionStringByName(string name)
        {
            // Assume failure.
            string returnValue = null;

            // Look for the name in the connectionStrings section.
            ConnectionStringSettings settings = ConfigurationManager.ConnectionStrings[name];

            // If found, return the connection string.
            if (settings != null)
                returnValue = settings.ConnectionString;

            return returnValue;
        }
    }
}