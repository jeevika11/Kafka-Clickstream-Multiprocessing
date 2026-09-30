"""
memory_profiler.py
----------------------------------------------------
Task 8: Dynamic Garbage Collection Optimization
Module: Memory Allocation Profiler

Uses Python's tracemalloc module to:

    - Start memory tracing
    - Measure current and peak memory
    - Capture memory snapshots
    - Compare snapshots
    - Identify top memory allocations
    - Demonstrate allocation growth
    - Release allocated objects
"""

import tracemalloc
import gc
import time


# ============================================================
# CONFIGURATION
# ============================================================

TEST_OBJECTS = 5000


# ============================================================
# MEMORY ALLOCATION FUNCTION
# ============================================================

def create_memory_objects(number_of_objects):

    objects = []

    for index in range(number_of_objects):

        data = {
            "id": index,
            "name": f"object-{index}",
            "values": [
                index,
                index * 2,
                index * 3,
                index * 4
            ]
        }

        objects.append(data)

    return objects


# ============================================================
# DISPLAY MEMORY USAGE
# ============================================================

def display_memory_usage(title):

    current, peak = tracemalloc.get_traced_memory()

    print("\n" + "-" * 60)
    print(title)
    print("-" * 60)

    print(
        f"Current memory : "
        f"{current / 1024:.2f} KB"
    )

    print(
        f"Peak memory    : "
        f"{peak / 1024:.2f} KB"
    )

    return current, peak


# ============================================================
# DISPLAY TOP ALLOCATIONS
# ============================================================

def display_top_allocations(
    snapshot,
    limit=5
):

    print("\n" + "-" * 60)
    print("TOP MEMORY ALLOCATIONS")
    print("-" * 60)

    statistics = snapshot.statistics(
        "lineno"
    )

    if not statistics:

        print(
            "No allocation statistics available."
        )

        return

    for index, statistic in enumerate(
        statistics[:limit],
        start=1
    ):

        print(
            f"{index}. {statistic}"
        )


# ============================================================
# SNAPSHOT COMPARISON
# ============================================================

def compare_snapshots(
    first_snapshot,
    second_snapshot,
    limit=5
):

    print("\n" + "-" * 60)
    print("SNAPSHOT COMPARISON")
    print("-" * 60)

    differences = second_snapshot.compare_to(
        first_snapshot,
        "lineno"
    )

    if not differences:

        print(
            "No memory differences detected."
        )

        return

    for index, difference in enumerate(
        differences[:limit],
        start=1
    ):

        print(
            f"{index}. {difference}"
        )


# ============================================================
# MEMORY PROFILING TEST
# ============================================================

