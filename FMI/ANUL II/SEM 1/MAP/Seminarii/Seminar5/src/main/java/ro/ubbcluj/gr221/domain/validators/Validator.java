package ro.ubbcluj.gr221.domain.validators;

public interface Validator<T> {
    void validate(T entity) throws ValidationException;
}