"""
serializer.py
----------------------------------------------------
Task 6: Binary Column Serializer

Stores columnar data in contiguous binary memory using:

    - struct
    - bytearray
    - explicit byte offsets

Numeric columns are stored as fixed-width binary values.

Categorical columns are stored using dictionary IDs.
"""

import struct


class ColumnSerializer:

    def __init__(self):

        # Main contiguous binary memory
        self.buffer = bytearray()

        # Metadata for each column
        self.columns = {}

    # ========================================================
    # NUMERIC COLUMN
    # ========================================================

    def add_numeric_column(
        self,
        name,
        values,
        fmt="<d"
    ):
        """
        Serialize a numeric column.

        Default format:
            <d = little-endian float64
        """

        start_offset = len(self.buffer)

        item_size = struct.calcsize(fmt)

        for value in values:

            self.buffer.extend(
                struct.pack(
                    fmt,
                    value
                )
            )

        end_offset = len(self.buffer)

        self.columns[name] = {
            "type": "numeric",
            "format": fmt,
            "item_size": item_size,
            "count": len(values),
            "start": start_offset,
            "end": end_offset
        }

    # ========================================================
    # INTEGER COLUMN
    # ========================================================

    def add_integer_column(
        self,
        name,
        values
    ):
        """
        Serialize integer values as 64-bit integers.
        """

        start_offset = len(self.buffer)

        fmt = "<q"
        item_size = struct.calcsize(fmt)

        for value in values:

            self.buffer.extend(
                struct.pack(
                    fmt,
                    int(value)
                )
            )

        end_offset = len(self.buffer)

        self.columns[name] = {
            "type": "integer",
            "format": fmt,
            "item_size": item_size,
            "count": len(values),
            "start": start_offset,
            "end": end_offset
        }

    # ========================================================
    # DICTIONARY-ENCODED COLUMN
    # ========================================================

    def add_dictionary_column(
        self,
        name,
        encoded_values
    ):
        """
        Store dictionary IDs as unsigned 32-bit integers.
        """

        start_offset = len(self.buffer)

        fmt = "<I"
        item_size = struct.calcsize(fmt)

        for value in encoded_values:

            self.buffer.extend(
                struct.pack(
                    fmt,
                    int(value)
                )
            )

        end_offset = len(self.buffer)

        self.columns[name] = {
            "type": "dictionary",
            "format": fmt,
            "item_size": item_size,
            "count": len(encoded_values),
            "start": start_offset,
            "end": end_offset
        }

    # ========================================================
    # READ SINGLE VALUE
    # ========================================================

    def read_value(
        self,
        column_name,
        index
    ):
        """
        Read one value directly from the bytearray.
        """

        metadata = self.columns[column_name]

        if index < 0 or index >= metadata["count"]:
            raise IndexError(
                "Column index out of range"
            )

        offset = (
            metadata["start"]
            +
            index * metadata["item_size"]
        )

        value = struct.unpack_from(
            metadata["format"],
            self.buffer,
            offset
        )[0]

        return value

    # ========================================================
    # READ COLUMN
    # ========================================================

    def read_column(
        self,
        column_name
    ):
        """
        Decode an entire column.
        """

        metadata = self.columns[column_name]

        values = []

        for index in range(
            metadata["count"]
        ):

            values.append(
                self.read_value(
                    column_name,
                    index
                )
            )

        return values

    # ========================================================
    # SLICE COLUMN
    # ========================================================

    def slice_column(
        self,
        column_name,
        start,
        end
    ):
        """
        Read a slice directly from the binary buffer.

        Example:

            slice_column("amount", 2, 5)

        returns rows 2, 3 and 4.
        """

        metadata = self.columns[column_name]

        start = max(0, start)
        end = min(
            metadata["count"],
            end
        )

        if start >= end:
            return []

        values = []

        for index in range(
            start,
            end
        ):

            values.append(
                self.read_value(
                    column_name,
                    index
                )
            )

        return values

    # ========================================================
    # COLUMN METADATA
    # ========================================================

    def column_info(
        self,
        column_name
    ):
        """
        Return metadata for a column.
        """

        return self.columns[column_name].copy()

    # ========================================================
    # TOTAL MEMORY
    # ========================================================

    def memory_size(self):

        return len(self.buffer)

    # ========================================================
    # DISPLAY STORAGE
    # ========================================================

    def display_layout(self):

        print("\nCOLUMNAR MEMORY LAYOUT")
        print("-" * 60)

        for name, metadata in self.columns.items():

            print(
                f"{name:<15}"
                f"start={metadata['start']:<6} "
                f"end={metadata['end']:<6} "
                f"count={metadata['count']:<5} "
                f"type={metadata['type']}"
            )

        print("-" * 60)

        print(
            f"Total binary memory : "
            f"{len(self.buffer)} bytes"
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("BINARY COLUMN SERIALIZER TEST")
    print("=" * 60)

    serializer = ColumnSerializer()

    # --------------------------------------------------------
    # Example numeric column
    # --------------------------------------------------------

    amounts = [
        500.0,
        300.0,
        650.0,
        200.0,
        800.0
    ]

    serializer.add_numeric_column(
        "amount",
        amounts
    )

    # --------------------------------------------------------
    # Example integer column
    # --------------------------------------------------------

    ids = [
        1,
        2,
        3,
        4,
        5
    ]

    serializer.add_integer_column(
        "id",
        ids
    )

    # --------------------------------------------------------
    # Dictionary encoded category column
    # --------------------------------------------------------

    categories = [
        0,
        1,
        0,
        2,
        1
    ]

    serializer.add_dictionary_column(
        "category",
        categories
    )

    # --------------------------------------------------------
    # Display storage layout
    # --------------------------------------------------------

    serializer.display_layout()

    # --------------------------------------------------------
    # Read values
    # --------------------------------------------------------

    print("\nREAD SINGLE VALUES")

    print(
        "amount[0] :",
        serializer.read_value(
            "amount",
            0
        )
    )

    print(
        "amount[3] :",
        serializer.read_value(
            "amount",
            3
        )
    )

    print(
        "id[2]     :",
        serializer.read_value(
            "id",
            2
        )
    )

    print(
        "category[4] :",
        serializer.read_value(
            "category",
            4
        )
    )

    # --------------------------------------------------------
    # Read columns
    # --------------------------------------------------------

    print("\nFULL COLUMNS")

    print(
        "IDs       :",
        serializer.read_column("id")
    )

    print(
        "Amounts   :",
        serializer.read_column("amount")
    )

    print(
        "Categories:",
        serializer.read_column("category")
    )

    # --------------------------------------------------------
    # Slice query
    # --------------------------------------------------------

    print("\nSLICE QUERY")

    print(
        "Amount rows 1-4:",
        serializer.slice_column(
            "amount",
            1,
            4
        )
    )

    print(
        "ID rows 0-3:",
        serializer.slice_column(
            "id",
            0,
            3
        )
    )

    # --------------------------------------------------------
    # Memory information
    # --------------------------------------------------------

    print("\nTOTAL MEMORY")

    print(
        f"Binary storage: "
        f"{serializer.memory_size()} bytes"
    )

    print("\n" + "=" * 60)
    print("SERIALIZER TEST COMPLETED")
    print("=" * 60)