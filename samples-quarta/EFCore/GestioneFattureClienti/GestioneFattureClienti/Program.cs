using GestioneFattureClienti.Data;
using System.Text;
using GestioneFattureClienti.Model;
using Microsoft.EntityFrameworkCore.Storage;
using Microsoft.EntityFrameworkCore.Infrastructure;

Console.OutputEncoding = Encoding.UTF8;
Thread.CurrentThread.CurrentCulture = System.Globalization.CultureInfo.GetCultureInfo("it-IT");

ModalitàOperativa modalitàOperativa = ModalitàOperativa.Nessuna;
//colore di default della console
Console.ForegroundColor = ConsoleColor.Cyan;
//gestione del menu
bool uscitaDalProgramma = false;
do
{
    //gestione della scelta 
    bool correctInput = false;
    do
    {
        Console.WriteLine("Inserire la modalità operativa [CreazioneDb, LetturaDb, ModificaFattura, CancellazioneFattura, CancellazioneDb, Nessuna]");
        correctInput = Enum.TryParse(Console.ReadLine(), true, out modalitàOperativa);
        if (correctInput)
        {
            switch (modalitàOperativa)
            {
                case ModalitàOperativa.CreazioneDb:
                    CreazioneDb();
                    break;
                case ModalitàOperativa.LetturaDb:
                    LetturaDb();
                    break;
                case ModalitàOperativa.ModificaFattura:
                    ModificaFattura();
                    break;
                case ModalitàOperativa.CancellazioneFattura:
                    CancellazioneFattura();
                    break;
                case ModalitàOperativa.CancellazioneDb:
                    CancellazioneDb();
                    break;
                default:
                    WriteLineWithColor("Non è stata impostata nessuna modalità operativa", ConsoleColor.Yellow);
                    break;
            }
        }
        if (!correctInput)
        {
            Console.Clear();
            WriteLineWithColor("Il valore inserito non corrisponde a nessuna opzione valida.\nI valori ammessi sono: [Creazione, Lettura, Modifica, Cancellazione, Nessuna]", ConsoleColor.Red);
        }
    } while (!correctInput);
    Console.WriteLine("Uscire dal programma?[Si, No]");
    uscitaDalProgramma = Console.ReadLine()?.ToLower().StartsWith("si") ?? false;
    Console.Clear();
} while (!uscitaDalProgramma);

static void CreazioneDb()
{
    FattureClientiContext db = new();
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
        }
    }
    else //il database non esiste
    {
        //ricreiamo il database a partire dal model (senza dati --> tabelle vuote)
        db.Database.EnsureCreated();
        //popoliamo il database
        PopulateDb(db);
    }

    static void PopulateDb(FattureClientiContext db)
    {
        //Creazione dei Clienti - gli id vengono generati automaticamente come campi auto-incremento quando si effettua l'inserimento, tuttavia
        //è bene inserire esplicitamente l'id degli oggetti quando si procede all'inserimento massivo gli elementi mediante un foreach perché
        //EF core potrebbe inserire nel database gli oggetti in un ordine diverso rispetto a quello del foreach
        // https://stackoverflow.com/a/54692592
        // https://stackoverflow.com/questions/11521057/insertion-order-of-multiple-records-in-entity-framework/
        List<Cliente> listaClienti = new()
        {
            new (){ClienteId=1, RagioneSociale= "Cliente 1", PartitaIVA= "1111111111", Citta = "Napoli", Via="Via dei Mille", Civico= "23", CAP="80100"},
            new (){ClienteId=2, RagioneSociale= "Cliente 2", PartitaIVA= "1111111112", Citta = "Roma", Via="Via dei Fori Imperiali", Civico= "1", CAP="00100"},
            new (){ClienteId=3, RagioneSociale= "Cliente 3", PartitaIVA= "1111111113", Citta = "Firenze", Via="Via Raffaello", Civico= "10", CAP="50100"}
        };

        //Creazione delle Fatture
        List<Fattura> listaFatture = new()
        {
            new (){FatturaId=1, Data= DateTime.Now.Date, Importo = 1200.45m, ClienteId = 1},
            new (){FatturaId=2, Data= DateTime.Now.AddDays(-5).Date, Importo = 3200.65m, ClienteId = 1},
            new (){FatturaId=3, Data= new DateTime(2019,10,20).Date, Importo = 5200.45m, ClienteId = 1},
            new (){FatturaId=4, Data= DateTime.Now.Date, Importo = 5200.45m, ClienteId = 2},
            new (){FatturaId=5, Data= new DateTime(2019,08,20).Date, Importo = 7200.45m, ClienteId = 2}
        };
        Console.WriteLine("Inseriamo i clienti nel database");
        listaClienti.ForEach(c => db.Add(c));
        db.SaveChanges();
        Console.WriteLine("Inseriamo le fatture nel database");
        listaFatture.ForEach(f => db.Add(f));
        db.SaveChanges();
    }
}

