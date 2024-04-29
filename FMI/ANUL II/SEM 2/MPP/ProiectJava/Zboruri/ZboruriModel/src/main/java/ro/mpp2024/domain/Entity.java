package ro.mpp2024.domain;

import java.io.Serializable;
import java.util.Objects;

public class Entity<ID> implements Serializable {
    private ID Id;

    public ID getId() {
        return Id;
    }

    public void setId(ID id) {
        this.Id = id;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Entity<?> entity)) return false;
        return getId().equals(entity.getId());
    }

    @Override
    public int hashCode() {
        return Objects.hash(getId());
    }

    @Override
    public String toString() {
        return "Entity{" +
                "id=" + Id +
                '}';
    }
}
