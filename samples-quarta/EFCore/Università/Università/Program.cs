using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Storage;
using Università.Data;
using Università.Model;

namespace Università;

class Program
{
    /// <summary>
    /// Popola il database
    /// </summary>
    public static void PopulateDB()
    {
        //1) inserisco istanze nelle tabelle che non hanno chiavi esterne -->CorsoDiLaurea, Docente
        //creo una lista di CorsoDiLaurea e di Docente
        List<Docente> docenti = new()
        {
            new (){CodDocente=1, Cognome="Malafronte", Nome="Gennaro",Dipartimento=Dipartimento.IngegneriaInformatica },
            new (){CodDocente=2, Cognome="Rossi", Nome="Mario", Dipartimento=Dipartimento.Matematica},
            new (){CodDocente=3, Cognome="Verdi", Nome="Giuseppe", Dipartimento=Dipartimento.Fisica},
            new (){CodDocente=4, Cognome= "Smith", Nome="Albert", Dipartimento=Dipartimento.Economia}
        };
        List<CorsoLaurea> corsiDiLaurea = new() {
            new (){CorsoLaureaId = 1,TipoLaurea=TipoLaurea.Magistrale, Facoltà=Facoltà.Ingegneria},
            new (){CorsoLaureaId = 2,TipoLaurea=TipoLaurea.Triennale, Facoltà=Facoltà.MatematicaFisicaScienze},
            new (){CorsoLaureaId = 3,TipoLaurea=TipoLaurea.Magistrale, Facoltà=Facoltà.Economia},

        };
        using (var db = new UniversitàContext())
        {
            docenti.ForEach(d => db.Add(d));
            corsiDiLaurea.ForEach(cl => db.Add(cl));
            db.SaveChanges();
        }
        //2) inserisco altre istanze: Inserisco istanze di Corso e di Studente
        List<Corso> corsi = new()
        {
            new (){CodiceCorso=1,Nome="Fondamenti di Informatica 1", CodDocente=1},
            new (){CodiceCorso=2,Nome="Analisi Matematica 1", CodDocente=2},
            new (){CodiceCorso=3,Nome="Fisica 1", CodDocente=3},
            new (){CodiceCorso=4, Nome="Microeconomia 1", CodDocente=4}
        };
        List<Studente> studenti = new()
        {
            new (){Matricola=1, Nome="Giovanni", Cognome="Casiraghi", CorsoLaureaId=1, AnnoNascita=2000},
            new (){Matricola=2, Nome="Alberto", Cognome="Angela", CorsoLaureaId=2, AnnoNascita=1999},
            new (){Matricola=3, Nome="Piero", Cognome="Gallo", CorsoLaureaId=3, AnnoNascita=2000}
        };
        using (var db = new UniversitàContext())
        {
            corsi.ForEach(c => db.Add(c));
            studenti.ForEach(s => db.Add(s));
            db.SaveChanges();
        }
        //4) inserisco le frequenze - è la tabella molti a molti
        List<Frequenta> frequenze = new()
        {
            new (){Matricola=1, CodCorso=1},// Giovanni Casiraghi frequenze il corso di Fondamenti di Informatica 1
            new (){Matricola=1, CodCorso=2},// Giovanni Casiraghi frequenze il corso di Analisi Matematica 1
            new (){Matricola=2, CodCorso=2},
            new (){Matricola=2, CodCorso=3},
            new (){Matricola=3, CodCorso=4}
        };
        using (var db = new UniversitàContext())
        {
            frequenze.ForEach(f => db.Add(f));
            db.SaveChanges();
        }

    }

    /// <summary>
    /// Stampa a Console l'elenco degli studenti
    /// </summary>
    public static void PrintStudents()
    {
        using var db = new UniversitàContext();
        //leggo gli studenti
        List<Studente> studenti = db.Studenti.ToList();
        //stampo gli studenti
        studenti.ForEach(s => Console.WriteLine($"Matricola = {s.Matricola}, Nome = {s.Nome}, Cognome = {s.Cognome}"));
    }

