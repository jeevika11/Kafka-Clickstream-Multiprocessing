# Task 8 – Dynamic Garbage Collection Optimization & Memory Leak Profiler Harness

## 📌 Overview

This project implements a diagnostic memory-management and profiling harness in Python.

The objective is to explore Python's low-level garbage collection mechanisms, trace heap memory allocations, analyze circular references, and identify memory-management issues using built-in and external profiling tools.

The implementation demonstrates:

- Dynamic garbage collection configuration
- Circular reference creation
- Manual garbage collection
- Heap memory tracing
- Memory allocation snapshot comparison
- Object reference graph analysis
- Back-reference detection
- Memory cleanup verification

---

## 🎯 Objective

The main objective of Task 8 is to build a diagnostic monitoring harness capable of:

1. Creating deliberate circular references.
2. Configuring Python's cyclic garbage collector.
3. Measuring garbage collection behavior.
4. Tracking heap memory allocations.
5. Comparing memory snapshots.
6. Inspecting object reference relationships.
7. Detecting and cleaning circular references.
8. Verifying memory cleanup programmatically.

---

## 🛠️ Required Technology Stack

- Python 3.10+
- `gc`
- `tracemalloc`
- `objgraph`

### Standard Library Modules

The following modules are included with Python:

```text
gc
tracemalloc
time
subprocess
sys
os