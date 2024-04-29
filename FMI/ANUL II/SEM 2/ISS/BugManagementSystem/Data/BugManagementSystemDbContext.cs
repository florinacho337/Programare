using Microsoft.EntityFrameworkCore;
using Model;

namespace Data;

public class BugManagementSystemDbContext(string connectionString) : DbContext
{
    public DbSet<Bug> Bugs { get; set; }
    public DbSet<Employee> Employees { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Employee>()
            .HasKey(e => e.Username);
    }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseSqlite("Data Source=/home/florin/FMI/AN II Sem 2/ISS/BugManagementSystem/Data/bugManagementSystem.db");
    }
}