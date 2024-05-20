import 'dart:io';
import 'dart:math';

class Customer {
  final int id;
  final int serviceTime; // in seconds
  DateTime arrivalTime;
  DateTime? startTime;
  DateTime? endTime;

  Customer(this.id)
      : serviceTime = Random().nextInt(10) + 1,
        arrivalTime = DateTime.now();
}

class Teller {
  final int id;
  final List<Customer> queue;
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
          customer = queue.removeAt(0);
        } else {
          customer = queue.removeAt(0);
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
  final List<Customer> queue = [];
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

  Future<Map<String, double>> start() async {
    await generateCustomers();
    await Future.wait(tellers.map((teller) => teller.serveCustomer()));

    // Calculate metrics
    return _calculateMetrics();
  }

  Map<String, double> _calculateMetrics() {
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

    return {
      'Average Turnaround Time': avgTurnaroundTime,
      'Average Waiting Time': avgWaitingTime,
      'Average Response Time': avgResponseTime,
    };
  }
}

void main() async {
  print("Select Scheduling Algorithm:");
  print("1. First-Come-First-Serve (FCFS)");
  print("2. Shortest Job First (SJF)");
  print("3. Round Robin (RR)");

  int choice = int.parse(stdin.readLineSync() ?? '1');
  String algorithm;

  switch (choice) {
    case 1:
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
  Map<String, double> metrics = await bankSimulation.start();

  // Output HTML with embedded JavaScript for Chart.js
  String htmlContent = '''
  <!DOCTYPE html>
  <html>
  <head>
    <title>Bank Simulation Metrics</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  </head>
  <body>
    <canvas id="turnaroundChart" width="400" height="400"></canvas>
    <canvas id="waitingChart" width="400" height="400"></canvas>
    <canvas id="responseChart" width="400" height="400"></canvas>
    <script>
      var turnaroundChart = new Chart(document.getElementById('turnaroundChart').getContext('2d'), {
          type: 'bar',
          data: {
              labels: ['${algorithm}'],
              datasets: [{
                  label: 'Average Turnaround Time',
                  data: [${metrics['Average Turnaround Time']}],
                  backgroundColor: 'rgba(255, 99, 132, 0.2)',
                  borderColor: 'rgba(255, 99, 132, 1)',
                  borderWidth: 1
              }]
          },
          options: {
              scales: {
                  y: {
                      beginAtZero: true
                  }
              }
          }
      });
      var waitingChart = new Chart(document.getElementById('waitingChart').getContext('2d'), {
          type: 'bar',
          data: {
              labels: ['${algorithm}'],
              datasets: [{
                  label: 'Average Waiting Time',
                  data: [${metrics['Average Waiting Time']}],
                  backgroundColor: 'rgba(54, 162, 235, 0.2)',
                  borderColor: 'rgba(54, 162, 235, 1)',
                  borderWidth: 1
              }]
          },
          options: {
              scales: {
                  y: {
                      beginAt
              y: {
                  beginAtZero: true
              }
          }
      });
      var responseChart = new Chart(document.getElementById('responseChart').getContext('2d'), {
          type: 'bar',
          data: {
              labels: ['${algorithm}'],
              datasets: [{
                  label: 'Average Response Time',
                  data: [${metrics['Average Response Time']}],
                  backgroundColor: 'rgba(75, 192, 192, 0.2)',
                  borderColor: 'rgba(75, 192, 192, 1)',
                  borderWidth: 1
              }]
          },
          options: {
              scales: {
                  y: {
                      beginAtZero: true
                  }
              }
          }
      });
    </script>
  </body>
  </html>
  ''';

  // Write HTML content to a file
  File('bank_simulation_metrics.html').writeAsStringSync(htmlContent);

  print(
      'HTML file with charts generated. Open bank_simulation_metrics.html in a web browser to view the charts.');
}
