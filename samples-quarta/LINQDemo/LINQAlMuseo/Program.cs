//file Program.cs - utilizzo di Top Level Statements
//Esercizio: LINQ al museo
using LinqAlMuseo;
using System.Globalization;
using System.Text;

//creazione delle collection
//si parte da quelle che non puntano a nulla, ossia quelle che non hanno chiavi esterne
IList<Artista> artisti = new List<Artista>()
            {
                new (){Id=1, Cognome="Picasso", Nome="Pablo", Nazionalita="Spagna"},
                new (){Id=2, Cognome="Dalì", Nome="Salvador", Nazionalita="Spagna"},
                new (){Id=3, Cognome="De Chirico", Nome="Giorgio", Nazionalita="Italia"},
                new (){Id=4, Cognome="Guttuso", Nome="Renato", Nazionalita="Italia"}
            };
//poi le collection che hanno Fk
IList<Opera> opere = new List<Opera>() {
                new (){Id=1, Titolo="Guernica", Quotazione=50000000.00m , FkArtista=1},//opera di Picasso
                new (){Id=2, Titolo="I tre musici", Quotazione=15000000.00m, FkArtista=1},//opera di Picasso
                new (){Id=3, Titolo="Les demoiselles d’Avignon", Quotazione=12000000.00m,  FkArtista=1},//opera di Picasso
                new (){Id=4, Titolo="La persistenza della memoria", Quotazione=16000000.00m,  FkArtista=2},//opera di Dalì
                new (){Id=5, Titolo="Metamorfosi di Narciso", Quotazione=8000000.00m, FkArtista=2},//opera di Dalì
                new (){Id=6, Titolo="Le Muse inquietanti", Quotazione=22000000.00m,  FkArtista=3},//opera di De Chirico
            };
IList<Personaggio> personaggi = new List<Personaggio>() {
                new (){Id=1, Nome="Uomo morente", FkOperaId=1},//un personaggio di Guernica 
                new (){Id=2, Nome="Un musicante", FkOperaId=2},
                new (){Id=3, Nome="una ragazza di Avignone", FkOperaId=3},
                new (){Id=4, Nome="una seconda ragazza di Avignone", FkOperaId=3},
                new (){Id=5, Nome="Narciso", FkOperaId=5},
                new (){Id=6, Nome="Una musa metafisica", FkOperaId=6},
            };

//impostiamo la console in modo che stampi correttamente il carattere dell'euro e che utilizzi le impostazioni di cultura italiana
Console.OutputEncoding = Encoding.UTF8;
Thread.CurrentThread.CurrentCulture = new CultureInfo("it-IT");

//Le query da sviluppare sono:
//Effettuare le seguenti query:
//1)    Stampare le opere di un dato autore (ad esempio Picasso)
//2)    Riportare per ogni nazionalità (raggruppare per nazionalità) gli artisti
//3)    Contare quanti sono gli artisti per ogni nazionalità (raggruppare per nazionalità e contare)
//4)    Trovare la quotazione media, minima e massima delle opere di Picasso
//5)    Trovare la quotazione media, minima e massima di ogni artista
//6)    Raggruppare le opere in base alla nazionalità e in base al cognome dell’artista (Raggruppamento in base a più proprietà)
//7)    Trovare gli artisti di cui sono presenti almeno 2 opere
//8)    Trovare le opere che hanno personaggi
//9)    Trovare le opere che non hanno personaggi
//10)   Trovare l’opera con il maggior numero di personaggi


//svolgimento delle query richieste
//1) Stampare le opere di un dato autore (ad esempio Picasso)
Console.WriteLine("**** 1) Stampare le opere di un dato autore (ad esempio Picasso)\n");
//facciamo prima il filtraggio con la Where e poi la join
var opereDiArtista = artisti.Where(a => a.Cognome == "Picasso").Join(opere,
    a => a.Id,
    o => o.FkArtista,
    (a, o) => o.Titolo);
opereDiArtista.ToList().ForEach(t => Console.WriteLine(t));
//altro metodo: facciamo prima la Join e poi il filtraggio con la Where sull'autore
Console.WriteLine();
var opereDiArtista2 = artisti.Join(opere,
    a => a.Id,
    o => o.FkArtista,
    (a, o) => new { a, o }).Where(t => t.a.Cognome == "Picasso");
