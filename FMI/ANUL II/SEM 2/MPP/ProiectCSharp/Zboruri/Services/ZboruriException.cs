namespace Services;

public class ZboruriException : Exception
{
    public ZboruriException()
    {
    }

    public ZboruriException(String message) : base(message)
    {
    }

    public ZboruriException(String message, Exception cause) : base(message, cause)
    {
    }
}