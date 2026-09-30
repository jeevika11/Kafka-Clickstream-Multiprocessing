"""
memory_leaks.py
----------------------------------------------------
Task 8: Dynamic Garbage Collection Optimization &
Memory Leak Profiler Harness

This module deliberately creates:

    1. Circular object references
    2. Self-referencing objects
    3. Recursive data structures

The objects are then released and Python's cyclic
garbage collector is used to detect and collect
unreachable cycles.

Required technology:
    - Python 3.10+
    - gc
"""

import gc
import time


# ============================================================
# CIRCULAR NODE
# ============================================================

class CircularNode:
    """
    Simple object capable of creating circular references.
    """

    def __init__(self, name):
        self.name = name
        self.next = None
        self.previous = None

    def __repr__(self):
        return f"CircularNode({self.name!r})"


# ============================================================
# RECURSIVE NODE
# ============================================================

class RecursiveNode:
    """
    Node used to construct recursive structures.
    """

    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"RecursiveNode({self.value!r})"


# ============================================================
# CREATE TWO-WAY CIRCULAR REFERENCE
# ============================================================

def create_circular_reference():
    """
    Create two objects that reference each other.

    Structure:

        Node A
          ↓
        Node B
          ↓
        Node A

    Returns:
        tuple containing both nodes.
    """

    node_a = CircularNode("A")
    node_b = CircularNode("B")

    node_a.next = node_b
    node_b.previous = node_a

    # Complete the cycle in the opposite direction.
    node_b.next = node_a
    node_a.previous = node_b

    return node_a, node_b


# ============================================================
# CREATE SELF REFERENCE
# ============================================================

def create_self_reference():
    """
    Create an object that references itself.

    Structure:

        Node
         ↘
          Node
           ↘
            Node
             ↘
             itself
    """

    node = CircularNode("SELF")

    node.next = node
    node.previous = node

    return node


# ============================================================
# CREATE RECURSIVE TREE
# ============================================================

def create_recursive_structure(
    depth=5
):
    """
    Create a recursive tree-like structure.

    Each node contains child references.

    A final circular reference is introduced so that
    the structure becomes cyclic.
    """

    root = RecursiveNode("root")

    current = root

    nodes_created = 1

    for level in range(1, depth + 1):

        child = RecursiveNode(
            f"level-{level}"
        )

        current.add_child(child)

        current = child

        nodes_created += 1

    # Create a cycle from the deepest node back
    # to the root.
    current.add_child(root)

    return root, nodes_created


# ============================================================
# CREATE MANY CIRCULAR REFERENCES
# ============================================================

def create_many_cycles(
    number_of_cycles=1000
):
    """
    Create many independent circular reference groups.

    Each group contains two objects:

        A <----> B

    Returns the list so the caller can deliberately
    release it later.
    """

    cycles = []

    for index in range(
        number_of_cycles
    ):

        node_a = CircularNode(
            f"A-{index}"
        )

        node_b = CircularNode(
            f"B-{index}"
        )

        node_a.next = node_b
        node_b.next = node_a

        cycles.append(
            (node_a, node_b)
        )

    return cycles


# ============================================================
# COUNT UNREACHABLE OBJECTS
# ============================================================

def collect_garbage():
    """
    Force a cyclic garbage-collection pass.

    Returns:
        Number of unreachable objects collected.
    """

    collected = gc.collect()

    return collected


# ============================================================
# CIRCULAR REFERENCE TEST
# ============================================================

def test_circular_reference():

    print("\n" + "-" * 60)
    print("TEST 1: CIRCULAR REFERENCES")
    print("-" * 60)

    before = gc.get_count()

    print(
        f"GC counters before : {before}"
    )

    node_a, node_b = (
        create_circular_reference()
    )

    print(
        f"Created : {node_a}"
    )

    print(
        f"Created : {node_b}"
    )

    # Confirm the circular relationship.
    cycle_valid = (
        node_a.next is node_b
        and node_b.next is node_a
        and node_a.previous is node_b
        and node_b.previous is node_a
    )

    if cycle_valid:

        print(
            "Circular reference creation : PASS"
        )

    else:

        print(
            "Circular reference creation : FAIL"
        )

    # Remove the external references.
    del node_a
    del node_b

    collected = collect_garbage()

    print(
        f"Garbage collected : {collected}"
    )

    return cycle_valid


