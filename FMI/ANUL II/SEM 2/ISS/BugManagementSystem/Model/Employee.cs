using System.ComponentModel.DataAnnotations;

namespace Model;

public class Employee(string username, string password, string name = "", Role role = Role.Validator)
    : Entity<string>
{
    [Key]
    public string Username { get; init; } = username;
    public string Password { get; init; } = password;
    public string Name { get; init; } = name;
    public Role Role { get; init; } = role;

    public override string ToString()
    {
        return
            $"{nameof(Username)}: {Username}, {nameof(Password)}: {Password}, {nameof(Name)}: {Name}, {nameof(Role)}: {Role}";
    }
}