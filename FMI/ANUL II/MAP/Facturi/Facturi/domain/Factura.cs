using System;
using System.Collections.Generic;

namespace Facturi.domain
{
    public class Factura: Document
    {
        public DateTime DataScadenta { get; set; }

        public Categorie Categorie { get; set; }

        public List<Achizitie> Achzitii { get; set; }
        
        public override string ToString()
        {
            return this.Id + "," + this.DataScadenta + "," + this.Categorie;
        }
    }
}