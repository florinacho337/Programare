using System;
using Facturi.domain;
using Facturi.repository;
using Facturi.repository.InFileRepositories;
using Facturi.service;

namespace Facturi.presentation
{
    public class UserInterface
    {
        private Service _service;

        public UserInterface()
        {
            IRepository<string, Document> dRepository = new DocumentInFileRepository("/home/florin/FMI/MAP/Facturi/Facturi/documente.txt");
            IRepository<string, Factura> fRepository = new FacturaInFileRepository("/home/florin/FMI/MAP/Facturi/Facturi/facturi.txt", "/home/florin/FMI/MAP/Facturi/Facturi/achizitii.txt", "/home/florin/FMI/MAP/Facturi/Facturi/documente.txt");
            IRepository<string, Achizitie> aRepository = new AchizitieInFileRepository("/home/florin/FMI/MAP/Facturi/Facturi/achizitii.txt", "/home/florin/FMI/MAP/Facturi/Facturi/facturi.txt","/home/florin/FMI/MAP/Facturi/Facturi/documente.txt");
            this._service = new Service(aRepository, fRepository, dRepository);
        }
        
        public void run()
        {
            meniu();
            while (true)
            {
                Console.Write(">>");
                var comanda = Console.ReadLine();
                comanda = comanda.Replace(" ", "");
                if (comanda == "") continue;

                switch (comanda)
                {
                    case "documente_din_2023":
                        documenteDin2023();
                        break;
                    case "facturi_scadente_luna_curenta":
                        facturiScadenteLunaCurenta();
                        break;
                    case "facturi_3_produse":
                        facturi3Produse();
                        break;
                    case "achizitii_utilities":
                        achizitiiUtilities();
                        break;
                    case "categorie_maxima":
                        categorieMaxima();
                        break;
                    case "meniu":
                        meniu();
                        break;
                    case "exit":
                        return;
                    default:
                        Console.WriteLine("Comanda invalida!");
                        break;
                }

                Console.WriteLine("Pentru a afisa meniul tastati \"meniu\"!");
            }
        }

        private void categorieMaxima()
        {
            Console.WriteLine(_service.getCategorieMaxima());
        }

        private void achizitiiUtilities()
        {
            foreach (var achizitie in _service.getAchizitiiUtilities())
            {
                Console.WriteLine(achizitie);
            }
        }

        private void facturi3Produse()
        {
            foreach (var factura in _service.getFacturi3Produse())
            {
                Console.WriteLine(factura);
            }
        }

        private void facturiScadenteLunaCurenta()
        {
            foreach (var factura in _service.getFacturiScadente())
            {
                Console.WriteLine(factura);
            }
        }

        private void documenteDin2023()
        {
            foreach (var document in _service.getDocumente2023())
            {
                Console.WriteLine(document);
            }
        }

        private void meniu()
        {
            Console.WriteLine("-----------------------------------------------------------------------------------------------");
            Console.WriteLine("|                                        FACTURI                                              |");
            Console.WriteLine("|                                                                                             |");
            Console.WriteLine("|Afiseaza toate documentele emise in anul 2023 (documente_din_2023)                           |");
            Console.WriteLine("|Afiseaza facturile scadente in luna curenta (facturi_scadente_luna_curenta)                  |");
            Console.WriteLine("|Afiseaza facturile cu cel putin 3 produse achizitionate (facturi_3_produse)                  |");
            Console.WriteLine("|Afiseaza toate achizitiile din categoria Utilities (achizitii_utilities)                     |");
            Console.WriteLine("|Afiseaza categoria de facturi care a inregistrat cele mai multe cheltuieli (categorie_maxima)|");
            Console.WriteLine("|Iesi din program (exit)                                                                      |");
            Console.WriteLine("-----------------------------------------------------------------------------------------------");
        }
    }
}