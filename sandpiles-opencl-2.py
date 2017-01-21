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

output_dir = 'borders'
amnt = 2**20

sandpiles = Sandpiles()

os.makedirs(output_dir, exist_ok=True)

with Tee(os.path.join(output_dir, 'log.txt'), 'w+'):
    for item in queue:
        if not item.get('active', True):
            continue

        print(item['filename'])

        sandpile = sandpiles.create_sandpile(shape=tuple(item['shape']))

        size_path = os.path.join(output_dir, item['filename'])

        sandpile.data[0,:] = amnt
        sandpile.data[sandpile.data.shape[0]-1,:] = amnt
        for x in range(sandpile.data.shape[0]):
            sandpile.data[x,0] = amnt
            sandpile.data[x,item['shape'][1]-1] = amnt
        print(sandpile.solve())

        i = sandpile.to_image(COLORS)
        i.save(size_path + '.png')
        sandpile.save_array(size_path)

        print('-' * 75)
