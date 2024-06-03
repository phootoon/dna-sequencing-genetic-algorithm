def preprocess_spectrum(fragments, l):
    def can_merge(f1, f2):
        """Check if the last l-1 characters of f1 match the first l-1 characters of f2."""
        return f1[-(l - 1):] == f2[:(l - 1)]

    used = set()
    new_spectrum = []

    for i in range(len(fragments)):
        if i in used:
            continue
        chain = fragments[i]
        used.add(i)

        while True:
            found = False
            for j in range(len(fragments)):
                if j not in used and can_merge(chain, fragments[j]):
                    chain += fragments[j][-(l - 1):][-1]  # Add only the non-overlapping character
                    used.add(j)
                    found = True
                    break
            if not found:
                break

        new_spectrum.append(chain)

    return new_spectrum


# Example usage
fragments = ["CTAGA", "TAGAC", "AGACG", "TATCC", "ACGTT", "CGTTC"]
l = 5
result = preprocess_spectrum(fragments, l)
print(result)  # Output: ['CTAGACG', 'TATCC', 'ACGTTC']
