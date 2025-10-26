# Quick Start Guide

Get started with the Kernel and OS Evaluation System in minutes.

## Installation

No installation required! Just Python 3.6+.

## Basic Usage

### 1. Evaluate a Kernel/OS Codebase

```bash
python3 evaluate.py /path/to/your/kernel/source
```

### 2. View Results

The tool displays results in the console and saves detailed data to `evaluation_results.json`.

### 3. Interpret Scores

- **90-100%**: Production-ready
- **70-89%**: Well-developed
- **50-69%**: Core features present
- **30-49%**: Minimal/educational
- **Below 30%**: Incomplete

## Example Walkthrough

### Step 1: Test with the included example

```bash
cd /path/to/co9n8no
python3 evaluate.py examples/simple_kernel/
```

Expected output:
```
Scanning source directory: examples/simple_kernel/
Found 3 source files

Evaluating kernel primitives...
  boot: 79.7%
  scheduling: 68.0%
  ...

Overall Score: 22.2%
```

### Step 2: Review detailed results

```bash
cat evaluation_results.json
```

or open in your favorite JSON viewer.

### Step 3: Understand what's missing

Look for 0% scores to identify missing components:
- `system_call_interface: 0.0%` → Need to implement syscalls
- `virtual_memory: 0.0%` → Need paging/MMU support

## Common Use Cases

### Evaluate Linux Kernel

```bash
python3 evaluate.py /usr/src/linux
```

### Evaluate Educational Kernel (xv6)

```bash
git clone https://github.com/mit-pdos/xv6-public.git
python3 evaluate.py xv6-public/
```

### Compare Two Implementations

```bash
python3 evaluate.py kernel_v1/ > results_v1.txt
python3 evaluate.py kernel_v2/ > results_v2.txt
diff results_v1.txt results_v2.txt
```

### Custom File Extensions

By default, the tool scans: `.c`, `.h`, `.cpp`, `.cc`, `.s`, `.asm`

To customize, modify the `scan_directory` method in `evaluate.py`:

```python
extensions = ['.c', '.h', '.rs']  # Add Rust files
```

## Understanding the Rubric

### The 10 Kernel Primitives

1. **Boot** - System initialization
2. **Scheduling** - Task scheduling
3. **Process/Thread Management** - Process lifecycle
4. **Memory** - Memory allocation
5. **Interrupt Handling** - IRQ/exception handling
6. **System Call Interface** - User-kernel interface
7. **Basic I/O** - Input/output operations
8. **Synchronisation** - Locks, semaphores
9. **Timers/Clock** - Time management
10. **Protection** - Memory protection, privilege levels

### The 8 OS Services

1. **Virtual Memory** - Paging, MMU
2. **Driver Framework** - Device drivers
3. **Filesystem** - File operations
4. **Networking** - Network stack
5. **IPC** - Inter-process communication
6. **Security** - Access control
7. **Power Management** - ACPI, power saving
8. **Profiling** - Performance analysis

## Customizing the Rubric

### Change Weights

Edit `rubric.json`:

```json
"scheduling": {
  "weight": 20,  // Changed from 15
  ...
}
```

### Add Evidence Cues

```json
"boot": {
  ...
  "evidence_cues": [
    "boot",
    "init",
    "my_custom_boot_function"  // Add your keywords
  ]
}
```

### Adjust Targets

```json
"scheduling": {
  ...
  "target_functions": 30,  // Changed from 20
  "target_sloc": 1200     // Changed from 800
}
```

## Running Tests

Verify the system works correctly:

```bash
python3 test_evaluation.py
```

Expected output:
```
Running tests for kernel evaluation system
======================================================================
Testing rubric structure...
✓ Rubric structure is valid
...
All tests passed! ✓
```

## Troubleshooting

### No source files found

**Problem**: `Found 0 source files`

**Solution**: 
- Check the path is correct
- Ensure directory contains `.c`, `.h`, or other supported files
- Check file permissions

### Low scores despite implementation

**Problem**: Score is 0% but you have the code

**Solution**:
- Check if your code uses standard naming (e.g., `schedule`, `fork`, `malloc`)
- Review evidence cues in `rubric.json`
- Add custom evidence cues for your implementation

### Python errors

**Problem**: Script fails to run

**Solution**:
- Ensure Python 3.6+ is installed: `python3 --version`
- Check file encoding (should be UTF-8)
- Verify `rubric.json` is valid JSON

## Next Steps

1. Read the full [README.md](README.md) for complete documentation
2. Check [METHODOLOGY.md](METHODOLOGY.md) for scoring details
3. Customize the rubric for your needs
4. Evaluate your kernel/OS implementation
5. Use results to guide development

## Support

For questions or issues:
1. Check the documentation files
2. Review the example kernel in `examples/simple_kernel/`
3. Run the test suite to verify installation
4. Examine `evaluation_results.json` for detailed breakdown

---

Happy evaluating! 🚀
