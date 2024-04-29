namespace Services;

public class BmsException: Exception
{
    public BmsException()
    {
    }

    public BmsException(String message) : base(message)
    {
    }

    public BmsException(String message, Exception cause) : base(message, cause)
    {
    }
}