using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Storage;
using Romanzi.Data;
using Romanzi.Model;

InitTest();
WriteLineWithColor("\nEsecuzione di Q1: " +
    "\ncreare un metodo che prende in input la nazionalità e stampa gli autori che hanno la nazionalità specificata" +
    "\nCaso della nazionalità Americana\n", ConsoleColor.Cyan);
Q1("Americana");

WriteLineWithColor("\nEsecuzione di Q2: " +
    "\ncreare un metodo che prende in input il nome e il cognome di un autore e stampa tutti i romanzi di quell’autore" +
    "\nCaso di Enrest Hemingway\n",ConsoleColor.Cyan);
Q2("Ernest", "Hemingway");

WriteLineWithColor("\nEsecuzione di Q3: " +
    "\ncreare un metodo che prende in input la nazionalità e stampa quanti romanzi di quella nazionalità sono presenti nel database" +
    "\nCaso della nazionalità Americana\n", ConsoleColor.Cyan);
Q3("Americana");

WriteLineWithColor("\nEsecuzione di Q4: " +
    "\ncreare un metodo che per ogni nazionalità stampa quanti romanzi di autori di quella nazionalità sono presenti nel database\n", ConsoleColor.Cyan);
Q4();
WriteLineWithColor("\nEsecuzione di Q5: " +
    "\ncreare un metodo che stampa il nome dei personaggi presenti in romanzi di autori di una data nazionalità" +
    "\nCaso della nazionalità Inglese\n", ConsoleColor.Cyan);
Q5("Inglese");

//Q1: creare un metodo che prende in input la nazionalità e
//stampa gli autori che hanno la nazionalità specificata 
static void Q1(string nazionalità)
{
    using var db = new RomanziContext();
    Console.WriteLine($"Artisti di nazionalità {nazionalità}");
    db.Autori
        .Where(a => a.Nazionalità != null
            && a.Nazionalità.Equals(nazionalità))
        .ToList()
        .ForEach(a => Console.WriteLine($"{a.Nome} {a.Cognome}"));

}

//Q2: creare un metodo che prende in input il nome e il cognome di un autore
//e stampa tutti i romanzi di quell’autore
static void Q2(string nome, string cognome)
{
    using var db = new RomanziContext();
    //primo modo - uso di inner join
    Console.WriteLine("primo modo - uso di Join");
    db.Autori
         .Where(a => a.Nome.Equals(nome)
            && a.Cognome.Equals(cognome))//filtriamo per nome e cognome
         .Join(db.Romanzi,//Join con romanzi
             a => a.AutoreId,
             r => r.AutoreId,
             (a, r) => new { a.Nome, a.Cognome, r.Titolo, r.AnnoPubblicazione })//prendiamo le colonne che interessano
         .ToList()//restituiamo al client il risultato
         .ForEach(t => Console.WriteLine(t));//processiamo il risultato

    //secondo metodo - uso di navigation property a partire da Romanzi
    Console.WriteLine("secondo modo - uso di navigation property a partire da Romanzi");
    db.Romanzi
        .Where(r => r.Autore.Nome.Equals(nome)
            && r.Autore.Cognome.Equals(cognome))
        .ToList()//restituiamo al client il risultato
        .ForEach(t => Console.WriteLine($"\t{t.Titolo} {t.AnnoPubblicazione}"));//processiamo il risultato

    //terzo modo - uso di navigation property
    Console.WriteLine("terzo modo - uso di navigation property a partire da Autori - più involuto");
    db.Autori
         .Where(a => a.Nome.Equals(nome)
            && a.Cognome.Equals(cognome))//filtriamo per nome e cognome
         .Select(a => new { a, RomanziDiAutore = a.Romanzi })//usiamo la navigation property a.Romanzi
         .ToList()//restituiamo al client il risultato
         .ForEach(t =>
         { //processiamo il risultato
             Console.WriteLine($"Autore = {t.a.Nome} {t.a.Cognome}");
             if (t.RomanziDiAutore != null)
             {
                 foreach (var libro in t.RomanziDiAutore)
                 {
                     Console.WriteLine($"\t{libro.Titolo} {libro.AnnoPubblicazione}");
                 }
             }
         });

    //quarto modo - uso di navigation property e di Include 
    //👇👇👇
    //ATTENZIONE! Le collection property e le navigation property non sono automaticamente caricate nell'app, quando si esegue una query.
    //https://learn.microsoft.com/en-us/ef/core/querying/related-data/
    //https://learn.microsoft.com/en-us/ef/core/querying/related-data/eager
    //👆👆👆
    //In questo esempio se togliessimo l'include e commentassimo i due modi precedenti di eseguire la query
    //vedremmo che il risultato non includerebbe i Romanzi
    Console.WriteLine("quarto modo - uso di navigation property e di Include");
    db.Autori
         .Where(a => a.Nome.Equals(nome)
            && a.Cognome.Equals(cognome))//filtriamo per nome e cognome
         .Include(a => a.Romanzi)//chiediamo al provider del database di caricare i romanzi tramite la navigation property
         .ToList()//restituiamo al client il risultato
         .ForEach(a =>
         { //processiamo il risultato
             Console.WriteLine($"Autore = {a.Nome} {a.Cognome}");
             if (a.Romanzi != null)
             {
                 foreach (var libro in a.Romanzi)
                 {
                     Console.WriteLine($"\t{libro.Titolo} {libro.AnnoPubblicazione}");
                 }
             }
         });
}

