import matplotlib.pyplot as plt

# Read metrics from the file
with open('metrics.txt', 'r') as file:  #metrics wala file read garya
    lines = file.readlines()
    avg_turnaround_time = float(lines[0].split(': ')[1])
    avg_waiting_time = float(lines[1].split(': ')[1])
    avg_response_time = float(lines[2].split(': ')[1])

# Plot the metrics
metrics = ['Average Turnaround Time', 'Average Waiting Time', 'Average Response Time']
values = [avg_turnaround_time, avg_waiting_time, avg_response_time]

plt.bar(metrics, values, color=['blue', 'orange', 'green'])
plt.xlabel('Metrics')
plt.ylabel('Time (seconds)')
plt.title('Bank Simulation Metrics')
plt.show()
