#define KERNEL_1 // 0 for gather, 1 for scatter, 2 for gather-scatter, 3 for multigather, 4 for multiscatter
const int delta = 10;
const int n = 128;
const int target_size = 21271;
const int source_len = 10;
const int pat_len = 7;
const int pat[7] = {
  0, 9900, 9999, 10000, 10001, 10100, 20000,
};

const double source[70] = {
  479, 862, 897, 572, 148, 312, 810, 38, 958, 683, 689, 967, 818, 840, 672, 94, 16, 468, 239, 743, 749, 535, 782, 191, 67, 671, 183, 623, 722, 760, 355, 616, 904, 345, 535, 441, 654, 501, 478, 682, 143, 59, 825, 134, 191, 506, 436, 654, 826, 38, 939, 485, 404, 376, 248, 356, 240, 232, 237, 282, 960, 556, 437, 296, 133, 955, 420, 883, 400, 392,
};

