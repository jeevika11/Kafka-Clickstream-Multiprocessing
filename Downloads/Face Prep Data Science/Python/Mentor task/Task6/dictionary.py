"""
dictionary.py
----------------------------------------------------
Task 6: Dictionary Encoding

Implements dictionary encoding for categorical values.

Example:

    Electronics -> 0
    Furniture   -> 1
    Groceries   -> 2

Repeated strings are stored only once in the dictionary.
"""

import struct


class DictionaryEncoder:

    def __init__(self):

        # String -> integer ID
        self.value_to_id = {}

        # Integer ID -> string
        self.id_to_value = []

    # --------------------------------------------------------
    # Encode
    # --------------------------------------------------------

    def encode(self, value):

        if value in self.value_to_id:
            return self.value_to_id[value]

        index = len(self.id_to_value)

        self.value_to_id[value] = index
        self.id_to_value.append(value)

        return index

    # --------------------------------------------------------
    # Decode
    # --------------------------------------------------------

    def decode(self, index):

        return self.id_to_value[index]

    # --------------------------------------------------------
    # Encode multiple values
    # --------------------------------------------------------

    def encode_many(self, values):

        return [
            self.encode(value)
            for value in values
        ]

    # --------------------------------------------------------
    # Dictionary size
    # --------------------------------------------------------

    def size(self):

        return len(self.id_to_value)

    # --------------------------------------------------------
    # Serialize dictionary
    # --------------------------------------------------------

    def serialize(self):

        buffer = bytearray()

        # Number of dictionary values
        buffer.extend(
            struct.pack(
                "<I",
                len(self.id_to_value)
            )
        )

        for value in self.id_to_value:

            encoded = value.encode("utf-8")

            # String length
            buffer.extend(
                struct.pack(
                    "<I",
                    len(encoded)
                )
            )

            # String bytes
            buffer.extend(encoded)

        return buffer

    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    def display(self):

        print("Dictionary:")

        for index, value in enumerate(
            self.id_to_value
        ):

            print(
                f"  {index} -> {value}"
            )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("DICTIONARY ENCODER TEST")
    print("=" * 60)

    encoder = DictionaryEncoder()

    values = [
        "Electronics",
        "Furniture",
        "Electronics",
        "Groceries",
        "Furniture",
        "Electronics"
    ]

    encoded = encoder.encode_many(values)

    print("\nOriginal values:")
    print(values)

    print("\nEncoded values:")
    print(encoded)

    print()

    encoder.display()

    print("\nDecoded values:")

    for index in encoded:

        print(
            index,
            "->",
            encoder.decode(index)
        )

    print("\nDictionary size:", encoder.size())

    serialized = encoder.serialize()

    print(
        "Serialized dictionary size:",
        len(serialized),
        "bytes"
    )

    print("\n" + "=" * 60)
    print("DICTIONARY TEST COMPLETED")
    print("=" * 60)