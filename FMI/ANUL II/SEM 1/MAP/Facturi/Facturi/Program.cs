using System;
using Facturi.domain;
using Facturi.presentation;
using Facturi.repository;
using Facturi.repository.InFileRepositories;

namespace Facturi
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            UserInterface ui = new UserInterface();
            ui.run();
        }
    }
}