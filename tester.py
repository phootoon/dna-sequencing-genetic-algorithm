import itertools

# Function to read sequences from file
def read_sequences(filename):
    with open(filename, 'r') as file:
        sequences = [line.strip() for line in file.readlines()]
    return sequences

# Function to check if lhs can be covered by rhs with given overlap
def covered(lhs, rhs, overlap):
    return lhs[-overlap:] == rhs[:overlap]

# Function to create overlap graph
def create_graph(sequences, k_base_size):
    size = len(sequences)
    E = [[] for _ in range(size)]
    reversed_E = [[] for _ in range(size)]

    for i in range(size):
        for j in range(size):
            if i == j:
                continue
            for k in range(1, k_base_size + 1):
                if covered(sequences[i], sequences[j], k):
                    E[i].append((j, k))
                    reversed_E[j].append((i, k))
                    break
    return E, reversed_E

# Function to find node with smallest coverage
def node_with_smallest_coverage(E, visited):
    min_coverage = float('inf')
    node = -1
    for i, edges in enumerate(E):
        if visited[i]:
            continue
        for _, coverage in edges:
            if coverage < min_coverage:
                min_coverage = coverage
                node = i
    return node

# DFS function to traverse the graph and build a sequence
def traverse(node, edges, visited):
    if visited[node]:
        return []
    visited[node] = True
    sequence = [node]
    if edges[node]:
        next_node = sorted(edges[node], key=lambda x: x[1])[0][0]
        sequence.extend(traverse(next_node, edges, visited))
    return sequence

# Function to find sequences in the graph
def multi_move(E, reversed_E):
    sequences = []
    visited = [False] * len(E)
    node = node_with_smallest_coverage(E, visited)
    while node != -1:
        seq = traverse(node, reversed_E, visited)
        seq.reverse()
        seq.extend(traverse(node, E, [False] * len(E)))
        if len(seq) > 1:
            sequences.append(seq)
        node = node_with_smallest_coverage(E, visited)
    return sequences

# Function to calculate overlap between two sequences
def calculate_overlap(lhs, rhs):
    for i in range(len(rhs), 0, -1):
        if lhs[-i:] == rhs[:i]:
            return len(rhs) - i
    return -1

# Function to merge two sequences
def merge_nodes(lhs, rhs):
    if not rhs:
        return lhs
    if not lhs:
        return rhs
    overlap = calculate_overlap(lhs, rhs)
    return lhs + rhs[overlap:]

# Function to merge a sequence of nodes
def merge_sequence(sequence, sequences):
    result = sequences[sequence[0]]
    for i in range(1, len(sequence)):
        result = merge_nodes(result, sequences[sequence[i]])
    return result

# Function to find the best sequence
def best_sequence(sequences, reads, max_sequence):
    best_seq = ""
    best_coverage = 0

    for perm in itertools.permutations(sequences):
        curr_seq = merge_sequence(perm[0], reads)
        coverage = len(perm[0])
        for s in perm[1:]:
            new_seq = merge_nodes(curr_seq, merge_sequence(s, reads))
            if len(new_seq) <= max_sequence:
                curr_seq = new_seq
                coverage += len(s)
            else:
                break
        if coverage > best_coverage or (coverage == best_coverage and len(curr_seq) < len(best_seq)):
            best_seq = curr_seq
            best_coverage = coverage
    return best_seq, best_coverage

# Main function to run the algorithm
def main(filename, max_sequence, max_nucleotides, k_base_size=5):
    sequences = read_sequences(filename)
    E, reversed_E = create_graph(sequences, k_base_size)
    found_sequences = multi_move(E, reversed_E)
    best_seq, coverage = best_sequence(found_sequences, sequences, max_sequence)
    return best_seq, coverage

if __name__ == "__main__":
    filename = "data.txt"  # Replace with the path to your file
    max_sequence = 206  # Replace with your max sequence length
    max_nucleotides = 160  # Replace with your max nucleotides count
    k_base_size = 5

    best_seq, coverage = main(filename, max_sequence, max_nucleotides, k_base_size)
    print(f"Best sequence: {best_seq}")
    print(f"Coverage: {coverage}")
