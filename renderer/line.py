def get_line_coords(start, end):
    """
    Bresenham's line drawing algorithm.
    The implementations is symmetric, i.e. it returns the same sequence of
    coordinates for (start, end) and (end, start)
        :param start: (x, y)-coordinate tuple of starting point
        :param end: (x, y)-coordinate tuple of ending point
        :returns: tuples of (x, y)-coordinates for the pixels representing the
                  line
    """
    coords = []

    x1, y1 = start
    x2, y2 = end

    rotated = False
    # If the line is steep (i.e. y grows faster than x), we rotate the line.
    # The goal is to always end up with a line that has a |slope| <= 1, for the
    # rest of the algorithm
    if abs(y2 - y1) > abs(x2 - x1):
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        rotated = True

    # To ensure the same sequence of points is returned regardless of the order
    # in which the start and end points are passed, we always have the point
    # with the smaller x-coordinate as the first argument for the rest of the
    # algorithm
    if x1 > x2:
        (x1, x2) = (x2, x1)
        (y1, y2) = (y2, y1)

    dx = x2 - x1
    dy = y2 - y1

    error_inc = abs(2 * dy)
    error_dec = 2 * dx
    error = error_inc - dx
    y = y1
    y_step = 1 if dy > 0 else -1
    for x in range(x1, x2 + 1):
        # For |slopes| > 1, the line is rotated, so the coordinates need to be
        # swapped accordingly
        coords.append((x, y) if not rotated else (y, x))
        if error > 0:
            y += y_step
            error -= error_dec
        error += error_inc
    return coords


if __name__ == "__main__":
    from PIL import Image

    RED = (255, 0, 0)
    WHITE = (255, 255, 255)

    canvas = Image.new("RGB", (100, 100))

    def draw(canvas, coords, color=RED):
        for x, y in coords:
            # The canvas' (0, 0) is in the top left corner. We want it to be in
            # the bottom left
            canvas.putpixel((x, 99 - y), color)
        return canvas

    draw(canvas, get_line_coords((13, 20), (80, 40)))
    draw(canvas, get_line_coords((20, 13), (40, 80)))
    draw(canvas, get_line_coords((80, 40), (13, 20)), WHITE)
    canvas.show()
