using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text.Json.Serialization;
using ApiClientAuth.Models;

namespace ApiClientAuth;

public class ImageDownloadResult
{
    public string FilePath { get; set; } = string.Empty;
    public int ByteCount { get; set; }
    public Uri ImageUri { get; set; } = new("http://localhost");
}

public class CategoryAverageResult
{
    public string Category { get; set; } = string.Empty;
    public decimal AveragePrice { get; set; }
    public int Count { get; set; }
}

public class CategoryTopProducts
{
    public string Category { get; set; } = string.Empty;
    public IReadOnlyList<Product> Products { get; set; } = [];
}

public class PagedProductsResult
{
    public IReadOnlyList<Product> Items { get; set; } = [];
    public int Page { get; set; }
    public int PageSize { get; set; }
    public int? TotalCount { get; set; }
}

public class ApiClient : IDisposable
{
    private readonly HttpClient _httpClient;

    public ApiClient(string apiBaseUrl)
    {
        _httpClient = new HttpClient
        {
            BaseAddress = new Uri(apiBaseUrl)
        };

        _httpClient.DefaultRequestHeaders.Accept.Clear();
        _httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
    }

    public async Task<bool> LoginAsync(string email, string password)
    {
        var loginRequest = new LoginRequest { Email = email, Password = password };
        using HttpResponseMessage response = await _httpClient.PostAsJsonAsync("/login", loginRequest);

        if (!response.IsSuccessStatusCode)
        {
            return false;
        }

        LoginResponse? loginResponse = await response.Content.ReadFromJsonAsync<LoginResponse>();
        if (string.IsNullOrWhiteSpace(loginResponse?.AccessToken))
        {
            return false;
        }

        _httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", loginResponse.AccessToken);
        return true;
    }

    public async Task<List<Product>> GetAllProductsAsync()
    {
        const string endpoint = "/products";
        using HttpResponseMessage response = await _httpClient.GetAsync(endpoint);
        await EnsureSuccessAsync(response, $"GET {endpoint}");

        return await response.Content.ReadFromJsonAsync<List<Product>>() ?? [];
    }

    public async Task<Product?> GetProductByIdAsync(int id)
    {
        string endpoint = $"/products/{id}";
        using HttpResponseMessage response = await _httpClient.GetAsync(endpoint);

        if (response.StatusCode == HttpStatusCode.NotFound)
        {
            return null;
        }

        await EnsureSuccessAsync(response, $"GET {endpoint}");
        return await response.Content.ReadFromJsonAsync<Product>();
    }

    public async Task<ImageDownloadResult?> DownloadProductImageAsync(int productId, string? downloadsFolder = null)
    {
        Product? product = await GetProductByIdAsync(productId);
        if (product == null)
        {
            return null;
        }

        string? imageUrl = !string.IsNullOrWhiteSpace(product.Thumbnail)
            ? product.Thumbnail
            : product.Images?.FirstOrDefault(i => !string.IsNullOrWhiteSpace(i.Url))?.Url;

        if (string.IsNullOrWhiteSpace(imageUrl))
        {
            return null;
        }

        Uri imageUri = Uri.TryCreate(imageUrl, UriKind.Absolute, out var absoluteUri)
            ? absoluteUri
            : new Uri(_httpClient.BaseAddress!, imageUrl);

        using HttpResponseMessage imageResponse = await _httpClient.GetAsync(imageUri);
        await EnsureSuccessAsync(imageResponse, $"GET image {imageUri}");

        byte[] imageBytes = await imageResponse.Content.ReadAsByteArrayAsync();
        if (imageBytes.Length == 0)
        {
            return null;
        }

        string extension = Path.GetExtension(imageUri.AbsolutePath);
        if (string.IsNullOrWhiteSpace(extension))
        {
            extension = ".img";
        }

        string targetFolder = downloadsFolder ?? Path.Combine(AppContext.BaseDirectory, "downloads");
        Directory.CreateDirectory(targetFolder);

        string safeCategory = string.IsNullOrWhiteSpace(product.Category) ? "unknown" : product.Category;
        string safeCategoryFilePart = string.Concat(safeCategory.Where(ch => !Path.GetInvalidFileNameChars().Contains(ch)));
        if (string.IsNullOrWhiteSpace(safeCategoryFilePart))
        {
            safeCategoryFilePart = "unknown";
        }

        string filePath = Path.Combine(targetFolder, $"product-{productId}-{safeCategoryFilePart}{extension}");
        await File.WriteAllBytesAsync(filePath, imageBytes);

        return new ImageDownloadResult
        {
            FilePath = filePath,
            ByteCount = imageBytes.Length,
            ImageUri = imageUri
        };
    }

    public async Task<ImageDownloadResult?> DownloadProductImageSimpleAsync(int productId, string? downloadsFolder = null)
    {
        Product? product = await GetProductByIdAsync(productId);
        string? imageUrl = product?.Thumbnail ?? product?.Images?.FirstOrDefault()?.Url;

        if (string.IsNullOrWhiteSpace(imageUrl))
        {
            return null;
        }

        Uri imageUri = Uri.TryCreate(imageUrl, UriKind.Absolute, out var absoluteUri)
            ? absoluteUri
            : new Uri(_httpClient.BaseAddress!, imageUrl);

        byte[] bytes = await _httpClient.GetByteArrayAsync(imageUri);
        if (bytes.Length == 0)
        {
            return null;
        }

        string extension = Path.GetExtension(imageUri.AbsolutePath);
        if (string.IsNullOrWhiteSpace(extension))
        {
            extension = ".img";
        }

        string targetFolder = downloadsFolder ?? Path.Combine(AppContext.BaseDirectory, "downloads");
        Directory.CreateDirectory(targetFolder);
        string filePath = Path.Combine(targetFolder, $"product-{productId}-simple{extension}");

        await File.WriteAllBytesAsync(filePath, bytes);
        return new ImageDownloadResult
        {
            FilePath = filePath,
            ByteCount = bytes.Length,
            ImageUri = imageUri
        };
    }

