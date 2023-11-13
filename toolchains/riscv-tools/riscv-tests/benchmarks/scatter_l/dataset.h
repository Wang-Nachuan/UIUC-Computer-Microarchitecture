#define KERNEL_1 // 0 for gather, 1 for scatter, 2 for gather-scatter, 3 for multigather, 4 for multiscatter
const int delta = 8;
const int n = 10;
const int target_size = 273;
const int source_len = 4;
const int pat_len = 5;
const int pat[5] = {
  0, 99, 100, 101, 200,
};

const double source[20] = {
  250, 113, 970, 749, 112, 793, 396, 637, 841, 875, 13, 299, 285, 173, 372, 959, 682, 849, 854, 343,
};

