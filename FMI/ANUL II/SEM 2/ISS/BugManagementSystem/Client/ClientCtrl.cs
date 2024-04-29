using System.Collections;
using Model;
using Services;
using Utils;

namespace Client;

public class ClientCtrl: IbmsObserver
{
    public event EventHandler<BmsEventArgs> UpdateEvent;
    private readonly IBmsServices _server;
    // private Employee _currentAngajat;

    public ClientCtrl(IBmsServices server)
    {
        this._server = server;
        // _currentAngajat = null;
    }

    public List<Employee> GetAllEmployees()
    {
        return _server.GetAllEmployees();
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
        _server.AddEmployee(employee);
        BmsEventArgs bmsArgs = new BmsEventArgs(BmsEvent.EmployeeAdded, employee);
        OnUserEvent(bmsArgs);
    }
    
    public void RemoveEmployee(string username)
    {
        if (username == "" || username == null)
        {
            MessageAlert.ShowErrorMessage("Please select an employee from the table!");
            return;
        }
        _server.RemoveEmployee(username);
        BmsEventArgs bmsArgs = new BmsEventArgs(BmsEvent.EmployeeRemoved, username);
        OnUserEvent(bmsArgs);
    }
    
    protected virtual void OnUserEvent(BmsEventArgs e)
    {
        if (UpdateEvent == null) return;
        UpdateEvent(this, e);
        Console.WriteLine("Update Event called");
    }

    public void Close()
    {
        _server.Close();
    }
}