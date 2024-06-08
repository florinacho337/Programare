namespace Client;

public enum ZboruriAngajatEvent
{
    TicketBought
};

public class ZboruriAngajatEventArgs(ZboruriAngajatEvent angajatEvent, object data) : EventArgs
{
    public ZboruriAngajatEvent AngajatEventType => angajatEvent;

    public object Data => data;
}