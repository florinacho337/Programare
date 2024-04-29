package ro.mpp2024.repository;

import ro.mpp2024.domain.Entity;

/**
 * CRUD operations repository interface
 *
 * @param <ID> - type E must have an attribute of type ID
 * @param <E>  -  type of entities saved in repository
 */
public interface Repository<ID, E extends Entity<ID>> {
    /**
     * @return the number of entities
     */
    int size();

    /**
     * @param id -the id of the entity to be returned
     *           id must not be null
     * @return the entity with the given id
     * @throws IllegalArgumentException if id is null.
     */
    E findOne(ID id);

    /**
     * @return all entities
     */
    Iterable<E> findAll();

    /**
     * @param entity entity must be not null
     * @throws IllegalArgumentException if the given entity is null.     *
     */
    void save(E entity);


    /**
     * removes the entity with the specified id
     *
     * @param id id must be not null
     * @throws IllegalArgumentException if the given id is null.
     */
    void delete(ID id);

    /**
     * @param entity entity must not be null
     * @throws IllegalArgumentException if the given entity is null.
     */
    void update(ID id, E entity);
}
