using System;
using System.Collections.Generic;
using System.IO;
using Facturi.domain;
using Facturi.Repository;
using Facturi.Repository.utils;

namespace Facturi.repository.InFileRepositories
{
    public class AchizitieInFileRepository: InFileRepository<string, Achizitie>
    {
        private string facturaFileName;
        private string documentFileName;
        public AchizitieInFileRepository(string fileName, string facturaFileName, string documentFileName) : base(fileName, null)
        {
            this.facturaFileName = facturaFileName;
            this.documentFileName = documentFileName;
            loadFromFile();
        }

        private new void loadFromFile()
        {
            using (StreamReader sr = new StreamReader(fileName))
            {
                string line;
                List<Factura> facturi = DataReader.ReadData(facturaFileName, LineToEntityMapping.CreateFactura);
                List<Document> documente = DataReader.ReadData(documentFileName, LineToEntityMapping.CreateDocument);
                while ((line = sr.ReadLine()) != null)
                {
                    string[] fields = line.Split(',');
                    Factura factura = facturi.Find(x => x.Id.Equals(fields[4]));
                    Document document = documente.Find(x => x.Id.Equals(factura.Id));
                    
                    Achizitie achizitie = new Achizitie()
                    {
                        Id = fields[0],
                        Produs = fields[1],
                        Cantitate = Convert.ToInt32(fields[2]),
                        PretProdus = Convert.ToDouble(fields[3]),
                        Factura = factura
                    };
                    
                    factura.Nume = document.Nume;
                    factura.DataEmitere = document.DataEmitere;
                    if (factura.Achzitii == null)
                        factura.Achzitii = new List<Achizitie>();
                    factura.Achzitii.Add(achizitie);

                    base._dictionary[achizitie.Id] = achizitie;
                }
            }
        }
    }
}