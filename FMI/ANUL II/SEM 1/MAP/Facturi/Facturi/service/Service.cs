using System;
using System.Collections.Generic;
using System.Linq;
using Facturi.domain;
using Facturi.repository;

namespace Facturi.service
{
    public class Service
    {
        private IRepository<string, Achizitie> _repoAchizitii;
        private IRepository<string, Factura> _repoFacturi;
        private IRepository<string, Document> _repoDocument;

        public Service(IRepository<string, Achizitie> repoAchizitii, IRepository<string, Factura> repoFacturi, IRepository<string, Document> repoDocument)
        {
            _repoAchizitii = repoAchizitii;
            _repoFacturi = repoFacturi;
            _repoDocument = repoDocument;
        }
        
        public IEnumerable<(string, DateTime)> getDocumente2023()
        {
            return from document in _repoDocument.FindAll()
                where document.DataEmitere.Year == 2023
                select (document.Nume, document.DataEmitere);
        }
        
        public IEnumerable<(string, DateTime)> getFacturiScadente() => from factura in _repoFacturi.FindAll() 
            where factura.DataScadenta.Year == DateTime.Now.Year & factura.DataScadenta.Month == DateTime.Now.Month 
            select (factura.Nume, factura.DataScadenta);

        public IEnumerable<(string, int)> getFacturi3Produse()
        {
            return from factura in _repoFacturi.FindAll()
                where factura.Achzitii.Sum(a => a.Cantitate) > 3
                select (factura.Nume, factura.Achzitii.Sum(a => a.Cantitate));
        }
        public IEnumerable<(string, string)> getAchizitiiUtilities()
        {
            return from achizitie in _repoAchizitii.FindAll()
                where achizitie.Factura.Categorie == Categorie.Utilities
                select (achizitie.Produs, achizitie.Factura.Nume);
        }
        public Categorie getCategorieMaxima()
        {
            return (from factura in _repoFacturi.FindAll()
                group factura.Achzitii.Sum(a => a.Cantitate * a.PretProdus) by factura.Categorie
                into g
                select (g.Key, g.Sum())).OrderByDescending(a => a.Item2).First().Key;
        }
    }
}