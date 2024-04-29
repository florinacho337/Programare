namespace Model
{
    [Serializable]
    public class Bilet:Entity<int>
    {
        public string Client { get; set; }
        public string Oras { get; set; }
        public string Tara { get; set; }
        public List<TuristBilet> Turisti { get; set; }
        public int NrLocuri { get; set; }
        public Zbor Zbor { get; set; }
        
        public Bilet()
        {
        }

        public Bilet(string client, string oras, string tara, List<TuristBilet> turisti, int nrLocuri, Zbor zbor)
        {
            Client = client;
            Oras = oras;
            Tara = tara;
            Turisti = turisti;
            NrLocuri = nrLocuri;
            Zbor = zbor;
        }

        public override string ToString()
        {
            return $"{nameof(Client)}: {Client}, {nameof(Oras)}: {Oras}, {nameof(Tara)}: {Tara}, {nameof(Turisti)}: {Turisti}, {nameof(NrLocuri)}: {NrLocuri}, {nameof(Zbor)}: {Zbor}";
        }
    }
}