"""
columnar_engine.py
----------------------------------------------------
Task 6: In-Memory Columnar Database Representation
          (Apache Arrow-like) from Scratch

Features:
    - Columnar data representation
    - Native bytearray storage
    - struct-based binary serialization
    - ctypes memory inspection
    - Dictionary encoding for categorical values
    - Explicit column offsets
    - Raw byte-vector slice queries
    - No Pandas
    - No NumPy
"""

import struct
import ctypes


# ============================================================
# BINARY SERIALIZER
# ============================================================

class BinarySerializer:
    """
    Handles serialization of primitive values into bytearrays.
    """

    def __init__(self):
        self.buffer = bytearray()

    # --------------------------------------------------------
    # Reset
    # --------------------------------------------------------

    def clear(self):
        self.buffer.clear()

    # --------------------------------------------------------
    # Current offset
    # --------------------------------------------------------

    def offset(self):
        return len(self.buffer)

    # --------------------------------------------------------
    # Write integer
    # --------------------------------------------------------

    def write_int32(self, value):
        """
        Store a signed 32-bit integer.
        """
        self.buffer.extend(
            struct.pack("<i", int(value))
        )

    # --------------------------------------------------------
    # Write unsigned integer
    # --------------------------------------------------------

    def write_uint32(self, value):
        """
        Store an unsigned 32-bit integer.
        """
        self.buffer.extend(
            struct.pack("<I", int(value))
        )

    # --------------------------------------------------------
    # Write float
    # --------------------------------------------------------

    def write_float64(self, value):
        """
        Store a 64-bit floating-point value.
        """
        self.buffer.extend(
            struct.pack("<d", float(value))
        )

    # --------------------------------------------------------
    # Write bytes
    # --------------------------------------------------------

    def write_bytes(self, data):
        self.buffer.extend(data)

    # --------------------------------------------------------
    # Read integer
    # --------------------------------------------------------

    def read_int32(self, offset):
        return struct.unpack_from(
            "<i",
            self.buffer,
            offset
        )[0]

    # --------------------------------------------------------
    # Read unsigned integer
    # --------------------------------------------------------

    def read_uint32(self, offset):
        return struct.unpack_from(
            "<I",
            self.buffer,
            offset
        )[0]

    # --------------------------------------------------------
    # Read float
    # --------------------------------------------------------

    def read_float64(self, offset):
        return struct.unpack_from(
            "<d",
            self.buffer,
            offset
        )[0]

    # --------------------------------------------------------
    # Memory size
    # --------------------------------------------------------

    def size(self):
        return len(self.buffer)


# ============================================================
# DICTIONARY ENCODER
# ============================================================

class DictionaryEncoder:
    """
    Dictionary encodes repeated categorical strings.

    Example:

        Electronics -> 0
        Furniture   -> 1
        Groceries   -> 2
    """

    def __init__(self):
        self.dictionary = {}
        self.values = []

    # --------------------------------------------------------
    # Encode one value
    # --------------------------------------------------------

    def encode(self, value):

        value = str(value)

        if value not in self.dictionary:

            index = len(self.values)

            self.dictionary[value] = index
            self.values.append(value)

        return self.dictionary[value]

    # --------------------------------------------------------
    # Decode one index
    # --------------------------------------------------------

    def decode(self, index):

        return self.values[index]

    # --------------------------------------------------------
    # Decode many
    # --------------------------------------------------------

    def decode_all(self, indices):

        return [
            self.decode(index)
            for index in indices
        ]

    # --------------------------------------------------------
    # Dictionary size
    # --------------------------------------------------------

    def size(self):

        return len(self.values)

    # --------------------------------------------------------
    # Serialize dictionary
    # --------------------------------------------------------

    def serialize(self):

        serializer = BinarySerializer()

        for value in self.values:

            encoded = value.encode("utf-8")

            # Store string length
            serializer.write_uint32(
                len(encoded)
            )

            # Store string bytes
            serializer.write_bytes(
                encoded
            )

        return serializer.buffer


# ============================================================
# COLUMN
# ============================================================

