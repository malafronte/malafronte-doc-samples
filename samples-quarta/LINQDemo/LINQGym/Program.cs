using System.Collections;
using System.Threading.Channels;

namespace LINQGym
{
    class Student
    {
        public int StudentID { get; set; }
        public string? StudentName { get; set; }
        public int Age { get; set; }
        public double MediaVoti { get; set; }

        public override string ToString()
        {
            return string.Format($"[StudentID = {StudentID}, StudentName = {StudentName}, Age = {Age}, MediaVoti = {MediaVoti}]");
        }
    }

    class Assenza
    {
        public int ID { get; set; }
        public DateTime Giorno { get; set; }
        public int StudentID { get; set; }
    }

    class Persona
    {
        public string? Nome { get; set; }
        public int Eta { get; set; }

        public override string ToString()
        {
            return string.Format($"[Nome = {Nome}, Età = {Eta}]");
        }
    }
    internal class Program
    {
        //stiamo definendo un tipo di puntatore a funzione
        delegate bool CondizioneRicerca(Student s);

        public static void AzioneSuElemento(Student s)
        {
            Console.WriteLine(s);
        }

        //metodo statico
        public static bool VerificaCondizione(Student s)
        {
            return s.Age >= 18 && s.Age <= 25;
        }
        static void Main(string[] args)
        {
            //condizione: non devono esistere due studenti con lo stesso StudentID
            //in questo caso si dice che StudetID è chiave primaria della collection
            Student[] studentArray1 = {
            new () { StudentID = 1, StudentName = "John", Age = 18 , MediaVoti= 6.5},
            new () { StudentID = 2, StudentName = "Steve",  Age = 21 , MediaVoti= 8},
            new () { StudentID = 3, StudentName = "Bill",  Age = 25, MediaVoti= 7.4},
            new () { StudentID = 4, StudentName = "Ram" , Age = 20, MediaVoti = 10},
            new () { StudentID = 5, StudentName = "Ron" , Age = 31, MediaVoti = 9},
            new () { StudentID = 6, StudentName = "Chris",  Age = 17, MediaVoti = 8.4},
            new () { StudentID = 7, StudentName = "Rob",Age = 19  , MediaVoti = 7.7},
            new () { StudentID = 8, StudentName = "Robert",Age = 22, MediaVoti = 8.1},
            new () { StudentID = 11, StudentName = "John",  Age = 21 , MediaVoti = 8.5},
            new () { StudentID = 12, StudentName = "Bill",  Age = 25, MediaVoti = 7},
            new () { StudentID = 13, StudentName = "Ram" , Age = 20, MediaVoti = 9 },
            new () { StudentID = 14, StudentName = "Ron" , Age = 31, MediaVoti = 9.5},
            new () { StudentID = 15, StudentName = "Chris",  Age = 17, MediaVoti = 8},
            new () { StudentID = 16, StudentName = "Rob2",Age = 19  , MediaVoti = 7},
            new () { StudentID = 17, StudentName = "Robert2",Age = 22, MediaVoti = 8},
            new () { StudentID = 18, StudentName = "Alexander2",Age = 18, MediaVoti = 9},
            };

            Student[] studentResultArray;
            List<Student> studentResultList;

            //definiamo delle condizioni di ricerca
            //primo modo: uso di Func con lambda
            Func<Student, bool> condizioneDiRicerca = s => s.Age >= 18 && s.Age <= 25;

            //secondo modo: uso di un delegato implementato attraverso lambda
            CondizioneRicerca condizioneDiRicerca2 = s => s.Age >= 18 && s.Age <= 25;
            //terzo modo: uso di un delegato che punta a un metodo precedentemente definito
            CondizioneRicerca condizioneDiRicerca3 = VerificaCondizione;
            //quarto modo: usiamo direttamente la lambda - il più comodo

            //creo una lista con gli stessi oggetti presenti nell'array
            List<Student> studentList1 = studentArray1.ToList();
            //studio della clausola Where
            //trovare tutti gli studenti che hanno età compresa tra 18 e 25 anni, caso dell'array
            studentResultArray = studentArray1.Where(s => s.Age >= 18 && s.Age <= 25).ToArray();
            studentResultList = studentArray1.Where(s => s.Age >= 18 && s.Age <= 25).ToList();
            //verifichiamo che il risultato sia corretto con una stamapa
            foreach (Student student in studentResultList)
            {
                Console.WriteLine(student);
            }

            //processing sull'array risultato
            Console.WriteLine("\nprocessing sull'array risultato");
            foreach (Student student in studentResultArray)
            {
                Console.WriteLine(student);
            }
            //processing degli elementi di un array usando il LINQ
            Console.WriteLine("\nEsempio di Action su array");
            Array.ForEach(studentResultArray, AzioneSuElemento);
            //Stampa media voti
            Console.WriteLine("\nStampa età e  media voti");
            Array.ForEach(studentResultArray, s =>
            {
                Console.Write(s.StudentName+ " ");
                Console.Write(s.Age + " ");
                Console.WriteLine(s.MediaVoti);
            });

            //processing degli elementi di una lista usando il LINQ
            Console.WriteLine("\nProcessing degli elementi di una lista usando il LINQ");
            studentResultList.ForEach(s =>
            {
                Console.Write(s.StudentName + " ");
                Console.Write(s.Age + " ");
                Console.WriteLine(s.MediaVoti);
            });

            //USO DELLA VERSIONE CON INDICE DELLA WHERE

            //il metodo Where ha anche una versione con l'indice della collection
            //in questo esempio prendiamo solo quelli che verificano la condizione sull'età e hanno indice pari
            Console.WriteLine("selezioniamo solo quelli che verificano la condizione e hanno indice pari");

            studentResultArray = studentArray1.Where(
                (s, i) => (s.Age >= 18 && s.Age <= 25) && i % 2 == 0).ToArray();
            Console.WriteLine("stampa su array");
            Array.ForEach(studentResultArray, s => Console.WriteLine(s.StudentName + " age = " + s.Age));

            studentResultList = studentList1.Where(
                (s, i) => (s.Age >= 18 && s.Age <= 25) && i % 2 == 0).ToList();
            Console.WriteLine("stampa su list");
            studentResultList.
                ForEach(s => Console.WriteLine(s.StudentName + " age = " + s.Age));

            // E' possibile anche far applicare più volte la where per ottenere filtraggi multipli
            Console.WriteLine("doppia where: quelli che verificano la condizione e che hanno ID>3");
            studentResultList = studentList1.
                Where(s => s.Age >= 18 && s.Age <= 25).
                Where(s => s.StudentID > 3).ToList();
            studentResultList.
                ForEach(s => Console.WriteLine(s.StudentName + " age = " + s.Age + " ID = " + s.StudentID));

            //Studiamo la clausola OfType
            //nel caso di collection di tipo diverso è possibile trarre vantaggio dal metodo OfType
            IList mixedList = new ArrayList();
            mixedList.Add(5);
            mixedList.Add("numero uno");
            mixedList.Add(true);
            mixedList.Add("numero due");
            mixedList.Add(new Student() { StudentID = 10, Age = 30, StudentName = "Roberto" });
            List<string> mixedListResult = mixedList.OfType<string>().ToList();
            //IList mixedListResult2 =
            //    (from s in mixedList.OfType<Student>()
            //     where s.Age > 20
            //     select s).
            //    ToList();
            List<Student> mixedListResult2 =
            mixedList.OfType<Student>().Where(s => s.Age > 20).ToList();
            Console.WriteLine("\nStampa del risultato con OfType method");
            mixedListResult.ForEach(s => Console.WriteLine(s));
            mixedListResult2.ForEach(s => Console.WriteLine(s));

            //Studiamo la clausola OrderBy

            //ordiniamo una lista di elementi
            Console.WriteLine("\nOrdiniamo gli elementi di una lista con la clausola OrderBy");
            Console.WriteLine("\nOrdiniamo in base all'età - LINQ method");
            //per invertire l'ordine esiste anche OrderByDescending
            studentResultArray = studentArray1.OrderBy(s => s.Age).ToArray();
            Console.WriteLine("stampa su array");
            Array.ForEach(studentResultArray, s => Console.WriteLine(s.StudentName + " age = " + s.Age));

            studentResultList = studentList1.OrderBy(s => s.Age).ToList();
            Console.WriteLine("\nstampa su list");
            studentResultList.
                ForEach(s => Console.WriteLine(s.StudentName + " age = " + s.Age));
            //su una sola pipe
            Console.WriteLine("Elaborazione di ordinamento e stampa su una sola pipe di codice");
            studentList1
                .OrderBy(s => s.Age)
                .ToList()
                .ForEach(s => Console.WriteLine(s.StudentName + " age = " + s.Age));
            Console.WriteLine("\nOrdiniamo in base all'età - LINQ query");
            studentResultArray = (from s in studentArray1
                                  orderby s.Age
                                  select s).ToArray();
            Console.WriteLine("stampa su array");
            Array.ForEach(studentResultArray, s => Console.WriteLine(s.StudentName + " age = " + s.Age));

            studentResultList = (from s in studentList1
                                 orderby s.Age
                                 select s).ToList();
            Console.WriteLine("\nstampa su list");
            studentResultList.
                ForEach(s => Console.WriteLine(s.StudentName + " age = " + s.Age));

            //ordinamenti multipli
            Console.WriteLine("\nOrdinamenti multipli - LINQ method");
            studentResultArray = studentArray1
                .OrderBy(s => s.Age)
                .ThenBy(s => s.StudentName)
                .ToArray();
            Console.WriteLine("stampa su array");
            Array.ForEach(studentResultArray, s => Console.WriteLine(s.StudentName + " age = " + s.Age));

            studentResultList = studentList1.OrderBy(s => s.Age).ThenBy(s => s.StudentName).ToList();
            Console.WriteLine("\nstampa su list");
            studentResultList.
                ForEach(s => Console.WriteLine(s.StudentName + " age = " + s.Age));

            //Console.WriteLine("\nOrdinamenti multipli - LINQ query");
            //studentResultArray = (from s in studentArray1
            //                      orderby s.Age, s.StudentName descending
            //                      select s).ToArray();
            //Console.WriteLine("stampa su array");
            //Array.ForEach(studentResultArray, s => Console.WriteLine(s.StudentName + " age = " + s.Age));

            //studentResultList = (from s in studentList1
            //                     orderby s.Age, s.StudentName descending
            //                     select s).ToList();
            //Console.WriteLine("\nstampa su list");
            //studentResultList.
            //    ForEach(s => Console.WriteLine(s.StudentName + " age = " + s.Age));

            //Studiamo la clausola select - proiettiamo gli elementi della sequenza in una nuova forma
            Console.WriteLine("\nClausola select - LINQ method");
            Console.WriteLine("\nUso di tipi anonimi");
            //uso di tipi anonimi
            Array.ForEach(
                studentArray1.
                Select(s => new { Nome = s.StudentName, Eta = s.Age }).
                ToArray(),
                 Console.WriteLine);
            Console.WriteLine("\nUso di tipi anonimi - stampa solo il nome");
            studentList1.
                Select(s => new { Nome = s.StudentName, Eta = s.Age }).
                ToList().
                ForEach(p => Console.WriteLine(p.Nome));

            Console.WriteLine("\nUso di tipi non anonimi - stampa solo il nome");
            studentList1.
                Select(s => new Persona() { Nome = s.StudentName, Eta = s.Age }).
                ToList().
                ForEach(p => Console.WriteLine(p.Nome));
            Console.WriteLine("Primo esempio di raggruppamento - raggruppiamo in base all'età");
            //Group By
            //IEnumerable<IGrouping< int, Student>>?
            var groupedResult = studentList1.GroupBy(s => s.Age);
            foreach (var group in groupedResult)
            {
                Console.WriteLine("Group key(Age) = {0}", group.Key);
                foreach (var student in group)
                {
                    Console.WriteLine("Student = {0}", student);
                }
                //calcoliamo una funzione di gruppo: min, max, avg, count
                // funzione count: quanti studenti con la stessa età
                Console.WriteLine("Numero studenti con la stessa età nel gruppo = {0}", group.Count());
                Console.WriteLine("Valore medio dei voti = {0}", group.Average(s => s.MediaVoti));
                Console.WriteLine("Voto massimo nel gruppo = {0}", group.Max(s => s.MediaVoti));
                Console.WriteLine("Voto minimo nel gruppo = {0}", group.Min(s => s.MediaVoti));
                //C# implementa anche il metodo ToLookup che fa la stessa cosa di GroupBy ma la 
                //differenza sta nel fatto che con grandi basi di dati ToLookup carica tutto il risultato in memoria
                //GroupBy carica il risultato associato a una chiave quando serve
                //https://stackoverflow.com/questions/10215428/why-are-tolookup-and-groupby-different
                //https://stackoverflow.com/a/10215531
            }
            Console.WriteLine("STAMPA RAGGRUPPAMENTO PER NOME");
            var groupedResult2 = studentList1.GroupBy(s => s.StudentName);
            foreach (var group in groupedResult2)
            {
                Console.WriteLine("Chiave di raggruppamento (Nome) = " + group.Key);
                foreach (var student in group)
                {
                    Console.WriteLine(student);
                }
                Console.WriteLine("Numero studenti omonimi: " + group.Count());
                Console.WriteLine("Voto medio degli omonimi: " + group.Average(s => s.MediaVoti));
            }
            //intersezione tra due collection - Join
            //creiamo un elenco di assenze di studenti
            List<Assenza> assenzeList1 = new List<Assenza>
            {
                new (){ID = 1, Giorno = DateTime.Today, StudentID = 1 },
                new (){ID = 2, Giorno = DateTime.Today.AddDays(-1) ,StudentID = 1 },
                new (){ID = 3, Giorno = DateTime.Today.AddDays(-3), StudentID = 1 },
                new (){ID = 4, Giorno = new DateTime(2020,11,30), StudentID = 2 },
                new (){ID = 5, Giorno = new DateTime(2020,11,8), StudentID = 3 }
            };
            //vogliamo riportare il nome dello studente e le date delle sue assenze 
            //facciamo una join tra la lista degli studenti e la lista delle assenze degli studenti e poi facciamo la proiezione del risultato su un nuovo oggetto
            var innerJoinStudentiAssenze = studentList1.Join(assenzeList1,
                s => s.StudentID,
                a => a.StudentID,
                (s, a) => new { ID = s.StudentID, Nome = s.StudentName, GiornoAssenza = a.Giorno });
            foreach (var obj in innerJoinStudentiAssenze)
            {
                Console.WriteLine($"ID = {obj.ID}, Nome = {obj.Nome}, GiornoAssenza = {obj.GiornoAssenza.ToShortDateString()}");
            }
        }
    }
}