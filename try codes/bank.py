import random
import time
import matplotlib.pyplot as plt

class Customer:
    def __init__(self, id):
        self.id = id
        self.service_time = random.randint(1, 10)  # in seconds
        self.arrival_time = time.time()
        self.start_time = None
        self.end_time = None

class Teller:
    def __init__(self, id, queue, scheduling_algorithm):
        self.id = id
        self.queue = queue
        self.scheduling_algorithm = scheduling_algorithm

    def serve_customer(self):
        while True:
            if self.queue:
                if self.scheduling_algorithm == 'SJF':
                    customer = min(self.queue, key=lambda x: x.service_time)
                    self.queue.remove(customer)
                else:
                    customer = self.queue.pop(0)

                customer.start_time = time.time()
                print(f'Customer {customer.id} is in Teller {self.id}')
                time.sleep(customer.service_time)
                customer.end_time = time.time()
                print(f'Customer {customer.id} leaves the Teller {self.id}')
            else:
                time.sleep(0.1)

class BankSimulation:
    def __init__(self, scheduling_algorithm):
        self.queue_max_size = 10
        self.customers = []
        self.tellers = []
        self.scheduling_algorithm = scheduling_algorithm
        self.queue = []

        for i in range(3):
            self.tellers.append(Teller(i + 1, self.queue, self.scheduling_algorithm))

    def generate_customers(self):
        customer_id = 1
        while True:
            if len(self.queue) < self.queue_max_size:
                new_customer = Customer(customer_id)
                self.queue.append(new_customer)
                print(f'Customer {new_customer.id} enters the Queue')
                self.customers.append(new_customer)
                time.sleep(random.randint(1, 3))
                customer_id += 1
            else:
                print('Queue is FULL.')
                time.sleep(1)

    def start(self):
        import threading

        threading.Thread(target=self.generate_customers, daemon=True).start()

        for teller in self.tellers:
            threading.Thread(target=teller.serve_customer, daemon=True).start()

        time.sleep(30)

        self.calculate_and_plot_metrics()

    def calculate_and_plot_metrics(self):
        served_customers = [c for c in self.customers if c.end_time]
        avg_turnaround_time = sum(c.end_time - c.arrival_time for c in served_customers) / len(served_customers)
        avg_waiting_time = sum(c.start_time - c.arrival_time for c in served_customers) / len(served_customers)
        avg_response_time = sum(c.start_time - c.arrival_time for c in served_customers) / len(served_customers)

        labels = ['Average Turnaround Time', 'Average Waiting Time', 'Average Response Time']
        values = [avg_turnaround_time, avg_waiting_time, avg_response_time]

        plt.bar(labels, values, color=['red', 'blue', 'green'])
        plt.ylabel('Time (seconds)')
        plt.title('Bank Simulation Metrics')
        plt.show()

if __name__ == '__main__':
    print("Select Scheduling Algorithm:")
    print("1. First-Come-First-Serve (FCFS)")
    print("2. Shortest Job First (SJF)")
    print("3. Round Robin (RR)")

    choice = int(input() or '1')
    algorithm = {1: 'FCFS', 2: 'SJF', 3: 'RR'}.get(choice, 'FCFS')

    bank_simulation = BankSimulation(algorithm)
    bank_simulation.start()
