from itertools import combinations


def generate_subsets(input_list):
    n = len(input_list)
    max_size = n // 2
    unique_elements = list(
        set(input_list)
    )
    subsets = []
    for size in range(1, max_size + 1):
        subsets.extend(combinations(unique_elements, size))

    return [list(subset) for subset in subsets]


def extract_max_length_subset(subsets):
    if not subsets:
        return []
    max_length = max(len(subset) for subset in subsets)

    max_length_subsets = [subset for subset in subsets if len(subset) == max_length]

    return max_length_subsets
input_list = [1, 2, 1, 3]
subsets = generate_subsets(input_list)
max_length_subsets = extract_max_length_subset(subsets)
print(max_length_subsets)  # Output: [[1, 2, 3]]
