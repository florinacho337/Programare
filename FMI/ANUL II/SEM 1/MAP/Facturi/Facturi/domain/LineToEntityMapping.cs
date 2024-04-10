using System;

namespace Facturi.domain
{
    public class LineToEntityMapping
    {
        public static Document CreateDocument(string line)
        {
            string[] fields = line.Split(',');
            return new Document()
            {
                Id = fields[0],
                Nume = fields[1],
                DataEmitere = Convert.ToDateTime(fields[2])
            };
        }

        public static Achizitie CreateAchizitie(string line)
        {
            string[] fields = line.Split(',');
            return new Achizitie()
            {
                Id = fields[0],
                Produs = fields[1],
                Cantitate = Convert.ToInt32(fields[2]),
                PretProdus = Convert.ToDouble(fields[3]),
                Factura = new Factura()
                {
                    Id = fields[4]
                }
            };
        }

        public static Factura CreateFactura(string line)
        {
            string[] fields = line.Split(',');
            return new Factura()
            {
                Id = fields[0],
                DataScadenta = Convert.ToDateTime(fields[1]),
                Categorie = (Categorie)Enum.Parse(typeof(Categorie), fields[2])
            };
        }
    }
}