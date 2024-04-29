using Model;

namespace Networking;

public class ProtoUtils
{
    public static Model.Employee GetEmployee(Request request)
    {
        var employee = new Model.Employee(request.Employee.Username, request.Employee.Password, request.Employee.Name,
            (Role)Enum.Parse(typeof(Role), request.Employee.Role.ToString()));
        return employee;
    }

    public static Response CreateOkResponse()
    {
        return new Response {Type = Response.Types.Type.Ok};
    }

    public static Response CreateErrorResponse(string eMessage)
    {
        return new Response {Type = Response.Types.Type.Error, Message = eMessage};
    }
    
    public static Response CreateGetEmployeesResponse(List<Model.Employee> employees)
    {
        return new Response
        {
            Type = Response.Types.Type.GetEmployees,
            Employees = {employees.Select(e => new Employee
            {
                Username = e.Username,
                Name = e.Name,
                Password = e.Password,
                Role = (Employee.Types.Role) Enum.Parse(typeof(Role), e.Role.ToString())
            })}
        };
    }

    public static Request CreateGetEmployeesRequest()
    {
        return new Request {Type = Request.Types.Type.GetEmployees};
    }

    public static List<Model.Employee> GetEmployees(Response response)
    {
        List<Model.Employee> employees = new();
        foreach (var employee in response.Employees)
        {
            employees.Add(new Model.Employee(employee.Username, employee.Password, employee.Name,
                (Role)Enum.Parse(typeof(Role), employee.Role.ToString())));
        }
        return employees;
    }

    public static Request CreateAddEmployeeRequest(Model.Employee employee)
    {
        return new Request
        {
            Type = Request.Types.Type.AddEmployee,
            Employee = new Employee
            {
                Username = employee.Username,
                Password = employee.Password,
                Name = employee.Name,
                Role = (Employee.Types.Role) Enum.Parse(typeof(Role), employee.Role.ToString())
            }
        };
    }

    public static Request CreateRemoveEmployeeRequest(string username)
    {
        return new Request { Type = Request.Types.Type.RemoveEmployee, Username = username };
    }
}