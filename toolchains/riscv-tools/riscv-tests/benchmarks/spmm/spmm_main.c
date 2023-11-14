#include "util.h"
// #include <stdio.h>
//--------------------------------------------------------------------------
// Input/Reference Data

#include "dataset2.h"

void spmm(int rows, int cols, const double* A_val, const int* A_idx,
          const int* A_ptr, const double B[K][N], double* C)
{
  for (int i = 0; i < rows; i++)
  {
    for (int j = 0; j < cols; j++)
    {
      double cij = 0;
      for (int k = A_ptr[i]; k < A_ptr[i+1]; k++)
      {
        cij += A_val[k] * B[A_idx[k]][j];
      }
      C[i * cols + j] = cij;
    }
  }
}

//--------------------------------------------------------------------------
// Main

int main( int argc, char* argv[] )
{
  double C[M * N];

#if PREALLOCATE
  spmm(M, N, A_val, A_idx, A_ptr, B, C);
#endif

  setStats(1);
  spmm(M, N, A_val, A_idx, A_ptr, B, C);
  setStats(0);

  printStats();

  // return verifyDouble(M * N, C,  &result[0][0]);
  // int verification_result = verifyDouble(M * N, C, &result[0][0]);
  // printf("Verification Result: %d\n", verification_result);

  return 0;
}