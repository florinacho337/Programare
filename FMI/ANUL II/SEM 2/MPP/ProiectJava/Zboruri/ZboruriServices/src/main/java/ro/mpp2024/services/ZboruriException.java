package ro.mpp2024.services;

public class ZboruriException extends Exception{
    public ZboruriException(){}
    public ZboruriException(String message) {
        super(message);
    }
    public ZboruriException(String message, Throwable cause) {
        super(message, cause);
    }
}
