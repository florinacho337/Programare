namespace Utils;

using System.Security.Cryptography;
using System.Text;

public class PasswordEncoder
{
    private static byte[] GetSha(string input)
    {
        using SHA256 sha256Hash = SHA256.Create();
        // ComputeHash - returns byte array  
        byte[] bytes = sha256Hash.ComputeHash(Encoding.UTF8.GetBytes(input));
        return bytes;
    }

    private static string ToHexString(byte[] hash)
    {
        // Convert byte array to a string   
        StringBuilder builder = new StringBuilder();
        foreach (var t in hash)
        {
            builder.Append(t.ToString("x2"));
        }
        return builder.ToString();
    }

    public static string Encrypt(string input)
    {
        return ToHexString(GetSha(input));
    }
}