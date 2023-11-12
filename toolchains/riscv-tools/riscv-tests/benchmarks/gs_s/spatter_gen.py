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

k = input("Enter the kernel type, g for gather, s for scatter, gs for gather-scatter, mg for multigather, ms for multiscatter: ")
if k.lower() == 'g':
    kernel = 0
elif k.lower() == 's':
    kernel = 1
elif k.lower() == 'gs':
    kernel = 2
elif k.lower() == 'mg':
    kernel = 3
elif k.lower() == 'ms':
    kernel = 4
else:
    print("Invalid kernel type entered.")
    kernel = None
if kernel == 0:
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
            f.write(f"#define KERNEL_{kernel}; // 0 for gather, 1 for scatter, 2 for gather-scatter, 3 for multigather, 4 for multiscatter\n")
            f.write(f"const int delta = {delta};\n")
            f.write(f"const int n = {n};\n")
            f.write(f"const int target_len = {target_len};\n")
            f.write(f"const int pat_len = {len(pattern)};\n")
            print_array_int("pat", pattern, file=f)
            print_array_double("source", source, file=f)
elif kernel == 1:
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

    delta = int(input("Enter the stride between each scatter (delta): "))
    # Get the number of scatter, ensuring it's a power of 2 expression
    while True:
        try:
            n_expr = input("Enter the number of scatter (n) as a power of 2 (e.g., 2**2 or 2^3): ")
            n = safe_eval(n_expr)
            print(f"The evaluated number of scatter is: {n}")
            break
        except ValueError as ve:
            print(ve)
    source_len = int(input("Enter the source length (source_len): "))
    save_to_file = input("Save to file 'dataset.h'? (y or n): ")
    max_val = max(pattern)
    target_size = delta * (n - 1) + max_val + 1
    source_size = len(pattern) * source_len
    source = [random.randint(0, 999) for _ in range(source_size)]


    if save_to_file.lower() == 'y':
        with open("dataset.h", "w") as f:
            f.write(f"#define KERNEL_{kernel} // 0 for gather, 1 for scatter, 2 for gather-scatter, 3 for multigather, 4 for multiscatter\n")
            f.write(f"const int delta = {delta};\n")
            f.write(f"const int n = {n};\n")
            f.write(f"const int target_size = {target_size};\n")
            f.write(f"const int source_len = {source_len};\n")
            f.write(f"const int pat_len = {len(pattern)};\n")
            print_array_int("pat", pattern, file=f)
            print_array_double("source", source, file=f)