    /// <summary>
    /// Stampa a console l'elenco dei corsi
    /// </summary>
    public static void PrintCourses()
    {
        //leggo gli studenti
        using var db = new UniversitàContext();
        List<Corso> corsi = db.Corsi.ToList();
        corsi.ForEach(s => Console.WriteLine($"CodCorso = {s.CodiceCorso}, Nome = {s.Nome}, CodDocente = {s.CodDocente}"));

    }

    /// <summary>
    /// Un metodo che stampa i corsi seguiti da uno studente di cui si conosce nome e cognome
    /// </summary>
    /// <param name="nomeStudente">Nome dello studente</param>
    /// <param name="cognomeStudente">Nome dello studente</param>
    public static void PrintCorsiDiStudente(string nomeStudente, string cognomeStudente)
    {
        //trovare i corsi seguiti da uno studente - doppio join
        using var db = new UniversitàContext();
        //attenzione - potrebbero esserci casi di omonimia!
        var corsiFrequentatiDaStudente = db.Studenti
            .Where(s => s.Nome.ToUpper().Equals(nomeStudente.ToUpper())
                && s.Cognome.ToUpper().Equals(cognomeStudente.ToUpper()))
            .Join(db.Frequenze,
                s => s.Matricola,
                f => f.Matricola,
                (s, f) => new { f.CodCorso });
        //Console.WriteLine($"\nQuery eseguita sul database per {nameof(corsiFrequentatiDaStudente)} = {corsiFrequentatiDaStudente.ToQueryString()}\n");
        var dettaglioCorsiFrequentati = corsiFrequentatiDaStudente
            .Join(db.Corsi,
                cf => cf.CodCorso,
                c => c.CodiceCorso,
                (cf, c) => c);
        //Console.WriteLine($"\nQuery eseguita sul database per {nameof(dettaglioCorsiFrequentati)} = {dettaglioCorsiFrequentati.ToQueryString()}\n");
        dettaglioCorsiFrequentati.ToList().ForEach(c => Console.WriteLine($"Nome Corso = {c.Nome}"));

        Console.WriteLine("Altro metodo - uso di navigation property");
        //altro metodo - navigation property
        db.Studenti
            .Where(s => s.Nome.ToUpper().Equals(nomeStudente.ToUpper())
            && s.Cognome.ToUpper().Contains(cognomeStudente.ToUpper()))
            //how to flatten a list of list in C#: https://stackoverflow.com/questions/1145558/linq-list-of-lists-to-single-list
            .SelectMany(x => x.Corsi)
            .ToList()
            .ForEach(c => Console.WriteLine($"Nome Corso = {c.Nome}"));

    }

    /// <summary>
    /// Stampa a console il numero di corsi seguiti da uno studente
    /// </summary>
    /// <param name="codStudente">Codice dello studente di cui si vuole contare i corsi</param>
    public static void PrintNumeroCorsiDiStudente(int codStudente)
    {
        using var db = new UniversitàContext();
        //uso della tabella di collegamento molti a molti - Frequenta in questo caso
        Console.WriteLine("Uso della tabella di collegamento molti a molti - Frequenta");
        var numeroCorsiFrequentatiDaStudente = db.Frequenze.Where(f => f.Matricola == codStudente).Count();
        Console.WriteLine($"Numero corsi frequentati dallo studente con Matricola = {codStudente} " +
            $"-> numero corsi: {numeroCorsiFrequentatiDaStudente}");

        //Uso di collection property
        Console.WriteLine("Uso di collection property");
        db.Studenti.
            Where(s => s.Matricola == codStudente)
            .Select(s => new { s.Matricola, s.Nome, s.Cognome, NumeroCorsi = s.Corsi.Count })
            .ToList()
            .ForEach(s => Console.WriteLine($"Numero corsi frequentati dallo studente matricola {s.Matricola} {s.Nome} {s.Cognome} -> numero corsi: {s.NumeroCorsi}"));

        //Uso di Entry per recuperare dati di una collection collegata a un oggettio già caricato in memoria
        Console.WriteLine("Uso di Entry per recuperare dati di una collection collegata a un oggettio già caricato in memoria");
        var studente = db.Studenti.Where(s => s.Matricola == codStudente).FirstOrDefault();
        if (studente != null)
        { //come effettuare una query su una collection property: https://www.entityframeworktutorial.net/EntityFramework4.3/explicit-loading-with-dbcontext.aspx
            var numeroCorsiFrequentatiDaStudente2 = db.Entry(studente).Collection(s => s.Corsi).Query().Count();
            Console.WriteLine($"Numero corsi frequentati dallo studente con Matricola = " +
                $"{codStudente} -> numero corsi: {numeroCorsiFrequentatiDaStudente2}");
        }

    }

