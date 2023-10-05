namespace DemoEventsSimple
{
    //Define publisher class as Pub
    public class Pub
    {
        //OnChange property containing all the 
        //list of subscribers callback methods
        public event Action OnChange = delegate { };
        public event Action<int> OnGetInput = delegate { };

        public void Raise()
        {
            //Invoke OnChange Action
            OnChange();
        }

        //un esempio che prende in input un parametro di tipo intero
        public void RaiseWithInput(int p)
        {
            //Invoke OnGetInput Action
            OnGetInput(p);
        }
    }

    internal class Program
    {
        static void Main(string[] args)
        {
            //Initialize pub class object
            Pub p = new();

            //register for OnChange event - Subscriber 1
            p.OnChange += () => Console.WriteLine("Subscriber 1!");
            //register for OnChange event - Subscriber 2
            p.OnChange += () => Console.WriteLine("Subscriber 2!");

            //raise the event
            p.Raise();
            //After this Raise() method is called
            //all subscribers callback methods will get invoked

            //definiamo una variabile locale per dimostrare il concetto di closure
            int x = 5;

            //subscriber all'evento OnGetInput: accetta in input un numero intero
            p.OnGetInput += (q) => {
                Console.WriteLine("OnGetInput fired");
                q = x + 1;
                Console.WriteLine($"parametro locale q = {q}");
                Console.WriteLine($"riferimento esterno alla lambda expression x = {x}");
            };

            Console.WriteLine("Invochiamo RaiseWithInput");
            //qui passiamo un valore intero che corrisponderà alla q
            p.RaiseWithInput(6);
        }
    }

}