def run_memory_profile():

    print("\n" + "=" * 60)
    print("MEMORY ALLOCATION PROFILING")
    print("=" * 60)

    # --------------------------------------------------------
    # Start tracing
    # --------------------------------------------------------

    tracemalloc.start()

    print(
        "\ntracemalloc tracing :",
        "STARTED"
    )

    # --------------------------------------------------------
    # Initial memory
    # --------------------------------------------------------

    initial_current, initial_peak = (
        display_memory_usage(
            "INITIAL MEMORY"
        )
    )

    # --------------------------------------------------------
    # First snapshot
    # --------------------------------------------------------

    snapshot_before = (
        tracemalloc.take_snapshot()
    )

    # --------------------------------------------------------
    # Create objects
    # --------------------------------------------------------

    start = time.perf_counter()

    objects = create_memory_objects(
        TEST_OBJECTS
    )

    creation_time = (
        time.perf_counter()
        - start
    )

    print(
        f"\nObjects created : "
        f"{len(objects):,}"
    )

    print(
        f"Creation time   : "
        f"{creation_time:.6f} seconds"
    )

    # --------------------------------------------------------
    # Memory after allocation
    # --------------------------------------------------------

    allocated_current, allocated_peak = (
        display_memory_usage(
            "MEMORY AFTER ALLOCATION"
        )
    )

    # --------------------------------------------------------
    # Second snapshot
    # --------------------------------------------------------

    snapshot_after = (
        tracemalloc.take_snapshot()
    )

    # --------------------------------------------------------
    # Display allocation statistics
    # --------------------------------------------------------

    display_top_allocations(
        snapshot_after
    )

    # --------------------------------------------------------
    # Compare snapshots
    # --------------------------------------------------------

    compare_snapshots(
        snapshot_before,
        snapshot_after
    )

    # --------------------------------------------------------
    # Verify allocation increased
    # --------------------------------------------------------

    allocation_increased = (
        allocated_current
        > initial_current
    )

    print("\n" + "-" * 60)

    print(
        "Allocation growth :",
        "PASS"
        if allocation_increased
        else "FAIL"
    )

    # --------------------------------------------------------
    # Release objects
    # --------------------------------------------------------

    del objects

    gc.collect()

    # --------------------------------------------------------
    # Final memory
    # --------------------------------------------------------

    final_current, final_peak = (
        display_memory_usage(
            "MEMORY AFTER CLEANUP"
        )
    )

    # --------------------------------------------------------
    # Stop tracing
    # --------------------------------------------------------

    tracemalloc.stop()

    print(
        "\ntracemalloc tracing :",
        "STOPPED"
    )

    return {
        "initial_current": initial_current,
        "initial_peak": initial_peak,
        "allocated_current": allocated_current,
        "allocated_peak": allocated_peak,
        "final_current": final_current,
        "final_peak": final_peak,
        "allocation_increased": allocation_increased
    }


# ============================================================
# TRACEMALLOC RESET TEST
# ============================================================

def test_tracemalloc_reset():

    print("\n" + "-" * 60)
    print("TRACEMALLOC RESET TEST")
    print("-" * 60)

    tracemalloc.start()

    first_objects = create_memory_objects(
        1000
    )

    current_before_reset, peak_before_reset = (
        tracemalloc.get_traced_memory()
    )

    print(
        f"Memory before reset : "
        f"{current_before_reset / 1024:.2f} KB"
    )

    print(
        f"Peak before reset   : "
        f"{peak_before_reset / 1024:.2f} KB"
    )

    # Clear the first allocation.
    del first_objects

    gc.collect()

    # Reset peak tracking.
    tracemalloc.reset_peak()

    current_after_reset, peak_after_reset = (
        tracemalloc.get_traced_memory()
    )

    print(
        f"Memory after reset  : "
        f"{current_after_reset / 1024:.2f} KB"
    )

    print(
        f"Peak after reset    : "
        f"{peak_after_reset / 1024:.2f} KB"
    )

    reset_pass = (
        peak_after_reset
        >= current_after_reset
    )

    print(
        "Reset operation     :",
        "PASS"
        if reset_pass
        else "FAIL"
    )

    tracemalloc.stop()

    return reset_pass


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print(
        "TASK 8: MEMORY ALLOCATION PROFILER"
    )
    print("=" * 60)

    # --------------------------------------------------------
    # Run profiling
    # --------------------------------------------------------

    profile_result = run_memory_profile()

    profile_pass = (
        profile_result["allocation_increased"]
        and
        profile_result["allocated_peak"]
        >=
        profile_result["allocated_current"]
    )

    # --------------------------------------------------------
    # Test reset functionality
    # --------------------------------------------------------

    reset_pass = (
        test_tracemalloc_reset()
    )

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("MEMORY PROFILER SUMMARY")
    print("=" * 60)

    print(
        "Memory allocation tracking :",
        "PASS"
        if profile_pass
        else "FAIL"
    )

    print(
        "Snapshot analysis          :",
        "PASS"
        if profile_pass
        else "FAIL"
    )

    print(
        "tracemalloc reset          :",
        "PASS"
        if reset_pass
        else "FAIL"
    )

    all_passed = (
        profile_pass
        and reset_pass
    )

    print("\n" + "=" * 60)

    if all_passed:

        print(
            "MEMORY PROFILER TEST : PASS"
        )

    else:

        print(
            "MEMORY PROFILER TEST : FAIL"
        )

    print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()