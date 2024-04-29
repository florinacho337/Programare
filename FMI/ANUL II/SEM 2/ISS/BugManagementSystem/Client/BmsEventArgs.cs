namespace Client;

public enum BmsEvent
{
    EmployeeAdded, EmployeeRemoved
};

public class BmsEventArgs(BmsEvent angajatEvent, object data) : EventArgs
{
    public BmsEvent AngajatEventType => angajatEvent;

    public object Data => data;
}