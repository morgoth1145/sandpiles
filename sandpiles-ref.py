import heapq

grid = {}

for i in range(15):
    queue = [(2**i, (0, 0))]

    radius = 0

    while len(queue):
        count, pos = heapq.heappop(queue)
        count += grid.pop(pos, 0)
        spill, rem = divmod(count, 4)
        grid[pos] = rem
        x, y = pos
        new_radius = max(radius, abs(x), abs(y))
        if new_radius > radius:
            radius = new_radius
        if not spill:
            continue
        for pos in [(x-1, y),
                    (x+1, y),
                    (x, y-1),
                    (x, y+1)]:
            count = spill + grid.pop(pos, 0)
            heapq.heappush(queue, (count, pos))

    print(i, radius)
