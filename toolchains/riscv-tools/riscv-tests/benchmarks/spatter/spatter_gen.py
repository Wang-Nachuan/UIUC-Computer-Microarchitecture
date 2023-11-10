import random

# uniform_pattern(length, gap)
# returns a pattern of length length with a gap of size gap between each element
def uniform_pattern(length, gap):
    return [i * gap for i in range(length)]


# ms1_pattern(length, gap_locations, gaps)
# returns a pattern of length length with gaps of size gaps[i] at locations gap_locations[i]
def ms1_pattern(length, gap_locations, gaps):
    pattern = list(range(length))
    
    # Make sure gaps is a list and has the correct number of elements
    if not isinstance(gaps, list):
        raise TypeError("gaps must be a list")
    if not isinstance(gap_locations, list):
        raise TypeError("gap_locations must be a list")
    
    if len(gaps) == 1:
        gaps *= len(gap_locations)
        
    for i, gl in enumerate(gap_locations):
        # Ensure the gap location is within the valid range
        if gl < 1 or gl >= length:
            raise ValueError("Gap location must be within the range of the pattern")
        pattern[gl] = pattern[gl - 1] + gaps[i]
        # Update the values after the gap
        for j in range(gl + 1, length):
            pattern[j] = pattern[j - 1] + 1
    
    return pattern

def laplacian_pattern(dimension, pseudo_order, problem_size):
    pattern = []
    array = []
    for i in range(0, dimension):
        array.append(problem_size**i)
    # print(array)
    mid = (pseudo_order * problem_size **(dimension - 1))
    pattern.append(mid)
    for i in range(1, pseudo_order + 1):
        for j in range(0, dimension):
            pattern.append(mid - i * array[j])
            pattern.append(mid + i * array[j])
    pattern.sort()
    return pattern

# print(laplacian_pattern(1, 1, 100))  # result: [0, 1, 2]
# print(laplacian_pattern(2, 1, 100))  # result: [0, 99, 100, 101, 200]
# print(laplacian_pattern(3, 1, 100))  # result: [0, 9900, 9999, 10000, 10001, 10100, 20000]
# print(laplacian_pattern(2, 2, 100))  # result: [0, 100, 198, 199, 200, 201, 202, 300, 400]

def safe_eval(expr):
    expr = expr.replace('^', '**')
    if not set(expr).issubset(set('01234567890*^ ')):
        raise ValueError("Invalid expression. Only digits, '^', and '**' are allowed.")
    try:
        return eval(expr, {"__builtins__": None})
    except SyntaxError as e:
        raise ValueError("Incorrect format for expression.") from e

def write_pattern_to_header(pattern, f):
    f.write(f"const double pat[{len(pattern)}] = {{\n")
    for i, val in enumerate(pattern):
        f.write(f"  {val},\n")
    f.write("};\n\n")

def print_array_double(name, array, file=None):
    print(f"const double {name}[{len(array)}] = {{", file=file)
    print("  " + ", ".join(map(str, array)) + ",", file=file)
    print("};\n", file=file)

def print_array_int(name, array, file=None):
    print(f"const int {name}[{len(array)}] = {{", file=file)
    print("  " + ", ".join(map(str, array)) + ",", file=file)
    print("};\n", file=file)


kernel = 0 #TODO

p = input("Enter the pattern, u for UNIFORM, s for Mostly Stride-1, l for Laplacian, c for custom: ")

if p.lower() == 'u':
    length = int(input("Enter the length of the pattern: "))
    gap = int(input("Enter the size of each jump (gap): "))
    pattern = uniform_pattern(length, gap)
    print("UNIFORM pattern:",pattern)

elif p.lower() == 's':
    length = int(input("Enter the length of the pattern: "))
    gap_locations = input("Enter the gap locations (comma separated): ")
    gaps = input("Enter the size of the gaps (comma separated): ")
    gap_locations = [int(x) for x in gap_locations.split(',')]
    gaps = [int(x) for x in gaps.split(',')]
    pattern = ms1_pattern(length, gap_locations, gaps)
    print("Mostly Stride-1 pattern:", pattern)

elif p.lower() == 'l':
    dimension = int(input("Enter the dimension of the stencil(dimension): "))
    pseudo_order = int(input("Enter the length of a branch of the stencil(pseudo_order): "))
    problem_size = int(input("Enter the length of each dimension of the problem(problem size): "))
    pattern = laplacian_pattern(dimension, pseudo_order, problem_size)
    print("LAPLACIAN pattern:", pattern)

elif p.lower() == 'c':
    pattern = input("Enter the pattern (comma separated): ")
    pattern = [int(x) for x in pattern.split(',')]
    print("Custom pattern:", pattern)

else:
    print("Invalid pattern type entered.")
    pattern = None

delta = int(input("Enter the stride between each gather (delta): "))
# Get the number of gathers, ensuring it's a power of 2 expression
while True:
    try:
        n_expr = input("Enter the number of gathers (n) as a power of 2 (e.g., 2**2 or 2^3): ")
        n = safe_eval(n_expr)
        print(f"The evaluated number of gathers is: {n}")
        break
    except ValueError as ve:
        print(ve)
target_len = int(input("Enter the target length (target_len): "))
save_to_file = input("Save to file 'dataset.h'? (y or n): ")
max_val = max(pattern)
source_size = delta * (n - 1) + max_val + 1
source = [random.randint(0, 999) for _ in range(source_size)]


if save_to_file.lower() == 'y':
    with open("dataset.h", "w") as f:
        f.write(f"const int kernel = {kernel}; // 0 for gather, 1 for scatter, 2 for gather-scatter, 3 for multigather, 4 for multiscatter\n")
        f.write(f"const int delta = {delta};\n")
        f.write(f"const int n = {n};\n")
        f.write(f"const int target_len = {target_len};\n")
        f.write(f"const int pat_len = {len(pattern)};\n")
        print_array_int("pat", pattern, file=f)
        print_array_double("source", source, file=f)

