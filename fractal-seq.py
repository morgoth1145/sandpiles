import os

from constants import COLORS
from runner import run

output_dir = 'fractals'

def sequence(sandpile, filename, symmetry_modes):
    size_directory = os.path.join(output_dir, filename)
    os.makedirs(size_directory, exist_ok=True)

    sandpile.save_array(os.path.join(size_directory, '00'))
    sandpile.to_image(COLORS).save(os.path.join(size_directory, '00.png'))

    for count in range(1, 21):
        sandpile.data += 1
        print(count, sandpile.solve())

        sandpile.save_array(os.path.join(size_directory, '%02d' % count))
        i = sandpile.to_image(COLORS)
        i.save(os.path.join(size_directory, '%02d.png' % count))

##    sandpile.data += 4
##
##    print(sandpile.solve())
##
##    i = sandpile.to_image(COLORS)
##    i.save(os.path.join(output_dir, filename + '.png'))
##
##    sandpile.save_array(os.path.join(output_dir, filename]))
##
##    
##
##    gif_directory = os.path.join(output_dir, filename)
##    os.makedirs(gif_directory, exist_ok=True)
##
##    for idx, images in enumerate(chunker(sandpile.gen_solve_frames(COLORS),
##                                         2**10)):
##        images[0].save(os.path.join(gif_directory, '%d.gif' % idx),
##                       save_all=True,
##                       append_images=list(images[1:]),
##                       duration=1,
##                       optimize=True)

run('main_queue.json', output_dir, sequence)