elif kernel == 2:
    p = input("Enter the gather pattern, u for UNIFORM, s for Mostly Stride-1, l for Laplacian, c for custom: ")
    if p.lower() == 'u':
        length_g = int(input("Enter the length of the pattern: "))
        gap_g = int(input("Enter the size of each jump (gap): "))
        pattern_g = uniform_pattern(length_g, gap_g)
        print("UNIFORM gather pattern:",pattern_g)

    elif p.lower() == 's':
        length_g = int(input("Enter the length of the pattern: "))
        gap_locations_g = input("Enter the gap locations (comma separated): ")
        gaps_g = input("Enter the size of the gaps (comma separated): ")
        gap_locations_g = [int(x) for x in gap_locations_g.split(',')]
        gaps_g = [int(x) for x in gaps_g.split(',')]
        pattern_g = ms1_pattern(length_g, gap_locations_g, gaps_g)
        print("Mostly Stride-1 pattern:", pattern_g)

    elif p.lower() == 'l':
        dimension_g = int(input("Enter the dimension of the stencil(dimension): "))
        pseudo_order_g = int(input("Enter the length of a branch of the stencil(pseudo_order): "))
        problem_size_g = int(input("Enter the length of each dimension of the problem(problem size): "))
        pattern_g = laplacian_pattern(dimension_g, pseudo_order_g, problem_size_g)
        length_g = len(pattern_g)
        print("LAPLACIAN pattern:", pattern_g)

    elif p.lower() == 'c':
        pattern_g = input("Enter the pattern (comma separated): ")
        pattern_g = [int(x) for x in pattern_g.split(',')]
        length_g = len(pattern_g)
        print("Custom pattern:", pattern_g)

    else:
        print("Invalid pattern type entered.")
        pattern = None
    
    p_s = input("Enter the scatter pattern, u for UNIFORM, s for Mostly Stride-1, l for Laplacian, c for custom: ")
    if p_s.lower() == 'u':
        length_s = int(input("Enter the length of the pattern: "))
        while (length_g != length_s):
            print("The length of gather pattern and scatter pattern must be the same!")
            length_s = int(input("Enter the length of the pattern: "))
        gap_s = int(input("Enter the size of each jump (gap): "))
        pattern_s = uniform_pattern(length_s, gap_s)
        print("UNIFORM scatter pattern:",pattern_s)
    
    elif p_s.lower() == 's':
        length_s = int(input("Enter the length of the pattern: "))
        while (length_g != length_s):
            print("The length of gather pattern and scatter pattern must be the same!")
            length_s = int(input("Enter the length of the pattern: "))
        gap_locations_s = input("Enter the gap locations (comma separated): ")
        gaps_s = input("Enter the size of the gaps (comma separated): ")
        gap_locations_s = [int(x) for x in gap_locations_s.split(',')]
        gaps_s = [int(x) for x in gaps_s.split(',')]
        pattern_s = ms1_pattern(length_s, gap_locations_s, gaps_s)
        print("Mostly Stride-1 scatter pattern:", pattern_s)
    
    elif p_s.lower() == 'l':
        dimension_s = int(input("Enter the dimension of the stencil(dimension): "))
        pseudo_order_s = int(input("Enter the length of a branch of the stencil(pseudo_order): "))
        problem_size_s = int(input("Enter the length of each dimension of the problem(problem size): "))
        pattern_s = laplacian_pattern(dimension_s, pseudo_order_s, problem_size_s)
        length_s = len(pattern_s)
        while (length_g != length_s):
            print("The length of gather pattern and scatter pattern must be the same!")
            dimension_s = int(input("Enter the dimension of the stencil(dimension): "))
            pseudo_order_s = int(input("Enter the length of a branch of the stencil(pseudo_order): "))
            problem_size_s = int(input("Enter the length of each dimension of the problem(problem size): "))
            pattern_s = laplacian_pattern(dimension_s, pseudo_order_s, problem_size_s)
            length_s = len(pattern_s)
        print("LAPLACIAN scatter pattern:", pattern_s)
    
    elif p_s.lower() == 'c':
        pattern_s = input("Enter the pattern (comma separated): ")
        pattern_s = [int(x) for x in pattern_s.split(',')]
        length_s = len(pattern_s)
        while (length_g != length_s):
            print("The length of gather pattern and scatter pattern must be the same!")
            pattern_s = input("Enter the pattern (comma separated): ")
            pattern_s = [int(x) for x in pattern_s.split(',')]
            length_s = len(pattern_s)
        print("Custom scatter pattern:", pattern_s)

    delta_g = int(input("Enter the stride between each gather (delta): "))
    delta_s = int(input("Enter the stride between each scatter (delta): "))
    # Get the number of gathers, ensuring it's a power of 2 expression
    # Get the number of scatter, ensuring it's a power of 2 expression
    while True:
        try:
            n_expr = input("Enter the number of gather-scatter (n) as a power of 2 (e.g., 2**2 or 2^3): ")
            n = safe_eval(n_expr)
            print(f"The evaluated number of scatter is: {n}")
            break
        except ValueError as ve:
            print(ve)
    save_to_file = input("Save to file 'dataset.h'? (y or n): ")
    max_val_g = max(pattern_g)
    max_val_s = max(pattern_s)
    target_size = delta_s * (n - 1) + max_val_s + 1
    source_size = delta_g * (n - 1) + max_val_g + 1
    source = [random.randint(0, 999) for _ in range(source_size)]

    if save_to_file.lower() == 'y':
        with open("dataset.h", "w") as f:
            f.write(f"#define KERNEL_{kernel} // 0 for gather, 1 for scatter, 2 for gather-scatter, 3 for multigather, 4 for multiscatter\n")
            f.write(f"const int delta_gather = {delta_g};\n")
            f.write(f"const int delta_scatter = {delta_s};\n")
            f.write(f"const int n = {n};\n")
            f.write(f"const int target_size = {target_size};\n")
            # f.write(f"const int source_len = {source_len};\n")
            f.write(f"const int pat_len = {len(pattern_g)};\n")
            print_array_int("gather_pat", pattern_g, file=f)
            print_array_int("scatter_pat", pattern_s, file=f)
            print_array_double("source", source, file=f)