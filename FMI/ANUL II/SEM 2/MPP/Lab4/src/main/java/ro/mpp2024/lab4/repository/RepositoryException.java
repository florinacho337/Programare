package ro.mpp2024.lab4.repository;

public class RepositoryException extends RuntimeException {
    public RepositoryException(){}

    public RepositoryException(String message){
        super(message);
    }
    public RepositoryException(Exception ex){
        super(ex);
    }
}