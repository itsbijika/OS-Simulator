# Operating System Algorithm Simulator — Documentation

This document explains the simulator's capabilities, algorithms, UI, and usage. It consolidates the detailed information previously in the README.

## Overview
The simulator is an educational desktop application that demonstrates core Operating System concepts with interactive visuals:
- CPU Scheduling
- Memory Management
- Disk Scheduling
- Process Management

The app is built with Python and Tkinter and is intended for learning, classroom demos, and quick experimentation.

## Installation and Run
Requirements:
- Python 3.8 or later
- Tkinter (included with most Python distributions)

Optional packages:
- See requirements.txt

Run:
```bash
python main.py
```

## Modules and Features

### 1. Process Manager
Interactive process creation and memory mapping.
- Create processes with names and memory sizes
- Live physical memory map visualization
- Terminate processes and observe memory being freed
- Distinguishes system and user processes
- Shows memory addresses and allocation segments

Learning outcomes:
- Variable partitioning and segmentation
- Internal vs external fragmentation
- Process lifecycle and memory allocation

### 2. File System (if present)
Create files with content and observe disk allocation.
- Create files with name, size, and content
- View, read, and delete files
- Visual disk block allocation map per file
- Observe fragmentation and block reuse

Learning outcomes:
- Disk block allocation
- Fragmentation behavior
- File system operations

### 3. OS Dashboard (if present)
Real-time system snapshot.
- CPU, memory, and disk usage indicators
- Process list and uptime
- Auto-refreshing view for demonstration

### 4. CPU Scheduling
Implements classic CPU scheduling algorithms with a Gantt chart:
- FCFS (First Come First Serve)
- SJF (Shortest Job First, non-preemptive)
- Priority (non-preemptive)
- Round Robin (time quantum)

Features:
- Step-by-step execution recorded in a Gantt chart
- Waiting time and turnaround time per process
- Averages across all processes

Usage:
1. Choose an algorithm
2. Add processes (PID, Arrival, Burst, Priority)
3. For Round Robin, set the time quantum
4. Click Simulate to draw the chart and show metrics

Example input:
- P1: Arrival=0, Burst=5, Priority=2
- P2: Arrival=1, Burst=3, Priority=1
- P3: Arrival=2, Burst=8, Priority=3

### 5. Memory Management
Implements variable partition allocation strategies:
- First Fit
- Best Fit
- Worst Fit

Features:
- Add blocks and allocate/deallocate requests
- Color-coded memory blocks and statistics
- Fragmentation indicators and utilization

Usage:
1. Add memory blocks
2. Select allocation algorithm
3. Allocate requests by process and size
4. Deallocate by process ID

### 6. Disk Scheduling
Implements head movement algorithms with a timeline visualization:
- FCFS
- SSTF
- SCAN
- C-SCAN
- LOOK
- C-LOOK

Features:
- Head movement sequence
- Seek sequence and total seek
- Algorithm comparison window (if enabled)

Usage:
1. Set disk size and initial head position
2. Add requests or use Quick Setup
3. Choose algorithm and direction (when applicable)
4. Run simulation to visualize the path and statistics

## Algorithms: Notes and Tradeoffs

### CPU Scheduling
- FCFS: Simple; may cause convoy effect
- SJF: Minimizes average waiting time; may starve long jobs
- Priority: Chooses lowest numeric priority; may starve low-priority jobs
- Round Robin: Fair sharing; overhead depends on time quantum

### Memory Allocation
- First Fit: Fast, may fragment
- Best Fit: Minimizes immediate waste, may increase fragmentation elsewhere
- Worst Fit: Preserves larger holes; may increase fragmentation

### Disk Scheduling
- FCFS: Fair but potentially high seek time
- SSTF: Greedy nearest request; risk of starvation
- SCAN: Elevator to end then reverse
- C-SCAN: Wraps to start; uniform wait times
- LOOK: Reverses at last request rather than disk end
- C-LOOK: Circular LOOK between first/last requests

## Project Structure
```
OS_Sim/
├── main.py                 # Application entry
├── cpu_scheduling.py       # CPU scheduling UI and logic
├── memory_management.py    # Memory allocation UI and logic
├── disk_scheduling.py      # Disk scheduling UI and logic
├── process_manager.py      # Process and memory manager
├── utils.py                # Common utilities
├── test_simulator.py       # Tests
├── QUICKSTART.py           # Helper/quick start script (optional)
├── README.md               # Minimal overview
└── DOCUMENTATION.md        # Detailed docs (this file)
```

## Usage Tips
- Start with small examples to validate behavior
- Use the quick setup buttons where available
- For Round Robin, try different time quantum values
- For disk scheduling, vary direction and head start position
- Observe fragmentation behavior in memory allocation after allocate/deallocate cycles

## Development Notes
- GUI built using Tkinter frames and canvases
- Visualizations use canvas primitives for portability
- The code aims to separate UI setup from algorithm logic where practical

## Testing
- Basic tests live in test_simulator.py (if present)
- Manual testing through the GUI is encouraged for visual validation

## Limitations
- Simulations are pedagogical, not optimized for performance at large scales
- The file system and dashboard features are basic demonstrations
