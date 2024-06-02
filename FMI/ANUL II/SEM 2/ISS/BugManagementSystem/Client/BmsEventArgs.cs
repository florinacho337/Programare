namespace Client;

public enum BmsEvent
{
    EmployeeAdded, EmployeeRemoved,
    BugReported, BugUpdated, BugFixed
};

public class BmsEventArgs(BmsEvent angajatEvent, object data) : EventArgs
{
    public BmsEvent AngajatEventType => angajatEvent;

    public object Data => data;
}