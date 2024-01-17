using System.Collections.Generic;
using Facturi.domain;

namespace Facturi.repository
{
    public interface IRepository<ID, E> where E: Entity<ID>
    {
        IEnumerable<E> FindAll();
    }
}