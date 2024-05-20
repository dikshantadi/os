import 'dart:async';
import 'dart:collection';
import 'dart:math';

void main() {
  final bankSimulation = BankSimulation();
  bankSimulation.start(
      'FCFS'); // Change this to 'FCFS' or 'SJF' to run different algorithms
}

class BankSimulation {
  final Queue<Customer> queue = Queue<Customer>();
  final List<Teller> tellers = List.generate(3, (index) => Teller(index + 1));
  bool simulationRunning = true;
  final Random random = Random();

  void start(String schedulingAlgorithm) {
    _startCustomerArrival();
    for (var teller in tellers) {
      switch (schedulingAlgorithm) {
        case 'FCFS':
          _startTellerServiceFCFS(teller);
          break;
        case 'SJF':
          _startTellerServiceSJF(teller);
          break;
        case 'RR':
          int quantum = 3; // Define the time quantum for Round Robin
          _startTellerServiceRR(teller, quantum);
          break;
        default:
          print('Invalid scheduling algorithm');
          return;
      }
    }
    _waitForTermination();
  }

  void _startCustomerArrival() {
    Timer.periodic(Duration(seconds: random.nextInt(3) + 1), (timer) {
      if (!simulationRunning) {
        timer.cancel();
        return;
      }
      final customer = Customer(random.nextInt(10) + 1);
      queue.add(customer);
      print('Customer ${customer.id} enters the Queue');
    });
  }

  void _startTellerServiceFCFS(Teller teller) {
    Timer.periodic(Duration(milliseconds: 500), (timer) async {
      if (!simulationRunning) {
        timer.cancel();
        return;
      }
      if (queue.isNotEmpty) {
        final customer = queue.removeFirst();
        print('Customer ${customer.id} is in Teller ${teller.id}');
        await Future.delayed(Duration(seconds: customer.serviceTime));
        print('Customer ${customer.id} leaves the Teller ${teller.id}');
      }
    });
  }

  void _startTellerServiceSJF(Teller teller) {
    Timer.periodic(Duration(milliseconds: 500), (timer) async {
      if (!simulationRunning) {
        timer.cancel();
        return;
      }
      if (queue.isNotEmpty) {
        final sortedQueue = queue.toList()
          ..sort((a, b) => a.serviceTime.compareTo(b.serviceTime));
        final customer = sortedQueue.first;
        queue.remove(customer);
        print(
            'Customer ${customer.id} (Shortest Job) is in Teller ${teller.id}');
        await Future.delayed(Duration(seconds: customer.serviceTime));
        print(
            'Customer ${customer.id} (Shortest Job) leaves the Teller ${teller.id}');
      }
    });
  }

  void _startTellerServiceRR(Teller teller, int quantum) {
    Timer.periodic(Duration(milliseconds: 500), (timer) async {
      if (!simulationRunning) {
        timer.cancel();
        return;
      }
      if (queue.isNotEmpty) {
        final customer = queue.removeFirst();
        final serveTime = min(quantum, customer.remainingTime);
        print(
            'Customer ${customer.id} (Round Robin) is in Teller ${teller.id}');
        await Future.delayed(Duration(seconds: serveTime));
        customer.remainingTime -= serveTime;
        if (customer.remainingTime > 0) {
          queue.add(customer);
          print(
              'Customer ${customer.id} (Round Robin) goes back to the Queue with ${customer.remainingTime} seconds remaining');
        } else {
          print(
              'Customer ${customer.id} (Round Robin) leaves the Teller ${teller.id}');
        }
      }
    });
  }

  void _waitForTermination() {
    Future.delayed(Duration(seconds: 60), () {
      simulationRunning = false;
      print('Simulation ended');
    });
  }
}

class Customer {
  static int _idCounter = 0;
  final int id;
  final int serviceTime;
  int remainingTime;

  Customer(this.serviceTime)
      : id = ++_idCounter,
        remainingTime = serviceTime;
}

class Teller {
  final int id;
  Teller(this.id);
}
