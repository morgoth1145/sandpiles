#include "utils.h"

inline int_type adjusted_self(int_type amnt) {
    return amnt % 4;
}

inline int_type adjusted_neighbor(int_type amnt) {
    return amnt / 4;
}

__kernel void run_iteration(__global int_type *grid, __global int_type *new_grid)
{
    const size_t x = get_global_id(0);
    const size_t y = get_global_id(1);
    
    const size_t WIDTH = get_global_size(0);
    const size_t HEIGHT = get_global_size(1);
    
    int_type amnt = adjusted_self(grid[flat_idx(x, y, WIDTH, HEIGHT)]);
    if (x > 0) {
        amnt += adjusted_neighbor(grid[flat_idx(x-1, y, WIDTH, HEIGHT)]);
    }
    if (x < WIDTH-1) {
        amnt += adjusted_neighbor(grid[flat_idx(x+1, y, WIDTH, HEIGHT)]);
    }
    if (y > 0) {
        amnt += adjusted_neighbor(grid[flat_idx(x, y-1, WIDTH, HEIGHT)]);
    }
    if (y < HEIGHT-1) {
        amnt += adjusted_neighbor(grid[flat_idx(x, y+1, WIDTH, HEIGHT)]);
    }
    new_grid[flat_idx(x, y, WIDTH, HEIGHT)] = amnt;
}