opereDiArtista2.ToList().ForEach(t => Console.WriteLine(t.o.Titolo));
Console.WriteLine();
//altro modo:
//step n.1: calcoliamo l'id di Picasso
//step. n.2: calcoliamo le opere di quell'autore
var autore = artisti.Where(a => a.Cognome == "Picasso").FirstOrDefault();
if (autore != null)
{
    var opereDiArtista3 = opere.Where(o => o.FkArtista == autore.Id);
    opereDiArtista3.ToList().ForEach(t => Console.WriteLine(t.Titolo));
}


//2) Riportare per ogni nazionalità (raggruppare per nazionalità) gli artisti
Console.WriteLine("\n**** 2) Riportare per ogni nazionalità (raggruppare per nazionalità) gli artisti\n");

//raggruppare gli artisti per nazionalità
var artistiPerNazionalità = artisti.GroupBy(a => a.Nazionalita);
foreach (var group in artistiPerNazionalità)
{
    Console.WriteLine($"Nazionalità: {group.Key}");
    foreach (var artista in group)
    {
        Console.WriteLine($"\t{artista.Nome} {artista.Cognome}");
    }
}

//3) Contare quanti sono gli artisti per ogni nazionalità (raggruppare per nazionalità e contare)
Console.WriteLine("\n**** 3) Contare quanti sono gli artisti per ogni nazionalità (raggruppare per nazionalità e contare)\n");

foreach (var group in artistiPerNazionalità)
{
    Console.WriteLine($"Nazionalità: {group.Key} Numero artisti: {group.Count()}");
}

//4) Trovare la quotazione media, minima e massima delle opere di Picasso
Console.WriteLine("\n**** 4) Trovare la quotazione media, minima e massima delle opere di Picasso\n");
//troviamo le opere di Picasso
var opereDiPicasso = artisti.Where(a => a.Cognome == "Picasso")
    .Join(opere,
    a => a.Id,
    o => o.FkArtista,
    (a, o) => o).ToList();
//troviamo le quotazioni
var quotazioneMinima = opereDiPicasso.Min(o => o.Quotazione);
var quotazioneMedia = opereDiPicasso.Average(o => o.Quotazione);
var quotazioneMassima = opereDiPicasso.Max(o => o.Quotazione);
//stampiamo il risultato
Console.WriteLine($"Quotazione minima = {quotazioneMinima}, " +
    $"quotazione media = {quotazioneMedia:F2}, quotazione massima = {quotazioneMassima}");

//5) Trovare la quotazione media, minima e massima di ogni artista
Console.WriteLine("\n**** 5) Trovare la quotazione media, minima e massima di ogni artista\n");
//raggruppiamo per artista (usando FkArtista) e poi su ogni gruppo di opere calcoliamo le funzioni di gruppo
var operePerArtista = opere.GroupBy(o => o.FkArtista);
foreach (var group in operePerArtista)
{
    Console.Write($"Id artista = {group.Key} ");
    //voglio conoscere i dettagli dell'artista di cui conosco l'id
    var artista = artisti.Where(a => a.Id == group.Key).FirstOrDefault();
    if (artista != null)
    {
        Console.Write($"{artista.Nome} {artista.Cognome} ");
    }
    Console.WriteLine($"Quotazione minima = {group.Min(o => o.Quotazione):C2};" +
        $" media = {group.Average(o => o.Quotazione):C2};" +
        $" massima = {group.Max(o => o.Quotazione):C2}");
}

//stessa query - versione con inner join
//effettuiamo prima la join tra opere e artisti e poi il raggruppamento
var opereDiArtistaGroupBy = artisti.Join(opere,
    a => a.Id,
    o => o.FkArtista,
    (a, o) => new { a, o }).GroupBy(t => t.a.Id);

foreach (var group in opereDiArtistaGroupBy)
{
    Console.Write($"Id artista = {group.Key} |");
    var artistaOpera = group.FirstOrDefault();
    if (artistaOpera != null)
    {
        Console.Write($"Cognome = {artistaOpera.a.Cognome}");
    }
    Console.WriteLine($" | Quotazione media ={group.Average(t => t.o.Quotazione):C2} " +
    $" | Quotazione minima = {group.Min(t => t.o.Quotazione):C2} " +
    $" | Quotazione massima = {group.Max(t => t.o.Quotazione):C2} ");
}

//6) Raggruppare le opere in base alla nazionalità e in base al cognome dell’artista (Raggruppamento in base a più proprietà)
Console.WriteLine("\n**** 6) Raggruppare le opere in base alla nazionalità e in base al cognome dell’artista (Raggruppamento in base a più proprietà)\n");
var opereDiArtistaGroupByMultiplo = artisti.Join(opere,
    a => a.Id,
    o => o.FkArtista,
    (a, o) => new { a, o }).GroupBy(t => new { t.a.Nazionalita, t.a.Cognome });

