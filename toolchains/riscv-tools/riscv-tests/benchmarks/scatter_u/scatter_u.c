#include "dataset.h" 
// #include <stdio.h>
#include "util.h"
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

void scatter_smallbuf_serial(
        double* restrict target,
        const double* restrict source, // source array
        const int* restrict pat, // index pattern array
        int pat_len,  // length of index pattern
        int delta, // stride between each gather
        int n, // number of gathers
        int source_len) {

    for (int i = 0; i < n; i++) {
        double* sl = source + pat_len*(i % source_len);
        // Pick which elements are written to in a way that
        // is hard to optimize out with a compiler
        double* tl = target + delta * i;

        for (int j = 0; j < pat_len; j++) {
            tl[pat[j]] = sl[j];
        }
    }
}

void sg_smallbuf_serial(
        const double* restrict gather,
        double* restrict scatter,
        const int* restrict gather_pat, //gather index pattern array
        const int* restrict scatter_pat, //scatter index pattern array
        int pat_len,  // length of index pattern
        int delta_gather, // stride between each gather
        int delta_scatter, // stride between each scatter
        int n) {// number of gathers

    for (int i = 0; i < n; i++) {
        double* tl = scatter + delta_scatter * i;
        double* sl = gather + delta_gather * i; 

        for (int j = 0; j < pat_len; j++) {
            tl[scatter_pat[j]] = sl[gather_pat[j]];
        }
    }

}

int main(int argc, char* argv[]) {
    #ifdef KERNEL_0
        double target[target_len * pat_len]; 
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
    #endif
    #ifdef KERNEL_1
        double target[target_size]; 
        // for (int i = 0; i < target_size; i++) {
        //     target[i] = 0;
        // }
        // setStats(1);
        scatter_smallbuf_serial(target, source, pat, pat_len, delta, n, source_len);
        // setStats(0);
        // Print the resulting matrix
        // for (int i = 0; i < target_size; i++) {
        //     // Accessing element in row-major order
        //     printf("%f ", target[i]);
        // }
    #endif
    #ifdef KERNEL_2
        double target[target_size];  
        setStats(1);
        sg_smallbuf_serial(source, target, gather_pat, scatter_pat, pat_len, delta_gather, delta_scatter, n);
        // for (int i = 0; i < target_size; i++) {
        //     // Accessing element in row-major order
        //     printf("%f ", target[i]);
        // }
       setStats(0);
    #endif
    return 0; 
}





