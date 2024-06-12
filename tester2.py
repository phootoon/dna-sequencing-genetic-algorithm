import itertools

# Read the input data from the file
with open('data.txt', 'r') as file:
    lines = file.readlines()

# Extract the strand and parts
strand = lines[0].strip()
parts = [line.strip() for line in lines[1:]]

# Initialize sequence and start_position
sequence = list(range(len(parts)))
start_position = [-1] * len(parts)
end_strand = ''


def trim(s):
    return s.strip()


def check_overlap(str_a, str_b):
    for pos in range(len(str_a)):
        finished = True
        for pos_b in range(len(str_b)):
            if pos + pos_b >= len(str_a):
                return pos
            if str_b[pos_b] != str_a[pos + pos_b]:
                finished = False
                break
        if finished:
            return pos
    return len(str_a)


def compare():
    global end_strand
    analyzing_strand = strand
    strand_position = 0
    starting_on = 0
    finished = True

    for current in sequence:
        finished = True
        constructed = analyzing_strand[:strand_position]
        starting_on = check_overlap(constructed, parts[current])
        part_pos = 0
        for i in range(starting_on, len(parts[current])):
            if strand_position >= len(analyzing_strand):
                finished = False
                break
            if parts[current][i] == analyzing_strand[strand_position]:
                strand_position += 1
            else:
                while strand_position < len(analyzing_strand) and parts[current][i] != analyzing_strand[
                    strand_position]:
                    analyzing_strand = analyzing_strand[:strand_position] + analyzing_strand[strand_position + 1:]
                if strand_position < len(analyzing_strand) and parts[current][i] == analyzing_strand[strand_position]:
                    strand_position += 1
            part_pos += 1

        print(
            f"Part {current}, start_position: {starting_on}, part_pos: {part_pos}, strand_position: {strand_position}")
        print(f"Analyzing strand: {analyzing_strand}")

        if finished:
            start_position[current] = starting_on
        else:
            start_position[current] = -1

    end_strand = analyzing_strand


# Find the correct sequence
found = False
for perm in itertools.permutations(sequence):
    sequence = list(perm)
    print(f"Trying permutation: {sequence}")
    compare()
    print(f"Start positions: {start_position}")
    if all(start != -1 for start in start_position):
        found = True
        break

if found:
    print("Found a valid permutation!")
    print("End strand:", end_strand)
    print("Start positions:", " ".join(str(start + 1) for start in start_position))
else:
    print("No valid permutation found.")
