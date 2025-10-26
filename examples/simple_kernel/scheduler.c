/*
 * Simple Kernel Scheduler
 * Demonstrates scheduling and context switching
 */

#include <stdint.h>

#define MAX_PROCESSES 64
#define TIMESLICE 10

// Process control block
struct pcb {
    int pid;
    int priority;
    int state;
    uint32_t esp;
    uint32_t ebp;
};

// Scheduler state
static struct pcb process_table[MAX_PROCESSES];
static int current_process = 0;
static int num_processes = 0;

/**
 * Initialize the scheduler
 */
void scheduler_init(void) {
    for (int i = 0; i < MAX_PROCESSES; i++) {
        process_table[i].pid = -1;
        process_table[i].state = 0;
    }
    current_process = 0;
    num_processes = 0;
}

/**
 * Add a process to the scheduler
 */
int schedule_process(int priority) {
    if (num_processes >= MAX_PROCESSES) {
        return -1;
    }
    
    int pid = num_processes;
    process_table[pid].pid = pid;
    process_table[pid].priority = priority;
    process_table[pid].state = 1;  // Ready
    
    num_processes++;
    return pid;
}

/**
 * Round-robin scheduler
 */
void schedule(void) {
    int next = (current_process + 1) % num_processes;
    
    // Find next ready process
    while (process_table[next].state != 1) {
        next = (next + 1) % num_processes;
        if (next == current_process) {
            return;  // No ready processes
        }
    }
    
    if (next != current_process) {
        context_switch(current_process, next);
        current_process = next;
    }
}

/**
 * Context switch between processes
 */
void context_switch(int from, int to) {
    // Save current context
    struct pcb *from_pcb = &process_table[from];
    struct pcb *to_pcb = &process_table[to];
    
    // Switch stack pointers
    uint32_t temp_esp = from_pcb->esp;
    from_pcb->esp = to_pcb->esp;
    to_pcb->esp = temp_esp;
    
    // Switch base pointers
    uint32_t temp_ebp = from_pcb->ebp;
    from_pcb->ebp = to_pcb->ebp;
    to_pcb->ebp = temp_ebp;
}

/**
 * Task switch helper
 */
void task_switch(void) {
    schedule();
}

/**
 * Get current process ID
 */
int get_current_pid(void) {
    return process_table[current_process].pid;
}

/**
 * Set process priority
 */
void set_priority(int pid, int priority) {
    if (pid >= 0 && pid < num_processes) {
        process_table[pid].priority = priority;
    }
}
