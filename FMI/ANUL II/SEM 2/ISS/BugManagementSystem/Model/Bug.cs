namespace Model;

public class Bug : Entity<int>
{
    public Bug()
    {
    }
    public Bug(string name, string description, Severity severity, string status)
    {
        Name = name;
        Description = description;
        Severity = severity;
        Status = status;
    }

    public string Name { get; set; }
    public string Description { get; set; }
    public Severity Severity { get; set; }
    public string Status { get; set; }

    public override string ToString()
    {
        return
            $"{nameof(Name)}: {Name}, {nameof(Description)}: {Description}, {nameof(Severity)}: {Severity}, {nameof(Status)}: {Status}";
    }
}