foreach (var group in opereDiArtistaGroupByMultiplo)
{
    //Console.WriteLine($"Chiave di raggruppamento = {group.Key}");
    //foreach (var item in group)
    //{
    //    Console.WriteLine($"Elemento = {item}");
    //}
    Console.WriteLine($"{group.Key.Nazionalita} {group.Key.Cognome} ");
    foreach (var item in group)
    {
        Console.WriteLine($"\tOpera = {item.o.Titolo}");
    }
}

//7)Trovare gli artisti di cui sono presenti almeno 2 opere
Console.WriteLine("\n**** 7) Trovare gli artisti di cui sono presenti almeno 2 opere\n");
//intanto calcolo gli artisti di cui ho almeno un'opera
var artistiConAlmeno1Opera = artisti.Join(opere,
    a => a.Id,
    o => o.FkArtista,
    (a, o) => a);
//per calcolare gli artisti di cui sono presenti almeno due opere procedo così:
//raggruppo gli artisti per FkArtista e successivamente filtro in base al conteggio degli 
//elementi in ogni gruppo
Console.WriteLine("Artisti con almeno due opere");
var artistiConAlmeno2Opere = opere.GroupBy(o => o.FkArtista)
    .Where(g => g.Count() >= 2).Join(artisti,
    g => g.Key,
    a => a.Id,
    (g, a) => a);
foreach (var artista in artistiConAlmeno2Opere)
{
    Console.WriteLine(artista);
}

//altra variante - riporta gli artisti con il relativo numero di opere
opere.GroupBy(o => o.FkArtista).
Select(group => new { group.Key, NumeroOpere = group.Count() }).
Where(g => g.NumeroOpere >= 2).
Join(artisti,
a2 => a2.Key,
a => a.Id,
(a2, a) => new { ID = a.Id, NomeArtista = a.Cognome, a2.NumeroOpere }
).ToList().ForEach(s => Console.WriteLine(s));

//foreach (var group in artistiConAlmeno2Opera)
//{
//    Console.WriteLine($"{group.Key}");
//}

//8)Trovare le opere che hanno personaggi
Console.WriteLine("\n**** 8) Trovare le opere che hanno personaggi\n");
//le opere con personaggi (è una semplice join)
var opereConPersonaggi = opere.Join(personaggi,
    o => o.Id,
    p => p.FkOperaId,
    (o, p) => o);
Console.WriteLine("Opere con personaggi");
foreach (var opera in opereConPersonaggi)
{
    Console.WriteLine(opera);
}

//9)Trovare le opere che non hanno personaggi
Console.WriteLine("\n**** 9) Trovare le opere che non hanno personaggi\n");
//opere senza personaggi: dall'insieme delle opere prendo solo quelle che non sono contenute in opereConPersonaggi
var opereSenzaPersonaggi = opere
    .Where(o => !opereConPersonaggi.Contains(o));

Console.WriteLine("Opere senza personaggi");
foreach (var opera in opereSenzaPersonaggi)
{
    Console.WriteLine(opera);
}

//10)Trovare le opere con il maggior numero di personaggi
Console.WriteLine("\n**** 10) Trovare le opere con il maggior numero di personaggi\n");
//primo step: calcolo il numero di personaggi per opera
var personaggiPerOpera = personaggi.
                GroupBy(p => p.FkOperaId).
                Select(group => new { IdOpera = group.Key, NumeroPersonaggi = group.Count() });
//secondo step: dobbiamo filtrare gli oggetti in modo da prendere solo quelli con il numero massimo di personaggi
var numeroMassimoPersonaggi = personaggiPerOpera.Max(t => t.NumeroPersonaggi);
//terzo step: filtro i dati in modo da prendere solo gli oggetti con il numero massimo di personaggi
var opereConMaxNumeroPersonaggi = personaggiPerOpera
    .Where(t => t.NumeroPersonaggi == numeroMassimoPersonaggi)
    .Join(opere,
    t => t.IdOpera,
    o => o.Id,
    (t, o) => new { id = o.Id, Titolo = o.Titolo, Personaggi = t.NumeroPersonaggi });
foreach (var item in opereConMaxNumeroPersonaggi)
{
    Console.WriteLine(item);
}