    /// <summary>
    /// Stampa a console il numero di corsi seguiti da uno studente
    /// </summary>
    /// <param name="nomeStudente"></param>
    /// <param name="cognomeStudente"></param>
    public static void PrintNumeroCorsiDiStudente(string nomeStudente, string cognomeStudente)
    {
        using var db = new UniversitàContext();
        //https://docs.microsoft.com/en-us/ef/core/miscellaneous/collations-and-case-sensitivity
        //https://medium.com/@bridgesquared/efcore-sqlite-case-insensitive-order-21371b256e5
        //https://github.com/dotnet/efcore/issues/8033
        //per SQLite la collation predefinita è case sensitive

        //versione con join e group by
        db.Studenti
            .Where(s => s.Nome.ToUpper().Equals(nomeStudente.ToUpper())
                && s.Cognome.ToUpper().Equals(cognomeStudente.ToUpper()))
            .Join(db.Frequenze,
                s => s.Matricola,
                f => f.Matricola,
                (s, f) => new { s.Matricola, s.Nome, s.Cognome, f.CodCorso })
            .GroupBy(t => t.Matricola)
            .Select(g => new { Matricola = g.Key, g.First().Nome, g.First().Cognome, NumeroCorsi = g.Count() })
            .ToList()
            .ForEach(s => Console.WriteLine($"Numero corsi frequentati dallo studente matricola " +
            $"{s.Matricola} {s.Nome} {s.Cognome} -> numero corsi: {s.NumeroCorsi}"));

        //Uso di collection property
        //poiché vengono dati in input nome e cognome, ci potrebbero essere più studenti con lo stesso nome e cognome
        //quindi il risultato dovrebbe riportare, per ciascuno il numero di conrsi seguiti

        Console.WriteLine("Uso di collection property");
        db.Studenti
            .Where(s => s.Nome.ToUpper().Contains(nomeStudente.ToUpper())
                && s.Cognome.ToUpper().Contains(cognomeStudente.ToUpper()))
            .Select(s => new { s.Matricola, s.Nome, s.Cognome, NumeroCorsi = s.Corsi.Count })
            .ToList()
            .ForEach(s => Console.WriteLine($"Numero corsi frequentati dallo studente matricola " +
            $"{s.Matricola} {s.Nome} {s.Cognome} -> numero corsi: {s.NumeroCorsi}"));
    }

    /// <summary>
    /// Modifica il docente di un corso di cui è noto l’id
    /// </summary>
    /// <param name="codCorso">codice del corso</param>
    /// <param name="nuovoCodDocente">nuovo codice del docente</param>
    public static void ModificaDocenteCorso(int codCorso, int nuovoCodDocente)
    {
        using var db = new UniversitàContext();
        //accedo al corso
        var corso = db.Corsi.Find(codCorso);
        //accedo al docente per verificare che esiste quel docente
        var docente = db.Docenti.Find(nuovoCodDocente);
        //se esiste il docente con il nuovoCodDocente aggiorno il corso
        if (docente != null && corso != null)
        {
            corso.CodDocente = nuovoCodDocente;
            db.SaveChanges();
            Console.WriteLine("Aggiornamento effettuato");
        }
        else if (docente == null)
        {
            Console.WriteLine("Impossibile aggiornare, il docente con il codice specificato non esiste");
        }
        else if (corso == null)
        {
            Console.WriteLine("Impossibile aggiornare, il corso il codice specificato non esiste");
        }
    }

