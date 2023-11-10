const int kernel = 0; // 0 for UNIFORM, 1 for MS1, 2 for LAPLACIAN
const int delta = 8;
const int n = 2;
const int target_len = 2;
const int pat_len = 8;
const int pat[8] = {
  0, 1, 2, 3, 4, 5, 6, 7,
};

const double source[16] = {
  533, 549, 563, 950, 201, 365, 161, 439, 262, 283, 181, 876, 283, 886, 663, 968,
};

