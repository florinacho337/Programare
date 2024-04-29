using System.ComponentModel.DataAnnotations;

namespace Model;

public class Employee(string username, string password, string name, Role role)
    : Entity<string>
{
    [Key]
    public string Username { get; set; } = username;
    public string Password { get; set; } = password;
    public string Name { get; set; } = name;
    public Role Role { get; set; } = role;

    public override string ToString()
    {
        return
            $"{nameof(Username)}: {Username}, {nameof(Password)}: {Password}, {nameof(Name)}: {Name}, {nameof(Role)}: {Role}";
    }
}