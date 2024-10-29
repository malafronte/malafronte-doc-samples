using MigrationsTest.Data;
using MigrationsTest.Model;

using var db = new BloggingContext();
// Note: This sample requires the database to be created before running.
Console.WriteLine($"Database path: {db.DbPath}.");

// Create
Console.WriteLine("Inserting a new blog");
db.Add(new Blog { Name="Il blog di EF Core" });
db.SaveChanges();

// Read
Console.WriteLine("Querying for a blog");
var blog = db.Blogs
    .OrderBy(b => b.Id)
    .First();
Console.WriteLine($"blog: {blog.Name}");
