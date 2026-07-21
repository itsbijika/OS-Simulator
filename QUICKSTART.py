import tkinter as tk
from tkinter import scrolledtext


def show_quick_start():
    root = tk.Tk()
    root.title("OS Simulator - Quick Start Guide")
    root.geometry("700x600")
    
    # Create scrolled text widget
    text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=35,
                                     font=("Courier", 10))
    text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    # Quick start content
    content = """
╔════════════════════════════════════════════════════════════════════════╗
║             OS ALGORITHM SIMULATOR MINIPROJECT - QUICK START GUIDE                  ║
╚════════════════════════════════════════════════════════════════════════╝

🚀 GETTING STARTED
─────────────────────────────────────────────────────────────────────────

1. Launch the application:
   python main.py

2. Select a module:
   - CPU Scheduling
   - Memory Management  
   - Disk Scheduling

3. Follow module-specific instructions below


📊 CPU SCHEDULING MODULE
─────────────────────────────────────────────────────────────────────────

ALGORITHMS:
  • FCFS (First Come First Serve)
  • SJF (Shortest Job First)
  • Priority Scheduling
  • Round Robin

QUICK DEMO:
  1. Select algorithm (try FCFS first)
  2. Add these processes:
     - P1: Arrival=0, Burst=5, Priority=2
     - P2: Arrival=1, Burst=3, Priority=1  
     - P3: Arrival=2, Burst=8, Priority=3
  3. Click "Simulate"
  4. View Gantt chart and metrics

TIPS:
  • For Round Robin, set Time Quantum = 2
  • Lower priority number = Higher priority
  • Watch for average waiting time differences


💾 MEMORY MANAGEMENT MODULE
─────────────────────────────────────────────────────────────────────────

ALGORITHMS:
  • First Fit
  • Best Fit
  • Worst Fit

QUICK DEMO:
  1. Click "Quick Setup (5 blocks)" to create memory blocks
  2. Try allocating these processes:
     - P1: 50 KB
     - P2: 150 KB
     - P3: 80 KB
  3. Compare results with different algorithms
  4. Try deallocating P2 and allocating P4: 100 KB

TIPS:
  • Green blocks = Free memory
  • Red blocks = Allocated memory
  • Watch internal fragmentation values
  • Try same requests with all three algorithms


💿 DISK SCHEDULING MODULE
─────────────────────────────────────────────────────────────────────────

ALGORITHMS:
  • FCFS, SSTF
  • SCAN, C-SCAN
  • LOOK, C-LOOK

QUICK DEMO:
  1. Set Initial Head = 50
  2. Set Disk Size = 200
  3. Click "Quick Setup (Example)" for standard test case
  4. Try FCFS first, then compare with SSTF
  5. Try SCAN with direction = right

TIPS:
  • Graph shows head movement pattern
  • Total seek time = efficiency metric
  • SSTF usually has lowest seek time
  • SCAN/LOOK prevent starvation


🎯 DEMO PREPARATION (VIVA)
─────────────────────────────────────────────────────────────────────────

KEY POINTS TO EXPLAIN:

CPU Scheduling:
  ✓ How does FCFS cause convoy effect?
  ✓ Why SJF minimizes average waiting time?
  ✓ What is the role of time quantum in RR?
  
Memory Management:
  ✓ Difference: Internal vs External fragmentation
  ✓ Best Fit minimizes wasted space - why?
  ✓ When would you use Worst Fit?

Disk Scheduling:
  ✓ Why is FCFS bad for disk I/O?
  ✓ Difference between SCAN and LOOK?
  ✓ Why C-SCAN better than SCAN?


📐 IMPORTANT FORMULAS
─────────────────────────────────────────────────────────────────────────

CPU Scheduling:
  Turnaround Time = Completion Time - Arrival Time
  Waiting Time = Turnaround Time - Burst Time
  
Memory Management:
  Internal Fragmentation = Allocated Block Size - Requested Size
  Utilization = (Allocated Memory / Total Memory) × 100%
  
Disk Scheduling:
  Seek Time = |Current Position - Next Position|
  Total Seek Time = Sum of all seek distances


⚡ KEYBOARD SHORTCUTS
─────────────────────────────────────────────────────────────────────────

  None currently - use mouse/buttons


🐛 TROUBLESHOOTING
─────────────────────────────────────────────────────────────────────────

Problem: Window too small
Solution: Maximize the window or adjust your screen resolution

Problem: Can't add processes
Solution: Ensure all fields have valid numbers

Problem: Simulation shows nothing  
Solution: Make sure you've added processes/blocks/requests first

Problem: Tkinter not found
Solution: Reinstall Python with Tkinter option checked


📚 RECOMMENDED TESTING SCENARIOS
─────────────────────────────────────────────────────────────────────────

CPU Scheduling Test Cases:

Test 1 - Convoy Effect (FCFS):
  P1: AT=0, BT=24    (long process first)
  P2: AT=1, BT=3     (short processes wait)
  P3: AT=2, BT=3

Test 2 - Priority Comparison:
  P1: AT=0, BT=5, Priority=3
  P2: AT=1, BT=3, Priority=1  (highest priority)
  P3: AT=2, BT=8, Priority=2

Test 3 - Round Robin (Quantum=2):
  P1: AT=0, BT=5
  P2: AT=1, BT=4
  P3: AT=2, BT=2
  P4: AT=3, BT=1


Memory Management Test Cases:

Test 1 - All Algorithms Comparison:
  Blocks: 100, 200, 300, 150, 250 KB
  Requests: P1=50, P2=150, P3=80, P4=200, P5=100 KB
  (Try with First/Best/Worst Fit and compare)

Test 2 - Fragmentation Study:
  Blocks: 100, 100, 100, 100 KB
  Requests: P1=50, P2=50, P3=50, P4=50 KB
  (Shows internal fragmentation)


Disk Scheduling Test Cases:

Classic Test (From textbooks):
  Initial Head: 50
  Disk Size: 200
  Requests: 98, 183, 37, 122, 14, 124, 65, 67
  (Try all 6 algorithms and compare seek times)


🎓 LEARNING OBJECTIVES CHECKLIST
─────────────────────────────────────────────────────────────────────────

After using this simulator, you should understand:

□ How different scheduling algorithms affect process wait time
□ Why some algorithms may cause starvation
□ The tradeoff between fairness and efficiency
□ How memory allocation affects fragmentation
□ Why disk scheduling matters for I/O performance
□ How to calculate and interpret performance metrics


💡 BEST PRACTICES
─────────────────────────────────────────────────────────────────────────

1. Start with simple examples (2-3 processes)
2. Use Quick Setup for standard test cases
3. Try same input with different algorithms
4. Note the metrics differences
5. Understand WHY results differ
6. Practice explaining the logic out loud


📞 GETTING HELP
─────────────────────────────────────────────────────────────────────────

1. Read algorithm comments in source code
2. Check README.md for detailed documentation
3. Review OS textbook for algorithm theory
4. Experiment with different inputs


═══════════════════════════════════════════════════════════════════════

Press ESC or click Close to exit this guide and start using the simulator!

Good luck with your OS project! 🎉
═══════════════════════════════════════════════════════════════════════
"""
    
    text.insert(1.0, content)
    text.config(state=tk.DISABLED)  # Make read-only
    
    # Close button
    close_btn = tk.Button(root, text="Close & Start Simulator",
                         command=root.destroy,
                         bg="#3498db", fg="white",
                         font=("Arial", 12, "bold"),
                         cursor="hand2", pady=10)
    close_btn.pack(pady=10)
    
    # Bind ESC key to close
    root.bind('<Escape>', lambda e: root.destroy())
    
    root.mainloop()


if __name__ == "__main__":
    show_quick_start()
    
    # After closing quick start, launch main app
    print("\nLaunching OS Simulator...")
    print("Run: python main.py")
