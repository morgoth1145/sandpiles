#include "utils.h"

__constant uchar red[COLOR_COUNT] = {RED_VALS};
__constant uchar green[COLOR_COUNT] = {GREEN_VALS};
__constant uchar blue[COLOR_COUNT] = {BLUE_VALS};

__kernel void to_image(const __global int_type *grid, __global uchar *image)
{
    const size_t x = get_global_id(0);
    const size_t y = get_global_id(1);
    
    const size_t WIDTH = get_global_size(0);
    const size_t HEIGHT = get_global_size(1);
    
    const size_t idx = flat_idx(x, y, WIDTH, HEIGHT);
    
    int_type amnt = grid[idx];
    amnt = (amnt < 0) ? 0 : amnt;
    amnt = (amnt > COLOR_COUNT-1) ? COLOR_COUNT-1 : amnt;
    
    image[3*idx+0] = red[amnt];
    image[3*idx+1] = green[amnt];
    image[3*idx+2] = blue[amnt];
}
