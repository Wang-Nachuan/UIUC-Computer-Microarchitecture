#define KERNEL_2 // 0 for gather, 1 for scatter, 2 for gather-scatter, 3 for multigather, 4 for multiscatter
const int delta_gather = 2;
const int delta_scatter = 3;
const int n = 2;
const int target_size = 66;
const int pat_len = 8;
const int gather_pat[8] = {
  0, 3, 6, 9, 12, 15, 18, 21,
};

const int scatter_pat[8] = {
  0, 8, 16, 24, 32, 40, 48, 56,
};

const double source[28] = {
  931, 921, 279, 129, 723, 299, 56, 41, 811, 265, 889, 530, 791, 330, 712, 420, 697, 615, 579, 283, 271, 466, 215, 452, 441, 285, 957, 347,
};

