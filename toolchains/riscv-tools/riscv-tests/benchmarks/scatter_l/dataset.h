#define KERNEL_1 // 0 for gather, 1 for scatter, 2 for gather-scatter, 3 for multigather, 4 for multiscatter
const int delta = 1;
const int n = 64;
const int target_size = 5064;
const int source_len = 5;
const int pat_len = 7;
const int pat[7] = {
  0, 2450, 2499, 2500, 2501, 2550, 5000,
};

const double source[35] = {
  229, 588, 241, 618, 534, 55, 185, 392, 501, 633, 3, 443, 459, 656, 664, 297, 932, 542, 546, 534, 563, 931, 950, 20, 13, 27, 190, 443, 959, 961, 690, 456, 838, 937, 93,
};

