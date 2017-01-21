import enum
import os
import time

import numpy
import pyopencl as cl
from PIL import Image

import pyopencl.array

class SymmetryMode(enum.Enum):
    SYMMETRY_OFF = 0
    SYMMETRY_ON = 1
    SYMMETRY_ON_WITH_OVERLAP = 2

def isqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

class Sandpiles:
    def __init__(self):
        self._ctx = cl.create_some_context()
        self._queue = cl.CommandQueue(self._ctx)

    def create_sandpile(self, shape, symmetry_modes):
        return _Sandpile(self._ctx, self._queue, shape, symmetry_modes)

def _gen_macros(shape, symmetry_modes):
    yield 'INT_TYPE=unsigned int'
    yield 'GRID_WIDTH=%d' % shape[0]
    yield 'GRID_HEIGHT=%d' % shape[1]
    yield 'X_SYMMETRY_MODE=%s' % symmetry_modes[0].name
    yield 'Y_SYMMETRY_MODE=%s' % symmetry_modes[1].name

def _macros_to_options(macros):
    return ['-D' + m for m in macros]

class _Sandpile:
    def __init__(self, ctx, queue, shape, symmetry_modes):
        self._ctx = ctx
        self._queue = queue
        self._symmetry_modes = symmetry_modes

        with open('sandpile.cl') as f:
            program = cl.Program(self._ctx, f.read())

        options = _macros_to_options(_gen_macros(shape, symmetry_modes))
        self._program = program.build(options=options)

        from pyopencl.reduction import ReductionKernel
        self._diff_krnl = ReductionKernel(self._ctx,
                                          numpy.uint32,
                                          neutral='0',
                                          reduce_expr='a+b',
                                          map_expr='grid[i]!=new_grid[i]',
                                          arguments='__global unsigned int *grid, __global unsigned int *new_grid')

        self.data = pyopencl.array.zeros(self._queue,
                                         shape,
                                         numpy.uint32)

    def solve(self):
        start = time.perf_counter()

        run_iter_krnl = self._program.run_iteration

        iterations = 0
        adaptive_iterations = 1

        grid = self.data
        new_grid = pyopencl.array.empty(self._queue,
                                        grid.shape,
                                        grid.dtype)

        run_iter_krnl(self._queue,
                      grid.shape,
                      None,
                      grid.base_data,
                      new_grid.base_data)
        grid, new_grid = new_grid, grid
        iterations += 1

        while True:
            diff_evnt = self._diff_krnl(grid,
                                        new_grid,
                                        queue=self._queue)

            for _ in range(adaptive_iterations):
                iteration_event = run_iter_krnl(self._queue,
                                                grid.shape,
                                                None,
                                                grid.base_data,
                                                new_grid.base_data)
                grid, new_grid = new_grid, grid
                iterations += 1

            diff_count = diff_evnt.get()
            if 0 == diff_count:
                self.data = new_grid
                iteration_event.wait()
                return iterations, time.perf_counter()-start
            adaptive_iterations = isqrt(diff_count)

    def gen_solve_frames(self, colors):
        img_creator = self._get_image_creator(colors)

        run_iter_krnl = self._program.run_iteration

        yield img_creator.create_image(self.data)

        grid = self.data
        new_grid = pyopencl.array.empty(self._queue,
                                        grid.shape,
                                        grid.dtype)

        while True:
            run_iter_krnl(self._queue,
                          self.data.shape,
                          None,
                          grid.base_data,
                          new_grid.base_data)
            grid, new_grid = new_grid, grid

            if 0 == self._diff_krnl(grid,
                                    new_grid,
                                    queue=self._queue).get():
                self.data = grid
                return

            yield img_creator.create_image(grid)

    def to_image(self, colors):
        return self._get_image_creator(colors).create_image(self.data)

    def save_array(self, filename):
        numpy.savez_compressed(filename,
                               a=self.data.get())

    def _get_image_creator(self, colors):
        return _ImageCreator(self._ctx,
                             self._queue,
                             self.data.shape,
                             self._symmetry_modes,
                             colors)

class _ImageCreator:
    def __init__(self, ctx, queue, shape, symmetry_modes, colors):
        self._ctx = ctx
        self._queue = queue
        self._shape = shape

        if symmetry_modes[0] == SymmetryMode.SYMMETRY_OFF:
            image_width = shape[0]
        elif symmetry_modes[0] == SymmetryMode.SYMMETRY_ON:
            image_width = 2*shape[0]
        elif symmetry_modes[0] == SymmetryMode.SYMMETRY_ON_WITH_OVERLAP:
            image_width = 2*shape[0]-1

        if symmetry_modes[1] == SymmetryMode.SYMMETRY_OFF:
            image_height = shape[1]
        elif symmetry_modes[1] == SymmetryMode.SYMMETRY_ON:
            image_height = 2*shape[1]
        elif symmetry_modes[1] == SymmetryMode.SYMMETRY_ON_WITH_OVERLAP:
            image_height = 2*shape[1]-1

        red = [str(c[0]) for c in colors]
        green = [str(c[1]) for c in colors]
        blue = [str(c[2]) for c in colors]

        with open('to_image.cl') as f:
            program = f.read()

        macros = list(_gen_macros(shape, symmetry_modes))
        macros.append('COLOR_COUNT=%d' % len(colors))
        macros.append('RED_VALS=%s' % ', '.join(red))
        macros.append('GREEN_VALS=%s' % ', '.join(green))
        macros.append('BLUE_VALS=%s' % ', '.join(blue))
        macros.append('IMAGE_WIDTH=%d' % image_width)
        macros.append('IMAGE_HEIGHT=%s' % image_height)
        options = _macros_to_options(macros)

        self._program = cl.Program(self._ctx, program).build(options=options)

        self._to_image_krnl = self._program.to_image

        self._data = pyopencl.array.empty(self._queue,
                                          (image_width, image_height, 3),
                                          numpy.uint8)

    def create_image(self, data):
        shape = data.shape

        assert(self._shape == shape)

        self._to_image_krnl(self._queue,
                            shape,
                            None,
                            data.base_data,
                            self._data.base_data)

        return Image.fromarray(self._data.get(), 'RGB')
