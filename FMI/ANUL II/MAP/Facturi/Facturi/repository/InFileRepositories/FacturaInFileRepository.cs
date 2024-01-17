using System;
using System.Collections.Generic;
using System.IO;
using Facturi.domain;
using Facturi.Repository;
using Facturi.Repository.utils;

namespace Facturi.repository.InFileRepositories
{
    public class FacturaInFileRepository: InFileRepository<string, Factura>
    {
        private string achizitiiFileName;
        private string documenteFileName;
        
        public FacturaInFileRepository(string fileName, string achizitiiFileName, string documenteFileName) : base(fileName, null)
        {
            this.achizitiiFileName = achizitiiFileName;
            this.documenteFileName = documenteFileName;
            loadFromFile();
        }

        private new void loadFromFile()
        {
            List<Achizitie> achizitii = DataReader.ReadData(achizitiiFileName, LineToEntityMapping.CreateAchizitie);
            List<Document> documente = DataReader.ReadData(documenteFileName, LineToEntityMapping.CreateDocument);
            using (StreamReader sr = new StreamReader(fileName))
            {
                string line;
                while ((line = sr.ReadLine()) != null)
                {
                    string[] fields = line.Split(',');
                    List<Achizitie> achizitiiFactura = achizitii.FindAll(x => x.Factura.Id.Equals(fields[0]));
                    Document document = documente.Find(x => x.Id.Equals(fields[0]));
                    Factura factura = new Factura()
                    {
                        Id = fields[0],
                        Nume = document.Nume,
                        DataEmitere = document.DataEmitere,
                        Achzitii = achizitiiFactura,
                        Categorie = (Categorie)Enum.Parse(typeof(Categorie), fields[2]),
                        DataScadenta = DateTime.Parse(fields[1])
                    };
                    foreach (var achizitie in achizitiiFactura)
                    {
                        achizitie.Factura = factura;
                    }
                    base._dictionary[factura.Id] = factura;
                }
            }
        }
    }
}