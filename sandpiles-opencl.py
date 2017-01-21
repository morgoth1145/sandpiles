import json
import os

from sandpile import Sandpiles
from tee import Tee
from utils import chunker

os.environ['PYOPENCL_CTX'] = '0'

COLORS = [
    (0, 0, 255), # BLUE
    (255, 255, 0), # YELLOW
    (0, 255, 255), # CYAN
    (139, 69, 19), # SADDLEBROWN
    (255, 255, 255), # WHITE
]

with open('queue.json') as f:
    queue = json.load(f)

output_dir = 'fractals'

sandpiles = Sandpiles()

os.makedirs(output_dir, exist_ok=True)

with Tee(os.path.join(output_dir, 'log.txt'), 'w+'):
    for item in queue:
        if not item.get('active', True):
            continue

        print(item['filename'])

        sandpile = sandpiles.create_sandpile(shape=tuple(item['shape']))

        size_directory = os.path.join(output_dir, item['filename'])
        os.makedirs(size_directory, exist_ok=True)

        sandpile.to_image(COLORS).save(os.path.join(size_directory, '00.png'))
        sandpile.save_array(os.path.join(size_directory, '00'))

        for count in range(1, 21):
            sandpile.data += 1
            print(count, sandpile.solve())

            i = sandpile.to_image(COLORS)
            i.save(os.path.join(size_directory, '%02d.png' % count))
            sandpile.save_array(os.path.join(size_directory, '%02d' % count))

##        sandpile.data += 4

##        print(sandpile.solve())
##
##        i = sandpile.to_image(COLORS)
##        i.save(os.path.join(output_dir, item['filename'] + '.png'))
##
##        sandpile.save_array(os.path.join(output_dir, item['filename']))

        

##        gif_directory = os.path.join(output_dir, item['filename'])
##        os.makedirs(gif_directory, exist_ok=True)
##
##        for idx, images in enumerate(chunker(sandpile.gen_solve_frames(COLORS),
##                                             2**10)):
##            images[0].save(os.path.join(gif_directory, '%d.gif' % idx),
##                           save_all=True,
##                           append_images=list(images[1:]),
##                           duration=1,
##                           optimize=True)

        print('-' * 75)