static void LetturaDb()
{
    //recuperiamo i dati dal database
    FattureClientiContext db = new();
    //Nel caso in cui il database fosse stato eliminato ricreiamo un nuovo database vuoto a partire dal Model
    db.Database.EnsureCreated();
    //Il codice seguente è scritto in modo che se anche non ci fossero dati nelle tabelle non verrebbero sollevate eccezioni
    Console.WriteLine("Recuperiamo i dati dal database - senza alcuna elaborazione");
    List<Cliente> listaClienti = db.Clienti.ToList();
    List<Fattura> listaFatture = db.Fatture.ToList();
    Console.WriteLine("Stampa dei clienti");
    listaClienti.ForEach(c => Console.WriteLine(c));
    Console.WriteLine("Stampa delle fatture");
    listaFatture.ForEach(f => Console.WriteLine(f));

    Console.WriteLine("Recuperiamo i dati dal database - uso di WHERE");
    Console.WriteLine("Recuperiamo i dati dal database - trovare le fatture fatte da almeno tre giorni");
    db.Fatture.Where(f => f.Data < DateTime.Now.AddDays(-2)).ToList().ForEach(f => Console.WriteLine(f));
    Console.WriteLine("Recuperiamo i dati dal database - trovare l'importo complessivo delle fatture fatte da almeno tre giorni ");
    Console.WriteLine($"Importo complessivo: {db.Fatture.Where(f => f.Data < DateTime.Now.AddDays(-2)).Sum(f => (double)f.Importo):C2}");
    Console.WriteLine("Recuperiamo i dati dal database - trovare l'importo medio delle fatture fatte da almeno tre giorni ");
    static bool searchPredicate(Fattura f) => f.Data < DateTime.Now.AddDays(-2);
    var count = db.Fatture.Where(searchPredicate).Count();
    //se non ci sono elementi nella collection i metodi Average, Max e Min sollevano l'eccezione InvalidOperationException
    if (count > 0)
    {
        Console.WriteLine($"Importo medio: {db.Fatture.Where(searchPredicate).Average(f => (double)f.Importo):C2}");
        Console.WriteLine("Recuperiamo i dati dal database - trovare l'importo massimo delle fatture fatte da almeno tre giorni ");
        Console.WriteLine($"Importo massimo: {db.Fatture.Where(searchPredicate).Max(f => (double)f.Importo):C2}");
        Console.WriteLine("Recuperiamo i dati dal database - trovare l'importo minimo delle fatture fatte da almeno tre giorni ");
        Console.WriteLine($"Importo minimo: {db.Fatture.Where(searchPredicate).Min(f => (double)f.Importo):C2}");
        Console.WriteLine("Recuperiamo i dati dal database - trovare il numero delle fatture fatte da almeno tre giorni ");
        Console.WriteLine("Numero fatture: " + count);
    }
    Console.WriteLine("Recuperiamo i dati dal database - uso di WHERE e JOIN");
    Console.WriteLine("trovare il nome e l'indirizzo dei clienti che hanno speso più di 5000 EUR");
    var clientiConSpesa5000Plus = db.Fatture.Where(f => f.Importo > 5000).Join(db.Clienti,
        f => f.ClienteId,
        c => c.ClienteId,
        (f, c) => new { NumeroFattura = f.FatturaId, DataFattura = f.Data, NomeCliente = c.RagioneSociale, Indirizzo = c.Via + " N." + c.Civico + " " + c.CAP + " " + c.Citta });
    clientiConSpesa5000Plus.ToList().ForEach(c => Console.WriteLine(c));

    //altro modo - uso delle navigation properties
    Console.WriteLine("Recuperiamo i dati dal database - Uso di Navigation Property per ottenere i dati dei clienti a partire dalle fatture");
    var clientiConSpesa5000Plus2 = db.Fatture.Where(f => f.Importo > 5000).
        Select(f => new
        {
            NumeroFattura = f.FatturaId,
            DataFattura = f.Data,
            NomeCliente = f.Cliente.RagioneSociale,
            Indirizzo = f.Cliente.Via + " N." + f.Cliente.Civico + " " + f.Cliente.CAP + " " + f.Cliente.Citta
        });
    clientiConSpesa5000Plus2.ToList().ForEach(c => Console.WriteLine(c));
}

