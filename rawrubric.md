## Kernel/OS Functionality Scoring Rubric

This rubric defines a **standardised metric** for evaluating how well a software repository implements core **kernel** and **operating‑system (OS)** primitives. It is based on the function manifest and status report from the Echo.Kern project and draws on general operating‑system principles ([Wikipedia: Kernel](https://en.wikipedia.org/wiki/Kernel_(operating_system)#:~:text=operating%20system%20%20that%20always,for%20the%20central%20processing%20unit)). The goal is to provide a repeatable method for scoring any repository – regardless of its intended purpose – so we can measure whether it contains kernel/OS functionality and how complete those features are relative to the expectations of an AGI‑ready kernel.

## 1 Design principles

1. **Use a canonical feature list.** The rubric draws on the 10 core kernel primitives identified in the Echo.OCC evaluation (boot/init, scheduling, process management, memory management, interrupt handling, system calls, basic I/O, synchronisation primitives, timers/clock and protection/privilege separation) ([Wikipedia: Kernel](https://en.wikipedia.org/wiki/Kernel_(operating_system)#:~:text=operating%20system%20%20that%20always,for%20the%20central%20processing%20unit)). These are supplemented with platform‑level OS services (virtual memory, device drivers, filesystem, networking, inter‑process communication, security subsystems, power management and profiling) found in the Echo.Kern function manifest ([Wikipedia: Kernel](https://en.wikipedia.org/wiki/Kernel_(operating_system)#:~:text=operating%20system%20%20that%20always,for%20the%20central%20processing%20unit)) and status report.
2. **Weight by importance.** Each feature is assigned a weight reflecting its criticality. Core kernel primitives receive higher weights than platform features. Within the core, boot/initialisation and CPU scheduling carry the highest weight because no kernel can operate without them, while timers/clock have a lower weight. Platform services receive moderate weights because they are needed for a full OS but not to boot a minimal kernel.
3. **Measure both presence and completeness.** A repository may expose some primitives but only partially implement them. To capture this nuance, each category's score is the product of:
	- **Presence:** whether any evidence of the feature exists (binary or graded by textual/functional evidence).
	- **Completeness:** how fully that feature is implemented. The manifest and status report define functions and target SLOC; the fraction of those present in the repository determines completeness. If the repository implements 3 of 10 required functions in a category, completeness is 0.30.
	- **Weight:** the category's importance multiplier.
4. **Total scores normalised to 100.** Kernel and OS scores are normalised separately. A high kernel score indicates the repository contains significant kernel primitives; a low score suggests it is application‑level or "other".

## 2 Kernel primitives and weights

The table below lists the **core kernel primitives**, summarises evidence to look for, and assigns a **weight** (total weight&nbsp;=&nbsp;60). The evidence column suggests keywords or files one might search for in a repository. The target number of functions is taken from the Echo.Kern manifest and status report ([Wikipedia: Kernel](https://en.wikipedia.org/wiki/Kernel_(operating_system)#:~:text=operating%20system%20%20that%20always,for%20the%20central%20processing%20unit)); these numbers provide the basis for the completeness ratio.

| Primitive | Weight | Evidence/keywords | Manifest target | Manifest functions | Notes |
| --- | --- | --- | --- | --- | --- |
| **Boot / initialisation** | **10** | files like `boot.c`, `stage0_bootstrap`, `init_membranes`, assembly boot code | 12 functions (~5 k SLOC) | `boot_init`, `stage0_bootstrap`, `stage1_init`, `init_cpu`, `init_memory_early`, `init_gdt`, `init_idt_early`, `load_kernel_image`, `parse_multiboot`, `setup_initial_page_tables`, `enable_paging`, `jump_to_kernel` | Must bring CPU/memory to known state ([Wikipedia: Kernel](https://en.wikipedia.org/wiki/Kernel_(operating_system)#:~:text=operating%20system%20%20that%20always,for%20the%20central%20processing%20unit)). |
| **CPU scheduling** | **9** | `scheduler.c`, `sched_*` functions, context switch routines | 18 functions (~8 k SLOC) | `sched_init`, `sched_tick`, `schedule`, `context_switch`, `pick_next_task`, `enqueue_task`, `dequeue_task`, `set_task_priority`, `get_current_task`, `yield_cpu`, `sleep`, `wake_up`, `round_robin_schedule`, `priority_schedule`, `init_runqueue`, `add_to_runqueue`, `remove_from_runqueue`, `update_task_runtime` | Includes tick handler and runqueue management ([Wikipedia: Kernel](https://en.wikipedia.org/wiki/Kernel_(operating_system)#:~:text=operating%20system%20%20that%20always,for%20the%20central%20processing%20unit)). |
| **Process/thread management** | **8** | functions to create/destroy processes/threads, `fork`, `spawn`, `thread_init` | 24 functions (~10 k SLOC) | `process_create`, `process_destroy`, `process_fork`, `process_exec`, `process_wait`, `process_exit`, `process_kill`, `thread_create`, `thread_destroy`, `thread_join`, `thread_detach`, `get_process_by_pid`, `get_thread_by_tid`, `init_pcb`, `init_tcb`, `clone_address_space`, `setup_user_stack`, `setup_kernel_stack`, `copy_process_context`, `free_process_resources`, `zombie_cleanup`, `orphan_process_reparent`, `signal_process`, `deliver_signal` | May overlap with scheduler; presence of thread structures and context management. |
| **Memory management** | **8** | `malloc`, `memory.c`, `alloc_page`, `free`, hypergraph allocator | 24 functions (~12 k SLOC) | `kmalloc`, `kfree`, `vmalloc`, `vfree`, `alloc_page`, `free_page`, `alloc_pages`, `free_pages`, `get_free_page`, `__get_free_pages`, `slab_create`, `slab_destroy`, `slab_alloc`, `slab_free`, `kmem_cache_create`, `kmem_cache_destroy`, `kmem_cache_alloc`, `kmem_cache_free`, `init_memory_manager`, `register_memory_region`, `split_page_block`, `merge_page_blocks`, `get_page_stats`, `dump_memory_map` | Basic heap/stack plus virtual memory support ([Wikipedia: Kernel](https://en.wikipedia.org/wiki/Kernel_(operating_system)#:~:text=operating%20system%20%20that%20always,for%20the%20central%20processing%20unit)). |
| **Interrupt handling &amp; traps** | **6** | `interrupt.c`, `vector_table`, `IRQ_handler`, trap stubs | 15 functions (~6 k SLOC) | `init_interrupts`, `register_interrupt_handler`, `unregister_interrupt_handler`, `do_irq`, `irq_handler`, `exception_handler`, `setup_idt`, `load_idt`, `enable_interrupts`, `disable_interrupts`, `save_interrupt_state`, `restore_interrupt_state`, `handle_page_fault`, `handle_div_by_zero`, `handle_general_protection_fault` | Handles hardware interrupts and synchronous faults. |
| **System call interface** | **5** | `syscalls.c`, syscall table, ABI entry points | 32 functions (~10 k SLOC) | `syscall_init`, `syscall_handler`, `sys_read`, `sys_write`, `sys_open`, `sys_close`, `sys_fork`, `sys_exec`, `sys_exit`, `sys_wait`, `sys_kill`, `sys_getpid`, `sys_getppid`, `sys_sbrk`, `sys_mmap`, `sys_munmap`, `sys_ioctl`, `sys_stat`, `sys_fstat`, `sys_lseek`, `sys_chdir`, `sys_getcwd`, `sys_mkdir`, `sys_rmdir`, `sys_unlink`, `sys_pipe`, `sys_dup`, `sys_dup2`, `sys_signal`, `sys_sigaction`, `sys_sleep`, `register_syscall` | Gateway between user mode and kernel services ([Wikipedia: Kernel](https://en.wikipedia.org/wiki/Kernel_(operating_system)#:~:text=operating%20system%20%20that%20always,for%20the%20central%20processing%20unit)). |
| **Basic I/O primitives** | **5** | `io.c`, device register access, `read/write` low‑level operations, HALs | 20 functions (~7 k SLOC) | `io_init`, `inb`, `inw`, `inl`, `outb`, `outw`, `outl`, `io_read`, `io_write`, `io_read_buffer`, `io_write_buffer`, `mmio_read`, `mmio_write`, `port_map`, `port_unmap`, `console_init`, `console_putc`, `console_puts`, `console_getc`, `tty_write` | Minimal means to talk to devices or hardware ports. |
| **Low‑level synchronisation** | **4** | `spinlock`, `mutex`, `atomic`, `barrier` functions, lock structs | 16 functions (~4 k SLOC) | `spinlock_init`, `spinlock_acquire`, `spinlock_release`, `mutex_init`, `mutex_lock`, `mutex_unlock`, `mutex_trylock`, `semaphore_init`, `semaphore_wait`, `semaphore_signal`, `atomic_read`, `atomic_write`, `atomic_inc`, `atomic_dec`, `barrier`, `memory_barrier` | Required for safe concurrency. |
| **Timers and clock** | **3** | `timer.c`, tick counter, `clock_gettime`, scheduling quantum | 10 functions (~3 k SLOC) | `timer_init`, `timer_interrupt`, `get_ticks`, `set_timer`, `cancel_timer`, `sleep_ticks`, `clock_gettime`, `clock_settime`, `rtc_read`, `rtc_write` | Provides timekeeping and periodic interrupts. |
| **Protection / privilege separation** | **2** | `mmu`, `protect`, `privilege`, `user/kernel mode switch` | 14 functions (~6 k SLOC) | `mmu_init`, `set_privilege_level`, `switch_to_user_mode`, `switch_to_kernel_mode`, `check_user_access`, `validate_user_pointer`, `copy_from_user`, `copy_to_user`, `protect_kernel_memory`, `tlb_flush`, `tlb_flush_entry`, `get_current_privilege`, `enable_memory_protection`, `disable_memory_protection` | Ensures isolation and privilege boundaries. |

### Scoring calculation for a primitive

For each primitive i, calculate:

```
score_i = weight_i × presence_i × completeness_i
```

Functions can be counted using static analysis: search for function prototypes matching names in the manifest or measure lines of code in relevant files. If static analysis isn't available, approximate completeness by the proportion of required sub‑modules present (e.g., if `scheduler.c` exists but `sched_policy.c` and `scheduler.h` are missing, completeness&nbsp;≈&nbsp;⅓). Sum all `score_i` across the 10 primitives. Finally, normalise the kernel score:

```
kernel_score = (Σ score_i / 60) × 100
```

## 3 Operating‑system (platform) services

Beyond the core kernel, a full operating system offers higher‑level services. These categories use lower weights (total weight = 40) and can be scored similarly. A high OS score indicates the repository contains substantial platform code (drivers, filesystems, networking, etc.).

| Service | Weight | Evidence/keywords | Manifest target | Manifest functions | Notes |
| --- | --- | --- | --- | --- | --- |
| **Virtual memory / paging** | **8** | `page_table`, `virtual memory`, `mmu`, `paging.c` | ~28 functions (~15 k SLOC) | `vmm_init`, `create_page_table`, `destroy_page_table`, `map_page`, `unmap_page`, `map_pages`, `unmap_pages`, `get_physical_address`, `handle_page_fault`, `alloc_page_table`, `free_page_table`, `clone_page_table`, `setup_kernel_paging`, `setup_user_paging`, `flush_tlb`, `flush_tlb_single`, `mark_page_present`, `mark_page_writable`, `mark_page_user`, `mark_page_executable`, `get_page_flags`, `set_page_flags`, `allocate_virtual_range`, `free_virtual_range`, `map_physical_memory`, `identity_map`, `copy_on_write_handler`, `swap_out_page` | Implements address translation and memory protection. |
| **Device driver framework** | **8** | `driver`, `register_driver`, bus abstractions, HAL stubs | ~35 functions (~20 k SLOC) | `driver_init`, `register_driver`, `unregister_driver`, `probe_device`, `remove_device`, `init_device`, `shutdown_device`, `suspend_device`, `resume_device`, `driver_open`, `driver_close`, `driver_read`, `driver_write`, `driver_ioctl`, `register_bus`, `unregister_bus`, `scan_bus`, `match_driver_device`, `bind_driver`, `unbind_driver`, `get_driver_by_name`, `get_device_by_id`, `allocate_device_resource`, `free_device_resource`, `request_irq`, `free_irq`, `dma_alloc`, `dma_free`, `dma_map`, `dma_unmap`, `create_device_node`, `remove_device_node`, `driver_sysfs_add`, `driver_sysfs_remove`, `hal_init` | Framework for attaching devices; includes neuromorphic HAL ([Wikipedia: Kernel](https://en.wikipedia.org/wiki/Kernel_(operating_system)#:~:text=operating%20system%20%20that%20always,for%20the%20central%20processing%20unit)). |
| **Filesystem / VFS** | **7** | `fs.c`, `vfs`, `open`, `read/write`, inode structures | ~42 functions (~25 k SLOC) | `vfs_init`, `register_filesystem`, `unregister_filesystem`, `mount`, `unmount`, `vfs_open`, `vfs_close`, `vfs_read`, `vfs_write`, `vfs_lseek`, `vfs_stat`, `vfs_fstat`, `vfs_mkdir`, `vfs_rmdir`, `vfs_unlink`, `vfs_rename`, `vfs_link`, `vfs_symlink`, `vfs_readlink`, `vfs_chmod`, `vfs_chown`, `alloc_inode`, `free_inode`, `read_inode`, `write_inode`, `dirty_inode`, `delete_inode`, `alloc_dentry`, `free_dentry`, `lookup_dentry`, `create_file`, `delete_file`, `truncate_file`, `get_super_block`, `put_super_block`, `sync_filesystem`, `get_filesystem_stats`, `path_walk`, `resolve_path`, `canonicalize_path`, `check_permission`, `update_access_time` | A virtual file system layer over a hypergraph FS. |
| **Networking stack** | **5** | `socket`, `network.c`, `tcp`, `udp`, driver glue | ~58 functions (~35 k SLOC) | `net_init`, `socket_create`, `socket_bind`, `socket_listen`, `socket_accept`, `socket_connect`, `socket_send`, `socket_recv`, `socket_sendto`, `socket_recvfrom`, `socket_close`, `socket_shutdown`, `socket_setsockopt`, `socket_getsockopt`, `packet_receive`, `packet_transmit`, `eth_init`, `eth_send`, `eth_receive`, `arp_init`, `arp_lookup`, `arp_resolve`, `arp_update`, `ip_init`, `ip_send`, `ip_receive`, `ip_forward`, `ip_fragment`, `ip_reassemble`, `icmp_init`, `icmp_send`, `icmp_receive`, `udp_init`, `udp_send`, `udp_receive`, `udp_checksum`, `tcp_init`, `tcp_send`, `tcp_receive`, `tcp_connect`, `tcp_accept`, `tcp_close`, `tcp_retransmit`, `tcp_ack`, `tcp_checksum`, `route_init`, `route_add`, `route_delete`, `route_lookup`, `netif_init`, `netif_register`, `netif_unregister`, `netif_up`, `netif_down`, `skb_alloc`, `skb_free`, `skb_clone`, `protocol_register` | May be absent in embedded kernels. |
| **Inter‑process communication (IPC)** | **4** | `message_queue`, `pipe`, `signal`, `psystem_membranes` | ~18 functions (~10 k SLOC) | `ipc_init`, `pipe_create`, `pipe_read`, `pipe_write`, `pipe_close`, `mqueue_create`, `mqueue_destroy`, `mqueue_send`, `mqueue_receive`, `shm_create`, `shm_attach`, `shm_detach`, `shm_destroy`, `signal_send`, `signal_handler_set`, `signal_pending`, `psystem_membrane_init`, `psystem_membrane_transport` | Includes message passing and P‑system membranes. |
| **Security subsystems** | **3** | `crypto`, `authentication`, `capability`, `attestation` | ~30 functions (~18 k SLOC) | `security_init`, `capability_init`, `capability_check`, `capability_grant`, `capability_revoke`, `authenticate_user`, `authenticate_process`, `check_access`, `audit_log`, `crypto_init`, `hash_data`, `verify_hash`, `encrypt_data`, `decrypt_data`, `generate_key`, `sign_data`, `verify_signature`, `attestation_init`, `attest_boot`, `attest_code`, `verify_attestation`, `create_secure_channel`, `credential_create`, `credential_verify`, `selinux_init`, `selinux_check`, `apparmor_init`, `apparmor_check`, `acl_check`, `acl_set` | Includes cryptographic attestation used in Stage0 boot ([Wikipedia: Kernel](https://en.wikipedia.org/wiki/Kernel_(operating_system)#:~:text=operating%20system%20%20that%20always,for%20the%20central%20processing%20unit)). |
| **Power management** | **3** | `power.c`, `sleep`, `wake`, energy budgets | ~22 functions (~12 k SLOC) | `power_init`, `set_power_state`, `get_power_state`, `suspend_system`, `resume_system`, `hibernate`, `shutdown`, `reboot`, `cpu_idle`, `cpu_freq_set`, `cpu_freq_get`, `device_suspend`, `device_resume`, `pm_register_device`, `pm_unregister_device`, `battery_status`, `ac_adapter_status`, `thermal_monitor`, `set_sleep_state`, `wake_event_register`, `power_budget_init`, `power_budget_update` | Optional for embedded or research kernels. |
| **Profiling &amp; debug** | **2** | `profiler.c`, `trace`, `debug`, performance counters | ~25 functions (~15 k SLOC) | `profiler_init`, `profiler_start`, `profiler_stop`, `profiler_sample`, `profiler_report`, `trace_init`, `trace_event`, `trace_function_enter`, `trace_function_exit`, `trace_print`, `kprobe_init`, `kprobe_register`, `kprobe_unregister`, `ftrace_init`, `ftrace_enable`, `ftrace_disable`, `perf_counter_init`, `perf_counter_read`, `perf_counter_reset`, `debug_init`, `debug_print`, `stack_trace`, `memory_dump`, `register_dump`, `breakpoint_set` | Tools to monitor and tune performance. |

Compute each service's score with the same formula as core primitives and normalise to obtain an **OS score** (0–100). When calculating the completeness ratio, use the target SLOC from the manifest or status report as the denominator; count SLOC in the repository's corresponding modules as the numerator.

## 4 Classification and interpretation

After computing **kernel\_score** and **os\_score**, classify the repository:

| Classification | Criteria | Interpretation |
| --- | --- | --- |
| **Kernel‑grade** | kernel\_score ≥ 60; os\_score &gt; 40 | Contains substantial core primitives and enough platform code to act as a standalone or research kernel. |
| **Kernel‑prototype** | 30 ≤ kernel\_score &lt; 60 | Implements some core primitives but is missing critical parts; may be a research experiment or early prototype. |
| **OS‑platform** | kernel\_score &lt; 30 and os\_score ≥ 50 | Lacks kernel primitives but provides platform services (e.g., drivers, filesystems) on top of an existing kernel. |
| **Application / other** | kernel\_score &lt; 30 and os\_score &lt; 50 | Primarily user‑space code or unrelated library; not a kernel or OS. |

These thresholds can be adjusted to suit specific evaluation goals. For AGI‑OS readiness, a repository should aim for kernel\_score ≥ 70 and os\_score ≥ 70.

## 5 How to apply this rubric

1. **Extract manifest and status data.** Use the Echo.Kern function manifest and status report as the canonical list of required functions. For each category, note the target functions/SLOC ([Wikipedia: Kernel](https://en.wikipedia.org/wiki/Kernel_(operating_system)#:~:text=operating%20system%20%20that%20always,for%20the%20central%20processing%20unit)). Update this list as the kernel evolves.
2. **Analyse the repository.** Use static analysis tools or manual inspection to identify files and functions that match each category. Count matching functions or SLOC to estimate completeness. Searching for keywords and comparing function prototypes is a practical starting point.
3. **Compute per‑category scores.** Determine presence (0, 0.5, 1) and completeness ratio, multiply by the weight and sum across categories. Normalise to derive kernel and OS scores.
4. **Interpret results.** Use the classification table to determine whether the repository behaves like a kernel, an OS platform, an application, or something else. Document which features are present and which are missing to guide integration efforts.

## 6 Example

Suppose repository **X** contains a `scheduler.c` with three scheduling functions, a `memory.c` with a simple allocator, and a `syscalls.c` exposing five basic system calls. It lacks boot code and interrupt handlers. Presence scores for scheduling, memory management and system calls are 1 (evidence exists); completeness for those categories might be 3/18 = 0.17, 1/24 = 0.04 and 5/32 = 0.16 respectively. Scores would be:

```makefile
Boot = 10 × 0 × 0 = 0
Scheduling = 9 × 1 × 0.17 ≈ 1.53
Process mgmt = 8 × 0 × 0 = 0 (absent)
Memory mgmt = 8 × 1 × 0.04 ≈ 0.32
Interrupts = 6 × 0 × 0 = 0
Syscalls = 5 × 1 × 0.16 ≈ 0.80
I/O = 5 × 0 × 0 = 0
Synchronisation = 4 × 0 × 0 = 0
Timers = 3 × 0 × 0 = 0
Protection = 2 × 0 × 0 = 0
Total core score = 1.53 + 0.32 + 0.80 = 2.65
kernel_score = 2.65 / 60 × 100 ≈ 4.4 (very low)
```

The OS‑level categories would likely also score near zero. **X** would therefore classify as *application/other* (contains fragments of kernel logic but not enough to be considered a kernel).

## 7 Extending the rubric

The rubric can be refined by:

- **Adding sub‑weights within categories** based on the manifest's priority (critical/high/medium/low). For example, within the scheduler category, context switching functions may receive higher weight than secondary scheduling policies. This allows more granular scoring.
- **Incorporating runtime tests.** Beyond static analysis, use automated tests to validate functional behaviour (e.g., does the scheduler enforce time‑slicing? does memory allocation protect against overlaps?). Pass/fail outcomes could adjust completeness scores.
- **Customising for domains.** If evaluating research kernels for neuromorphic computing, emphasise ESN reservoir and P‑system primitives (from the Echo.Kern manifest) or include extension categories from the manifest's "Extensions" section, adjusting the weights accordingly.

## 8 Conclusion

By anchoring the evaluation to a clear taxonomy of kernel and OS primitives ([Wikipedia: Kernel](https://en.wikipedia.org/wiki/Kernel_(operating_system)#:~:text=operating%20system%20%20that%20always,for%20the%20central%20processing%20unit)) and using weighted scores to reflect presence and completeness, this rubric provides a comprehensive and quantitative method to assess repositories for their suitability as AGI‑OS kernels or platforms. The rubric is flexible and can evolve as new primitives emerge, ensuring that evaluations remain aligned with the state‑of‑the‑art.

---

For additional details, see also: [rubric-kern-os-plat.docx](rubric-kern-os-plat.docx).
