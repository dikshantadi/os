import matplotlib.pyplot as plt

def read_metrics(file_path):
    metrics = {}
    with open(file_path, 'r') as file:
        for line in file:
            name, value = line.strip().split(': ')
            metrics[name] = float(value)
    return metrics

# Read metrics from files
fcfs_metrics = read_metrics('FCFS_metrics.txt')
sjf_metrics = read_metrics('SJF_metrics.txt')
rr_metrics = read_metrics('RR_metrics.txt')

# Prepare data for plotting
algorithms = ['FCFS', 'SJF', 'RR']
avg_turnaround_times = [fcfs_metrics['Average Turnaround Time'], sjf_metrics['Average Turnaround Time'], rr_metrics['Average Turnaround Time']]
avg_waiting_times = [fcfs_metrics['Average Waiting Time'], sjf_metrics['Average Waiting Time'], rr_metrics['Average Waiting Time']]
avg_response_times = [fcfs_metrics['Average Response Time'], sjf_metrics['Average Response Time'], rr_metrics['Average Response Time']]

# Plot Average Turnaround Time
plt.figure(figsize=(10, 5))

plt.subplot(1, 3, 1)
plt.bar(algorithms, avg_turnaround_times, color=['blue', 'green', 'red'])
plt.xlabel('Scheduling Algorithm')
plt.ylabel('Average Turnaround Time')
plt.title('Average Turnaround Time')

# Plot Average Waiting Time
plt.subplot(1, 3, 2)
plt.bar(algorithms, avg_waiting_times, color=['blue', 'green', 'red'])
plt.xlabel('Scheduling Algorithm')
plt.ylabel('Average Waiting Time')
plt.title('Average Waiting Time')

# Plot Average Response Time
plt.subplot(1, 3, 3)
plt.bar(algorithms, avg_response_times, color=['blue', 'green', 'red'])
plt.xlabel('Scheduling Algorithm')
plt.ylabel('Average Response Time')
plt.title('Average Response Time')

plt.tight_layout()
plt.show()
