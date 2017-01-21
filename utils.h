inline size_t flat_idx(size_t x, size_t y, size_t width, size_t height)
{
    return x*height + y;
}

#define SYMMETRY_OFF 0
#define SYMMETRY_ON 1
#define SYMMETRY_ON_WITH_OVERLAP 2

inline ELEM_TYPE get_left_neighbor(const __global ELEM_TYPE *grid, size_t x, size_t y) {
    return (x > 0)
        ? grid[flat_idx(x-1, y, GRID_WIDTH, GRID_HEIGHT)]
        : 0;
}

inline ELEM_TYPE get_right_neighbor(const __global ELEM_TYPE *grid, size_t x, size_t y) {
    return (x < GRID_WIDTH-1)
        ? grid[flat_idx(x+1, y, GRID_WIDTH, GRID_HEIGHT)]
#if SYMMETRY_OFF == X_SYMMETRY_MODE
        : 0;
#elif SYMMETRY_ON == X_SYMMETRY_MODE
        : grid[flat_idx(x, y, GRID_WIDTH, GRID_HEIGHT)];
#elif SYMMETRY_ON_WITH_OVERLAP == X_SYMMETRY_MODE
        : grid[flat_idx(x-1, y, GRID_WIDTH, GRID_HEIGHT)];
#endif
}

inline ELEM_TYPE get_top_neighbor(const __global ELEM_TYPE *grid, size_t x, size_t y) {
    return (y > 0)
        ? grid[flat_idx(x, y-1, GRID_WIDTH, GRID_HEIGHT)]
        : 0;
}

inline ELEM_TYPE get_bottom_neighbor(const __global ELEM_TYPE *grid, size_t x, size_t y) {
    return (y < GRID_HEIGHT-1)
        ? grid[flat_idx(x, y+1, GRID_WIDTH, GRID_HEIGHT)]
#if SYMMETRY_OFF == Y_SYMMETRY_MODE
        : 0;
#elif SYMMETRY_ON == Y_SYMMETRY_MODE
        : grid[flat_idx(x, y, GRID_WIDTH, GRID_HEIGHT)];
#elif SYMMETRY_ON_WITH_OVERLAP == Y_SYMMETRY_MODE
        : grid[flat_idx(x, y-1, GRID_WIDTH, GRID_HEIGHT)];
#endif
}