    /// <summary>
    /// Per ogni studente stampa il numero di corsi frequentati
    /// </summary>
    public static void PrintNumeroCorsiFrequentatiPerStudente()
    {
        //raggruppo su Frequenta per Matricola e poi faccio la join con Studente per avere i dati di ciascuno studente
        using var db = new UniversitàContext();

        //MOLTO IMPORTANTE: https://docs.microsoft.com/en-us/ef/core/what-is-new/ef-core-3.x/breaking-changes
        //https://docs.microsoft.com/en-us/ef/core/what-is-new/ef-core-3.x/breaking-changes#linq-queries-are-no-longer-evaluated-on-the-client
        //https://stackoverflow.com/questions/58138556/client-side-groupby-is-not-supported
        //https://stackoverflow.com/a/60778664
        //The LINQ GroupBy is much different from the SQL GROUP BY statement:
        //LINQ just divides the underlying collection into chunks depending on a key,
        //while SQL additionally applies an aggregation function to condense each of these chunks down into a single value.
        var grouped = db.Frequenze.GroupBy(f => f.Matricola).Select(e => new { e.Key, Count = e.Count() });
        //vedere anche
        //https://www.thinktecture.com/en/entity-framework-core/hidden-group-by-capabilities-in-3-0-part-1/
        //https://www.thinktecture.com/en/entity-framework-core/hidden-group-by-capabilities-in-3-0-part-2/

        //https://stackoverflow.com/questions/37527783/get-sql-code-from-an-entity-framework-core-iqueryablet
        //https://stackoverflow.com/a/51583047
        //richiede using Microsoft.EntityFrameworkCore;
        //Console.WriteLine($"\nQuery eseguita sul database per {nameof(grouped)} = {grouped.ToQueryString()}\n");

        var result = grouped
            .Join(db.Studenti,
                group => group.Key,
                s => s.Matricola,
                (group, s) => new { s.Matricola, s.Nome, s.Cognome, NumeroCorsiFrequentati = group.Count });
        //Console.WriteLine($"\nQuery eseguita sul database per {nameof(result)} = {result.ToQueryString()}\n");
        //stampa risultato
        result.ToList().ForEach(r => Console.WriteLine(r));

        ////IL SEGUENTE APPROCCIO NON FUNZIONA DA EC 3.X IN AVANTI
        ////il problema si ha quando si tenta di passare dalla GroupBy al ToList 
        //var grouped2 = db.Frequenta.GroupBy(f => f.Matricola);
        //var result2 = grouped2.Join(db.Studenti,
        //    group => group.Key,
        //    s => s.Matricola,
        //    (group, s) => new { s.Matricola, s.Nome, s.Cognome, NumeroCorsiFrequentati = group.Count() });
        ////stampa risultato
        ////qui ho un errore perché si tenta di trasformare la group by dell'SQL (aggregazione) in un collection di collection
        //result2.ToList().ForEach(r => Console.WriteLine(r));
    }


