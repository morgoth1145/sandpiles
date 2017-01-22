import os

from constants import COLORS
from sandpile import Sandpiles, SymmetryMode
from tee import Tee

target_radius = 25

os.environ['PYOPENCL_CTX'] = '0'

output_dir = 'infinite-trickle'

sandpiles = Sandpiles()

os.makedirs(output_dir, exist_ok=True)

def save(directory, num, sandpile):
    sandpile.save(os.path.join(directory, str(num)))

    i = sandpile.to_image(COLORS)
    i.save(os.path.join(directory, '%d.png' % num))

def get_radius(sandpile):
    arr = sandpile.data.get()

    idx = 0
    while not arr[idx,-1]:
        idx += 1

    return sandpile.data.shape[0]-idx

def get_next_best_radius(new_radius):
    return ((new_radius+7)//8) * 8

with Tee(os.path.join(output_dir, 'log.txt'), 'a+'):
    symmetry_modes = (
        SymmetryMode.SYMMETRY_ON_WITH_OVERLAP,
        SymmetryMode.SYMMETRY_ON_WITH_OVERLAP
    )

    sandpile = sandpiles.create_sandpile(shape=(8, 8),
                                         symmetry_modes=symmetry_modes)
    sandpile.data[-1, -1] = 1

    save(output_dir, 0, sandpile)

    for count in range(1, target_radius+1):
        saved_sandpile = sandpiles.try_load_sandpile(os.path.join(output_dir, str(count)))
        if saved_sandpile is not None:
            sandpile = saved_sandpile
            continue

        radius = get_radius(sandpile)
        new_radius = 3*radius//2
        new_radius = get_next_best_radius(new_radius)

        offset = new_radius - sandpile.data.shape[0]

        if offset > 0:
            print('Growing grid from %d to %d' % (sandpile.data.shape[0],
                                                  new_radius))
            sandpile = sandpiles.reshape_sandpile(sandpile,
                                                  (new_radius, new_radius),
                                                  (offset, offset))

        sandpile.data *= 2
        print(count, sandpile.solve())

        save(output_dir, count, sandpile)
