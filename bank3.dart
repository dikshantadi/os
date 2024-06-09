import 'dart:async';
import 'dart:collection';
import 'dart:io';
import 'dart:math';

class Customer {
  final int id;
  final int serviceTime;
  DateTime arrivalTime;
  DateTime? startTime;
  DateTime? endTime;

  Customer(this.id)
      : serviceTime = Random().nextInt(10) + 1,
        arrivalTime = DateTime.now();
}

class Teller {
  final int id;
  final Queue<Customer> queue;
  final String schedulingAlgorithm;
  bool _isBusy = false;

  Teller(this.id, this.queue, this.schedulingAlgorithm);

  Future<void> serveCustomer() async {
    while (true) {
      if (queue.isNotEmpty) {
        Customer customer;
        if (schedulingAlgorithm == 'SJF') {
          customer = (queue.toList()
                ..sort((a, b) => a.serviceTime.compareTo(b.serviceTime)))
              .first;
          queue.remove(customer);
        } else if (schedulingAlgorithm == 'RR') {
          customer = queue.removeFirst();
        } else {
          customer = queue.removeFirst();
        }

        customer.startTime = DateTime.now();
        print('Customer ${customer.id} is in Teller $id');
        _isBusy = true;
        await Future.delayed(Duration(seconds: customer.serviceTime));
        customer.endTime = DateTime.now();
        _isBusy = false;
        print('Customer ${customer.id} leaves the Teller $id');
      } else {
        await Future.delayed(Duration(milliseconds: 100));
      }
    }
  }
}

class BankSimulation {
  final int queueMaxSize = 10;
  final List<Customer> customers = [];
  final List<Teller> tellers = [];
  final String schedulingAlgorithm;
  final Queue<Customer> queue = Queue<Customer>();
  bool simulationRunning = true;

  BankSimulation(this.schedulingAlgorithm) {
    for (int i = 0; i < 3; i++) {
      tellers.add(Teller(i + 1, queue, schedulingAlgorithm));
    }
  }

  Future<void> generateCustomers() async {
    int customerId = 1;
    while (simulationRunning) {
      if (queue.length < queueMaxSize) {
        Customer newCustomer = Customer(customerId++);
        queue.add(newCustomer);
        print('Customer ${newCustomer.id} enters the Queue');
        customers.add(newCustomer);
        await Future.delayed(Duration(seconds: Random().nextInt(3) + 1));
      } else {
        print('Queue is FULL.');
        await Future.delayed(Duration(seconds: 1));
      }
    }
  }

  Future<void> start(String algorithm) async {
    Timer(Duration(seconds: 30), () {
      simulationRunning = false;
    });

    generateCustomers();
    tellers.forEach((teller) {
      teller.serveCustomer();
    });

    await Future.delayed(Duration(seconds: 30));

    _calculateAndExportMetrics(algorithm);
  }

  void _calculateAndExportMetrics(String algorithm) {
    double totalTurnaroundTime = 0;
    double totalWaitingTime = 0;
    double totalResponseTime = 0;

    for (var customer in customers) {
      if (customer.endTime != null) {
        var turnaroundTime =
            customer.endTime!.difference(customer.arrivalTime).inSeconds;
        var waitingTime =
            customer.startTime!.difference(customer.arrivalTime).inSeconds;
        var responseTime =
            customer.startTime!.difference(customer.arrivalTime).inSeconds;

        totalTurnaroundTime += turnaroundTime;
        totalWaitingTime += waitingTime;
        totalResponseTime += responseTime;
      }
    }

    int servedCustomers = customers.where((c) => c.endTime != null).length;

    double avgTurnaroundTime = totalTurnaroundTime / servedCustomers;
    double avgWaitingTime = totalWaitingTime / servedCustomers;
    double avgResponseTime = totalResponseTime / servedCustomers;

    final metricsFile = File('${algorithm}_metrics.txt');
    metricsFile
        .writeAsStringSync('Average Turnaround Time: $avgTurnaroundTime\n');
    metricsFile.writeAsStringSync('Average Waiting Time: $avgWaitingTime\n',
        mode: FileMode.append);
    metricsFile.writeAsStringSync('Average Response Time: $avgResponseTime\n',
        mode: FileMode.append);

    print('Metrics exported to ${algorithm}_metrics.txt');
  }
}

void main() async {
  print("Select Scheduling Algorithm:");
  print("1. First-Come-First-Serve (FCFS)");
  print("2. Shortest Job First (SJF)");
  print("3. Round Robin (RR)");

  int choice = int.parse(stdin.readLineSync() ?? '1'); //user ko input read
  String algorithm;

  switch (choice) {
    case 1:
      algorithm = 'FCFS';
      algorithm = 'FCFS';
      break;
    case 2:
      algorithm = 'SJF';
      break;
    case 3:
      algorithm = 'RR';
      break;
    default:
      print("Invalid choice. Defaulting to FCFS.");
      algorithm = 'FCFS';
  }

  BankSimulation bankSimulation = BankSimulation(algorithm);
  await bankSimulation.start(algorithm);
}
