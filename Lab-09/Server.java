import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class Server {

    public static void main(String[] args) {
        try {
            Calculator calculator = new CalculatorImpl();

            Registry registry = LocateRegistry.createRegistry(1099);

            registry.rebind("CalculatorService", calculator);

            System.out.println("RMI Server started...");
            System.out.println("CalculatorService is ready.");
            System.out.println("Waiting for client requests...");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
