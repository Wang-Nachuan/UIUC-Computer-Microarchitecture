#define KERNEL_0; // 0 for gather, 1 for scatter, 2 for gather-scatter, 3 for multigather, 4 for multiscatter
const int delta = 4;
const int n = 8;
const int target_len = 2;
const int pat_len = 10;
const int pat[10] = {
  0, 1, 11, 33, 34, 35, 36, 37, 38, 39,
};

const double source[68] = {
  317, 722, 404, 393, 405, 222, 480, 438, 2, 367, 758, 25, 303, 127, 467, 961, 287, 383, 555, 904, 544, 996, 565, 603, 276, 593, 874, 290, 895, 160, 784, 638, 93, 928, 40, 506, 646, 861, 944, 719, 664, 553, 451, 685, 783, 92, 246, 164, 651, 558, 60, 56, 284, 744, 471, 897, 667, 916, 62, 965, 628, 764, 307, 22, 195, 111, 650, 472,
};

