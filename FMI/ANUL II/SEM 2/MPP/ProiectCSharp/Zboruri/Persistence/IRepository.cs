using Model;

namespace Persistence
{
    public class RepositoryException:ApplicationException{
        public RepositoryException() { }
        public RepositoryException(String mess) : base(mess){}
        public RepositoryException(String mess, Exception e) : base(mess, e) { }
    }
    public interface IRepository<TId, TE> where TE:Entity<TId>
    {
        void Save(TE entity);
        void Update(TId id, TE update);
        TE FindOne(TId id);
        IEnumerable<TE> FindAll();
        void Delete(TId id);
    }
}