using Model;
using Services;
using Utils;

namespace Client;

public class ClientCtrl(IBmsServices server) : IBmsObserver
{
    public event EventHandler<BmsEventArgs> UpdateEvent;
    private Employee _currentEmployee;

    public List<Employee> GetAllEmployees()
    {
        return server.GetAllEmployees().FindAll(employee => employee.Role != Role.Admin);
    }
    
    public void AddEmployee(string username, string name, string password, string role)
    {
        if (username == "" || name == "" || password == "" || role == "Role" )
        {
            MessageAlert.ShowErrorMessage("Invalid data!");
            return;
        }
        Employee employee = new Employee(username, PasswordEncoder.Encrypt(password), name, (Role)Enum.Parse(typeof(Role), role))
        {
            Id = username
        };
        server.AddEmployee(employee);
        BmsEventArgs bmsArgs = new BmsEventArgs(BmsEvent.EmployeeAdded, employee);
        OnUserEvent(bmsArgs);
    }
    
    public void RemoveEmployee(string username)
    {
        if (username is "" or null)
        {
            MessageAlert.ShowErrorMessage("Please select an employee from the table!");
            return;
        }
        server.RemoveEmployee(username);
        BmsEventArgs bmsArgs = new BmsEventArgs(BmsEvent.EmployeeRemoved, username);
        OnUserEvent(bmsArgs);
    }
    
    protected virtual void OnUserEvent(BmsEventArgs e)
    {
        if (UpdateEvent == null) return;
        UpdateEvent(this, e);
        Console.WriteLine("Update Event called");
    }
    
    // -------------------------------------------------- NEW METHODS --------------------------------------------------

    public List<Bug> GetAllBugs()
    {
        return server.GetAllBugs();
    }

    public Employee Login(string username, string password)
    {
        var employee = new Employee(username, password)
        {
            Id = username
        };
        var foundEmployee = server.LogIn(employee, this);
        Console.WriteLine("Login succeeded ....");
        _currentEmployee = foundEmployee;
        Console.WriteLine("Current employee {0}", foundEmployee);
        return foundEmployee;
    }

    public void Logout()
    {
        server.LogOut(_currentEmployee);
        _currentEmployee = null;
    }

    public void ReportBug(string name, string description, string severity)
    {
        if (name == "" || description == "" || severity == "Severity")
        {
            MessageAlert.ShowErrorMessage("Invalid data!");
            return;
        }
        
        var bug = new Bug(name, description, (Severity)Enum.Parse(typeof(Severity), severity), "Not fixed");
        server.AddBug(bug);
    }

    public void BugAdded(Bug bugREntity)
    {
        var bmsArgs = new BmsEventArgs(BmsEvent.BugReported, bugREntity);
        OnUserEvent(bmsArgs);
    }

    public void BugUpdated(Bug newBug)
    {
        var bmsArgs = new BmsEventArgs(BmsEvent.BugUpdated, newBug);
        OnUserEvent(bmsArgs);
    }

    public void BugRemoved(Bug newBug)
    {
        var bmsArgs = new BmsEventArgs(BmsEvent.BugFixed, newBug);
        OnUserEvent(bmsArgs);
    }

    public void ModifyBug(int id, string? name, string? description, string? severity, string? status)
    {
        if (name == "" || description == "" || severity == "Severity")
        {
            MessageAlert.ShowErrorMessage("Invalid data!");
            return;
        }
        
        var bug = new Bug(name, description, (Severity)Enum.Parse(typeof(Severity), severity), status)
        {
            Id = id
        };
        server.UpdateBug(bug);
        MessageAlert.ShowMessage("Bug modified successfully!");
    }

    public void FixBug(int id)
    {
        var bug = new Bug()
        {
            Id = id
        };
        server.RemoveBug(bug);
        MessageAlert.ShowMessage("Bug fixed!");
    }
}