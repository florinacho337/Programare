using Facturi.domain;
using Facturi.Repository;

namespace Facturi.repository.InFileRepositories
{
    public class DocumentInFileRepository: InFileRepository<string, Document>
    {
        public DocumentInFileRepository(string fileName) : base(fileName, LineToEntityMapping.CreateDocument)
        {
            
        }
    }
}