    static void InitTest()
    {
        UniversitàContext db = new();
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
                PopulateDb();
                Console.WriteLine("Database ricreato correttamente");
            }
        }
        else //il database non esiste
        {
            //ricreiamo il database a partire dal model (senza dati --> tabelle vuote)
            db.Database.EnsureCreated();
            //popoliamo il database
            PopulateDb();
            Console.WriteLine("Database creato correttamente");
        }

        static void PopulateDb()
        {
            //1) inserisco istanze nelle tabelle che non hanno chiavi esterne -->CorsoDiLaurea, Docente
            //creo una lista di CorsoDiLaurea e di Docente
            List<Docente> docenti = new()
            {
                new (){CodDocente=1, Cognome="Malafronte", Nome="Gennaro",Dipartimento=Dipartimento.IngegneriaInformatica },
                new (){CodDocente=2, Cognome="Rossi", Nome="Mario", Dipartimento=Dipartimento.Matematica},
                new (){CodDocente=3, Cognome="Verdi", Nome="Giuseppe", Dipartimento=Dipartimento.Fisica},
                new (){CodDocente=4, Cognome= "Smith", Nome="Albert", Dipartimento=Dipartimento.Economia}
            };
            List<CorsoLaurea> corsiDiLaurea = new() 
            {
                new (){CorsoLaureaId = 1,TipoLaurea=TipoLaurea.Magistrale, Facoltà=Facoltà.Ingegneria},
                new (){CorsoLaureaId = 2,TipoLaurea=TipoLaurea.Triennale, Facoltà=Facoltà.MatematicaFisicaScienze},
                new (){CorsoLaureaId = 3,TipoLaurea=TipoLaurea.Magistrale, Facoltà=Facoltà.Economia},
            };
            using (var db = new UniversitàContext())
            {
                docenti.ForEach(d => db.Add(d));
                corsiDiLaurea.ForEach(cl => db.Add(cl));
                db.SaveChanges();
            }
            //2) inserisco altre istanze: Inserisco istanze di Corso e di Studente
            List<Corso> corsi = new()
            {
                new (){CodiceCorso=1,Nome="Fondamenti di Informatica 1", CodDocente=1},
                new (){CodiceCorso=2,Nome="Analisi Matematica 1", CodDocente=2},
                new (){CodiceCorso=3,Nome="Fisica 1", CodDocente=3},
                new (){CodiceCorso=4, Nome="Microeconomia 1", CodDocente=4}
            };
            List<Studente> studenti = new()
            {
                new (){Matricola=1, Nome="Giovanni", Cognome="Casiraghi", CorsoLaureaId=1, AnnoNascita=2000},
                new (){Matricola=2, Nome="Alberto", Cognome="Angela", CorsoLaureaId=2, AnnoNascita=1999},
                new (){Matricola=3, Nome="Piero", Cognome="Gallo", CorsoLaureaId=3, AnnoNascita=2000}
            };
            using (var db = new UniversitàContext())
            {
                corsi.ForEach(c => db.Add(c));
                studenti.ForEach(s => db.Add(s));
                db.SaveChanges();
            }
            //4) inserisco le frequenze - è la tabella molti a molti
            List<Frequenta> frequenze = new()
            {
                new (){Matricola=1, CodCorso=1},// Giovanni Casiraghi frequenze il corso di Fondamenti di Informatica 1
                new (){Matricola=1, CodCorso=2},// Giovanni Casiraghi frequenze il corso di Analisi Matematica 1
                new (){Matricola=2, CodCorso=2},
                new (){Matricola=2, CodCorso=3},
                new (){Matricola=3, CodCorso=4}
            };
            using (var db = new UniversitàContext())
            {
                frequenze.ForEach(f => db.Add(f));
                db.SaveChanges();
            }

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
    static void Main(string[] args)
    {


        InitTest();
        WriteLineWithColor("\nEsecuzione di Q1:" +
            "\nStampare l'elenco degli studenti: ", ConsoleColor.Cyan);
        PrintStudents();
        WriteLineWithColor("\nEsecuzione di Q2:" +
            "\nStampare l'elenco dei corsi", ConsoleColor.Cyan);
        PrintCourses();
        WriteLineWithColor("\nEsecuzione di Q3:" +
            "\nModificare il docente di un corso di cui è noto l’id:", ConsoleColor.Cyan);
        ModificaDocenteCorso(1, 1);
        WriteLineWithColor("\nDopo la modifica i corsi sono i seguenti:", ConsoleColor.Cyan);
        PrintCourses();
        WriteLineWithColor("\nEsecuzione di Q4:" +
            "\nStampare il numero di corsi seguiti dallo studente con id = 1:", ConsoleColor.Cyan);
        PrintNumeroCorsiDiStudente(1);
        WriteLineWithColor("\nEsecuzione di Q5:" +
             "\nStampare il numero di corsi seguiti dallo studente con Nome=\"Giovanni\" e Cognome =\"Casiraghi\"", ConsoleColor.Cyan);
        PrintNumeroCorsiDiStudente("Giovanni", "Casiraghi");
        WriteLineWithColor("\nEsecuzione di Q6:" +
            "\nStampare il numero di corsi seguiti da ogni studente", ConsoleColor.Cyan);
        PrintNumeroCorsiFrequentatiPerStudente();
        WriteLineWithColor("\nEsecuzione di Q7:" +
            "\nStampare i corsi seguiti dallo studente con Nome=\"Piero\" e Cognome =\"Gallo\"", ConsoleColor.Cyan);
        PrintCorsiDiStudente("Piero", "Gallo");
        WriteLineWithColor("Finito!", ConsoleColor.Cyan);

    }
}

