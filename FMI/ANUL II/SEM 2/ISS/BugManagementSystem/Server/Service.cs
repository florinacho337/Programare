using Data;
using Model;
using Services;

namespace Server;

public class Service(BugManagementSystemDbContext dbContext) : IBmsServices
{
    private readonly IDictionary<string, IBmsObserver> _loggedClients = new Dictionary<string, IBmsObserver>();

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

    // ---------------------------------------- NEW METHODS ----------------------------------------

    public List<Bug> GetAllBugs()
    {
        return dbContext.Bugs.ToList();
    }

    public Employee LogIn(Employee employee, IBmsObserver client)
    {
        var employeeRepo =
            dbContext.Employees.FirstOrDefault(e => e.Username == employee.Username && e.Password == employee.Password);
        if (employeeRepo == null) throw new BmsException("Username or password is incorrect!");
        if (!_loggedClients.TryAdd(employeeRepo.Username, client)) throw new BmsException("User already logged in!");
        return employeeRepo;
    }

    public void LogOut(Employee employee)
    {
        var localClient = _loggedClients[employee.Username];
        if (localClient == null)
            throw new BmsException("Employee " + employee.Username + " not logged in.");
        _loggedClients.Remove(employee.Username);
    }

    public void AddBug(Bug bug)
    {
        var bugR = dbContext.Bugs.Add(bug);
        dbContext.SaveChanges();
        NotifyClients(bugR.Entity, "addBug");
    }

    private void NotifyClients(Bug bug, string operation)
    {
        if (operation == "addBug")
            foreach (var employee in _loggedClients.Keys)
            {
                var client = _loggedClients[employee];
                Task.Run(() => client.BugAdded(bug));
            }
        else if (operation == "updateBug")
            foreach (var employee in _loggedClients.Keys)
            {
                var client = _loggedClients[employee];
                Task.Run(() => client.BugUpdated(bug));
            }
        else if (operation == "removeBug")
            foreach (var employee in _loggedClients.Keys)
            {
                var client = _loggedClients[employee];
                Task.Run(() => client.BugRemoved(bug));
            }
    }

    public void UpdateBug(Bug bug)
    {
        var existingBug = dbContext.Bugs.FirstOrDefault(b => b.Id == bug.Id);
        if (existingBug == null) return;
        dbContext.Entry(existingBug).CurrentValues.SetValues(bug);
        dbContext.SaveChanges();
        NotifyClients(existingBug, "updateBug");
    }

    public void RemoveBug(Bug bug)
    {
        var existingBug = dbContext.Bugs.FirstOrDefault(b => b.Id == bug.Id);
        if (existingBug == null) return;
        dbContext.Bugs.Remove(existingBug);
        dbContext.SaveChanges();
        NotifyClients(existingBug, "removeBug");
    }
}