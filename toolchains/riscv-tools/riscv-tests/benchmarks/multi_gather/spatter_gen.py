k = "mg" # the kernel type, g for gather
p1 = "u" # the pattern_p1, u for UNIFORM, s for Mostly Stride-1, l for Laplacian, c for custom: ")
p2 = "u" # the pattern_p2, u for UNIFORM, s for Mostly Stride-1, l for Laplacian, c for custom: ")
save_to_file = "y" #Save to file 'dataset.h'

# p1 
# UNIFORM Use
p1_length_u = 16 # the length of the pattern:   
p1_gap_u = 1 # the size of each jump (gap):

# Mostly Stride-1 Use
p1_length_s = 1 # the length of the pattern: 
p1_gap_locations_s = "1" # the gap locations (comma separated): 
p1_gaps_s = "2" # the size of the gaps (comma separated): ")

# l for Laplacian 
p1_dimension_l = 1 # the dimension of the stencil(dimension): "))
p1_pseudo_order_l = 2 # the length of a branch of the stencil(pseudo_order): "))
p1_problem_size_l = 3 # the length of each dimension of the problem(problem size): "))

# p2 
# UNIFORM Use
p2_length_u = 30 # the length of the pattern:   
p2_gap_u = 4 # the size of each jump (gap):

# Mostly Stride-1 Use
p2_length_s =  30# the length of the pattern: 
p2_gap_locations_s = "2" # the gap locations (comma separated): 
p2_gaps_s =  "3" # the size of the gaps (comma separated): ")

# l for Laplacian 
p2_dimension_l =  1 # the dimension of the stencil(dimension): "
p2_pseudo_order_l = 1 # the length of a branch of the stencil(pseudo_order): "))
p2_problem_size_l = 1 # the length of each dimension of the problem(problem size): "))

n = 2# the number of gathers 
delta = 4 # the stride between each gather (delta)
target_len = 2 # the target length (target_len)

import random
import sys
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

# k = input("Enter the kernel type, g for gather, s for scatter, gs for gather-scatter, mg for multigather, ms for multiscatter: ")
if k.lower() == 'mg':
    kernel = 3
else:
    print("Invalid kernel type entered.")
    kernel = None
if kernel == 3:
    # p = input("Enter the pattern, u for UNIFORM, s for Mostly Stride-1, l for Laplacian, c for custom: ")
    if p1.lower() == 'u':
        # length = int(input("Enter the length of the pattern: "))
        # gap = int(input("Enter the size of each jump (gap): "))
        pattern_p1 = uniform_pattern(p1_length_u, p1_gap_u)
        print("UNIFORM pattern_p1:",pattern_p1)

    elif p1.lower() == 's':
        # p1_length_s = int(input("Enter the length of the pattern: "))
        # p1_gap_locations_s = input("Enter the gap locations (comma separated): ")
        # p1_gaps_s = input("Enter the size of the gaps (comma separated): ")
        p1_gap_locations_s = [int(x) for x in p1_gap_locations_s.split(',')]
        p1_gaps_s = [int(x) for x in p1_gaps_s.split(',')]
        pattern_p1 = ms1_pattern(p1_length_s, p1_gap_locations_s, p1_gaps_s)
        print("Mostly Stride-1 pattern_p1:", pattern_p1)

    elif p1.lower() == 'l':
        # dimension = int(input("Enter the dimension of the stencil(dimension): "))
        # pseudo_order = int(input("Enter the length of a branch of the stencil(pseudo_order): "))
        # problem_size = int(input("Enter the length of each dimension of the problem(problem size): "))
        pattern_p1 = laplacian_pattern(p1_dimension_l, p1_pseudo_order_l, p1_problem_size_l)
        print("LAPLACIAN pattern_p1:", pattern_p1)

    elif p1.lower() == 'c':
        pattern_p1 = input("Enter the pattern (comma separated): ")
        pattern_p1 = [int(x) for x in pattern_p1.split(',')]
        print("Custom pattern_p1:", pattern_p1)
    else:
        print("Invalid pattern type entered.")
        pattern = None
    # delta = int(input("Enter the stride between each gather (delta): "))
    # Get the number of gathers, ensuring it's a power of 2 expression
    while True:
        try:
            # n_expr = input("Enter the number of gathers (n) as a power of 2 (e.g., 2**2 or 2^3): ")
            # n = safe_eval(n_expr)
            print(f"The evaluated number of gathers is: {n}")
            break
        except ValueError as ve:
            print(ve)
    # target_len = int(input("Enter the target length (target_len): "))
    # save_to_file = input("Save to file 'dataset.h'? (y or n): ")
    max_val = max(pattern_p1)
    if p2.lower() == 'u':
        # length = int(input("Enter the length of the pattern: "))
        # gap = int(input("Enter the size of each jump (gap): "))
        pattern_p2 = uniform_pattern(p2_length_u, p2_gap_u)
        print("UNIFORM pattern_p2:",pattern_p2)
    elif p2.lower() == 's':
        # p2_length_s = int(input("Enter the length of the pattern: "))
        # p2_gap_locations_s = input("Enter the gap locations (comma separated): ")
        # p2_gaps_s = input("Enter the size of the gaps (comma separated): ")
        p2_gap_locations_s = [int(x) for x in p2_gap_locations_s.split(',')]
        p2_gaps_s = [int(x) for x in p2_gaps_s.split(',')]
        pattern_p2 = ms1_pattern(p2_length_s, p2_gap_locations_s, p2_gaps_s)
        print("Mostly Stride-1 pattern_p2:", pattern_p2)
    elif p2.lower() == 'l':
        # dimension = int(input("Enter the dimension of the stencil(dimension): "))
        # pseudo_order = int(input("Enter the length of a branch of the stencil(pseudo_order): "))
        # problem_size = int(input("Enter the length of each dimension of the problem(problem size): "))
        pattern_p2 = laplacian_pattern(p2_dimension_l, p2_pseudo_order_l, p2_problem_size_l)
        print("LAPLACIAN pattern:", pattern_p2)
    elif p2.lower() == 'c':
        pattern_p2 = input("Enter the pattern (comma separated): ")
        pattern_p2 = [int(x) for x in pattern_p2.split(',')]
        print("Custom pattern:", pattern_p2)
    else:
        print("Invalid pattern type entered.")
        pattern = None
    
    if (max_val+1 > len(pattern_p2)):
        print("ERROR :The max index of pattern_p1 is larger than the length of pattern_p2!")
        sys.exit(1)

    max_val_2 = max(pattern_p2)
    source_size = delta * (n - 1) + max_val_2 + 1
    source = [random.randint(0, 999) for _ in range(source_size)]

    if save_to_file.lower() == 'y':
        with open("dataset.h", "w") as f:
            f.write(f"#define KERNEL_{kernel}; // 0 for gather, 1 for scatter, 2 for gather-scatter, 3 for multigather, 4 for multiscatter\n")
            f.write(f"const int delta = {delta};\n")
            f.write(f"const int n = {n};\n")
            f.write(f"const int target_len = {target_len};\n")
            f.write(f"const int pat_len = {len(pattern_p1)};\n")
            print_array_int("inner_pat", pattern_p1, file=f)
            print_array_int("outer_pat", pattern_p2, file=f)
            print_array_double("source", source, file=f)
