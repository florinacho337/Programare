using System.ComponentModel.DataAnnotations;
using Newtonsoft.Json;

namespace Model
{
    [Serializable]
    public class Angajat: Entity<string>
    {
        public Angajat(string username, string nume, string parola)
        {
            Username = username;
            Nume = nume;
            Parola = parola;
        }
        
        [JsonConstructor]
        public Angajat(string username, string parola) : this(username, "", parola) {}
        
        [Key]
        public string Username { get; set; }
        public string Nume { get; set; }
        public string Parola { get; set; }

        public override string ToString()
        {
            return $"{nameof(Username)}: {Username}, {nameof(Nume)}: {Nume}";
        }
    }
}