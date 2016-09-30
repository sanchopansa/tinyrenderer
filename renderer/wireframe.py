import itertools as it

import renderer.lib.objreader as reader


def get_wireframe_coords(canvas_width, canvas_height, vertices, faces):
    """
    Return the coordinates of a mesh

    :param canvas_width: the width of the canvas on which the mesh must be
                         drawn
    :param canvas_height: the height of the canvas on which the mesh must be
                          drawn
    :param vertices: the complete set of vertices from the Wavefront obj file
                     describing the mesh
    :param faces: the faces constituting the mesh
    :return: a set of 2-tuples, containing the (x, y) coordinates of the pixels
             constituting the mesh
    """
    coords = set()
    scale = lambda val: lambda dim: int(round((val + 1) * dim / 2))
    scale_x = lambda x: scale(x)(canvas_width - 1)
    scale_y = lambda y: scale(y)(canvas_height - 1)

    for face in faces:
        f_vertices = reader.face_to_vertices(face, vertices)
        for v1, v2 in zip(f_vertices,
                          it.chain(f_vertices[1:], [f_vertices[0]])):
            line = ((scale_x(v1[0]), scale_y(v1[1])),
                    (scale_x(v2[0]), scale_y(v2[1])))
            for x, y in get_line_coords(*line):
                coords.add((x, y))

    return coords


if __name__ == "__main__":
    from renderer.line import get_line_coords

    from PIL import Image

    vertices, _, _, faces = reader.read_obj(
        "/home/sancho/src/tinyrenderer/renderer/african_head.obj")
    canvas = Image.new("RGB", (500, 500))
    for x, y in get_wireframe_coords(500, 500, vertices, faces):
        try:
            canvas.putpixel((x, 499 - y), (255, 255, 255))
        except IndexError:
            print "Invalid coordinate: {}".format((x, y))
    canvas.show()
