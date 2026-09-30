"""
object_graph.py
----------------------------------------------------
Task 8: Dynamic Garbage Collection Optimization

Object Reference Graph Analyzer

Required technology:
    - objgraph
    - gc
    - Circular references
    - Object counting
    - Back-reference analysis
"""

import gc
import objgraph


# ============================================================
# CONFIGURATION
# ============================================================

TEST_OBJECTS = 100


# ============================================================
# GRAPH NODE
# ============================================================

class GraphNode:

    def __init__(self, name):

        self.name = name
        self.child = None
        self.parent = None

    def __repr__(self):

        return f"GraphNode({self.name})"


# ============================================================
# CREATE CIRCULAR GRAPH
# ============================================================

def create_circular_graph(number_of_nodes):

    nodes = []

    for index in range(number_of_nodes):

        node = GraphNode(
            f"Node-{index}"
        )

        nodes.append(node)

    # Connect every node to the next node.
    for index in range(number_of_nodes):

        current = nodes[index]

        next_node = nodes[
            (index + 1) % number_of_nodes
        ]

        current.child = next_node
        next_node.parent = current

    return nodes


# ============================================================
# COUNT GRAPH NODES
# ============================================================

def count_graph_nodes():

    return objgraph.count(
        "GraphNode"
    )


# ============================================================
# DISPLAY OBJECT COUNTS
# ============================================================

def display_object_counts():

    print("\n" + "-" * 60)
    print("OBJECT TYPE COUNTS")
    print("-" * 60)

    graph_nodes = objgraph.count(
        "GraphNode"
    )

    lists = objgraph.count(
        "list"
    )

    dictionaries = objgraph.count(
        "dict"
    )

    print(
        "GraphNode objects :",
        graph_nodes
    )

    print(
        "List objects      :",
        lists
    )

    print(
        "Dictionary objects:",
        dictionaries
    )

    return graph_nodes


# ============================================================
# MOST COMMON OBJECT TYPES
# ============================================================

def display_most_common_types():

    print("\n" + "-" * 60)
    print("MOST COMMON OBJECT TYPES")
    print("-" * 60)

    common_types = (
        objgraph.most_common_types(
            limit=10
        )
    )

    for object_type, count in common_types:

        print(
            f"{object_type:<25}"
            f"{count}"
        )


# ============================================================
# BACK-REFERENCE ANALYSIS
# ============================================================

def analyze_back_references(
    node,
    owner_list
):

    print("\n" + "-" * 60)
    print("BACK-REFERENCE ANALYSIS")
    print("-" * 60)

    print(
        "Target object:",
        node
    )

    try:

        chain = objgraph.find_backref_chain(
            node,
            lambda obj: obj is owner_list
        )

        if chain:

            print(
                "Back-reference chain found."
            )

            print(
                "Chain length:",
                len(chain)
            )

            for index, item in enumerate(
                chain,
                start=1
            ):

                print(
                    f"{index}. "
                    f"{type(item).__name__}"
                )

            # The important condition is that the
            # original list appears in the chain.
            chain_found = any(
                item is owner_list
                for item in chain
            )

            print(
                "Owner list detected:",
                chain_found
            )

            return chain_found

        print(
            "No back-reference chain found."
        )

        return False

    except Exception as error:

        print(
            "Back-reference analysis error:",
            error
        )

        return False


# ============================================================
# REFERENCE RELATIONSHIP TEST
# ============================================================

def test_reference_relationships(
    nodes
):

    print("\n" + "-" * 60)
    print("REFERENCE RELATIONSHIPS")
    print("-" * 60)

    first = nodes[0]

    print(
        "First node :",
        first
    )

    print(
        "Child      :",
        first.child
    )

    print(
        "Parent     :",
        first.parent
    )

    child_valid = (
        first.child is not None
    )

    parent_valid = (
        first.parent is not None
    )

    # Verify circular connection.
    circular_valid = (
        first.child.parent is first
    )

    print(
        "Child reference  :",
        "PASS"
        if child_valid
        else "FAIL"
    )

    print(
        "Parent reference :",
        "PASS"
        if parent_valid
        else "FAIL"
    )

    print(
        "Circular link     :",
        "PASS"
        if circular_valid
        else "FAIL"
    )

    return (
        child_valid
        and parent_valid
        and circular_valid
    )


# ============================================================
# CIRCULAR GRAPH CLEANUP
# ============================================================