static void ModificaFattura()
{

    FattureClientiContext db = new();
    //la modifica ha senso solo se il database esiste e ha almeno un paio di fatture inserite
    //Nel caso in cui il database fosse stato eliminato ricreiamo un nuovo database vuoto a partire dal Model
    db.Database.EnsureCreated();
    //Il codice seguente è scritto in modo che se anche non ci fossero dati nelle tabelle non verrebbero sollevate eccezioni
    var numeroFatture = db.Fatture.Count();
    if (numeroFatture > 2)
    {
        Console.WriteLine("\nModifichiamo i dati nel database");
        Console.WriteLine("Modifichiamo l'importo della prima fattura");

        Console.WriteLine("\nle fatture prima della modifica sono:\n");

        //stampiamo la lista delle fatture per vedere il risultato
        //se il database non esiste listaFatture sarà null.

        List<Fattura> listaFatture = db.Fatture.ToList();
        Console.WriteLine("Stampa delle fatture");
        listaFatture.ForEach(f => Console.WriteLine(f));

        //accediamo all'elemento da modificare
        Fattura? fattura = db.Fatture.Find(1);//trova l'entity con il valore della chiave (FatturaId) specificato
        if (fattura != null)//se ho trovato la fattura con FatturaId specificato
        {
            //modifichiamo la fattura
            fattura.Importo *= 1.2m;//incremento del 20% l'importo
            db.SaveChanges();//aggiorno il database

            //stampiamo la lista delle fatture per vedere il risultato
            listaFatture = db.Fatture.ToList();
            Console.WriteLine("Stampa delle fatture dopo la modifica");
            listaFatture.ForEach(f => Console.WriteLine(f));
        }
        Console.WriteLine("\nmodifichiamo anche la seconda fattura");
        //non è possibile usare ElementAt - https://stackoverflow.com/questions/5147767/why-is-the-query-operator-elementat-is-not-supported-in-linq-to-sql
        Fattura? secondaFattura = db.Fatture.Skip(1)?.First();
        if (secondaFattura != null)
        {
            secondaFattura.Importo *= 1.3m;
            db.SaveChanges();
            //stampiamo la lista delle fatture per vedere il risultato
            listaFatture = db.Fatture.ToList();
            Console.WriteLine("Stampa delle fatture");
            listaFatture.ForEach(f => Console.WriteLine(f));
        }
        Console.WriteLine("\nmodifichiamo anche l'ultima");
        //non è possibile usare ElementAt - https://stackoverflow.com/questions/5147767/why-is-the-query-operator-elementat-is-not-supported-in-linq-to-sql
        Fattura? ultimaFattura = db.Fatture.OrderBy(f => f.FatturaId).Last();
        if (ultimaFattura != null)
        {
            ultimaFattura.Importo *= 1.5m;
            db.SaveChanges();
            //stampiamo la lista delle fatture per vedere il risultato
            listaFatture = db.Fatture.ToList();
            Console.WriteLine("Stampa delle fatture");
            listaFatture.ForEach(f => Console.WriteLine(f));
        }
    }
    else
    {
        WriteLineWithColor("Non ci sono abbastanza Fatture nel database per eseguire la funzionalità richiesta", ConsoleColor.Red);
    }
}
static void CancellazioneFattura()
{
    FattureClientiContext db = new();
    //Nel caso in cui il database fosse stato eliminato ricreiamo un nuovo database vuoto a partire dal Model
    db.Database.EnsureCreated();
    //Il codice seguente è scritto in modo che se anche non ci fossero dati nelle tabelle non verrebbero sollevate eccezioni
    Console.WriteLine("\nEliminiamo un dato dal database");
    Console.WriteLine("\nPrima della cancellazione le fatture sono:");
    List<Fattura> listaFatture = db.Fatture.ToList();
    Console.WriteLine("Stampa delle fatture");
    listaFatture.ForEach(f => Console.WriteLine(f));
    Console.WriteLine("\nEliminiamo la terza fattura");
    //accediamo alla terza fattura - possiamo accedere o mediante chiave, oppure in base ad un elenco da cui prendiamo la terza
    //decidiamo di eliminare la fattura con FatturaId=3
    Fattura? fatturaDaEliminare = db.Fatture.Find(3);
    if (fatturaDaEliminare != null)//se abbiamo trovato la fattura con id =3
    {
        Console.WriteLine($"eliminiamo la fattura con id {fatturaDaEliminare.FatturaId}");
        db.Remove(fatturaDaEliminare);
        db.SaveChanges();
        //stampiamo nuovamente l'elenco delle fatture per verificare che la fattura con id specifico è stata eliminata
        listaFatture = db.Fatture.ToList();
        Console.WriteLine("Stampa delle fatture");
        listaFatture.ForEach(f => Console.WriteLine(f));
    }
    else
    {
        WriteLineWithColor("Non è stato possibile eliminare la fattura indicata, perché non esiste", ConsoleColor.Red);
    }
}

static void CancellazioneDb()
{
    FattureClientiContext db = new();
    WriteLineWithColor("Attenzione tutto il database andrà eliminato! Questa operazione non può essere revocata.\nSei sicuro di voler procedere? [Si, No]", ConsoleColor.Red);
    bool dbErase = Console.ReadLine()?.ToLower().StartsWith("si") ?? false;
    if (dbErase)
    {
        if (db.Database.EnsureDeleted())
        {
            Console.WriteLine("Database cancellato correttamente");
        }
        else
        {
            Console.WriteLine("Il database non esisteva e non è stata fatta alcuna azione");
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
enum ModalitàOperativa
{
    CreazioneDb,
    LetturaDb,
    ModificaFattura,
    CancellazioneFattura,
    CancellazioneDb,
    Nessuna
}