using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using Model;

namespace RESTClient;

class RESTClient
{
    private static readonly HttpClient Client = new HttpClient(new LoggingHandler(new HttpClientHandler()));
    private const string UrlBase = "http://localhost:5198/api/zboruri";

    public static void Main(string[] args)
    {
        RunAsync().Wait();
    }

    static async Task RunAsync()
    {
        Client.BaseAddress = new Uri(UrlBase);
        Client.DefaultRequestHeaders.Accept.Clear();
        Client.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
        
        Console.WriteLine("Get all Zbor objects");
        Zbor[] zboruri = await GetZboruriAsync(UrlBase);
        foreach (var zbor in zboruri)
        {
            Console.WriteLine(zbor);
        }
        
        Console.WriteLine("Get filtered Zbor objects");
        Zbor[] filteredZboruri = await GetZboruriFilteredAsync(UrlBase, "Amsterdam", DateTime.Parse("2024-09-13T00:00"), 2);
        foreach (var zbor in filteredZboruri)
        {
            Console.WriteLine(zbor);
        }
        
        Console.WriteLine("Create Zbor object");
        Zbor newZbor = new Zbor("destination", DateTime.Now, "airport", 5);
        Zbor createdZbor = await CreateZborAsync(UrlBase, newZbor);
        Console.WriteLine(createdZbor);

        Console.WriteLine("Update Zbor object");
        createdZbor.Destinatie = "new destination";
        await UpdateZborAsync(UrlBase + "/" + createdZbor.Id, createdZbor);

        Console.WriteLine("Delete Zbor object");
        await DeleteZborAsync(UrlBase + "/" + createdZbor.Id);
    }

    static async Task<Zbor[]> GetZboruriAsync(string path)
    {
        Zbor[] zboruri = null;
        HttpResponseMessage response = await Client.GetAsync(path);
        if (response.IsSuccessStatusCode)
        {
            zboruri = await response.Content.ReadFromJsonAsync<Zbor[]>();
        }
        return zboruri;
    }
    
    static async Task<Zbor[]> GetZboruriFilteredAsync(string path, string dest, DateTime date, int min)
    {
        Zbor[] zboruri = null;
        HttpResponseMessage response = await Client.GetAsync(path + $"/filter?dest={dest}&date={date}&min={min}");
        if (response.IsSuccessStatusCode)
        {
            zboruri = await response.Content.ReadFromJsonAsync<Zbor[]>();
        }
        return zboruri;
    }

    static async Task<Zbor> CreateZborAsync(string path, Zbor zbor)
    {
        Zbor createdZbor = null;
        HttpResponseMessage response = await Client.PostAsJsonAsync(path, zbor);
        if (response.IsSuccessStatusCode)
        {
            createdZbor = await response.Content.ReadFromJsonAsync<Zbor>();
        }
        return createdZbor;
    }

    static async Task UpdateZborAsync(string path, Zbor zbor)
    {
        HttpResponseMessage response = await Client.PutAsJsonAsync(path, zbor);
        if (!response.IsSuccessStatusCode)
        {
            Console.WriteLine("Error updating Zbor object");
        }
        
        Console.WriteLine("Updated Zbor object");
    }

    static async Task DeleteZborAsync(string path)
    {
        HttpResponseMessage response = await Client.DeleteAsync(path);
        if (!response.IsSuccessStatusCode)
        {
            Console.WriteLine("Error deleting Zbor object");
        }
        Console.WriteLine("Deleted Zbor object");
    }
}

public class LoggingHandler(HttpMessageHandler innerHandler) : DelegatingHandler(innerHandler)
{
    protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
    {
        Console.WriteLine("Request:");
        Console.WriteLine(request.ToString());
        if (request.Content != null)
        {
            Console.WriteLine(await request.Content.ReadAsStringAsync(cancellationToken));
        }
        Console.WriteLine();

        HttpResponseMessage response = await base.SendAsync(request, cancellationToken);

        Console.WriteLine("Response:");
        Console.WriteLine(response.ToString());
        if (response.Content != null)
        {
            Console.WriteLine(await response.Content.ReadAsStringAsync(cancellationToken));
        }
        Console.WriteLine();

        return response;
    }
}