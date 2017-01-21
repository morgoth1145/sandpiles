import os

from constants import COLORS
from runner import run

output_dir = 'trickle'
amnt = 2**30

def sequence(sandpile, filename, symmetry_modes):
    size_path = os.path.join(output_dir, filename)

    sandpile.data[-1,-1] = amnt
    print(sandpile.solve())

    sandpile.save_array(size_path)
    i = sandpile.to_image(COLORS)
    i.save(size_path + '.png')

run('trickle_queue.json', output_dir, sequence)
