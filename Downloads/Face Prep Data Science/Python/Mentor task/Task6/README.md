# Task 6 — In-Memory Columnar Database Representation (Apache Arrow-like) from Scratch

## Overview

This project implements an **in-memory columnar database representation from scratch**, inspired by modern columnar analytics storage systems such as Apache Arrow.

The system converts tabular records into separate binary column buffers and stores the data using Python's native `bytearray`. Primitive values are serialized using the `struct` module, while categorical values are compressed using **dictionary encoding**.

The implementation also demonstrates direct access to serialized data using explicit column offsets and performs slice queries directly on raw binary memory.

---

## Objective

The objective of Task 6 is to implement a columnar table representation using low-level Python data structures.

The project demonstrates:

- Column-oriented data representation
- Binary serialization
- Dictionary encoding
- Explicit column offsets
- Raw byte-vector access
- Memory-efficient categorical storage
- Slice queries
- Low-level memory inspection using `ctypes`

---

## Required Technology

- Python 3.10+
- `struct`
- `ctypes`
- Native `bytearray`

The core columnar engine does not require Pandas or NumPy.

---

## Features

### 1. Columnar Storage

Traditional row-oriented data can look like:

```text
ID | Category     | Amount
--------------------------
1  | Electronics  | 500
2  | Furniture    | 300
3  | Electronics  | 650
4  | Groceries    | 200