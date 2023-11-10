#include "dataset.h" 
#include "util.h"
// #include <stdio.h>
void gather_smallbuf_serial(
        double* restrict target,
        const double* restrict source, // source array
        const int* restrict pat, // index pattern array
        int pat_len,  // length of index pattern
        int delta, // stride between each gather
        int n, // number of gathers
        int target_len) {

    for (int i = 0; i < n; i++) {
        double* sl = source + delta * i;
        // Pick which elements are written to in a way that
        // is hard to optimize out with a compiler
        double* tl = target + pat_len * (i % target_len);

        for (int j = 0; j < pat_len; j++) {
            tl[j] = sl[pat[j]];
        }
    }
}

int main(int argc, char* argv[]) {
    double target[target_len * pat_len];
#if PREALLOCATE
    gather_smallbuf_serial(target, source, pat, pat_len, delta, n, target_len);
#endif
    setStats(1);
    gather_smallbuf_serial(target, source, pat, pat_len, delta, n, target_len);
    // Print the resulting matrix
    // for (int i = 0; i < target_len; i++) {
    //     for (int j = 0; j < pat_len; j++) {
    //         // Accessing element in row-major order
    //         printf("%f ", target[i * pat_len + j]);
    //     }
    // printf("\n"); // Newline for each row
    // } 
    setStats(0);
    return 0; 
}


