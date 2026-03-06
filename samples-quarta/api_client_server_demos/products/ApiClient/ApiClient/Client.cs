using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Net;
using System.Text.Json;
using ApiClient.Models;

namespace ApiClient;

public sealed class Client : IDisposable
{
    private readonly HttpClient _httpClient;

    public string ApiBaseUrl { get; }

    public Client(string apiBaseUrl)
    {
        ApiBaseUrl = apiBaseUrl;

        var handler = new HttpClientHandler
        {
            // Keep default certificate validation behavior.
            // Uncomment ONLY for local development with self-signed certs.
            // ServerCertificateCustomValidationCallback = HttpClientHandler.DangerousAcceptAnyServerCertificateValidator
        };

        _httpClient = new HttpClient(handler)
        {
            BaseAddress = new Uri(ApiBaseUrl)
        };

        _httpClient.DefaultRequestHeaders.Accept.Clear();
        _httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
    }

    public async Task<List<Product>> GetAllProductsAsync(bool includeRelated)
    {
        string endpoint = includeRelated ? "/products?includeRelated=true" : "/products";

        var products = await _httpClient.GetFromJsonAsync<List<Product>>(endpoint);
        return products ?? [];
    }

    public async Task<Product?> GetProductByIdAsync(int id)
    {
        string endpoint = $"/products/{id}";

        using HttpResponseMessage response = await _httpClient.GetAsync(endpoint);
        if (response.StatusCode == HttpStatusCode.NotFound)
        {
            return null;
        }

        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<Product>();
    }

    public async Task<Product?> CreateProductAsync(CreateProduct request)
    {
        using HttpResponseMessage response = await _httpClient.PostAsJsonAsync("/products", request);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<Product>();
    }

    public async Task<Product?> UpdateProductAsync(int id, UpdateProduct request)
    {
        string endpoint = $"/products/{id}";

        using HttpResponseMessage response = await _httpClient.PutAsJsonAsync(endpoint, request);
        response.EnsureSuccessStatusCode();

        if (response.Content.Headers.ContentLength is null or 0)
        {
            return null;
        }

        return await response.Content.ReadFromJsonAsync<Product>();
    }

    public async Task DeleteProductAsync(int id)
    {
        string endpoint = $"/products/{id}";

        using HttpResponseMessage response = await _httpClient.DeleteAsync(endpoint);
        response.EnsureSuccessStatusCode();
    }

    public async Task<string?> DownloadProductMediaByIdAsync(int productId)
    {
        Product? product = await GetProductByIdAsync(productId);
        if (product == null)
        {
            return null;
        }

        return await DownloadProductMediaAsync(product);
    }

    public async Task<string> DownloadProductMediaAsync(Product product)
    {
        string projectRoot = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", ".."));
        string baseFolder = Path.Combine(projectRoot, "DownloadedMedia", $"Product_{product.Id}");
        Directory.CreateDirectory(baseFolder);

        if (!string.IsNullOrWhiteSpace(product.Thumbnail))
        {
            await DownloadFileAsync(product.Thumbnail, Path.Combine(baseFolder, "thumbnail" + GetFileExtensionFromUrl(product.Thumbnail)));
        }

        if (product.Meta != null && !string.IsNullOrWhiteSpace(product.Meta.QrCode))
        {
            await DownloadFileAsync(product.Meta.QrCode, Path.Combine(baseFolder, "qrcode" + GetFileExtensionFromUrl(product.Meta.QrCode)));
        }

        if (product.Images != null && product.Images.Count > 0)
        {
            int imgIndex = 1;
            foreach (var img in product.Images)
            {
                if (!string.IsNullOrWhiteSpace(img.Url))
                {
                    string fileName = $"image_{imgIndex}" + GetFileExtensionFromUrl(img.Url);
                    await DownloadFileAsync(img.Url, Path.Combine(baseFolder, fileName));
                    imgIndex++;
                }
            }
        }

        return baseFolder;
    }

    public void Dispose()
    {
        _httpClient.Dispose();
    }

    private async Task DownloadFileAsync(string url, string localPath)
    {
        using var response = await _httpClient.GetAsync(url);
        response.EnsureSuccessStatusCode();
        await using var fs = new FileStream(localPath, FileMode.Create, FileAccess.Write, FileShare.None);
        await response.Content.CopyToAsync(fs);
    }

    private static string GetFileExtensionFromUrl(string urlOrPath)
    {
        if (string.IsNullOrWhiteSpace(urlOrPath))
        {
            return ".dat";
        }

        string pathPart = urlOrPath;
        int queryIndex = pathPart.IndexOf('?');
        if (queryIndex >= 0)
        {
            pathPart = pathPart[..queryIndex];
        }

        try
        {
            string ext = Path.GetExtension(pathPart);
            if (!string.IsNullOrWhiteSpace(ext) && ext != ".")
            {
                return ext;
            }
        }
        catch (ArgumentException)
        {
            // Fallback below.
        }
        catch (Exception)
        {
            // Fallback below.
        }

        if (Uri.IsWellFormedUriString(urlOrPath, UriKind.Absolute))
        {
            try
            {
                if (Uri.TryCreate(urlOrPath, UriKind.Absolute, out Uri? uri))
                {
                    string? fileName = uri.Segments.LastOrDefault();
                    if (!string.IsNullOrEmpty(fileName))
                    {
                        string extFromUri = Path.GetExtension(fileName);
                        if (!string.IsNullOrWhiteSpace(extFromUri) && extFromUri != ".")
                        {
                            return extFromUri;
                        }
                    }
                }
            }
            catch (Exception)
            {
                // Fallback below.
            }
        }

        return ".dat";
    }

}
