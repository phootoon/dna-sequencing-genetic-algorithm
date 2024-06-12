import random

def generate_dna_sequence(length):
    return ''.join(random.choice('ACGT') for _ in range(length))

def introduce_errors(sequence, error_rate=0.01):
    sequence = list(sequence)
    for i in range(len(sequence)):
        if random.random() < error_rate:
            sequence[i] = random.choice('ACGT')
    return ''.join(sequence)

def generate_reads(sequence, read_length, coverage, error_rate=0.01):
    reads = []
    for _ in range(coverage):
        start = random.randint(0, len(sequence) - read_length)
        read = sequence[start:start + read_length]
        read_with_errors = introduce_errors(read, error_rate)
        reads.append(read_with_errors)
    return reads

# Przykład użycia generatora
true_sequence = generate_dna_sequence(1000)
reads = generate_reads(true_sequence, read_length=100, coverage=20, error_rate=0.02)


class DNASequencer:
    def __init__(self, reads, k):
        self.reads = reads
        self.k = k
        self.graph = self.create_graph()
        self.reverse_graph = self.create_reverse_graph()

    def create_graph(self):
        graph = {}
        for i, read in enumerate(self.reads):
            graph[i] = []
            for j, other_read in enumerate(self.reads):
                if i != j:
                    overlap = self.get_overlap(read, other_read)
                    if overlap >= self.k:
                        graph[i].append((j, overlap))
        return graph

    def create_reverse_graph(self):
        reverse_graph = {}
        for node in self.graph:
            for edge in self.graph[node]:
                if edge[0] not in reverse_graph:
                    reverse_graph[edge[0]] = []
                reverse_graph[edge[0]].append((node, edge[1]))
        return reverse_graph

    def get_overlap(self, read1, read2):
        max_overlap = min(len(read1), len(read2))
        for i in range(max_overlap, 0, -1):
            if read1[-i:] == read2[:i]:
                return i
        return 0

    def find_best_path(self):
        best_path = []
        visited = set()
        for node in self.graph:
            if node not in visited:
                path = self.dfs(node, visited)
                if len(path) > len(best_path):
                    best_path = path
        return best_path

    def dfs(self, node, visited):
        visited.add(node)
        best_path = [node]
        for neighbor, _ in sorted(self.graph[node], key=lambda x: -x[1]):
            if neighbor not in visited:
                path = self.dfs(neighbor, visited)
                if len(path) > len(best_path):
                    best_path = path
        return [node] + best_path

    def assemble_sequence(self):
        best_path = self.find_best_path()
        sequence = self.reads[best_path[0]]
        for node in best_path[1:]:
            overlap = self.get_overlap(sequence, self.reads[node])
            sequence += self.reads[node][overlap:]
        return sequence

def evaluate_sequencer(true_sequence, sequenced_sequence):
    true_length = len(true_sequence)
    sequenced_length = len(sequenced_sequence)
    matched_bases = sum(1 for a, b in zip(true_sequence, sequenced_sequence) if a == b)
    accuracy = matched_bases / true_length
    coverage = sequenced_length / true_length
    return accuracy, coverage

# Przykład użycia
true_sequence = generate_dna_sequence(1000)
reads = generate_reads(true_sequence, read_length=100, coverage=20, error_rate=0.02)

sequencer = DNASequencer(reads, k=3)
sequenced_sequence = sequencer.assemble_sequence()

accuracy, coverage = evaluate_sequencer(true_sequence, sequenced_sequence)
print(f"Accuracy: {accuracy:.2%}, Coverage: {coverage:.2%}")