def test_circular_cleanup():

    print("\n" + "-" * 60)
    print("CIRCULAR REFERENCE CLEANUP")
    print("-" * 60)

    # Create the graph inside this function.
    # This is important because all references can
    # be removed before gc.collect() is called.

    nodes = create_circular_graph(
        TEST_OBJECTS
    )

    before_cleanup = count_graph_nodes()

    print(
        "GraphNode count before cleanup:",
        before_cleanup
    )

    # Keep the expected count.
    expected = len(nodes)

    # Remove references from the graph list.
    nodes.clear()

    # Delete the list itself.
    del nodes

    # Force cyclic garbage collection.
    collected = gc.collect()

    print(
        "Objects collected:",
        collected
    )

    after_cleanup = count_graph_nodes()

    print(
        "GraphNode count after cleanup :",
        after_cleanup
    )

    # The GraphNode objects should now be gone.
    cleanup_success = (
        after_cleanup == 0
    )

    # Some Python versions may report a different
    # collected count, so the actual requirement is
    # that the objects disappear from the heap.
    print(
        "Expected GraphNodes:",
        expected
    )

    print(
        "Circular cleanup:",
        "PASS"
        if cleanup_success
        else "FAIL"
    )

    return cleanup_success


# ============================================================
# OBJECT GRAPH ANALYSIS
# ============================================================

def run_object_graph_test():

    print("\n" + "=" * 60)
    print("OBJECT GRAPH ANALYSIS")
    print("=" * 60)

    # --------------------------------------------------------
    # Clean environment
    # --------------------------------------------------------

    gc.collect()

    initial_count = count_graph_nodes()

    print(
        "\nInitial GraphNode count:",
        initial_count
    )

    # --------------------------------------------------------
    # Create graph
    # --------------------------------------------------------

    nodes = create_circular_graph(
        TEST_OBJECTS
    )

    print(
        "\nCircular nodes created:",
        len(nodes)
    )

    # --------------------------------------------------------
    # Verify object creation
    # --------------------------------------------------------

    node_count = count_graph_nodes()

    print(
        "GraphNode objects found:",
        node_count
    )

    creation_pass = (
        node_count >= TEST_OBJECTS
    )

    print(
        "Object creation:",
        "PASS"
        if creation_pass
        else "FAIL"
    )

    # --------------------------------------------------------
    # Verify references
    # --------------------------------------------------------

    reference_pass = (
        test_reference_relationships(
            nodes
        )
    )

    # --------------------------------------------------------
    # Display object statistics
    # --------------------------------------------------------

    display_object_counts()

    display_most_common_types()

    # --------------------------------------------------------
    # Back-reference analysis
    #
    # We explicitly pass the owner list so objgraph can
    # locate the list that holds the target node.
    # --------------------------------------------------------

    backref_pass = (
        analyze_back_references(
            nodes[0],
            nodes
        )
    )

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # Delete our references here before leaving this function.
    # Otherwise the GraphNode objects remain reachable.
    # --------------------------------------------------------

    del nodes

    # At this point, the circular nodes may still exist
    # because they reference each other.
    #
    # Python's cyclic GC must collect them.

    collected = gc.collect()

    remaining = count_graph_nodes()

    print("\n" + "-" * 60)
    print("POST-ANALYSIS CLEANUP")
    print("-" * 60)

    print(
        "Objects collected:",
        collected
    )

    print(
        "GraphNode objects remaining:",
        remaining
    )

    cleanup_pass = (
        remaining == 0
    )

    print(
        "Post-analysis cleanup:",
        "PASS"
        if cleanup_pass
        else "FAIL"
    )

    return {
        "creation": creation_pass,
        "references": reference_pass,
        "backreferences": backref_pass,
        "cleanup": cleanup_pass
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print(
        "TASK 8: OBJECT REFERENCE GRAPH ANALYZER"
    )
    print("=" * 60)

    results = run_object_graph_test()

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print("\n" + "=" * 60)
    print("OBJECT GRAPH SUMMARY")
    print("=" * 60)

    print(
        "Circular object creation :",
        "PASS"
        if results["creation"]
        else "FAIL"
    )

    print(
        "Reference relationships   :",
        "PASS"
        if results["references"]
        else "FAIL"
    )

    print(
        "Back-reference analysis   :",
        "PASS"
        if results["backreferences"]
        else "FAIL"
    )

    print(
        "Circular cleanup          :",
        "PASS"
        if results["cleanup"]
        else "FAIL"
    )

    # --------------------------------------------------------
    # Final result
    # --------------------------------------------------------

    all_passed = (
        results["creation"]
        and results["references"]
        and results["backreferences"]
        and results["cleanup"]
    )

    print("\n" + "=" * 60)

    if all_passed:

        print(
            "OBJECT GRAPH TEST : PASS"
        )

    else:

        print(
            "OBJECT GRAPH TEST : FAIL"
        )

    print("=" * 60)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()