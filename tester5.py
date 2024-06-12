# def calculate_coverage_percentage(reference_sequence, reads):
#     covered_positions = sum(1 for read in reads for i in range(len(reference_sequence)) if read.startswith(reference_sequence[i:]))
#     total_positions = len(reference_sequence)
#     coverage_percentage = (covered_positions / total_positions) * 100
#     return coverage_percentage
#
# # Example data
# reference_sequence = "CCCCCCGGGCCGTCTACGATGCCCCCCGGGGGCATGGGTAGAAGGATTCCCCCCCCGGGCCGTCTTCGTGGGGCGGCAAGGCCGGGGGCATGGGTCGCCCCAGGCAATCCGCCGCCCGACGATGCCCCCCGGACGATGCCCCCCGGACGATGCCCCCCGGGGCATGGGTCCCGTCTTCCCCTCCGGTGGGCATGGGGCAAGGCCGG"
# reads = [
#     "AAGGCCGGCT", "ACACCCGCCG", "ACCAGGGCGT", "ACCATGGATG", "ACCCGCCGCC", "ACGATGCCCC", "AGAAGGATTC", "AGCTCACCAT", "AGGCACCAGG",
#     # List truncated for brevity...
# ]
#
# coverage_percentage = calculate_coverage_percentage(reference_sequence, reads)
# print("Percentage of Coverage:", coverage_percentage)


def calculate_coverage(best_sequence, sequences):
    best_length = len(best_sequence)
    coverage = [0] * best_length

    for seq in sequences:
        seq_length = len(seq)
        for i in range(best_length - seq_length + 1):
            # Check if the sequence can align at this position
            match = True
            for j in range(seq_length):
                if best_sequence[i + j] != seq[j]:
                    match = False
                    break
            if match:
                # Increase the coverage for the matched positions
                for j in range(seq_length):
                    coverage[i + j] += 1

    return coverage


# Given data
best_sequence = "CCCCCCGGGCCGTCTACGATGCCCCCCGGGGGCATGGGTAGAAGGATTCCCCCCCCGGGCCGTCTTCGTGGGGCGGCAAGGCCGGGGGCATGGGTCGCCCCAGGCAATCCGCCGCCCGACGATGCCCCCCGGACGATGCCCCCCGGACGATGCCCCCCGGGGCATGGGTCCCGTCTTCCCCTCCGGTGGGCATGGGGCAAGGCCGG"
sequences = [
    "AAGGCCGGCT", "ACACCCGCCG", "ACCAGGGCGT", "ACCATGGATG", "ACCCGCCGCC", "ACGATGCCCC", "AGAAGGATTC",
    "AGCTCACCAT", "AGGCACCAGG", "AGGCCGGCTT", "AGGGCGTGAT", "ATATCGCCGC", "ATCCGCCGCC", "ATCGCCGCGC",
    "ATGATATCGC", "ATGATGATAT", "ATGCCCCCCG", "ATGGATGATG", "CAAGGCCGGC", "CACACCCGCC", "CACCCGCCGC",
    "CAGAAGGATT", "CAGCTCACCA", "CAGGCACCAG", "CAGGGCGTGA", "CATGGATGAT", "CATGGGTCAG", "CATGTGCAAG",
    "CCACACCCGC", "CCAGCTCACC", "CCAGGCACCA", "CCAGGGCGTG", "CCATCGTGGG", "CCATGGATGA", "CCCAGGCACC",
    "CCCCAGGCAC", "CCCCCCGGGC", "CCCCCGGGCC", "CCCCGGGCCG", "CCCCTCCATC", "CCCGCCGCCA", "CCCGGGCCGT",
    "CCCGTCCACA", "CCCTCCATCG", "CCGATCCGCC", "CCGCCGCCAG", "CCGCCGCCCG", "CCGCGCTCGT", "CCGGCTTCGC",
    "CCGGGCCGTC", "CCGTCCACAC", "CCGTCTTCCC", "CCTATGTGGG", "CCTCCATCGT", "CGACAACGGC", "CGACGATGCC",
    "CGATCCGCCG", "CGATGCCCCC", "CGCCAGCTCA", "CGCCCCAGGC", "CGCCCGTCCA", "CGCCGCCAGC", "CGCCGCGCTC",
    "CGCGCTCGTC", "CGCGGGCGAC", "CGCTCGTCGT", "CGGCATGTGC", "CGGCTCCGGC", "CGGCTTCGCG", "CGGGCCGTCT",
    "CGGGCGACGA", "CGTCGACAAC", "CGTCGTCGAC", "CGTCTTCCCC", "CGTGATGGTG", "CGTGGGGCGC", "CTATGTGGGC",
    "CTCCATCGTG", "CTCCGGCATG", "CTCGTCGTCG", "CTTCCCCTCC", "CTTCGCGGGC", "GAAGGATTCC", "GACAACGGCT",
    "GACGATGCCC", "GATATCGCCG", "GATCCGCCGC", "GATGATATCG", "GATGCCCCCC", "GATTCCTATG", "GCAAGGCCGG",
    "GCACCAGGGC", "GCATGGGTCA", "GCCAGCTCAC", "GCCCCAGGCA", "GCCCGTCCAC", "GCCGATCCGC", "GCCGCCAGCT",
    "GCCGGCTTCG", "GCGACGATGC", "GCGCCCCAGG", "GCGCTCGTCG", "GCGGGCGACG", "GCGTGATGGT", "GCTCACCATG",
    "GCTCCGGCAT", "GCTCGTCGTC", "GGATGATGAT", "GGATTCCTAT", "GGCATGGGTC", "GGCATGTGCA", "GGCCGGCTTC",
    "GGCCGTCTTC", "GGCGACGATG", "GGCGCCCCAG", "GGCGTGATGG", "GGCTCCGGCA", "GGCTTCGCGG", "GGGCATGGGT",
    "GGGCGACGAT", "GGGCGCCCCA", "GGGCGTGATG", "GGGGCGCCCC", "GGTCAGAAGG", "GGTGGGCATG", "GTCAGAAGGA",
    "GTCCACACCC", "GTCGACAACG", "GTCTTCCCCT", "GTGATGGTGG", "GTGCAAGGCC", "GTGGGCATGG", "GTGGGGCGCC",
    "TATGTGGGCG", "TCAGAAGGAT", "TCCACACCCG", "TCCATCGTGG", "TCCCCTCCAT", "TCCGCCGCCC", "TCCGGCATGT",
    "TCCTATGTGG", "TCGACAACGG", "TCGCCGCGCT", "TCGCGGGCGA", "TCGTCGTCGA", "TCGTGGGGCG", "TCTTCCCCTC",
    "TGATATCGCC", "TGATGATATC", "TGATGGTGGG", "TGCAAGGCCG", "TGCCCCCCGG", "TGCCGATCCG", "TGGGCATGGG",
    "TGGGGCGCCC", "TGGGTCAGAA", "TGTGCAAGGC", "TTCCTATGTG", "TTCGCGGGCG", "TTGCCGATCC"
]

coverage = calculate_coverage(best_sequence, sequences)
print(coverage)

