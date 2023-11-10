import random
def uniform_pattern(length, gap):
    return [i * gap for i in range(length)]

def ms1_pattern(length, gap_locations, gaps):
    pattern = list(range(length))
    gaps = list(gaps)
    if len(gaps) == 1:
        gaps *= len(gap_locations)
    for i, gl in enumerate(gap_locations):
        pattern[gl] = pattern[gl-1] + gaps[i]
    return pattern

def laplacian_pattern(dimension, pseudo_order, problem_size):
    pattern = []
    if dimension == 1:
        for i in range(-pseudo_order, pseudo_order + 1):
            pattern.append(i + pseudo_order)
    elif dimension == 2:
        for i in range(-pseudo_order, pseudo_order + 1):
            for j in range(-pseudo_order, pseudo_order + 1):
                if i != 0 or j != 0:
                    pattern.append(i * problem_size + j + pseudo_order * (problem_size + 1))
    # Extend this pattern for dimension 3 and so on...
    return pattern

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

p = input("Enter the pattern, u for UNIFORM, s for Mostly Stride-1, l for Laplacian: ")

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
    dimension = int(input("Enter the dimension of the stencil: "))
    pseudo_order = int(input("Enter the length of a branch of the stencil: "))
    problem_size = int(input("Enter the length of each dimension of the problem: "))
    pattern = laplacian_pattern(dimension, pseudo_order, problem_size)
    print("LAPLACIAN pattern:", pattern)

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
        f.write(f"const int kernel = {kernel}; // 0 for UNIFORM, 1 for MS1, 2 for LAPLACIAN\n")
        f.write(f"const int delta = {delta};\n")
        f.write(f"const int n = {n};\n")
        f.write(f"const int target_len = {target_len};\n")
        f.write(f"const int pat_len = {len(pattern)};\n")
        print_array_int("pat", pattern, file=f)
        print_array_double("source", source, file=f)






