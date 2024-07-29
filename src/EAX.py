import random


def extract_edges(tour):
    """Extract edges from the given tour."""
    edges = set()
    for i in range(len(tour)):
        edges.add((tour[i], tour[(i + 1) % len(tour)]))
    return edges


def get_common_edges(parent1, parent2):
    """Get the common edges between two parents."""
    edges1 = extract_edges(parent1)
    edges2 = extract_edges(parent2)
    return edges1.intersection(edges2)


def build_adjacency_list(tour):
    """Build adjacency list from the given tour."""
    adjacency = {i: set() for i in tour}
    for i in range(len(tour)):
        adjacency[tour[i]].add(tour[(i + 1) % len(tour)])
        adjacency[tour[i]].add(tour[(i - 1) % len(tour)])
    return adjacency


def find_cycles(edges, start_node):
    """Find all cycles in the given edges starting from the start_node."""
    cycles = []
    visited = set()
    stack = [start_node]

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        cycle = [node]
        current = node
        while True:
            next_node = None
            for edge in edges:
                if edge[0] == current and edge[1] not in visited:
                    next_node = edge[1]
                    break
                elif edge[1] == current and edge[0] not in visited:
                    next_node = edge[0]
                    break
            if next_node is None:
                break
            cycle.append(next_node)
            visited.add(next_node)
            current = next_node
        cycles.append(cycle)
    return cycles


def ensure_first_node_zero(tour):
    """Ensure the first node of the tour is zero."""
    zero_index = tour.index(0)
    return tour[zero_index:] + tour[:zero_index]


def crossover_EAX(parent1, parent2):
    """Perform EAX crossover on two parents to produce an offspring."""
    common_edges = get_common_edges(parent1, parent2)
    adjacency1 = build_adjacency_list(parent1)
    adjacency2 = build_adjacency_list(parent2)

    AB_edges = []
    for i in range(len(parent1)):
        edge = (parent1[i], parent1[(i + 1) % len(parent1)])
        if edge not in common_edges and (edge[1], edge[0]) not in common_edges:
            AB_edges.append(edge)

    cycles = find_cycles(AB_edges, random.choice(parent1))

    offspring = list(parent1)
    for cycle in cycles:
        if random.random() < 0.5:
            for i in range(len(cycle) - 1):
                idx1 = offspring.index(cycle[i])
                idx2 = offspring.index(cycle[i + 1])
                offspring[idx1], offspring[idx2] = offspring[idx2], offspring[idx1]

    # Ensure the first node is zero
    offspring = ensure_first_node_zero(offspring)
    return offspring

# # Example usage
# parent1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# parent2 = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9, 12, 10, 11]
#
# offspring = crossover_EAX(parent1, parent2)
# print("Offspring:", offspring)
