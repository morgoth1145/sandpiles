import os
import time

import numpy
import pyopencl as cl
from PIL import Image

import pyopencl.array

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

    def create_sandpile(self, shape):
        return _Sandpile(self._ctx, self._queue, shape)

class _Sandpile:
    def __init__(self, ctx, queue, shape):
        self._ctx = ctx
        self._queue = queue

        with open('sandpiles.cl') as f:
            program = cl.Program(self._ctx, f.read())

        macros = []
        options = ['-D' + m for m in macros]
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

        iterations = 0
        adaptive_iterations = 1

        grid = self.data
        new_grid = pyopencl.array.empty(self._queue,
                                        grid.shape,
                                        grid.dtype)

        self._program.run_iteration(self._queue,
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
                iteration_event = self._program.run_iteration(self._queue,
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
        img_creator = _ImageCreator(self._ctx, self._queue, colors)

        yield img_creator.create_image(self.data)

        grid = self.data
        new_grid = pyopencl.array.empty(self._queue,
                                        grid.shape,
                                        grid.dtype)

        while True:
            self._program.run_iteration(self._queue,
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
        return _ImageCreator(self._ctx, self._queue, colors).create_image(self.data)

    def save_array(self, filename):
        numpy.savez_compressed(filename,
                               a=self.data.get())

class _ImageCreator:
    def __init__(self, ctx, queue, colors):
        self._ctx = ctx
        self._queue = queue

        red = [str(c[0]) for c in colors]
        green = [str(c[1]) for c in colors]
        blue = [str(c[2]) for c in colors]

        with open('to_image.cl') as f:
            program = f.read()

        program = program.replace('RED_VALS',
                                  ', '.join(str(c[0])
                                            for c in colors))
        program = program.replace('GREEN_VALS',
                                  ', '.join(str(c[1])
                                            for c in colors))
        program = program.replace('BLUE_VALS',
                                  ', '.join(str(c[2])
                                            for c in colors))
        program = program.replace('COLOR_COUNT',
                                  str(len(colors)))

        self._program = cl.Program(self._ctx, program).build()

    def create_image(self, data):
        shape = data.shape

        img_data = pyopencl.array.empty(self._queue,
                                        shape + (3,),
                                        numpy.uint8)

        self._program.to_image(self._queue,
                               shape,
                               None,
                               data.base_data,
                               img_data.base_data)

        return Image.fromarray(img_data.get(), 'RGB')
