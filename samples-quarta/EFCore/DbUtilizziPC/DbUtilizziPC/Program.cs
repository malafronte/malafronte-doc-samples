using DbUtilizziPC.Data;
using DbUtilizziPC.Model;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Storage;
using System.Text;

namespace DbUtilizziPC;
internal class Program
{
    enum ModalitàOperativa
    {
        CreazioneDb,
        Q1,
        Q2,
        Q3,
        Q4,
        Q5,
        Q6,
        Q7,
        Nessuna,
        CancellazioneDb
    }

    static void Main(string[] args)
    {
        Console.OutputEncoding = Encoding.UTF8;
        Thread.CurrentThread.CurrentCulture = System.Globalization.CultureInfo.GetCultureInfo("it-IT");
        //colore di default della console
        Console.ForegroundColor = ConsoleColor.Cyan;
        //gestione del menu
        bool uscitaDalProgramma;
        do
        {
            //gestione della scelta 
            bool correctInput;
            do
            {
                Console.Write("Inserire la modalità operativa [");
                foreach(var elem in Enum.GetNames(typeof(ModalitàOperativa)))
                {
                    Console.Write(elem+", ");
                }
                Console.WriteLine("]");
                correctInput = Enum.TryParse(Console.ReadLine(), true, out ModalitàOperativa modalitàOperativa);
                if (correctInput)
                {
                    switch (modalitàOperativa)
                    {
                        case ModalitàOperativa.CreazioneDb:
                            //using effettua il Dispose del context automaticamente
                            using(UtilizziPCContext db = new ())
                            {
                                CreazioneDb(db);
                            }
                            break;
                        case ModalitàOperativa.Q1:
                            Console.WriteLine("Q1: Contare gli alunni di una classe");
                            Console.WriteLine("Inserire la classe");
                            string? classe = Console.ReadLine()?.ToUpper();
                            if(classe != null)
                            {
                                using UtilizziPCContext db = new();
                                Q1(classe, db);
                            }
                            break;
                        case ModalitàOperativa.Q2:
                            Console.WriteLine("Q2: Riportare il numero di alunni per ogni classe");
                            using (UtilizziPCContext db = new())
                            {
                                Q2(db);
                            }
                            break;
                        case ModalitàOperativa.Q3:
                            Console.WriteLine("Q3: Stampa gli studenti che non hanno ancora restituito i computer (sono quelli collegati a Utilizza con DataOraFineUtilizzo pari a null)");
                            using (UtilizziPCContext db = new())
                            {
                                Q3(db);
                            }
                            break;
                        case ModalitàOperativa.Q4:
                            Console.WriteLine("Q4: Stampa l’elenco dei computer che sono stati utilizzati dagli studenti della classe specificata in input. ");
                            Console.WriteLine("Inserire la classe");
                            classe = Console.ReadLine()?.ToUpper();
                            if (classe != null)
                            {
                                using UtilizziPCContext db = new();
                                Q4(classe, db);
                            }
                            break;
                        case ModalitàOperativa.Q5:
                            Console.WriteLine("Q5: Dato un computer (di cui si conosce l’Id) riporta l’elenco degli studenti che lo hanno usato negli ultimi 30 giorni, con l'indicazione della DataOraInizioUtilizzo," +
                                "ordinando i risultati per classe e, a parità di classe, per data (mostrando prima le date più recenti)");
                            Console.WriteLine("Inserire l'id del computer");
                            bool correctId = int.TryParse(Console.ReadLine(), out int computerId) && computerId>=0;
                            if (correctId)
                            {
                                using UtilizziPCContext db = new();
                                Q5(computerId, db);
                            }
                            break;
                        case ModalitàOperativa.Q6:
                            Console.WriteLine("Q6: Stampa per ogni classe quanti utilizzi di computer sono stati fatti negli ultimi 30 giorni.");
                            using (UtilizziPCContext db = new())
                            {
                                Q6(db);
                            }
                            break;
                        case ModalitàOperativa.Q7:
                            Console.WriteLine("Q7: Stampa le classi che hanno utilizzato maggiormente i computer (quelle con il maggior numero di utilizzi) " +
                                "negli ultimi 30 giorni");
                            using (UtilizziPCContext db = new())
                            {
                                Q7(db);
                            }
                            break;
                        case ModalitàOperativa.CancellazioneDb:
                            using (UtilizziPCContext db = new())
                            {
                                CancellazioneDb(db);
                            }
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
    }
    static void CreazioneDb(UtilizziPCContext db)
    {
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

        static void PopulateDb(UtilizziPCContext db)
        {
            //Creazione dei Clienti - gli id vengono generati automaticamente come campi auto-incremento quando si effettua l'inserimento, tuttavia
            //è bene inserire esplicitamente l'id degli oggetti quando si procede all'inserimento massivo gli elementi mediante un foreach perché
            //EF core potrebbe inserire nel database gli oggetti in un ordine diverso rispetto a quello del foreach
            // https://stackoverflow.com/a/54692592
            // https://stackoverflow.com/questions/11521057/insertion-order-of-multiple-records-in-entity-framework/
             List<Classe> classi = new()
            {
                new (){Id =1, Nome="3IA", Aula="Est 1"},
                new (){Id =2,Nome="4IA", Aula="A32"},
                new (){Id =3,Nome="5IA", Aula="A31"},
                new (){Id =4,Nome="3IB", Aula="Est 2"},
                new (){Id =5,Nome="4IB", Aula="A30"},
                new (){Id =6,Nome="5IB", Aula="A32"},
            };

             List<Studente> studenti = new()
            {
                new (){Id = 1, Nome = "Mario", Cognome = "Rossi", ClasseId =1 },
                new (){Id = 2, Nome = "Giovanni", Cognome = "Verdi", ClasseId =1 },
                new (){Id = 3, Nome = "Piero", Cognome = "Angela", ClasseId = 1 },
                new (){Id = 4, Nome = "Leonardo", Cognome = "Da Vinci", ClasseId = 1 },
                new (){Id = 50, Nome = "Cristoforo", Cognome = "Colombo", ClasseId=2 },
                new (){Id = 51, Nome = "Piero", Cognome = "Della Francesca", ClasseId=2 },
                new (){Id = 82, Nome = "Alessandro", Cognome = "Manzoni", ClasseId=4 },
                new (){Id = 83, Nome = "Giuseppe", Cognome = "Parini", ClasseId=4 },
                new (){Id = 102, Nome = "Giuseppe", Cognome = "Ungaretti", ClasseId=3 },
                new (){Id = 103, Nome = "Luigi", Cognome = "Pirandello", ClasseId=3 },
                new (){Id = 131, Nome = "Enrico", Cognome = "Fermi", ClasseId=6 },
                new (){Id = 132, Nome = "Sandro", Cognome = "Pertini", ClasseId=6 },
            };

             List<Computer> computers = new()
            {
                new (){Id = 1, Modello="Hp 19 inc. 2019", Collocazione = "Bunker-D1-D5"},
                new (){Id = 2, Modello="Hp 19 inc. 2019", Collocazione = "Bunker-D1-D5"},
                new (){Id = 3, Modello="Hp 19 inc. 2019", Collocazione = "Bunker-D1-D5"},
                new (){Id = 4, Modello="Hp 19 inc. 2019", Collocazione = "Bunker-D1-D5"},
                new (){Id = 5, Modello="Hp 19 inc. 2019", Collocazione = "Bunker-D1-D5"},
                new (){Id = 6, Modello="Hp 19 inc. 2019", Collocazione = "Bunker-D6-D10"},
                new (){Id = 7, Modello="Hp 19 inc. 2019", Collocazione = "Bunker-D6-D10"},
                new (){Id = 8, Modello="Hp 19 inc. 2019", Collocazione = "Bunker-D6-D10"},
                new (){Id = 9, Modello="Hp 19 inc. 2019", Collocazione = "Bunker-D6-D10"},
                new (){Id = 10, Modello="Hp 19 inc. 2019", Collocazione = "Bunker-D6-D10"},
                new (){Id = 20, Modello="Lenovo i5 2020", Collocazione = "Bunker-D20-D25"},
                new (){Id = 21, Modello="Lenovo i5 2020", Collocazione = "Bunker-D20-D25"},
                new (){Id = 22, Modello="Lenovo i5 2020", Collocazione = "Bunker-D20-D25"},
                new (){Id = 23, Modello="Lenovo i5 2020", Collocazione = "Bunker-D20-D25"},
                new (){Id = 24, Modello="Lenovo i5 2020", Collocazione = "Bunker-D20-D25"},
                new (){Id = 61, Modello="Lenovo i5 2021", Collocazione = "Carrello-Mobile-S1"},
                new (){Id = 62, Modello="Lenovo i5 2021", Collocazione = "Carrello-Mobile-S2"},
                new (){Id = 63, Modello="Lenovo i5 2021", Collocazione = "Carrello-Mobile-S3"},
                new (){Id = 64, Modello="Lenovo i5 2021", Collocazione = "Carrello-Mobile-S4"},
                new (){Id = 65, Modello="Lenovo i5 2021", Collocazione = "Carrello-Mobile-S5"},
            };

             List<Utilizza> utilizzi = new()
            {
                new (){ComputerId = 61,StudenteId=1,
                    DataOraInizioUtilizzo = DateTime.Now.Add(- new TimeSpan(1,12,0)),
                    DataOraFineUtilizzo = DateTime.Now},
                new (){ComputerId = 61,StudenteId=1,
                    DataOraInizioUtilizzo = DateTime.Now.Add(- new TimeSpan(1,1,12,0)),
                    DataOraFineUtilizzo = DateTime.Now.Add(- new TimeSpan(1,0,0,0))},
                new (){ComputerId = 61,StudenteId=3,
                    DataOraInizioUtilizzo = DateTime.Today.AddDays(-2).AddHours(11),
                    DataOraFineUtilizzo = DateTime.Today.AddDays(-2).AddHours(12)},
                new (){ComputerId = 61,StudenteId=82,
                    DataOraInizioUtilizzo = DateTime.Today.AddDays(-1).AddHours(12),
                    DataOraFineUtilizzo = DateTime.Today.AddDays(-1).AddHours(13) },
                new (){ComputerId = 61,StudenteId=1,
                    DataOraInizioUtilizzo = DateTime.Today.AddHours(11),
                    DataOraFineUtilizzo = DateTime.Today.AddHours(12) },
                new (){ComputerId = 62,StudenteId=2,
                    DataOraInizioUtilizzo = DateTime.Today.AddDays(-2).AddHours(11),
                    DataOraFineUtilizzo = DateTime.Today.AddDays(-2).AddHours(12) },
                new (){ComputerId = 62,StudenteId=2,
                    DataOraInizioUtilizzo = DateTime.Today.AddDays(-1).AddHours(12),
                    DataOraFineUtilizzo = DateTime.Today.AddDays(-1).AddHours(13) },
                new (){ComputerId = 62,StudenteId=4,
                    DataOraInizioUtilizzo = DateTime.Today.AddHours(11),
                    DataOraFineUtilizzo = DateTime.Today.AddHours(11) },
                new (){ComputerId = 1,StudenteId=50,
                    DataOraInizioUtilizzo = DateTime.Today.AddDays(-2).AddHours(11),
                    DataOraFineUtilizzo = DateTime.Today.AddDays(-2).AddHours(12) },
                new (){ComputerId = 1,StudenteId=103,
                    DataOraInizioUtilizzo = DateTime.Today.AddDays(-1).AddHours(12),
                    DataOraFineUtilizzo = DateTime.Today.AddDays(-1).AddHours(13) },
                new (){ComputerId = 1,StudenteId=50,
                    DataOraInizioUtilizzo = DateTime.Today.AddHours(11),
                    DataOraFineUtilizzo = DateTime.Today.AddHours(12) },
                new (){ComputerId = 2,StudenteId=51,
                    DataOraInizioUtilizzo = DateTime.Today.AddDays(-1).AddHours(11),
                    DataOraFineUtilizzo = DateTime.Today.AddDays(-1).AddHours(12) },
                new (){ComputerId = 2,StudenteId=51,
                    DataOraInizioUtilizzo = DateTime.Today.AddDays(-1).AddHours(12),
                    DataOraFineUtilizzo = DateTime.Today.AddDays(-1).AddHours(13) },
                new (){ComputerId = 2,StudenteId=103,
                    DataOraInizioUtilizzo = DateTime.Today.AddHours(11),
                    DataOraFineUtilizzo = DateTime.Today.AddHours(12) },
                new (){ComputerId = 3,StudenteId=82,
                    DataOraInizioUtilizzo = DateTime.Today.AddDays(-2).AddHours(11),
                    DataOraFineUtilizzo = DateTime.Today.AddDays(-2).AddHours(12) },
                new (){ComputerId = 3,StudenteId=82,
                    DataOraInizioUtilizzo = DateTime.Today.AddDays(-1).AddHours(11),
                    DataOraFineUtilizzo = DateTime.Today.AddDays(-1).AddHours(13) },
                new (){ComputerId = 3,StudenteId=83,
                    DataOraInizioUtilizzo = DateTime.Today.AddHours(11),
                    DataOraFineUtilizzo = DateTime.Today.AddHours(12) },
                new (){ComputerId = 20,StudenteId=102,
                    DataOraInizioUtilizzo = DateTime.Today.AddDays(-2).AddHours(11),
                    DataOraFineUtilizzo = DateTime.Today.AddDays(-2).AddHours(12) },
                new (){ComputerId = 20,StudenteId=103,
                    DataOraInizioUtilizzo = DateTime.Today.AddDays(-1).AddHours(11),
                    DataOraFineUtilizzo = DateTime.Today.AddDays(-1).AddHours(12) },
                new (){ComputerId = 20,StudenteId=103,
                    DataOraInizioUtilizzo = DateTime.Today.AddHours(11),
                    DataOraFineUtilizzo = DateTime.Today.AddHours(12) },
                new (){ComputerId = 64,StudenteId=131,
                    DataOraInizioUtilizzo = DateTime.Now.Add(- new TimeSpan(0,12,0)),
                    DataOraFineUtilizzo = null},
                new (){ComputerId = 65,StudenteId=132,
                    DataOraInizioUtilizzo = DateTime.Now.Add(- new TimeSpan(1,12,0)),
                    DataOraFineUtilizzo = null},
            };
            Console.WriteLine("Inseriamo le classi nel database");
            classi.ForEach(c => db.Add(c));
            db.SaveChanges();
            Console.WriteLine("Inseriamo gli studenti nel database");
            studenti.ForEach(s => db.Add(s));
            db.SaveChanges();
            Console.WriteLine("Inseriamo i computers nel database");
            computers.ForEach(c => db.Add(c));
            db.SaveChanges();
            Console.WriteLine("Inseriamo gli utilizzi nel database");
            utilizzi.ForEach(u => db.Add(u));
            db.SaveChanges();
        }
    }
    //Q1: Contare gli alunni di una classe
    private static void Q1(string classe, UtilizziPCContext db)
    {
        //esiste al più una sola classe con un dato nome
       Classe? laClasse = db.Classi.Where(c => c.Nome==classe).FirstOrDefault();
        if (laClasse != null)
        {
            int numeroStudentiDellaClasse = db.Studenti.Where(s => s.ClasseId == laClasse.Id).Count();
            Console.WriteLine($"Il numero di studenti della classe {classe} è {numeroStudentiDellaClasse} ");
        }
        else
        {
            Console.WriteLine("Il nome fornito non corrisponde a nessuna classe");
        }
    }

    //Q2: Riportare il numero di alunni per ogni classe
    private static void Q2(UtilizziPCContext db)
    {
        //raggruppiamo gli studenti per classe e poi contiamo
        db.Studenti
            .GroupBy(s => s.Classe) //Classe è la navigation Property
            .Select(g => new { g.Key,  NumeroStudenti = g.Count() })//Key è un oggetto di tipo Classe
            .ToList()
            .ForEach(g => Console.WriteLine($"Classe = {g.Key.Nome}, Numero Alunni = {g.NumeroStudenti}"));
    }

    //Q3: Stampa gli studenti che non hanno ancora restituito i computer (sono quelli collegati a Utilizza con DataOraFineUtilizzo pari a null)
    private static void Q3(UtilizziPCContext db)
    {
        Console.WriteLine("Versione con Navigation Property");
        db.Utilizzi
            .Where(u => u.DataOraFineUtilizzo == null)
            //qui bisogna esplicitamente indicare ad EF Core di caricare anche la Classe di uno Studente
            .Include(u => u.Studente.Classe)
            .Select(u => u.Studente)
            .ToList()
            .ForEach(Console.WriteLine);

        Console.WriteLine("Versione con Join");
        db.Utilizzi
            .Where(u => u.DataOraFineUtilizzo == null)
            .Join(db.Studenti,
                u => u.StudenteId,
                s => s.Id,
                (u, s) => s)
            .Include(s => s.Classe)
            .ToList()
            .ForEach(Console.WriteLine);
    }

    //Q4: Stampa l’elenco dei computer che sono stati utilizzati dagli studenti della classe specificata in input. 
    private static void Q4(string classe, UtilizziPCContext db)
    {
        Console.WriteLine("Versione con Skip Navigation Property");
        db.Studenti
             .Where(s => s.Classe.Nome == classe)
             //in questo caso ad ogni studente è associata una lista di computer.
             //Per restituire una sola lista e non una lista di liste usare SelectMany
             .SelectMany(s => s.Computers) 
             .Distinct()
             .ToList()
             .ForEach(Console.WriteLine);

        Console.WriteLine("Versione con Join");
        db.Studenti
             .Where(s => s.Classe.Nome == classe)
             .Join(db.Utilizzi,
                s => s.Id,
                u => u.StudenteId,
                (s, u) => new { u.ComputerId })
             .Join(db.Computers,
                u => u.ComputerId,
                c => c.Id,
                (u, c) => c)
             .Distinct()
             .ToList()
             .ForEach(Console.WriteLine);
    }

    //Q5: Dato un computer (di cui si conosce l’Id) riporta l’elenco degli studenti che lo hanno usato negli ultimi 30 giorni,
    //con l'indicazione della DataOraInizioUtilizzo,ordinando i risultati per classe e, a parità di classe, per data
    //(mostrando prima le date più recenti)
    private static void Q5(int computerId, UtilizziPCContext db)
    {
        Console.WriteLine("Versione con Navigation Property");
        db.Utilizzi
            .Where(u => u.ComputerId == computerId && u.DataOraInizioUtilizzo >= DateTime.Now.AddDays(-30))
            .Include(u => u.Studente)
            .ThenInclude(s => s.Classe)
            .OrderBy(u => u.Studente.Classe.Nome)
            .ThenByDescending(u => u.DataOraInizioUtilizzo)
            .ToList()
            .ForEach(u => Console.WriteLine($"Studente = {u.Studente}, Data utilizzo computer = {u.DataOraInizioUtilizzo}"));

        Console.WriteLine("Versione con Skip Navigation - in questo caso vogliamo solo sapere quali sono gli studenti che hanno usato il computer");
        db.Computers
            .Where(c => c.Id == computerId)
            .Include(c => c.Studenti)
            .FirstOrDefault()?
            .Studenti
            .ToList()
            .ForEach(Console.WriteLine);

        Console.WriteLine("Versione con Join");
        db.Utilizzi
            .Where(u => u.ComputerId == computerId && u.DataOraInizioUtilizzo >= DateTime.Now.AddDays(-30))
            .Join(db.Studenti.Include(s => s.Classe),
                u => u.StudenteId,
                s => s.Id,
                (u, s) => new { s, u.DataOraInizioUtilizzo })
            .OrderBy(a => a.s.Classe.Nome)
            .ThenByDescending(a => a.DataOraInizioUtilizzo)
            .ToList()
            .ForEach(a => Console.WriteLine($"Studente = {a.s}, Data utilizzo computer = {a.DataOraInizioUtilizzo}"));
    }

    //Q6: Stampa per ogni classe quanti utilizzi di computer sono stati fatti negli ultimi 30 giorni.
    private static void Q6(UtilizziPCContext db)
    {
        Console.WriteLine("Versione con Navigation Property");
        db.Utilizzi
            .Where(u => u.DataOraInizioUtilizzo >= DateTime.Now.AddDays(-30))
            .GroupBy(u => u.Studente.Classe.Nome)
            .Select(g => new { NomeClasse = g.Key, NumeroUtilizzi = g.Count() })
            .ToList()
            .ForEach(Console.WriteLine);

        Console.WriteLine("Versione con Join");
        db.Studenti.Join(db.Utilizzi.Where(u => u.DataOraInizioUtilizzo >= DateTime.Now.AddDays(-30)),
                s => s.Id,
                u => u.StudenteId,
                (s, u) => new { NomeClasse = s.Classe.Nome, u })
            .GroupBy(a => a.NomeClasse)
            .Select(g => new { NomeClasse = g.Key, NumeroUtilizzi = g.Count() })
            .ToList()
            .ForEach(Console.WriteLine);
    }

    //Q7: Stampa le classi che hanno utilizzato maggiormente i computer (quelle con il maggior numero di utilizzi) negli ultimi 30 giorni
    private static void Q7(UtilizziPCContext db)
    {
        Console.WriteLine("Versione con Navigation Property");
        var nUtilizziPerClasse = db.Utilizzi
            .Where(u => u.DataOraInizioUtilizzo >= DateTime.Now.AddDays(-30))
            .GroupBy(u => u.Studente.Classe)
            .Select(g => new { NomeClasse = g.Key.Nome, NumeroUtilizzi = g.Count() });
        var classiConNumeroUtilizziMax = nUtilizziPerClasse
            .Where(u => u.NumeroUtilizzi == nUtilizziPerClasse.Max(u => u.NumeroUtilizzi));
        classiConNumeroUtilizziMax
            .ToList()
            .ForEach(Console.WriteLine);

        Console.WriteLine("Versione con Join");
        //con una prima query sul Database calcoliamo il numero di utilizzi per classe
        //Il risultato è un oggetto che implementa IQueryable sul database
        var numeroUtilizziPerClasse = db.Studenti
            .Join(db.Utilizzi.Where(u => u.DataOraInizioUtilizzo >= DateTime.Now.AddDays(-30)),
                s => s.Id,
                u => u.StudenteId,
                (s, u) => new { NomeClasse = s.Classe.Nome, u })
            .GroupBy(a => a.NomeClasse)
            .Select(g => new { NomeClasse = g.Key, NumeroUtilizzi = g.Count() });

        //Con una seconda query sul Database troviamo le classi che hanno il numero massimo di utilizzi
        var classiConNumeroUtilizziMassimo = numeroUtilizziPerClasse
            .Where(u => u.NumeroUtilizzi == numeroUtilizziPerClasse.Max(u => u.NumeroUtilizzi));
        //stampiamo il risultato nell'applicazione
        classiConNumeroUtilizziMassimo
            .ToList()
            .ForEach(Console.WriteLine);
    }
    static void CancellazioneDb(UtilizziPCContext db)
    {
        WriteLineWithColor("Attenzione, tutto il database andrà eliminato! Questa operazione non può essere revocata.\nSei sicuro di voler procedere? [Si, No]", ConsoleColor.Red);
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
    //Stampa a console con il colore di foreground selezionato e successivamente ripristina il colore precedente
    static void WriteLineWithColor(string text, ConsoleColor consoleColor)
    {
        ConsoleColor previousColor = Console.ForegroundColor;
        Console.ForegroundColor = consoleColor;
        Console.WriteLine(text);
        Console.ForegroundColor = previousColor;
    }
}