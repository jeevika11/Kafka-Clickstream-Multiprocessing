"""
task8.py
----------------------------------------------------
Task 8: Dynamic Garbage Collection Optimization
& Memory Leak Profiler Harness

Integrates:

    1. memory_leaks.py
    2. gc_optimizer.py
    3. memory_profiler.py
    4. object_graph.py

Required technologies:

    - gc
    - tracemalloc
    - objgraph

The program runs each module independently and
produces a final Task 8 verification summary.
"""

import subprocess
import sys
import os


# ============================================================
# CONFIGURATION
# ============================================================

MODULES = [
    "memory_leaks.py",
    "gc_optimizer.py",
    "memory_profiler.py",
    "object_graph.py"
]


# ============================================================
# RUN MODULE
# ============================================================

def run_module(module_name):

    print("\n" + "=" * 70)

    print(
        f"RUNNING MODULE: {module_name}"
    )

    print("=" * 70)

    try:

        result = subprocess.run(
            [
                sys.executable,
                module_name
            ],
            capture_output=True,
            text=True
        )

        # Display module output.
        print(
            result.stdout
        )

        # Display errors if present.
        if result.stderr:

            print(
                "\nERROR OUTPUT:"
            )

            print(
                result.stderr
            )

        # ----------------------------------------------------
        # Determine result
        # ----------------------------------------------------

        output = result.stdout

        passed = (
            result.returncode == 0
            and
            (
                "TEST : PASS" in output
                or
                "TEST COMPLETED" in output
                or
                "PASS" in output
            )
        )

        return passed

    except Exception as error:

        print(
            f"Error running {module_name}:"
        )

        print(
            error
        )

        return False


# ============================================================
# CHECK REQUIRED FILES
# ============================================================

def check_required_files():

    print("\n" + "=" * 70)
    print("CHECKING TASK 8 FILES")
    print("=" * 70)

    all_exist = True

    for module in MODULES:

        exists = os.path.exists(
            module
        )

        print(
            f"{module:<25}",
            "FOUND"
            if exists
            else "MISSING"
        )

        if not exists:

            all_exist = False

    return all_exist


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print(
        "TASK 8: DYNAMIC GARBAGE COLLECTION "
        "& MEMORY LEAK PROFILER"
    )
    print("=" * 70)

    print(
        "\nPython executable:"
    )

    print(
        sys.executable
    )

    # ========================================================
    # FILE CHECK
    # ========================================================

    files_ready = check_required_files()

    if not files_ready:

        print("\n" + "=" * 70)

        print(
            "TASK 8 VERIFICATION : FAIL"
        )

        print(
            "One or more required modules are missing."
        )

        print("=" * 70)

        return

    # ========================================================
    # RUN ALL MODULES
    # ========================================================

    results = {}

    for module in MODULES:

        results[module] = run_module(
            module
        )

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print("\n" + "=" * 70)
    print("TASK 8 FINAL VERIFICATION")
    print("=" * 70)

    for module, passed in results.items():

        print(
            f"{module:<25}",
            "PASS"
            if passed
            else "FAIL"
        )

    # ========================================================
    # COUNT RESULTS
    # ========================================================

    passed_count = sum(
        results.values()
    )

    total_count = len(
        results
    )

    print("\n" + "-" * 70)

    print(
        f"Tests passed : "
        f"{passed_count}/{total_count}"
    )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    all_passed = (
        passed_count == total_count
    )

    print("\n" + "=" * 70)

    if all_passed:

        print(
            "TASK 8 VERIFICATION : PASS"
        )

        print(
            "All memory-management modules "
            "completed successfully."
        )

    else:

        print(
            "TASK 8 VERIFICATION : FAIL"
        )

        print(
            "Check the failed module above."
        )

    print("=" * 70)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()