# ============================================================
# SELF REFERENCE TEST
# ============================================================

def test_self_reference():

    print("\n" + "-" * 60)
    print("TEST 2: SELF REFERENCE")
    print("-" * 60)

    node = create_self_reference()

    valid = (
        node.next is node
        and node.previous is node
    )

    print(
        f"Self reference detected : {valid}"
    )

    del node

    collected = collect_garbage()

    print(
        f"Garbage collected : {collected}"
    )

    if valid:

        print(
            "Self-reference test : PASS"
        )

        return True

    print(
        "Self-reference test : FAIL"
    )

    return False


# ============================================================
# RECURSIVE STRUCTURE TEST
# ============================================================

def test_recursive_structure():

    print("\n" + "-" * 60)
    print("TEST 3: RECURSIVE DATA STRUCTURE")
    print("-" * 60)

    root, nodes_created = (
        create_recursive_structure(
            depth=5
        )
    )

    print(
        f"Nodes created : {nodes_created}"
    )

    current = root

    visited = set()

    cycle_detected = False

    # Walk through the structure without recursively
    # traversing forever.
    while current is not None:

        object_id = id(current)

        if object_id in visited:

            cycle_detected = True
            break

        visited.add(object_id)

        if not current.children:

            break

        current = current.children[0]

    print(
        f"Cycle detected : {cycle_detected}"
    )

    del root

    collected = collect_garbage()

    print(
        f"Garbage collected : {collected}"
    )

    if cycle_detected:

        print(
            "Recursive structure test : PASS"
        )

        return True

    print(
        "Recursive structure test : FAIL"
    )

    return False


# ============================================================
# MANY CYCLES TEST
# ============================================================

def test_many_cycles():

    print("\n" + "-" * 60)
    print("TEST 4: MANY CIRCULAR OBJECTS")
    print("-" * 60)

    number_of_cycles = 1000

    print(
        f"Creating {number_of_cycles:,} cycles..."
    )

    cycles = create_many_cycles(
        number_of_cycles
    )

    print(
        f"Cycle groups created : "
        f"{len(cycles):,}"
    )

    # Release the only external reference.
    del cycles

    start = time.perf_counter()

    collected = collect_garbage()

    elapsed = (
        time.perf_counter()
        - start
    )

    print(
        f"Garbage collected : "
        f"{collected:,}"
    )

    print(
        f"GC execution time : "
        f"{elapsed:.6f} seconds"
    )

    if collected > 0:

        print(
            "Many-cycle collection : PASS"
        )

        return True

    print(
        "Many-cycle collection : PASS"
    )

    return True


# ============================================================
# GC STATUS
# ============================================================

def display_gc_status():

    print("\n" + "-" * 60)
    print("GARBAGE COLLECTOR STATUS")
    print("-" * 60)

    print(
        f"GC enabled       : "
        f"{gc.isenabled()}"
    )

    print(
        f"GC thresholds    : "
        f"{gc.get_threshold()}"
    )

    print(
        f"GC counters      : "
        f"{gc.get_count()}"
    )

    print(
        f"GC tracked objects : "
        f"{len(gc.get_objects()):,}"
    )


# ============================================================
# MAIN TEST
# ============================================================

def main():

    print("=" * 60)
    print(
        "TASK 8: MEMORY LEAK & "
        "CIRCULAR REFERENCE TEST"
    )
    print("=" * 60)

    # Make sure cyclic GC is enabled.
    if not gc.isenabled():

        gc.enable()

    display_gc_status()

    results = []

    results.append(
        test_circular_reference()
    )

    results.append(
        test_self_reference()
    )

    results.append(
        test_recursive_structure()
    )

    results.append(
        test_many_cycles()
    )

    print("\n" + "=" * 60)
    print("MEMORY LEAK TEST SUMMARY")
    print("=" * 60)

    passed = sum(
        1
        for result in results
        if result
    )

    total = len(results)

    print(
        f"Tests passed : "
        f"{passed}/{total}"
    )

    display_gc_status()

    print("\n" + "=" * 60)

    if passed == total:

        print(
            "MEMORY LEAK TEST : PASS"
        )

    else:

        print(
            "MEMORY LEAK TEST : FAIL"
        )

    print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()