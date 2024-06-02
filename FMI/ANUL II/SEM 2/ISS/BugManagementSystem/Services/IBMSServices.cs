using Model;

namespace Services;

public interface IBmsServices
{
    List<Employee> GetAllEmployees();
    void AddEmployee(Employee employee);
    void RemoveEmployee(string username);
    List<Bug> GetAllBugs();
    Employee LogIn(Employee employee, IBmsObserver client);
    void LogOut(Employee employee);
    void AddBug(Bug bug);
    void UpdateBug(Bug bug);
    void RemoveBug(Bug bug);
}