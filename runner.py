import json
import os

from sandpile import Sandpiles, SymmetryMode
from tee import Tee

os.environ['PYOPENCL_CTX'] = '0'

with open('queue.json') as f:
    queue = json.load(f)

sandpiles = Sandpiles()

def run(output_dir, sequence_fn):
    os.makedirs(output_dir, exist_ok=True)

    with Tee(os.path.join(output_dir, 'log.txt'), 'w+'):
        for item in queue:
            if not item.get('active', True):
                continue

            symmetry_modes = (
                SymmetryMode[item.get('x_symmetry_mode', 'SYMMETRY_OFF')],
                SymmetryMode[item.get('y_symmetry_mode', 'SYMMETRY_OFF')]
            )

            print(item['filename'])

            sandpile = sandpiles.create_sandpile(shape=tuple(item['shape']),
                                                 symmetry_modes=symmetry_modes)

            sequence_fn(sandpile, item['filename'], symmetry_modes)

            print('-' * 75)
