#include "utils.h"

__kernel void scale_grid(const __global ELEM_TYPE *grid, __global ELEM_TYPE *dest_grid, const uint factor_x, const uint factor_y) {
    const size_t x = get_global_id(0);
    const size_t y = get_global_id(1);
    
    const size_t dest_width = GRID_WIDTH*factor_x;
    const size_t dest_height = GRID_HEIGHT*factor_y;
    
    const ELEM_TYPE amnt = grid[flat_idx(x, y, GRID_WIDTH, GRID_HEIGHT)];
    
    for (size_t off_x = 0; off_x < factor_x; off_x++) {
        for (size_t off_y = 0; off_y < factor_y; off_y++) {
            dest_grid[flat_idx(x*factor_x + off_x, y*factor_y + off_y, dest_width, dest_height)] = amnt;
        }
    }
}

__kernel void reshape_grid(const __global ELEM_TYPE *grid, __global ELEM_TYPE *dest_grid, const uint dest_width, const uint off_x, const uint dest_height, const uint off_y) {
    const size_t x = get_global_id(0);
    const size_t y = get_global_id(1);
    
    const ELEM_TYPE amnt = grid[flat_idx(x, y, GRID_WIDTH, GRID_HEIGHT)];
    
    dest_grid[flat_idx(x+off_x, y+off_y, dest_width, dest_height)] = amnt;
}
