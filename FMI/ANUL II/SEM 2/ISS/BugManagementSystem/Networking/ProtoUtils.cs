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
        return response.Employees.Select(employee => new Model.Employee(employee.Username, employee.Password, employee.Name, (Role)Enum.Parse(typeof(Role), employee.Role.ToString()))).ToList();
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

    // -----------------------New methods-----------------------
    public static Request CreateGetBugsRequest()
    {
        return new Request {Type = Request.Types.Type.GetBugs};
    }

    public static List<Model.Bug> GetBugs(Response response)
    {
        return response.Bugs.Select(bug => new Model.Bug(bug.Name, bug.Description, (Severity)Enum.Parse(typeof(Severity), bug.Severity.ToString()), bug.Status) { Id = bug.Id }).ToList();
    }

    public static Response CreateGetBugsResponse(List<Model.Bug> bugs)
    {
        return new Response
        {
            Type = Response.Types.Type.GetBugs,
            Bugs = {bugs.Select(b => new Bug
            {
                Id = b.Id,
                Name = b.Name,
                Description = b.Description,
                Status = b.Status,
                Severity = (Bug.Types.Severity) Enum.Parse(typeof(Severity), b.Severity.ToString())
            })}
        };
    }

    public static Model.Employee GetEmployee(Response response)
    {
        return new Model.Employee(response.Employee.Username, response.Employee.Password, response.Employee.Name, (Role)Enum.Parse(typeof(Role), response.Employee.Role.ToString())) { Id = response.Employee.Username };
    }

    public static Request CreateLoginRequest(Model.Employee employee)
    {
        return new Request
        {
            Type = Request.Types.Type.Login,
            Employee = new Employee
            {
                Username = employee.Username,
                Password = employee.Password
            }
        };
    }

    public static Response CreateSuccessfulLoginResponse(Model.Employee foundEmployee)
    {
        return new Response
        {
            Type = Response.Types.Type.SuccessfulLogin,
            Employee = new Employee
            {
                Username = foundEmployee.Username,
                Password = foundEmployee.Password,
                Name = foundEmployee.Name,
                Role = (Employee.Types.Role) Enum.Parse(typeof(Role), foundEmployee.Role.ToString())
            }
        };
    }

    public static Request CreateLogoutRequest(Model.Employee employee)
    {
        return new Request {Type = Request.Types.Type.Logout, Employee = new Employee {Username = employee.Username}};
    }

    public static Request CreateAddBugRequest(Model.Bug bug)
    {
        return new Request
        {
            Type = Request.Types.Type.AddBug,
            Bug = new Bug
            {
                Name = bug.Name,
                Description = bug.Description,
                Severity = (Bug.Types.Severity) Enum.Parse(typeof(Severity), bug.Severity.ToString()),
                Status = bug.Status
            }
        };
    }

    public static Model.Bug GetBug(Request request)
    {
        return new Model.Bug(request.Bug.Name, request.Bug.Description, (Severity)Enum.Parse(typeof(Severity), request.Bug.Severity.ToString()), request.Bug.Status) {Id = request.Bug.Id};
    }

    public static Response CreateBugAddedResponse(Model.Bug bugREntity)
    {
        return new Response
        {
            Type = Response.Types.Type.AddBug,
            Bug = new Bug
            {
                Id = bugREntity.Id,
                Name = bugREntity.Name,
                Description = bugREntity.Description,
                Status = bugREntity.Status,
                Severity = (Bug.Types.Severity) Enum.Parse(typeof(Severity), bugREntity.Severity.ToString())
            }
        };
    }
    
    public static Model.Bug GetBug(Response response)
    {
        return new Model.Bug(response.Bug.Name, response.Bug.Description, (Severity)Enum.Parse(typeof(Severity), response.Bug.Severity.ToString()), response.Bug.Status) { Id = response.Bug.Id };
    }

    public static Request CreateUpdateBugRequest(Model.Bug bug)
    {
        return new Request
        {
            Type = Request.Types.Type.UpdateBug,
            Bug = new Bug
            {
                Id = bug.Id,
                Name = bug.Name,
                Description = bug.Description,
                Severity = (Bug.Types.Severity) Enum.Parse(typeof(Severity), bug.Severity.ToString()),
                Status = bug.Status
            }
        };
    }

    public static Response CreateBugUpdatedResponse(Model.Bug newBug)
    {
        return new Response
        {
            Type = Response.Types.Type.UpdateBug,
            Bug = new Bug
            {
                Id = newBug.Id,
                Name = newBug.Name,
                Description = newBug.Description,
                Status = newBug.Status,
                Severity = (Bug.Types.Severity) Enum.Parse(typeof(Severity), newBug.Severity.ToString())
            }
        };
    }

    public static Request CreateRemoveBugRequest(Model.Bug bug)
    {
        return new Request
        {
            Type = Request.Types.Type.RemoveBug,
            Bug = new Bug
            {
                Id = bug.Id,
            }
        };
    }

    public static Response CreateBugRemovedResponse(Model.Bug bug)
    {
        return new Response
        {
            Type = Response.Types.Type.RemoveBug,
            Bug = new Bug
            {
                Id = bug.Id
            }
        };
    }
}