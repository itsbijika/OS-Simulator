# Operating System Algorithm Simulator

A desktop app to visualize core OS concepts: CPU scheduling, memory management, disk scheduling, and basic process management. Built with Python and Tkinter.

## Requirements
- Python 3.8+
- Tkinter (bundled with most Python installers)

If Tkinter is not available in your Python installation:
```bash
pip install tkinter
```

## Quick Start
```bash
python main.py
```

## Modules
- CPU Scheduling: FCFS, SJF, Priority, Round Robin
- Memory Management: First Fit, Best Fit, Worst Fit
- Disk Scheduling: FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK
- Process Manager: Create/terminate processes with live memory allocation

## Project Structure
```
OS_Sim/
├── main.py
├── cpu_scheduling.py
├── memory_management.py
├── disk_scheduling.py
├── process_manager.py
├── utils.py
├── test_simulator.py
└── README.md
```

## Documentation
See DOCUMENTATION.md for full feature descriptions, algorithm explanations, and usage guides.

### Preparation Points:

1. **Understand the Logic**: Each algorithm is implemented with clear comments
2. **Know the Metrics**: 
   - Waiting Time = Turnaround Time - Burst Time
   - Turnaround Time = Completion Time - Arrival Time
   - Seek Time = Sum of head movements
3. **Explain Tradeoffs**: Discuss advantages and disadvantages
4. **Use Examples**: Quick setup provides good demo data
5. **Show Comparisons**: Run same input on different algorithms

### Common Demo Questions:

**CPU Scheduling:**
- What is convoy effect in FCFS?
- Why might SJF cause starvation?
- When is Round Robin preferred?

**Memory Management:**
- What is internal vs external fragmentation?
- Which fit algorithm minimizes wasted space?
- How to reduce fragmentation?

**Disk Scheduling:**
- Why is FCFS inefficient for disks?
- What's the difference between SCAN and LOOK?
- When is C-SCAN better than SCAN?

## Technical Details

### Technologies Used:
- **Language**: Python 3.7+
- **GUI Framework**: Tkinter
- **Standard Libraries**: time, math, collections

### Design Principles:
- **Modular Architecture**: Each module is independent
- **Clean Code**: Well-commented and readable
- **Educational Focus**: Clarity over complexity
- **Extensible**: Easy to add new algorithms

### Code Structure:
- **Separation of Concerns**: GUI and logic separated
- **Object-Oriented**: Classes for processes, blocks, etc.
- **Deterministic**: Same input produces same output
- **Commented**: Every algorithm has explanation

## Customization

### Adding a New CPU Scheduling Algorithm:

1. Add algorithm function in `cpu_scheduling.py`
2. Follow the pattern of existing algorithms
3. Update the radio button list
4. Add algorithm info to `utils.py`

Example:
```python
def simulate_custom_algorithm(self):
    """Your algorithm implementation"""
    # Calculate schedule
    # Populate self.gantt_data
    # Calculate metrics
    pass
```

### Modifying Visualizations:

All drawing code is in module-specific files:
- Gantt charts: `cpu_scheduling.py` → `draw_gantt_chart()`
- Memory blocks: `memory_management.py` → `draw_memory_visualization()`
- Disk movement: `disk_scheduling.py` → `draw_visualization()`

## Known Limitations

1. **No Animation Speed Control**: Visualizations are instant
2. **Limited to 20 Processes**: For readability in CPU scheduling
3. **Static Disk Size**: Cannot change during simulation
4. **No Save/Load**: Cannot save configurations
