import 'dart:async'; //async function
import 'dart:collection'; // queue
import 'dart:io'; //File system ko lagi
import 'dart:math'; //random number ko lagi

class Customer {
  //final means data type whose value cannot be changed once initialized
  //class name customer
  final int id; //each customer has id
  final int serviceTime; // in seconds //customer lai serve garne time
  DateTime
      arrivalTime; //arrive hune time ra DateTime xai built in function ho for date and time
  DateTime? startTime; //when the service begins
  DateTime? endTime; //service end hune time

  Customer(this.id)
      : serviceTime =
            Random().nextInt(10) + 1, //This is random number between 1 and 10
        arrivalTime =
            DateTime.now(); //arrival time lai aile ko datetime sanga rakheko
}

class Teller {
  //teller ko class
  final int id; //teller id
  final Queue<Customer> queue; //queue
  final String schedulingAlgorithm; //variable paxi used
  bool _isBusy = false;

  Teller(this.id, this.queue, this.schedulingAlgorithm); //constructor

  Future<void> serveCustomer() async {
    //servercustormer function
    while (true) {
      //keeps on running while true
      if (queue.isNotEmpty) {
        //checks if queue is empty or not
        Customer
            customer; //customer class ko object ko customer varible declare gareko
        if (schedulingAlgorithm == 'SJF') {
          customer = (queue.toList() //convert queue to list
                ..sort((a, b) => a.serviceTime.compareTo(
                    b.serviceTime))) //sorting list based on service time
              .first; //sjf ko first leko cuz it has shortest tiem
          queue.remove(customer);
        } else if (schedulingAlgorithm == 'RR') {
          customer = queue.removeFirst(); //first ko lai select gareko
        } else {
          customer = queue.removeFirst();
        }

        customer.startTime = DateTime.now();
        print(
            'Customer ${customer.id} is in Teller $id'); //prints which customer is in which teller
        _isBusy = true; //teller becomes busy
        await Future.delayed(Duration(seconds: customer.serviceTime));
        customer.endTime = DateTime.now();
        _isBusy = false; //after service is completed teller becomes available
        print('Customer ${customer.id} leaves the Teller $id'); //xodeko
      } else {
        await Future.delayed(Duration(milliseconds: 100));
      }
    }
  }
}

class BankSimulation {
  final int queueMaxSize = 10; //queue size
  final List<Customer> customers = []; //customer array
  final List<Teller> tellers = [];
  final String schedulingAlgorithm;
  final Queue<Customer> queue = Queue<Customer>();
  bool simulationRunning = true;

  BankSimulation(this.schedulingAlgorithm) {
    for (int i = 0; i < 3; i++) {
      //3 ta teller
      tellers.add(Teller(i + 1, queue, schedulingAlgorithm));
    }
  }

  Future<void> generateCustomers() async {
    //generate random customer
    int customerId = 1;
    while (simulationRunning) {
      if (queue.length < queueMaxSize) {
        Customer newCustomer =
            Customer(customerId++); //customer ayexi add garne
        queue.add(newCustomer); //like this
        print(
            'Customer ${newCustomer.id} enters the Queue'); //customer queue ma ayo
        customers.add(newCustomer);
        await Future.delayed(Duration(seconds: Random().nextInt(3) + 1));
      } else {
        print('Queue is FULL.');
        await Future.delayed(Duration(seconds: 1));
      }
    }
  }

  Future<void> start() async {
    //bank ko start
    Timer(Duration(seconds: 30), () {
      //30 sec paxi timer stop
      simulationRunning = false;
    });

    generateCustomers(); //customer generate gareko
    tellers.forEach((teller) {
      teller.serveCustomer();
    });

    // we Let the simulation run for a while
    await Future.delayed(Duration(seconds: 30));

    // Stop the simulation and calculate metrics
    _calculateAndExportMetrics();
  }

  void _calculateAndExportMetrics() {
    //export to python to plot graph
    double totalTurnaroundTime = 0; //initial value ZERO, yesma store garne
    double totalWaitingTime = 0;
    double totalResponseTime = 0;

    for (var customer in customers) {
      //customer in list customer
      if (customer.endTime != null) {
        //customer.endtime is not null
        var turnaroundTime = customer.endTime!
            .difference(customer.arrivalTime)
            .inSeconds; //calculates difference betwn end time and arrival
        //time
        var waitingTime =
            customer.startTime!.difference(customer.arrivalTime).inSeconds;
        var responseTime =
            customer.arrivalTime.difference(customer.startTime!).inSeconds;
//tyo store gareko
        totalTurnaroundTime +=
            turnaroundTime; //yo xai total ma each customer ko add gareko
        totalWaitingTime += waitingTime;
        totalResponseTime += responseTime;
      }
    }

    int servedCustomers = customers.where((c) => c.endTime != null).length;

    double avgTurnaroundTime =
        totalTurnaroundTime / servedCustomers; //calculating average
    double avgWaitingTime = totalWaitingTime / servedCustomers;
    double avgResponseTime = totalResponseTime / servedCustomers;

    // yo xai to Write metrics to a file
    final metricsFile = File('metrics.txt');
    metricsFile
        .writeAsStringSync('Average Turnaround Time: $avgTurnaroundTime\n');
    metricsFile.writeAsStringSync('Average Waiting Time: $avgWaitingTime\n',
        mode: FileMode.append);
    metricsFile.writeAsStringSync('Average Response Time: $avgResponseTime\n',
        mode: FileMode.append);

    print('Metrics exported to metrics.txt');
  }
} //simple bujna this function calculates how much time on average customers spend at
// the bank and then writes this information into a file so we can see it later

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
  await bankSimulation.start();
}