class Column:
    """
    Represents one column in the columnar table.
    """

    def __init__(self, name, column_type):

        self.name = name
        self.column_type = column_type

        self.offset = 0
        self.size = 0

        self.values = []


# ============================================================
# COLUMNAR TABLE
# ============================================================

class ColumnarTable:
    """
    Apache Arrow-like columnar representation.

    Every column is stored independently in binary form.
    """

    def __init__(self):

        self.columns = {}

        self.num_rows = 0

        self.memory = bytearray()

        self.column_offsets = {}

        self.dictionary_encoder = DictionaryEncoder()

        self.serializer = BinarySerializer()

    # ========================================================
    # LOAD RECORDS
    # ========================================================

    def load_records(self, records):
        """
        Load row-oriented records into columnar storage.

        Expected format:

            [
                (1, "Electronics", 500.0),
                (2, "Furniture", 300.0),
                ...
            ]
        """

        self.columns = {
            "ID": Column("ID", "int32"),
            "Amount": Column("Amount", "float64"),
            "Category": Column("Category", "dictionary")
        }

        self.num_rows = len(records)

        for record in records:

            record_id = record[0]
            category = record[1]
            amount = record[2]

            self.columns["ID"].values.append(
                int(record_id)
            )

            self.columns["Amount"].values.append(
                float(amount)
            )

            dictionary_index = (
                self.dictionary_encoder.encode(
                    category
                )
            )

            self.columns["Category"].values.append(
                dictionary_index
            )

    # ========================================================
    # SERIALIZE COLUMN
    # ========================================================

    def serialize(self):
        """
        Serialize all columns into one contiguous bytearray.
        """

        self.memory = bytearray()

        self.column_offsets = {}

        # ----------------------------------------------------
        # ID COLUMN
        # ----------------------------------------------------

        id_column = self.columns["ID"]

        id_column.offset = len(self.memory)

        for value in id_column.values:

            self.memory.extend(
                struct.pack(
                    "<i",
                    value
                )
            )

        id_column.size = (
            len(self.memory)
            - id_column.offset
        )

        self.column_offsets["ID"] = (
            id_column.offset
        )

        # ----------------------------------------------------
        # AMOUNT COLUMN
        # ----------------------------------------------------

        amount_column = self.columns["Amount"]

        amount_column.offset = len(self.memory)

        for value in amount_column.values:

            self.memory.extend(
                struct.pack(
                    "<d",
                    value
                )
            )

        amount_column.size = (
            len(self.memory)
            - amount_column.offset
        )

        self.column_offsets["Amount"] = (
            amount_column.offset
        )

        # ----------------------------------------------------
        # CATEGORY COLUMN
        # ----------------------------------------------------

        category_column = self.columns["Category"]

        category_column.offset = len(self.memory)

        for value in category_column.values:

            self.memory.extend(
                struct.pack(
                    "<I",
                    value
                )
            )

        category_column.size = (
            len(self.memory)
            - category_column.offset
        )

        self.column_offsets["Category"] = (
            category_column.offset
        )

        # ----------------------------------------------------
        # Store in serializer as well
        # ----------------------------------------------------

        self.serializer.buffer = bytearray(
            self.memory
        )

        return self.memory

    # ========================================================
    # READ ID
    # ========================================================

    def read_id(self, row_index):

        column = self.columns["ID"]

        offset = (
            column.offset
            + row_index * 4
        )

        return struct.unpack_from(
            "<i",
            self.memory,
            offset
        )[0]

    # ========================================================
    # READ AMOUNT
    # ========================================================

    def read_amount(self, row_index):

        column = self.columns["Amount"]

        offset = (
            column.offset
            + row_index * 8
        )

        return struct.unpack_from(
            "<d",
            self.memory,
            offset
        )[0]

    # ========================================================
    # READ CATEGORY
    # ========================================================

    def read_category(self, row_index):

        column = self.columns["Category"]

        offset = (
            column.offset
            + row_index * 4
        )

        dictionary_index = struct.unpack_from(
            "<I",
            self.memory,
            offset
        )[0]

        return self.dictionary_encoder.decode(
            dictionary_index
        )

    # ========================================================
    # READ CATEGORY INDEX
    # ========================================================

    def read_category_index(self, row_index):

        column = self.columns["Category"]

        offset = (
            column.offset
            + row_index * 4
        )

        return struct.unpack_from(
            "<I",
            self.memory,
            offset
        )[0]

    # ========================================================
    # SLICE QUERY
    # ========================================================

    def slice_rows(self, start, end):
        """
        Query rows directly from raw byte storage.

        No complete table reconstruction is required.
        """

        start = max(0, start)
        end = min(self.num_rows, end)

        result = []

        for row_index in range(start, end):

            result.append(
                (
                    self.read_id(row_index),
                    self.read_category(row_index),
                    self.read_amount(row_index)
                )
            )

        return result

    # ========================================================
    # AMOUNT SLICE
    # ========================================================

    def amount_slice(self, start, end):
        """
        Read only the Amount column from raw bytes.
        """

        start = max(0, start)
        end = min(self.num_rows, end)

        values = []

        column = self.columns["Amount"]

        for row_index in range(start, end):

            offset = (
                column.offset
                + row_index * 8
            )

            value = struct.unpack_from(
                "<d",
                self.memory,
                offset
            )[0]

            values.append(value)

        return values

    # ========================================================
    # ID SLICE
    # ========================================================

    def id_slice(self, start, end):
        """
        Read only the ID column from raw bytes.
        """

        start = max(0, start)
        end = min(self.num_rows, end)

        values = []

        column = self.columns["ID"]

        for row_index in range(start, end):

            offset = (
                column.offset
                + row_index * 4
            )

            value = struct.unpack_from(
                "<i",
                self.memory,
                offset
            )[0]

            values.append(value)

        return values

    # ========================================================
    # CATEGORY SLICE
    # ========================================================

    def category_slice(self, start, end):
        """
        Read only the Category column.
        """

        start = max(0, start)
        end = min(self.num_rows, end)

        values = []

        for row_index in range(start, end):

            values.append(
                self.read_category(row_index)
            )

        return values

    # ========================================================
    # COLUMN INFORMATION
    # ========================================================

    def column_information(self):

        print("\nCOLUMN OFFSETS")
        print("-" * 60)

        for name, column in self.columns.items():

            print(
                f"{name:<15}"
                f"Offset: {column.offset:<10}"
                f"Size: {column.size} bytes"
            )

    # ========================================================
    # DISPLAY FULL COLUMNS
    # ========================================================

    def display_columns(self):

        print("\nFULL COLUMNS")
        print("-" * 60)

        print(
            "IDs        :",
            self.id_slice(
                0,
                self.num_rows
            )
        )

        print(
            "Amounts    :",
            self.amount_slice(
                0,
                self.num_rows
            )
        )

        print(
            "Categories :",
            [
                self.read_category(i)
                for i in range(self.num_rows)
            ]
        )

    # ========================================================
    # DISPLAY RAW MEMORY
    # ========================================================

    def display_memory(self):

        print("\nRAW BINARY MEMORY")
        print("-" * 70)

        total_bytes = len(self.memory)

        print(
            f"Total bytes : {total_bytes}"
        )

        # ----------------------------------------------------
        # ctypes memory address
        # ----------------------------------------------------

        if len(self.memory) > 0:

            buffer_address = ctypes.addressof(
                ctypes.c_char.from_buffer(
                    self.memory
                )
            )

            print(
                f"ctypes buffer address : "
                f"{buffer_address}"
            )

        else:

            print(
                "ctypes buffer address : "
                "Buffer is empty"
            )

        # ----------------------------------------------------
        # First bytes
        # ----------------------------------------------------

        first_bytes = self.memory[
            :min(64, len(self.memory))
        ]

        print("\nFirst bytes:")

        print(
            list(first_bytes)
        )

        print("-" * 70)

    # ========================================================
    # MEMORY SIZE
    # ========================================================

    def memory_size(self):

        return len(self.memory)

    # ========================================================
    # DICTIONARY INFORMATION
    # ========================================================

    def display_dictionary(self):

        print("\nDICTIONARY")

        print("-" * 60)

        for index, value in enumerate(
            self.dictionary_encoder.values
        ):

            print(
                f"{index} -> {value}"
            )

        dictionary_bytes = (
            self.dictionary_encoder.serialize()
        )

        print(
            "\nDictionary size :",
            self.dictionary_encoder.size()
        )

        print(
            "Serialized dictionary size :",
            len(dictionary_bytes),
            "bytes"
        )


