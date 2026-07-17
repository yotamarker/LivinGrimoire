import LivinGrimoirePacket.LivinGrimoire.Brain;
import java.util.Scanner;
import java.util.concurrent.*;

static Brain b1 = new Brain();
static BlockingQueue<String> brainQueue = new LinkedBlockingQueue<>();

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
        scheduleTick(ticker);

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

static void scheduleTick(ScheduledExecutorService ticker) {
    ticker.schedule(() -> {
        try {
            brainQueue.put("");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return;
        }
        scheduleTick(ticker);
    }, (long) (b1.getTickInterval() * 1000), TimeUnit.MILLISECONDS);
}