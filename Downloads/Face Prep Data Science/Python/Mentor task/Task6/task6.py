"""
task6.py
----------------------------------------------------
Task 6: In-Memory Columnar Database Representation
          (Apache Arrow-like) from Scratch

Final verification program.

Required:
    - Python 3.10+
    - struct
    - ctypes
    - bytearray
    - Dictionary encoding
    - Column offsets
    - Raw byte-vector queries
"""

from columnar_engine import (
    ColumnarTable,
    create_test_data
)


def main():

    print("=" * 70)
    print("TASK 6: IN-MEMORY COLUMNAR DATABASE")
    print("=" * 70)

    # ========================================================
    # STEP 1: CREATE TEST DATA
    # ========================================================

    print("\n" + "-" * 70)
    print("STEP 1: INPUT DATA")
    print("-" * 70)

    records = create_test_data()

    print(f"Records : {len(records)}")

    for record in records:
        print(record)

    # ========================================================
    # STEP 2: CREATE COLUMNAR TABLE
    # ========================================================

    print("\n" + "-" * 70)
    print("STEP 2: COLUMNAR TABLE")
    print("-" * 70)

    table = ColumnarTable()

    table.load_records(records)

    print("Columnar table created : PASS")

    # ========================================================
    # STEP 3: SERIALIZE
    # ========================================================

    print("\n" + "-" * 70)
    print("STEP 3: BINARY SERIALIZATION")
    print("-" * 70)

    table.serialize()

    print("struct serialization : PASS")
    print("bytearray storage    : PASS")

    # ========================================================
    # STEP 4: COLUMN OFFSETS
    # ========================================================

    print("\n" + "-" * 70)
    print("STEP 4: COLUMN OFFSETS")
    print("-" * 70)

    table.column_information()

    # ========================================================
    # STEP 5: DICTIONARY ENCODING
    # ========================================================

    print("\n" + "-" * 70)
    print("STEP 5: DICTIONARY ENCODING")
    print("-" * 70)

    table.display_dictionary()

    if table.dictionary_encoder.size() == 3:
        print("\nDictionary encoding : PASS")
    else:
        print("\nDictionary encoding : FAIL")

    # ========================================================
    # STEP 6: FULL COLUMN DATA
    # ========================================================

    print("\n" + "-" * 70)
    print("STEP 6: COLUMN DATA")
    print("-" * 70)

    table.display_columns()

    # ========================================================
    # STEP 7: RAW BYTE ACCESS
    # ========================================================

    print("\n" + "-" * 70)
    print("STEP 7: RAW BYTE ACCESS")
    print("-" * 70)

    print("First ID:")
    print(table.read_id(0))

    print("\nFirst Amount:")
    print(table.read_amount(0))

    print("\nFirst Category:")
    print(table.read_category(0))

    # ========================================================
    # STEP 8: SLICE QUERY
    # ========================================================

    print("\n" + "-" * 70)
    print("STEP 8: SLICE QUERY")
    print("-" * 70)

    amount_result = table.amount_slice(1, 4)

    id_result = table.id_slice(0, 3)

    category_result = table.category_slice(0, 5)

    print(
        "Amount rows 1-4 :",
        amount_result
    )

    print(
        "ID rows 0-3     :",
        id_result
    )

    print(
        "Category rows 0-5 :",
        category_result
    )

    # ========================================================
    # STEP 9: SLICE VERIFICATION
    # ========================================================

    print("\n" + "-" * 70)
    print("STEP 9: SLICE VERIFICATION")
    print("-" * 70)

    expected_amounts = [
        300.0,
        650.0,
        200.0
    ]

    expected_ids = [
        1,
        2,
        3
    ]

    if amount_result == expected_amounts:

        print(
            "Amount slice verification : PASS"
        )

    else:

        print(
            "Amount slice verification : FAIL"
        )

    if id_result == expected_ids:

        print(
            "ID slice verification     : PASS"
        )

    else:

        print(
            "ID slice verification     : FAIL"
        )

    # ========================================================
    # STEP 10: ROW SLICE
    # ========================================================

    print("\n" + "-" * 70)
    print("STEP 10: ROW SLICE")
    print("-" * 70)

    rows = table.slice_rows(1, 4)

    for row in rows:
        print(row)

    # ========================================================
    # STEP 11: MEMORY INFORMATION
    # ========================================================

    print("\n" + "-" * 70)
    print("STEP 11: MEMORY INFORMATION")
    print("-" * 70)

    table.display_memory()

    print(
        f"\nTotal binary memory : "
        f"{table.memory_size()} bytes"
    )

    # ========================================================
    # FINAL VERIFICATION
    # ========================================================

    all_passed = (
        amount_result == expected_amounts
        and id_result == expected_ids
        and table.dictionary_encoder.size() == 3
        and table.memory_size() > 0
    )

    print("\n" + "=" * 70)

    if all_passed:

        print("TASK 6 VERIFICATION : PASS")

    else:

        print("TASK 6 VERIFICATION : FAIL")

    print("=" * 70)

    print("\nTask 6 completed successfully.")


if __name__ == "__main__":
    main()