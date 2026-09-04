import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.Scanner;

public class Client {

    public static void main(String[] args) {

        try {
            Scanner sc = new Scanner(System.in);

            Registry registry =
                    LocateRegistry.getRegistry("localhost", 1099);

            Calculator calculator =
                    (Calculator) registry.lookup("CalculatorService");

            System.out.print("Enter first number: ");
            int a = sc.nextInt();

            System.out.print("Enter second number: ");
            int b = sc.nextInt();

            System.out.println("\nRemote Method Invocation:");
            System.out.println("Addition = " + calculator.add(a, b));
            System.out.println("Multiplication = " + calculator.multiply(a, b));

            sc.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}