//Q3: creare un metodo che prende in input la nazionalità e stampa quanti romanzi di quella nazionalità
//sono presenti nel database
static void Q3(string nazionalità)
{
    using var db = new RomanziContext();

    //primo modo - uso di join
    var numeroRomanzi = db.Autori
          .Where(a => a.Nazionalità != null
            && a.Nazionalità.Equals(nazionalità))//filtriamo per nome e cognome
          .Join(db.Romanzi,//Join con romanzi
              a => a.AutoreId,
              r => r.AutoreId,
              (a, r) => new { r.RomanzoId })
          .Count();
    Console.WriteLine($"I romanzi di nazionalità {nazionalità} sono: {numeroRomanzi}");

    //secondo modo - uso di navigation property
    var numeroRomanzi2 = db.Romanzi
        .Where(r => r.Autore.Nazionalità != null
            && r.Autore.Nazionalità.Equals(nazionalità))
        .Count();
    Console.WriteLine("Secondo metodo");
    Console.WriteLine($"I romanzi di nazionalità {nazionalità} sono: {numeroRomanzi2}");
}
//Q4: creare un metodo che per ogni nazionalità stampa quanti romanzi di autori di quella
//nazionalità sono presenti nel database
static void Q4()
{
    //primo modo - facciamo una join seguita da un raggruppamento
    //In questo esempio è molto importante effettuare la Select dopo la GroupBy, altrimenti si ottiene un errore:
    //la Select serve a completare l'esecuzione della query all'interno del database con il calcolo di eventuale 
    //funzione di gruppo. Solo successivamente, con il ToList si restituisce il risultato della GroupBy all'applicazione
    Console.WriteLine("Primo metodo - uso di Join e di Group By");
    using var db = new RomanziContext();
    db.Autori
        .Join(db.Romanzi,
             a => a.AutoreId,
             r => r.AutoreId,
             (a, r) => new { Nazionalita = a.Nazionalità, r.RomanzoId })
        .GroupBy(r => r.Nazionalita)//effettuiamo il raggruppamento
        .Select(g => new { Nazionalità = g.Key, NumeroRomanzi = g.Count() })//calcoliamo la funzione di gruppo - Count in questo caso
        .ToList() //restituiamo il risultato all'app
        .ForEach(t => Console.WriteLine($"Nazionalità = {t.Nazionalità}; numero romanzi = {t.NumeroRomanzi}"));//processiamo il risultato

    //secondo modo - uso di navigation properties
    Console.WriteLine("\nSecondo metodo - uso di GroupBy con navigation properties");
    db.Romanzi
        .GroupBy(r => r.Autore.Nazionalità)//effettuo il raggruppamento
        .Select(g => new { Nazionalità = g.Key, NumeroRomanzi = g.Count() })//calcoliamo la funzione di gruppo - Count in questo caso
        .ToList()//restituiamo il risultato all'app
        .ForEach(t => Console.WriteLine($"Nazionalità = {t.Nazionalità}; numero romanzi = {t.NumeroRomanzi}"));//processiamo il risultato
}
//Q5: creare un metodo che stampa il nome dei personaggi presenti in romanzi di autori di una data nazionalità
static void Q5(string nazionalità)
{
    using var db = new RomanziContext();
    //primo modo - uso di join di join
    Console.WriteLine("Primo modo - uso di join");
    db.Autori
        .Where(a => a.Nazionalità != null
            && a.Nazionalità.Equals(nazionalità))
        .Join(db.Romanzi,
            a => a.AutoreId,
            r => r.AutoreId,
            (a, r) => new { r.RomanzoId })
        .Join(db.Personaggi,
            r => r.RomanzoId,
            p => p.RomanzoId,
            (r, p) => p)
        .ToList()
        .ForEach(p => Console.WriteLine($"{p.Nome} {p.Ruolo} {p.Sesso}"));

    //secondo modo - uso di navigation property
    Console.WriteLine("\nSecondo modo - uso di navigation property");
    db.Personaggi
        .Where(p => p.Romanzo.Autore.Nazionalità != null
            && p.Romanzo.Autore.Nazionalità.Equals(nazionalità))
        .ToList()
        .ForEach(p => Console.WriteLine($"{p.Nome} {p.Ruolo} {p.Sesso}"));

}



