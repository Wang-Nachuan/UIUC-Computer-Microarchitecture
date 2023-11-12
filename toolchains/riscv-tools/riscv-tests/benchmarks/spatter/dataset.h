#define KERNEL_1 // 0 for gather, 1 for scatter, 2 for gather-scatter, 3 for multigather, 4 for multiscatter
const int delta = 2;
const int n = 2;
const int target_size = 17;
const int source_len = 2;
const int pat_len = 8;
const int pat[8] = {
  0, 2, 4, 6, 8, 10, 12, 14,
};

const double source[16] = {
  734, 249, 214, 977, 816, 435, 442, 776, 626, 611, 360, 122, 411, 102, 866, 812,
};

