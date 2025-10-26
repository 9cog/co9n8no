# Evaluation Rubric Methodology

This document provides detailed information about the kernel and OS evaluation rubric.

## Scoring Methodology

### Component Evaluation

Each kernel primitive and OS service is evaluated using three metrics:

1. **Evidence Score (40% weight)**
   - Searches for evidence cues (keywords) in source code
   - Each occurrence of a cue contributes to the evidence count
   - Normalized formula: `min(100, (total_matches / 10) * 100)`
   - Rationale: 10 keyword matches is considered strong evidence

2. **Function Count Score (30% weight)**
   - Counts function definitions in files containing evidence
   - Formula: `min(100, (found_functions / target_functions) * 100)`
   - Capped at 100% to avoid over-crediting

3. **SLOC Score (30% weight)**
   - Counts source lines of code (excluding comments and blank lines)
   - Formula: `min(100, (found_sloc / target_sloc) * 100)`
   - Capped at 100% to avoid over-crediting

**Component Score** = (Evidence × 0.4) + (Functions × 0.3) + (SLOC × 0.3)

### Category Evaluation

Kernel primitives and OS services are evaluated separately, then combined:

1. **Kernel Primitives Score**
   - Weighted average: `Σ(component_score × weight) / Σ(weight)`
   - Total weight: 115

2. **OS Services Score**
   - Weighted average: `Σ(component_score × weight) / Σ(weight)`
   - Total weight: 100

3. **Overall Score**
   - Simple average: `(kernel_score + os_score) / 2`

## Weight Distribution

### Criticality Levels

Weights are assigned based on criticality:

- **Critical (15)**: Essential for basic OS operation
  - Examples: Scheduling, Process/Thread Management, Virtual Memory, Filesystem
  
- **High (10-13)**: Important for full functionality
  - Examples: Boot, Interrupt Handling, System Calls, Synchronization, Networking
  
- **Medium (8)**: Useful but not essential
  - Examples: Timers/Clock, Power Management
  
- **Low (5)**: Optional/debugging features
  - Examples: Profiling

### Kernel Primitives Weights

| Primitive | Weight | Criticality | Rationale |
|-----------|--------|-------------|-----------|
| Boot | 10 | Critical | Foundation for all operations |
| Scheduling | 15 | Critical | Core to multitasking |
| Process/Thread Management | 15 | Critical | Essential for program execution |
| Memory | 15 | Critical | Required for all operations |
| Interrupt Handling | 12 | High | Hardware interaction foundation |
| System Call Interface | 12 | High | User-kernel communication |
| Basic I/O | 8 | High | Fundamental interaction |
| Synchronisation | 10 | High | Prevents race conditions |
| Timers/Clock | 8 | Medium | Time-based operations |
| Protection | 10 | High | Security and isolation |

**Total: 115**

### OS Services Weights

| Service | Weight | Criticality | Rationale |
|---------|--------|-------------|-----------|
| Virtual Memory | 15 | Critical | Modern memory management |
| Driver Framework | 12 | High | Hardware abstraction |
| Filesystem | 15 | Critical | Persistent storage access |
| Networking | 13 | High | Communication capability |
| IPC | 10 | High | Process communication |
| Security | 12 | Critical | Access control and protection |
| Power Management | 8 | Medium | Energy efficiency |
| Profiling | 5 | Low | Development/debugging aid |

**Total: 100**

## Evidence Cues

Evidence cues are keywords that indicate the presence of a particular primitive or service. They are carefully chosen based on:

1. **Common naming conventions** in kernel development
2. **Standard terminology** from OS literature
3. **Platform-specific keywords** (x86, ARM, etc.)
4. **Function/variable naming patterns**

### Example: Boot Evidence Cues

```json
"evidence_cues": [
  "boot",       // General boot-related code
  "init",       // Initialization functions
  "startup",    // Startup sequences
  "bootloader", // Bootloader code
  "grub",       // GRUB-specific
  "multiboot"   // Multiboot specification
]
```

The tool searches for these as whole words (case-insensitive) to avoid false positives.

## Target Metrics

Target functions and SLOC are based on:

1. **Analysis of reference implementations** (Linux, FreeBSD, xv6)
2. **Complexity requirements** for minimal viable implementation
3. **Industry standards** for kernel components

### Example: Scheduling Targets

```json
"target_functions": 20,  // Based on minimal scheduler implementation
"target_sloc": 800       // Typical for round-robin + priority scheduling
```

Targets are intentionally set at "minimal viable" levels to:
- Not penalize minimal/educational implementations
- Provide meaningful comparison points
- Allow scoring above 100% for comprehensive implementations

## Usage Examples

### Evaluating a Full Kernel

```bash
python3 evaluate.py /path/to/linux/kernel
```

Expected scores for full-featured kernels: 80-100%

### Evaluating an Educational Kernel

```bash
python3 evaluate.py /path/to/xv6
```

Expected scores for educational kernels: 40-70%

### Evaluating a Minimal Kernel

```bash
python3 evaluate.py /path/to/minimal/kernel
```

Expected scores for minimal kernels: 20-40%

## Interpreting Results

### Score Ranges

- **90-100%**: Comprehensive, production-ready implementation
- **70-89%**: Well-developed with most features
- **50-69%**: Functional with core features
- **30-49%**: Minimal/educational implementation
- **10-29%**: Very basic or incomplete
- **0-9%**: Missing or negligible implementation

### Per-Component Analysis

The detailed output shows:
- Which components are strong/weak
- Evidence quality (keyword matches)
- Code quantity (functions/SLOC)
- Specific cues that were/weren't found

This helps identify:
1. **Missing functionality**: 0% scores indicate gaps
2. **Weak areas**: Low scores suggest incomplete implementation
3. **Strengths**: High scores show well-developed areas
4. **Balance**: Compare across primitives/services

## Customization

### Adjusting Weights

Modify weights in `rubric.json` based on your priorities:

```json
"scheduling": {
  "weight": 20,  // Increase if scheduling is more critical
  ...
}
```

### Adding Evidence Cues

Add domain-specific keywords:

```json
"evidence_cues": [
  ...,
  "your_custom_keyword",
  "project_specific_term"
]
```

### Changing Targets

Adjust targets based on your implementation scale:

```json
"target_functions": 30,  // For more complex implementations
"target_sloc": 1200
```

## Limitations

1. **Keyword-based detection**: May miss unconventionally named code
2. **Quantitative focus**: Doesn't evaluate code quality or correctness
3. **SLOC counting**: Simple heuristic, may miscount in complex cases
4. **Function counting**: Regex-based, may not catch all patterns
5. **No semantic analysis**: Doesn't verify actual functionality

## Best Practices

1. **Run on complete codebase**: Include all kernel/OS source
2. **Exclude generated files**: Focus on hand-written code
3. **Use consistent naming**: Follow conventions for better detection
4. **Supplement with manual review**: Use as a starting point, not final judgment
5. **Compare over time**: Track improvements in subsequent versions

## References

- Operating System Concepts (Silberschatz, Galvin, Gagne)
- Modern Operating Systems (Tanenbaum)
- Linux Kernel Development (Robert Love)
- The Design and Implementation of the FreeBSD Operating System
- xv6: A Simple, Unix-like Teaching Operating System
