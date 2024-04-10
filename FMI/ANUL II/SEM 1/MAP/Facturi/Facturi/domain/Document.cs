using System;

namespace Facturi.domain
{
    public class Document: Entity<string>
    {

        public string Nume { get; set; }

        public DateTime DataEmitere { get; set; }

        public override string ToString()
        {
            return Id + "," + Nume + "," + DataEmitere;
        }

        public string Id { get; set; }
    }
}