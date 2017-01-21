#include "utils.h"

__constant uchar red[COLOR_COUNT] = {RED_VALS};
__constant uchar green[COLOR_COUNT] = {GREEN_VALS};
__constant uchar blue[COLOR_COUNT] = {BLUE_VALS};

inline void put_pixel_colors(__global uchar *image, const size_t image_idx, const ELEM_TYPE amnt) {
    image[3*image_idx+0] = red[amnt];
    image[3*image_idx+1] = green[amnt];
    image[3*image_idx+2] = blue[amnt];
}

__kernel void to_image(const __global ELEM_TYPE *grid, __global uchar *image) {
    const size_t x = get_global_id(0);
    const size_t y = get_global_id(1);
    
    ELEM_TYPE amnt = grid[flat_idx(x, y, GRID_WIDTH, GRID_HEIGHT)];
    amnt = (amnt < 0) ? 0 : amnt;
    amnt = (amnt > COLOR_COUNT-1) ? COLOR_COUNT-1 : amnt;
    
    put_pixel_colors(image, flat_idx(x, y, IMAGE_WIDTH, IMAGE_HEIGHT), amnt);

#if SYMMETRY_OFF != X_SYMMETRY_MODE
    const size_t symmetric_x = IMAGE_WIDTH-x-1;
    put_pixel_colors(image, flat_idx(symmetric_x, y, IMAGE_WIDTH, IMAGE_HEIGHT), amnt);
#endif
    
#if SYMMETRY_OFF != Y_SYMMETRY_MODE
    const size_t symmetric_y = IMAGE_HEIGHT-y-1;
    put_pixel_colors(image, flat_idx(x, symmetric_y, IMAGE_WIDTH, IMAGE_HEIGHT), amnt);
#endif

#if SYMMETRY_OFF != X_SYMMETRY_MODE && SYMMETRY_OFF != Y_SYMMETRY_MODE
    put_pixel_colors(image, flat_idx(symmetric_x, symmetric_y, IMAGE_WIDTH, IMAGE_HEIGHT), amnt);
#endif
}
