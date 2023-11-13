#define KERNEL_0; // 0 for gather, 1 for scatter, 2 for gather-scatter, 3 for multigather, 4 for multiscatter
const int delta = 4;
const int n = 8;
const int target_len = 2;
const int pat_len = 16;
const int pat[16] = {
  0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30,
};

const double source[59] = {
  780, 298, 641, 857, 345, 826, 833, 574, 135, 60, 177, 737, 258, 14, 435, 946, 458, 176, 250, 696, 145, 259, 193, 478, 566, 742, 402, 906, 550, 240, 426, 832, 66, 593, 428, 314, 604, 317, 808, 16, 468, 499, 342, 56, 438, 677, 860, 987, 407, 281, 504, 24, 319, 617, 747, 621, 805, 846, 49,
};

