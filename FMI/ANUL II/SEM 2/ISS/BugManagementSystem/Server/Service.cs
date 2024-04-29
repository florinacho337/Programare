using Data;
using Model;
using Services;

namespace Server;

public class Service(BugManagementSystemDbContext dbContext) : IBmsServices
{
    // private readonly IDictionary <string, IbmsObserver> _loggedClients = new Dictionary<string, IbmsObserver>();

    public void Close()
    {
        throw new NotImplementedException();
    }

    public List<Employee> GetAllEmployees()
    {
        return dbContext.Employees.ToList();
    }

    public void AddEmployee(Employee employee)
    {
        dbContext.Employees.Add(employee);
        dbContext.SaveChanges();
    }

    public void RemoveEmployee(string username)
    {
        var employee = dbContext.Employees.FirstOrDefault(e => e.Username == username);
        if (employee == null) return;
        dbContext.Employees.Remove(employee);
        dbContext.SaveChanges();
    }
}