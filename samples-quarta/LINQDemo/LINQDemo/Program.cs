namespace LINQDemo
{
    class Student
    {
        public int StudentID { get; set; }
        public string? StudentName { get; set; }
        public int Age { get; set; }

        public override string ToString()
        {
            return string.Format($"[StudentID = {StudentID}, StudentName = {StudentName}, Age = {Age}]");
        }
    }
    internal class Program
    {
        static void Main(string[] args)
        {
            Student[] studentArray =
            {
                new () { StudentID = 1, StudentName = "John", Age = 18},
                new () { StudentID = 2, StudentName = "Steve",  Age = 21},
                new () { StudentID = 3, StudentName = "Bill",  Age = 25},
                new () { StudentID = 4, StudentName = "Ram" , Age = 20},
                new () { StudentID = 5, StudentName = "Ron" , Age = 31},
                new () { StudentID = 6, StudentName = "Chris",  Age = 17},
                new () { StudentID = 7, StudentName = "Rob", Age = 19},
            };
            List<Student> students = [];
            foreach (Student std in studentArray)
            {
                if (std.Age > 12 && std.Age < 20)
                {
                    students.Add(std);
                }
            }
            //write result
            foreach (var studente in students)
            {
                Console.WriteLine(studente);
            }
            Console.ReadLine();
        }

    }
}
