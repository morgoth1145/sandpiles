import os

from constants import COLORS
from runner import run

output_dir = 'fractals'

def sequence(sandpile, filename, symmetry_modes):
    size_directory = os.path.join(output_dir, filename)
    os.makedirs(size_directory, exist_ok=True)

    sandpile.save(os.path.join(size_directory, '00'))
    sandpile.to_image(COLORS).save(os.path.join(size_directory, '00.png'))

    for count in range(1, 21):
        sandpile.data += 1
        print(count, sandpile.solve())

        sandpile.save(os.path.join(size_directory, '%02d' % count))
        i = sandpile.to_image(COLORS)
        i.save(os.path.join(size_directory, '%02d.png' % count))

run('main_queue.json', output_dir, sequence)