static void InitTest()
{
    RomanziContext db = new();
    //verifichiamo se il database esista già
    //https://medium.com/@Usurer/ef-core-check-if-db-exists-feafe6e36f4e
    //https://stackoverflow.com/questions/33911316/entity-framework-core-how-to-check-if-database-exists
    if (db.Database.GetService<IRelationalDatabaseCreator>().Exists())
    {
        WriteLineWithColor("Il database esiste già, vuoi ricrearlo da capo? Tutti i valori precedentemente inseriti verranno persi. [Si, No]", ConsoleColor.Red);
        bool dbErase = Console.ReadLine()?.ToLower().StartsWith("si") ?? false;
        if (dbErase)
        {
            //cancelliamo il database se esiste
            db.Database.EnsureDeleted();
            //ricreiamo il database a partire dal model (senza dati --> tabelle vuote)
            db.Database.EnsureCreated();
            //inseriamo i dati nelle tabelle
            PopulateDb(db);
            Console.WriteLine("Database ricreato correttamente");
        }
    }
    else //il database non esiste
    {
        //ricreiamo il database a partire dal model (senza dati --> tabelle vuote)
        db.Database.EnsureCreated();
        //popoliamo il database
        PopulateDb(db);
        Console.WriteLine("Database creato correttamente");
    }

    static void PopulateDb(RomanziContext db)
    {
        //Almeno 5 autori di nazionalità compresa tra "Americana", "Belga", "Inglese".
        List<Autore> autori = new()
        {
            new (){AutoreId=1, Nome="Ernest",Cognome="Hemingway", Nazionalità="Americana"},//AutoreId=1
            new (){AutoreId=2,Nome="Philip",Cognome="Roth", Nazionalità="Americana"},//AutoreId=2
            new (){AutoreId=3,Nome="Thomas",Cognome="Owen", Nazionalità="Belga"},//AutoreId=3
            new (){AutoreId=4,Nome="William",Cognome="Shakespeare", Nazionalità="Inglese"},//AutoreId=4
            new (){AutoreId=5,Nome="Charles",Cognome="Dickens", Nazionalità="Inglese"},//AutoreId=5
        };

        autori.ForEach(a => db.Add(a));
        db.SaveChanges();
        //Almeno 10 romanzi degli autori precedentemente inseriti
        List<Romanzo> romanzi = new()
        {
            new (){RomanzoId=1, Titolo="For Whom the Bell Tolls", AnnoPubblicazione=1940, AutoreId=1},//RomanzoId=1
            new (){RomanzoId=2,Titolo="The Old Man and the Sea", AnnoPubblicazione=1952, AutoreId=1},
            new (){RomanzoId=3,Titolo="A Farewell to Arms",AnnoPubblicazione=1929, AutoreId=1},
            new (){RomanzoId=4,Titolo="Letting Go", AnnoPubblicazione=1962, AutoreId=2},
            new (){RomanzoId=5,Titolo="When She Was Good", AnnoPubblicazione=1967, AutoreId=2},
            new (){RomanzoId=6,Titolo="Destination Inconnue", AnnoPubblicazione=1942, AutoreId=3},
            new (){RomanzoId=7,Titolo="Les Fruits de l'orage", AnnoPubblicazione=1984, AutoreId=3},
            new (){RomanzoId=8,Titolo="Giulio Cesare", AnnoPubblicazione=1599, AutoreId=4},
            new (){RomanzoId=9,Titolo="Otello", AnnoPubblicazione=1604, AutoreId=4},
            new (){RomanzoId=10,Titolo="David Copperfield", AnnoPubblicazione=1849, AutoreId=5},
        };
        romanzi.ForEach(r => db.Add(r));
        db.SaveChanges();
        //Almeno 5 personaggi presenti nei romanzi precedentemente inseriti
        List<Personaggio> personaggi = new()
        {
            new (){PersonaggioId=1, Nome="Desdemona", Ruolo="Protagonista", Sesso="Femmina", RomanzoId=9},//PersonaggioId=1
            new (){PersonaggioId=2,Nome="Jago", Ruolo="Protagonista", Sesso="Maschio", RomanzoId=9},
            new (){PersonaggioId=3,Nome="Robert", Ruolo="Protagonista", Sesso="Maschio", RomanzoId=1},
            new (){PersonaggioId=4,Nome="Cesare", Ruolo="Protagonista", Sesso="Maschio", RomanzoId=8},
            new (){PersonaggioId=5,Nome="David", Ruolo="Protagonista", Sesso="Maschio", RomanzoId=10}
        };
        personaggi.ForEach(p => db.Add(p));
        db.SaveChanges();
    }

}

//stampa a console con il colore di foreground selezionato e successivamente ripristina il colore precedente
static void WriteLineWithColor(string text, ConsoleColor consoleColor)
{
    ConsoleColor previousColor = Console.ForegroundColor;
    Console.ForegroundColor = consoleColor;
    Console.WriteLine(text);
    Console.ForegroundColor = previousColor;
}

