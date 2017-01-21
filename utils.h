typedef unsigned int int_type;

inline size_t flat_idx(size_t x, size_t y, size_t WIDTH, size_t HEIGHT)
{
    return x*HEIGHT + y;
}