    public async Task<decimal?> GetAveragePriceAllProductsAsync()
    {
        List<Product> products = await GetAllProductsAsync();
        if (products.Count == 0)
        {
            return null;
        }

        return products.Average(p => p.Price);
    }

    public async Task<CategoryAverageResult?> GetAveragePriceByCategoryAsync(string category)
    {
        string endpoint = $"/products?category={Uri.EscapeDataString(category)}";
        using HttpResponseMessage response = await _httpClient.GetAsync(endpoint);
        await EnsureSuccessAsync(response, $"GET {endpoint}");

        List<Product> products = await response.Content.ReadFromJsonAsync<List<Product>>() ?? [];
        if (products.Count == 0)
        {
            return null;
        }

        decimal averagePrice = products.Average(p => p.Price);
        return new CategoryAverageResult
        {
            Category = category,
            AveragePrice = averagePrice,
            Count = products.Count
        };
    }

    public async Task<IReadOnlyList<CategoryTopProducts>> GetTopThreeProductsByRankingPerCategoryAsync()
    {
        const string endpoint = "/products?_sort=category,rating&_order=asc,desc";
        using HttpResponseMessage response = await _httpClient.GetAsync(endpoint);
        await EnsureSuccessAsync(response, $"GET {endpoint}");

        List<Product> products = await response.Content.ReadFromJsonAsync<List<Product>>() ?? [];
        var result = products
            .GroupBy(p => string.IsNullOrWhiteSpace(p.Category) ? "(senza categoria)" : p.Category!)
            .OrderBy(g => g.Key, StringComparer.OrdinalIgnoreCase)
            .Select(g => new CategoryTopProducts
            {
                Category = g.Key,
                Products = g.OrderByDescending(p => p.Rating).Take(3).ToList()
            })
            .ToList();

        return result;
    }

    public async Task<PagedProductsResult> ListProductsByCategoryPagedAndSortedAsync(string category, int page, int pageSize)
    {
        string endpoint = $"/products?category={Uri.EscapeDataString(category)}&_sort=price&_order=desc&_page={page}&_limit={pageSize}";
        using HttpResponseMessage response = await _httpClient.GetAsync(endpoint);
        await EnsureSuccessAsync(response, $"GET {endpoint}");

        List<Product> products = await response.Content.ReadFromJsonAsync<List<Product>>() ?? [];
        int? totalCount = null;

        if (response.Headers.TryGetValues("X-Total-Count", out IEnumerable<string>? totalCountValues) &&
            int.TryParse(totalCountValues.FirstOrDefault(), out int parsedCount))
        {
            totalCount = parsedCount;
        }

        return new PagedProductsResult
        {
            Items = products,
            Page = page,
            PageSize = pageSize,
            TotalCount = totalCount
        };
    }

    public async Task<Product?> CreateProductAsync(CreateProduct newProduct)
    {
        const string endpoint = "/products";
        using HttpResponseMessage response = await _httpClient.PostAsJsonAsync(endpoint, newProduct);

        await EnsureSuccessAsync(response, $"POST {endpoint}");
        return await response.Content.ReadFromJsonAsync<Product>();
    }

    public async Task<Product?> UpdateProductAsync(int id, UpdateProduct updateDto)
    {
        string endpoint = $"/products/{id}";
        using HttpResponseMessage response = await _httpClient.PutAsJsonAsync(endpoint, updateDto);

        await EnsureSuccessAsync(response, $"PUT {endpoint}");

        if (response.Content.Headers.ContentLength is 0)
        {
            return null;
        }

        return await response.Content.ReadFromJsonAsync<Product>();
    }

    public async Task<bool> DeleteProductAsync(int id)
    {
        string endpoint = $"/products/{id}";
        using HttpResponseMessage response = await _httpClient.DeleteAsync(endpoint);

        if (response.StatusCode == HttpStatusCode.NotFound)
        {
            return false;
        }

        await EnsureSuccessAsync(response, $"DELETE {endpoint}");
        return true;
    }

    public void Dispose()
    {
        _httpClient.Dispose();
    }

    private static async Task EnsureSuccessAsync(HttpResponseMessage response, string operation)
    {
        if (response.IsSuccessStatusCode)
        {
            return;
        }

        string errorBody = string.Empty;
        try
        {
            errorBody = await response.Content.ReadAsStringAsync();
        }
        catch
        {
            // Ignore response body read failures, status is still enough to surface the error.
        }

        string message = string.IsNullOrWhiteSpace(errorBody)
            ? $"{operation} failed with status {(int)response.StatusCode} ({response.StatusCode})."
            : $"{operation} failed with status {(int)response.StatusCode} ({response.StatusCode}). Body: {errorBody}";

        throw new HttpRequestException(message, null, response.StatusCode);
    }

    private class LoginRequest
    {
        [JsonPropertyName("email")]
        public string Email { get; set; } = string.Empty;

        [JsonPropertyName("password")]
        public string Password { get; set; } = string.Empty;
    }

    private class LoginResponse
    {
        [JsonPropertyName("access_token")]
        public string AccessToken { get; set; } = string.Empty;
    }
}
