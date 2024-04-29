namespace Model
{
    [Serializable]
    public class Zbor: Entity<int>
    {
        public string Destinatie { get; set; }
        public DateTime Plecare { get; set; }
        public string Aeroport { get; set; }
        public int NrLocuri { get; set; }

        public Zbor(string destinatie, DateTime plecare, string aeroport, int nrLocuri)
        {
            Destinatie = destinatie;
            Plecare = plecare;
            Aeroport = aeroport;
            NrLocuri = nrLocuri;
        }

        public override string ToString()
        {
            return $"{nameof(Destinatie)}: {Destinatie}, {nameof(Plecare)}: {Plecare}, {nameof(Aeroport)}: {Aeroport}, {nameof(NrLocuri)}: {NrLocuri}";
        }
    }
}