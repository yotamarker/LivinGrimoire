import LivinGrimoirePacket.LivinGrimoire.Brain;
import java.util.Scanner;
import java.util.concurrent.*;

static Brain b1 = new Brain();
static BlockingQueue<String> brainQueue = new LinkedBlockingQueue<>();
static int TICK_INTERVAL_MS = 2000;

void main() {
    Personality p1 = new Personality();
    p1.skillsPush(b1);

    Thread brainThread = new Thread(() -> {
        while (true) {
            try {
                String message = brainQueue.take();
                b1.doIt(message, "", "");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    });
    brainThread.setDaemon(true);
    brainThread.start();

    try (ScheduledExecutorService ticker = Executors.newSingleThreadScheduledExecutor(r -> {
        Thread t = new Thread(r);
        t.setDaemon(true);
        return t;
    })) {
        ticker.scheduleAtFixedRate(() -> {
            try {
                brainQueue.put("");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }, TICK_INTERVAL_MS, TICK_INTERVAL_MS, TimeUnit.MILLISECONDS);

        Scanner scanner = new Scanner(System.in);
        while (true) {
            String input = scanner.nextLine();
            if (input.trim().equalsIgnoreCase("exit")) {
                IO.println("Exiting...");
                System.exit(0);
            }
            try {
                brainQueue.put(input);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
}