# ============================================================
# TEST DATA
# ============================================================

def create_test_data():

    return [
        (1, "Electronics", 500.0),
        (2, "Furniture", 300.0),
        (3, "Electronics", 650.0),
        (4, "Groceries", 200.0),
        (5, "Furniture", 800.0),
        (6, "Electronics", 450.0),
        (7, "Groceries", 125.0),
        (8, "Furniture", 900.0),
        (9, "Electronics", 780.0),
        (10, "Groceries", 100.0)
    ]


# ============================================================
# MAIN TEST
# ============================================================

def main():

    print("=" * 70)
    print(
        "TASK 6: IN-MEMORY COLUMNAR DATABASE"
    )
    print("=" * 70)

    # --------------------------------------------------------
    # Create test records
    # --------------------------------------------------------

    records = create_test_data()

    print(
        f"\nRecords loaded : {len(records)}"
    )

    # --------------------------------------------------------
    # Create table
    # --------------------------------------------------------

    table = ColumnarTable()

    table.load_records(records)

    # --------------------------------------------------------
    # Serialize
    # --------------------------------------------------------

    print("\nSERIALIZING COLUMNAR DATA")
    print("-" * 70)

    table.serialize()

    print(
        "Columnar serialization : PASS"
    )

    # --------------------------------------------------------
    # Display column information
    # --------------------------------------------------------

    table.column_information()

    # --------------------------------------------------------
    # Display dictionary
    # --------------------------------------------------------

    table.display_dictionary()

    # --------------------------------------------------------
    # Display full columns
    # --------------------------------------------------------

    table.display_columns()

    # --------------------------------------------------------
    # Decoded values
    # --------------------------------------------------------

    print("\nDECODED VALUES")
    print("-" * 60)

    for index in range(
        table.num_rows
    ):

        category_index = (
            table.read_category_index(index)
        )

        category = (
            table.read_category(index)
        )

        print(
            f"{category_index} -> {category}"
        )

    # --------------------------------------------------------
    # Slice query
    # --------------------------------------------------------

    print("\nSLICE QUERY")
    print("-" * 60)

    print(
        "Amount rows 1-4 :",
        table.amount_slice(1, 4)
    )

    print(
        "ID rows 0-3     :",
        table.id_slice(0, 3)
    )

    print(
        "Category rows 2-6 :",
        table.category_slice(2, 6)
    )

    # --------------------------------------------------------
    # Full row slice
    # --------------------------------------------------------

    print("\nROW SLICE")
    print("-" * 60)

    rows = table.slice_rows(1, 4)

    for row in rows:

        print(row)

    # --------------------------------------------------------
    # Raw memory
    # --------------------------------------------------------

    table.display_memory()

    # --------------------------------------------------------
    # Memory statistics
    # --------------------------------------------------------

    print("\nTOTAL MEMORY")
    print("-" * 60)

    print(
        f"Binary storage : "
        f"{table.memory_size()} bytes"
    )

    # --------------------------------------------------------
    # Verification
    # --------------------------------------------------------

    expected_amounts = [
        300.0,
        650.0,
        200.0
    ]

    actual_amounts = table.amount_slice(
        1,
        4
    )

    if actual_amounts == expected_amounts:

        print(
            "\nSlice query verification : PASS"
        )

    else:

        print(
            "\nSlice query verification : FAIL"
        )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("COLUMNAR ENGINE TEST COMPLETED")
    print("=" * 70)


# ============================================================
# PROGRAM ENTRY
# ============================================================

if __name__ == "__main__":
    main()