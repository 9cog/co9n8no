# Kernel and OS Platform Services Evaluation System

This repository contains an evaluation rubric and tool for assessing kernel and operating system implementations based on core primitives and platform services.

## Overview

The evaluation system defines:
- **10 core kernel primitives** that form the foundation of any operating system kernel
- **8 OS platform services** that provide higher-level operating system functionality

Each primitive and service has:
- **Weight**: Based on criticality (critical=15, high=12-10, medium=8, low=5)
- **Evidence cues**: Keywords and patterns to look for in code
- **Target metrics**: Expected number of functions and source lines of code (SLOC)

## Kernel Primitives (Total Weight: 115)

### 1. Boot (Weight: 10, Critical)
System initialization and bootloader functionality.
- **Target**: 15 functions, 500 SLOC
- **Evidence cues**: boot, init, startup, bootloader, grub, multiboot

### 2. Scheduling (Weight: 15, Critical)
Process and thread scheduling algorithms.
- **Target**: 20 functions, 800 SLOC
- **Evidence cues**: schedule, scheduler, context_switch, task_switch, round_robin, priority

### 3. Process/Thread Management (Weight: 15, Critical)
Process creation, destruction, and thread management.
- **Target**: 25 functions, 1000 SLOC
- **Evidence cues**: process, thread, fork, exec, exit, wait, kill, pcb, tcb

### 4. Memory (Weight: 15, Critical)
Basic memory allocation and management.
- **Target**: 18 functions, 700 SLOC
- **Evidence cues**: malloc, free, kalloc, kfree, heap, memory_pool, slab

### 5. Interrupt Handling (Weight: 12, High)
Interrupt and exception handling mechanisms.
- **Target**: 20 functions, 600 SLOC
- **Evidence cues**: interrupt, irq, isr, exception, trap, idt, gdt

### 6. System Call Interface (Weight: 12, High)
System call interface and handling.
- **Target**: 30 functions, 900 SLOC
- **Evidence cues**: syscall, system_call, sysenter, int_0x80, syscall_table

### 7. Basic I/O (Weight: 8, High)
Basic input/output operations.
- **Target**: 15 functions, 500 SLOC
- **Evidence cues**: read, write, io, port, inb, outb, console, tty

### 8. Synchronisation (Weight: 10, High)
Synchronization primitives (locks, semaphores, etc.).
- **Target**: 12 functions, 400 SLOC
- **Evidence cues**: lock, unlock, mutex, semaphore, spinlock, atomic, barrier

### 9. Timers/Clock (Weight: 8, Medium)
Timer and clock management.
- **Target**: 10 functions, 350 SLOC
- **Evidence cues**: timer, clock, tick, jiffies, rtc, pit, hpet

### 10. Protection (Weight: 10, High)
Memory protection and privilege levels.
- **Target**: 12 functions, 450 SLOC
- **Evidence cues**: protection, privilege, ring, user_mode, kernel_mode, mmu, tlb

## OS Platform Services (Total Weight: 100)

### 1. Virtual Memory (Weight: 15, Critical)
Virtual memory management and paging.
- **Target**: 25 functions, 1200 SLOC
- **Evidence cues**: vmm, virtual_memory, paging, page_table, page_fault, mmap, swap

### 2. Driver Framework (Weight: 12, High)
Device driver framework and management.
- **Target**: 20 functions, 800 SLOC
- **Evidence cues**: driver, device, probe, register_driver, bus, pci, usb

### 3. Filesystem (Weight: 15, Critical)
Filesystem abstraction and implementation.
- **Target**: 35 functions, 1500 SLOC
- **Evidence cues**: filesystem, vfs, inode, dentry, mount, open, close, stat

### 4. Networking (Weight: 13, High)
Network stack and protocols.
- **Target**: 40 functions, 2000 SLOC
- **Evidence cues**: network, socket, tcp, udp, ip, ethernet, packet, skb

### 5. IPC (Weight: 10, High)
Inter-process communication mechanisms.
- **Target**: 18 functions, 700 SLOC
- **Evidence cues**: ipc, pipe, queue, message, shared_memory, signal

### 6. Security (Weight: 12, Critical)
Security mechanisms and access control.
- **Target**: 22 functions, 900 SLOC
- **Evidence cues**: security, access_control, permission, capability, selinux, apparmor, credential

### 7. Power Management (Weight: 8, Medium)
Power management and ACPI.
- **Target**: 15 functions, 600 SLOC
- **Evidence cues**: power, acpi, suspend, resume, sleep, cpufreq, idle

### 8. Profiling (Weight: 5, Low)
Performance profiling and debugging support.
- **Target**: 12 functions, 400 SLOC
- **Evidence cues**: profile, perf, trace, kprobe, ftrace, debug

## Usage

### Prerequisites
- Python 3.6 or higher
- Source code to evaluate (C/C++/assembly files)

### Running the Evaluation

```bash
python3 evaluate.py <source_directory> [rubric.json]
```

Example:
```bash
python3 evaluate.py /path/to/kernel/source
```

The tool will:
1. Scan the source directory for relevant files (.c, .h, .cpp, .s, .asm)
2. Search for evidence cues in the code
3. Count functions and SLOC in relevant files
4. Calculate scores for each primitive and service
5. Generate an overall evaluation score
6. Save detailed results to `evaluation_results.json`

### Scoring Methodology

For each primitive/service, the tool calculates:

1. **Evidence Score (40% weight)**
   - Based on keyword matches in code
   - Normalized to 100% scale

2. **Function Score (30% weight)**
   - Ratio of found functions to target
   - Capped at 100%

3. **SLOC Score (30% weight)**
   - Ratio of found SLOC to target
   - Capped at 100%

**Overall Component Score** = (Evidence × 0.4) + (Functions × 0.3) + (SLOC × 0.3)

**Final Scores**:
- Kernel Primitives Score: Weighted average based on component weights
- OS Services Score: Weighted average based on component weights
- Overall Score: Average of the two category scores

### Output

The tool produces:
- Console output with detailed breakdown
- `evaluation_results.json` with complete evaluation data

## Customizing the Rubric

Edit `rubric.json` to modify:
- Weights and criticality levels
- Evidence cues (keywords to search for)
- Target functions and SLOC counts
- Add or remove primitives/services

## Example Output

```
Scanning source directory: /path/to/kernel
Found 127 source files

Evaluating kernel primitives...
  boot: 75.3%
  scheduling: 82.1%
  process_thread_management: 78.9%
  ...

Evaluating OS platform services...
  virtual_memory: 68.4%
  driver_framework: 71.2%
  ...

======================================================================
EVALUATION SUMMARY
======================================================================

Kernel Primitives Score: 76.2%
OS Services Score:       65.8%
Overall Score:           71.0%

Total Files Scanned:     127
```

## License

This evaluation framework is provided as-is for educational and assessment purposes.
