namespace Model;

public class Bug(string name, string description, Severity severity, string status)
    : Entity<int>
{
    public string Name { get; set; } = name;
    public string Description { get; set; } = description;
    public Severity Severity { get; set; } = severity;
    public string Status { get; set; } = status;

    public override string ToString()
    {
        return
            $"{nameof(Name)}: {Name}, {nameof(Description)}: {Description}, {nameof(Severity)}: {Severity}, {nameof(Status)}: {Status}";
    }
}