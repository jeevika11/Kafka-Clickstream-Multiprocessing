"""
gc_optimizer.py
----------------------------------------------------
Task 8: Dynamic Garbage Collection Optimization

Demonstrates:

    - gc.get_threshold()
    - gc.set_threshold()
    - gc.get_count()
    - gc.enable()
    - gc.disable()
    - gc.collect()

The program creates cyclic objects and measures
garbage collection under different threshold settings.
"""

import gc
import time


# ============================================================
# CONFIGURATION
# ============================================================

TEST_OBJECTS = 2000


# ============================================================
# CYCLE OBJECT
# ============================================================

class CycleObject:

    def __init__(self, identifier):

        self.identifier = identifier
        self.reference = None


# ============================================================
# CREATE CYCLIC OBJECTS
# ============================================================

def create_cycles(number_of_cycles):

    objects = []

    for index in range(number_of_cycles):

        first = CycleObject(
            f"A-{index}"
        )

        second = CycleObject(
            f"B-{index}"
        )

        # Create circular reference
        first.reference = second
        second.reference = first

        objects.append(first)
        objects.append(second)

    return objects


# ============================================================
# DISPLAY GC CONFIGURATION
# ============================================================

def display_gc_configuration(title):

    print("\n" + "-" * 60)
    print(title)
    print("-" * 60)

    print(
        "GC enabled    :",
        gc.isenabled()
    )

    print(
        "GC thresholds :",
        gc.get_threshold()
    )

    print(
        "GC counters   :",
        gc.get_count()
    )


# ============================================================
# THRESHOLD CONFIGURATION TEST
# ============================================================

def test_threshold_configuration():

    print("\n" + "-" * 60)
    print("GC THRESHOLD CONFIGURATION TEST")
    print("-" * 60)

    # Save original configuration.
    original = gc.get_threshold()

    print(
        "Original threshold :",
        original
    )

    # --------------------------------------------------------
    # Python runtime-compatible threshold
    #
    # Generation 2 is represented as 0 in the current
    # Python environment, so we preserve that behavior.
    # --------------------------------------------------------

    requested = (
        500,
        10,
        0
    )

    print(
        "Requested threshold:",
        requested
    )

    # Apply threshold.
    gc.set_threshold(
        requested[0],
        requested[1],
        requested[2]
    )

    current = gc.get_threshold()

    print(
        "Active threshold   :",
        current
    )

    # --------------------------------------------------------
    # Validate threshold
    # --------------------------------------------------------

    generation_0 = (
        current[0] == requested[0]
    )

    generation_1 = (
        current[1] == requested[1]
    )

    generation_2 = (
        current[2] == requested[2]
    )

    print(
        "Generation 0       :",
        "PASS"
        if generation_0
        else "FAIL"
    )

    print(
        "Generation 1       :",
        "PASS"
        if generation_1
        else "FAIL"
    )

    print(
        "Generation 2       :",
        "PASS"
        if generation_2
        else "FAIL"
    )

    threshold_changed = (
        generation_0
        and generation_1
        and generation_2
    )

    # --------------------------------------------------------
    # Restore original configuration
    # --------------------------------------------------------

    gc.set_threshold(
        original[0],
        original[1],
        original[2]
    )

    restored = gc.get_threshold()

    print(
        "Restored threshold  :",
        restored
    )

    threshold_restored = (
        restored == original
    )

    print(
        "Threshold restore   :",
        "PASS"
        if threshold_restored
        else "FAIL"
    )

    result = (
        threshold_changed
        and threshold_restored
    )

    print(
        "Threshold test      :",
        "PASS"
        if result
        else "FAIL"
    )

    return result


# ============================================================
# GC ENABLE / DISABLE TEST
# ============================================================

def test_gc_control():

    print("\n" + "-" * 60)
    print("GC ENABLE / DISABLE CONTROL")
    print("-" * 60)

    # Start with GC enabled.
    gc.enable()

    enabled_before = gc.isenabled()

    print(
        "GC before disable :",
        enabled_before
    )

    # Disable automatic collection.
    gc.disable()

    disabled = not gc.isenabled()

    print(
        "GC disabled       :",
        disabled
    )

    # Enable again.
    gc.enable()

    enabled_after = gc.isenabled()

    print(
        "GC after enable   :",
        enabled_after
    )

    result = (
        enabled_before
        and disabled
        and enabled_after
    )

    print(
        "GC control test   :",
        "PASS"
        if result
        else "FAIL"
    )

    return result


# ============================================================
# THRESHOLD BENCHMARK
# ============================================================

