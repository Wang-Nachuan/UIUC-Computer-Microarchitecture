import random

def generate_sparse_matrix(rows, cols, nnz):
    pnnz = nnz / (rows * cols)
    idx = []
    p = [0]
    for i in range(rows):
        for j in range(cols):
            if random.random() < pnnz:
                idx.append(j)
        p.append(len(idx))
    values = [random.randint(0, 999) for _ in range(len(idx))]
    return values, idx, p

def generate_dense_matrix(rows, cols):
    return [[random.randint(0, 999) for _ in range(cols)] for _ in range(rows)]

def spmm(values, idx, ptr, B):
    result = []
    for i in range(len(ptr) - 1):
        row = [0] * len(B[0])
        for k in range(ptr[i], ptr[i+1]):
            for j in range(len(B[0])):
                row[j] += values[k] * B[idx[k]][j]
        result.append(row)
    return result

m = int(input("Enter the number of rows for matrix A: "))
k = int(input("Enter the number of columns for matrix A (rows for matrix B): "))
n = int(input("Enter the number of columns for matrix B: "))
approx_nnz = int(input("Enter the approximate number of non-zeros for matrix A: "))
save_to_file = input("Save to file 'dataset2.h'? (y or n): ")

A_values, A_idx, A_ptr = generate_sparse_matrix(m, k, approx_nnz)
B = generate_dense_matrix(k, n)
result = spmm(A_values, A_idx, A_ptr, B)

def print_vec(t, name, data, file=None):
    print(f"const {t} {name}[{len(data)}] = {{", file=file)
    print("  " + ",\n  ".join(map(str, data)), file=file)
    print("};", file=file)

def print_matrix(name, matrix, file=None):
    print(f"const double {name}[{len(matrix)}][{len(matrix[0])}] = {{", file=file)
    for row in matrix:
        print("  {" + ", ".join(map(str, row)) + "},", file=file)
    print("};", file=file)

if save_to_file.lower() == 'y':
    with open("dataset2.h", "w") as f:
        print(f"#define M {m}", file=f)
        print(f"#define K {k}", file=f)
        print(f"#define N {n}", file=f)
        print(f"#define NNZ {len(A_values)}", file=f)
        print_vec("double", "A_val", A_values, f)
        print_vec("int", "A_idx", A_idx, f)
        print_vec("int", "A_ptr", A_ptr, f)
        print_matrix("B", B, f)
        print_matrix("result", result, f)

print(f"#define M {m}")
print(f"#define K {k}")
print(f"#define N {n}")
print(f"#define NNZ {len(A_values)}")
print_vec("double", "A_val", A_values)
print_vec("int", "A_idx", A_idx)
print_vec("int", "A_ptr", A_ptr)
print_matrix("B", B)
print_matrix("result", result)