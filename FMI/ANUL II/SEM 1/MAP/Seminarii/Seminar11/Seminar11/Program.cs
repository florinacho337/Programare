using System;

namespace Seminar11
{
    internal class Program
    {
        public static void Main(string[] args)
        {
            Base b = new Derived();
            Derived d = new Derived();
            Console.WriteLine(b.m());
            Console.WriteLine(d.m());
        }
    }
}