import os

from constants import COLORS
from runner import run
from sandpile import SymmetryMode

output_dir = 'borders'
amnt = 2**20

def sequence(sandpile, filename, symmetry_modes):
    size_path = os.path.join(output_dir, filename)

    sandpile.data[0,:] = amnt
    if symmetry_modes[0] == SymmetryMode.SYMMETRY_OFF:
        sandpile.data[sandpile.data.shape[0]-1,:] = amnt
    for x in range(sandpile.data.shape[0]):
        sandpile.data[x,0] = amnt
        if symmetry_modes[1] == SymmetryMode.SYMMETRY_OFF:
            sandpile.data[x,sandpile.data.shape[1]-1] = amnt
    print(sandpile.solve())

    sandpile.save_array(size_path)
    i = sandpile.to_image(COLORS)
    i.save(size_path + '.png')

run(output_dir, sequence)
