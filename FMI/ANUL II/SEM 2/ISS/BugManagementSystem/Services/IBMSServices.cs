using Model;

namespace Services;

public interface IBmsServices
{
    void Close();
    List<Employee> GetAllEmployees();
    void AddEmployee(Employee employee);
    void RemoveEmployee(string username);
}