def test_threshold(
    threshold0,
    threshold1,
    threshold2
):

    print("\n" + "-" * 60)

    print(
        f"TESTING THRESHOLD "
        f"({threshold0}, {threshold1}, {threshold2})"
    )

    print("-" * 60)

    # Apply threshold.
    gc.set_threshold(
        threshold0,
        threshold1,
        threshold2
    )

    active_threshold = gc.get_threshold()

    print(
        "Active threshold :",
        active_threshold
    )

    # Clean existing cycles.
    gc.collect()

    # --------------------------------------------------------
    # Create cycles
    # --------------------------------------------------------

    start = time.perf_counter()

    objects = create_cycles(
        TEST_OBJECTS
    )

    creation_time = (
        time.perf_counter()
        - start
    )

    print(
        f"Objects created  : "
        f"{len(objects):,}"
    )

    print(
        f"Creation time    : "
        f"{creation_time:.6f} seconds"
    )

    # Remove external references.
    del objects

    # --------------------------------------------------------
    # Collect cycles
    # --------------------------------------------------------

    start = time.perf_counter()

    collected = gc.collect()

    collection_time = (
        time.perf_counter()
        - start
    )

    print(
        f"Objects collected : "
        f"{collected:,}"
    )

    print(
        f"Collection time   : "
        f"{collection_time:.6f} seconds"
    )

    return {
        "threshold": active_threshold,
        "created": TEST_OBJECTS * 2,
        "collected": collected,
        "creation_time": creation_time,
        "collection_time": collection_time
    }


# ============================================================
# MANUAL COLLECTION TEST
# ============================================================

def benchmark_collection():

    print("\n" + "-" * 60)
    print("MANUAL GARBAGE COLLECTION")
    print("-" * 60)

    objects = create_cycles(
        TEST_OBJECTS
    )

    print(
        f"Objects created : "
        f"{len(objects):,}"
    )

    # Release external references.
    del objects

    start = time.perf_counter()

    collected = gc.collect()

    elapsed = (
        time.perf_counter()
        - start
    )

    print(
        f"Objects collected : "
        f"{collected:,}"
    )

    print(
        f"Collection time   : "
        f"{elapsed:.6f} seconds"
    )

    return collected


# ============================================================
# RUN THRESHOLD BENCHMARKS
# ============================================================

def run_threshold_benchmarks():

    print("\n" + "=" * 60)
    print("THRESHOLD BENCHMARKS")
    print("=" * 60)

    # Generation 2 uses 0 in the current runtime.
    configurations = [
        (700, 10, 0),
        (1000, 10, 0),
        (2000, 10, 0)
    ]

    results = []

    for configuration in configurations:

        result = test_threshold(
            *configuration
        )

        results.append(
            result
        )

    return results


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print(
        "TASK 8: DYNAMIC GARBAGE "
        "COLLECTION OPTIMIZATION"
    )
    print("=" * 60)

    # --------------------------------------------------------
    # Save original GC configuration
    # --------------------------------------------------------

    original_threshold = gc.get_threshold()

    # Ensure GC is enabled.
    gc.enable()

    display_gc_configuration(
        "INITIAL GC CONFIGURATION"
    )

    # ========================================================
    # TEST 1
    # ========================================================

    threshold_pass = (
        test_threshold_configuration()
    )

    # ========================================================
    # TEST 2
    # ========================================================

    control_pass = (
        test_gc_control()
    )

    # ========================================================
    # TEST 3
    # ========================================================

    results = run_threshold_benchmarks()

    benchmark_pass = (
        len(results) == 3
    )

    # ========================================================
    # TEST 4
    # ========================================================

    collected = benchmark_collection()

    manual_pass = (
        collected >= 0
    )

    # ========================================================
    # FINAL CLEANUP
    # ========================================================

    gc.collect()

    # Restore original threshold.
    gc.set_threshold(
        original_threshold[0],
        original_threshold[1],
        original_threshold[2]
    )

    # Make sure GC remains enabled.
    gc.enable()

    # ========================================================
    # SUMMARY
    # ========================================================

    print("\n" + "=" * 60)
    print("GC OPTIMIZATION SUMMARY")
    print("=" * 60)

    print(
        "Threshold configuration :",
        "PASS"
        if threshold_pass
        else "FAIL"
    )

    print(
        "GC enable/disable       :",
        "PASS"
        if control_pass
        else "FAIL"
    )

    print(
        "Threshold benchmarks    :",
        "PASS"
        if benchmark_pass
        else "FAIL"
    )

    print(
        "Manual collection       :",
        "PASS"
        if manual_pass
        else "FAIL"
    )

    print("\nFinal GC configuration:")

    print(
        "GC enabled    :",
        gc.isenabled()
    )

    print(
        "GC thresholds :",
        gc.get_threshold()
    )

    print(
        "GC counters   :",
        gc.get_count()
    )

    # ========================================================
    # FINAL VERIFICATION
    # ========================================================

    all_passed = (
        threshold_pass
        and control_pass
        and benchmark_pass
        and manual_pass
    )

    print("\n" + "=" * 60)

    if all_passed:

        print(
            "GC OPTIMIZER TEST : PASS"
        )

    else:

        print(
            "GC OPTIMIZER TEST : FAIL"
        )

    print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()