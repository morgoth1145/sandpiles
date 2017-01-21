#include "utils.h"

inline INT_TYPE adjusted_self(INT_TYPE amnt) {
    return amnt % 4;
}

inline INT_TYPE adjusted_neighbor(INT_TYPE amnt) {
    return amnt / 4;
}

__kernel void run_iteration(const __global INT_TYPE *grid, __global INT_TYPE *new_grid) {
    const size_t x = get_global_id(0);
    const size_t y = get_global_id(1);
    
    const size_t self_idx = flat_idx(x, y, GRID_WIDTH, GRID_HEIGHT);
    
    INT_TYPE amnt = adjusted_self(grid[self_idx]);
    amnt += adjusted_neighbor(get_left_neighbor(grid, x, y));
    amnt += adjusted_neighbor(get_right_neighbor(grid, x, y));
    amnt += adjusted_neighbor(get_top_neighbor(grid, x, y));
    amnt += adjusted_neighbor(get_bottom_neighbor(grid, x, y));
    new_grid[self_idx] = amnt;
}
