from cfg_factory import create_cfg

if __name__ == "__main__":
    cfg = create_cfg()
    print("Control Flow Graph created successfully!")

    # Print some basic information about the CFG
    print(f"Number of nodes: {len(cfg.graph.nodes)}")
    print(f"Number of edges: {len(cfg.graph.edges)}")

    # Print edge weights
    print("\nEdge weights:")
    for (source, target), edge in cfg.edges.items():
        print(f"Edge {source} -> {target} ({edge.edge_type}): {edge.weight:.3f}")

    # Example: Get all paths from start to end
    paths = cfg.get_all_paths(0, 12)
    print(f"\nFound {len(paths)} paths from node 0 to node 12")