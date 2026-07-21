# Operating System Algorithm Simulator

A desktop application that visualizes core Operating System concepts through interactive simulations. The simulator allows users to understand and compare different OS algorithms including Process Management, CPU Scheduling, Memory Management, Disk Scheduling, File Management, and Page Replacement using a graphical interface built with Python and Tkinter.

# Requirements
- Python 3.8 or above
- Tkinter (included with most Python installations)

If Tkinter is unavailable:
```bash
pip install tkinter
```

# Quick Start

Run the application using:

```bash
python main.py
```
# Modules
# Process Management
- Create Process
- Execute Process
- Terminate Process
- Process State Visualization
- CPU Scheduling
- First Come First Serve (FCFS)
- Shortest Job First (SJF)
- Priority Scheduling
- Round Robin (RR)

# Features:

- Waiting Time
- Turnaround Time
- Completion Time
- Gantt Chart Visualization
  
# Memory Management
- First Fit
- Best Fit
- Worst Fit

# Features:
- Memory Block Allocation
- Free Memory Visualization
- Memory Utilization Statistics
 
# Disk Scheduling
- FCFS
- SSTF
- SCAN
- C-SCAN
- LOOK
- C-LOOK

# Features:
- Disk Head Movement
- Total Seek Distance
- Seek Sequence Visualization
  
# File Management
- Contiguous Allocation
- Linked Allocation
- Indexed Allocation

# Features:
- Block Allocation Visualization
- Storage Layout
- Allocation Comparison

# Page Replacement
Algorithms:
- FIFO (First In First Out)
- LRU (Least Recently Used)
- Optimal (Belady's Algorithm)
- Basic Page Replacement

# Features:
- Page Fault Counter
- Page Hit Counter
- Frame Visualization
- Step-by-Step Simulation
- Compare All Algorithms
- Adjustable Playback Speed
- Quick Setup Example

# Project Structure
```bash
OS_Sim/
│
├── main.py
├── theme.py
├── cpu_scheduling.py
├── memory_management.py
├── disk_scheduling.py
├── process_manager.py
├── file_management.py
├── page_replacement.py
├── utils.py
├── test_simulator.py
└── README.md
```

# Documentation
This simulator demonstrates the practical implementation of major Operating System algorithms.

Each module contains:
- User input section
- Algorithm selection
- Interactive visualization
- Performance metrics
- Simulation results

 # Preparation Points
# Understand the Logic
Every module demonstrates how an Operating System makes decisions in different scenarios.

Examples:

- CPU decides which process executes first.
- Memory decides where to allocate processes.
- Disk decides the order of servicing requests.
- Page Replacement decides which page should leave memory.
- File Management decides how files are stored.
- Process Management demonstrates process creation and execution.
  
# Know the Metrics
# CPU Scheduling

Waiting Time
```bash
Waiting Time = Turnaround Time − Burst Time
```

Turnaround Time
```bash
Turnaround Time = Completion Time − Arrival Time
```

Average Waiting Time
```bash
Sum of Waiting Times / Number of Processes
```
# Disk Scheduling
Seek Time
```bash
Seek Time = Total Head Movement
```

# Page Replacement

Page Fault

A requested page is not found in memory.

Page Hit

A requested page is already available in memory.

# Memory Management
Memory Utilization
```bash
Allocated Memory / Total Memory
```

# Explain Trade-Offs
# CPU Scheduling

FCFS
- Easy to implement
- May suffer from Convoy Effect

SJF
- Minimum average waiting time
- Can cause starvation

Priority
- High-priority tasks execute first
- Low-priority tasks may starve

Round Robin
- Fair CPU allocation
- Context switching overhead

#Memory Management
First Fit
- Fast allocation
- Can create fragmentation

Best Fit
- Minimizes unused memory
- Slower search

Worst Fit
- Leaves large free blocks
- Poor memory utilization
- 
#Disk Scheduling

FCFS
- Simple
- Large seek time

SSTF
- Lower seek time
- Starvation possible

SCAN
- Fair service
- More predictable

C-SCAN
- Uniform waiting time
- Better for heavy workloads

LOOK
- Avoids unnecessary head movement

C-LOOK
- More efficient than C-SCAN
  
# Page Replacement

FIFO
- Simple implementation
- May suffer from Belady's Anomaly

LRU
- Better performance
- Requires tracking page usage

Optimal
- Produces minimum page faults
- Impossible to implement in real operating systems because future references are unknown

Basic Page Replacement
- Easy to understand
- Demonstrates fundamental page replacement concepts
  
# Use Examples

The simulator provides:
- Manual Input
- Quick Setup Example
- Interactive Simulations
- Visualization of each algorithm

Users can compare different algorithms using the same input to observe performance differences.

# Technical Details
# Technologies Used

Language:
- Python 3.8+

GUI Framework:
- Tkinter

Libraries:
- tkinter
- ttk
- collections
- time
- math

# Design Principles
- Modular Architecture
- Object-Oriented Programming
- Clean and Readable Code
- Interactive GUI
- Educational Visualization
- Reusable Components
- Easy to Extend

# Code Structure
- GUI separated from algorithm logic
- Individual module for each Operating System concept
- Object-oriented implementation
- Reusable utility functions
- Consistent application theme

 # Customization
# Adding a New CPU Scheduling Algorithm
1. Add the algorithm in cpu_scheduling.py.
2. Update the algorithm selection menu.
3. Display the calculated metrics.
4. Update visualization if required.

# Adding a New Page Replacement Algorithm
1. Add the algorithm function in page_replacement.py.
2. Include it in the algorithm selection list.
3. Update the comparison feature.
4. Display page faults, page hits, and frame visualization.

# Visualizations
- Gantt Chart → cpu_scheduling.py
- Memory Allocation → memory_management.py
- Disk Head Movement → disk_scheduling.py
- File Allocation → file_management.py
- Process Table → process_manager.py
- Page Frame Animation → page_replacement.py

# Known Limitations
- Supports educational simulations only; not a real Operating System.
- Visualizations are step-based and intended for learning.
- Large input sizes may reduce GUI readability.
- Configurations cannot be saved or loaded.
Real hardware-level Operating System operations are not implem
