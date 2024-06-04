void firstFit(List<int> partitions, List<int> processes) {
  List<int> allocation = List.filled(processes.length, -1);

  for (int i = 0; i < processes.length; i++) {
    for (int j = 0; j < partitions.length; j++) {
      if (partitions[j] >= processes[i]) {
        allocation[i] = j;
        partitions[j] -= processes[i];
        break;
      }
    }
  }

  displayMemoryAllocation(partitions, allocation, processes);
}

void bestFit(List<int> partitions, List<int> processes) {
  List<int> allocation = List.filled(processes.length, -1);

  for (int i = 0; i < processes.length; i++) {
    int bestIdx = -1;
    for (int j = 0; j < partitions.length; j++) {
      if (partitions[j] >= processes[i]) {
        if (bestIdx == -1 || partitions[j] < partitions[bestIdx]) {
          bestIdx = j;
        }
      }
    }
    if (bestIdx != -1) {
      allocation[i] = bestIdx;
      partitions[bestIdx] -= processes[i];
    }
  }

  displayMemoryAllocation(partitions, allocation, processes);
}

void worstFit(List<int> partitions, List<int> processes) {
  List<int> allocation = List.filled(processes.length, -1);

  for (int i = 0; i < processes.length; i++) {
    int worstIdx = -1;
    for (int j = 0; j < partitions.length; j++) {
      if (partitions[j] >= processes[i]) {
        if (worstIdx == -1 || partitions[j] > partitions[worstIdx]) {
          worstIdx = j;
        }
      }
    }
    if (worstIdx != -1) {
      allocation[i] = worstIdx;
      partitions[worstIdx] -= processes[i];
    }
  }

  displayMemoryAllocation(partitions, allocation, processes);
}

void displayMemoryAllocation(
    List<int> partitions, List<int> allocation, List<int> processes) {
  for (int i = 0; i < partitions.length; i++) {
    String partitionInfo =
        "Partition ${i + 1} (Remaining Size: ${partitions[i]} KB) -> ";
    if (allocation.contains(i)) {
      int processIndex = allocation.indexOf(i);
      partitionInfo +=
          "Process $processIndex (Size: ${processes[processIndex]} KB)";
    } else {
      partitionInfo += "Free";
    }
    print(partitionInfo);
  }
}

void main() {
  List<int> partitionSizes = [100, 500, 200, 300, 600];
  List<int> processSizes = [212, 417, 112, 426];

  print("First Fit Allocation:");
  List<int> partitionsCopy = List.from(partitionSizes);
  firstFit(partitionsCopy, processSizes);

  print("\nBest Fit Allocation:");
  partitionsCopy = List.from(partitionSizes);
  bestFit(partitionsCopy, processSizes);

  print("\nWorst Fit Allocation:");
  partitionsCopy = List.from(partitionSizes);
  worstFit(partitionsCopy, processSizes);
}
