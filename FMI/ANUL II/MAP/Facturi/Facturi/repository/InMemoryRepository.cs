using System.Collections.Generic;
using Facturi.domain;

namespace Facturi.repository
{
    public class InMemoryRepository<ID, E>: IRepository<ID, E> where E: Entity<ID>
    {
            protected IDictionary<ID, E> _dictionary = new Dictionary<ID, E>();

            public IEnumerable<E> FindAll()
            {
                return _dictionary.Values;
            }
            
    }
}