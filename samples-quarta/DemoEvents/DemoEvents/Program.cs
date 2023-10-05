namespace DemoEvents
{
    public class Student
    {
        public int Id { get; set; }
        public string? Name { get; set; }
        public int Age { get; set; }
    }

    public class Exam
    {
        public int Id { get; set; }
        public string? Name { get; set; }
        public int Score { get; set; }
    }

    public class StudentTutor
    {
        public event Action<Student>? OnStudentReceived;
        public event Func<Student, Exam, int>? OnStudentTakeExam;

        //metodo che solleva l'evento StudentReceived
        public void StudentReceived(Student s)
        {
            OnStudentReceived?.Invoke(s);
        }

        //metodo che solleva l'evento StudentTakeExam
        public void StudentTakeExam(Student s, Exam e)
        {
            //callback function che restituisce il punteggio dell'esame
            int? score = OnStudentTakeExam?.Invoke(s, e);
            Console.WriteLine($"Lo studente {s.Name} ha sostenuto l'esame {e.Name} con un punteggio di {score}");
        }
    }

    internal class Program
    {
        static Random gen = new Random();
        static void Main(string[] args)
        {
            //creazione di un oggetto Publisher
            StudentTutor tutor = new StudentTutor();
            //creazione di un oggetto Publisher
            tutor.OnStudentReceived += (s) => Console.WriteLine($"Benvenuto {s.Name}");
            tutor.OnStudentTakeExam += Tutor_OnStudentTakeExam;

            //creazione di studenti ed esami
            Student marioRossi = new Student() { Id = 1, Name = "Mario Rossi", Age = 21 };
            Exam fisica1 = new() { Id = 1, Name = "Fisica 1" };
            Exam analisi1 = new() { Id = 2, Name = "Analisi 1" };

            //attivazione eventi
            tutor.StudentReceived(marioRossi);
            tutor.StudentTakeExam(marioRossi, fisica1);
            tutor.StudentTakeExam(marioRossi, analisi1);
            tutor.StudentTakeExam(marioRossi, fisica1);
            tutor.StudentTakeExam(marioRossi, analisi1);
            tutor.StudentTakeExam(marioRossi, fisica1);
            tutor.StudentTakeExam(marioRossi, analisi1);
        }

        //implementazione callback function corrispondenti agli eventi
        private static int Tutor_OnStudentTakeExam(Student s, Exam e)
        {
            return gen.Next(15, 31);
        }

        private static void Tutor_OnStudentReceived(Student s)
        {
            Console.WriteLine($"Benvenuto {s.Name}");
        }
    }
}