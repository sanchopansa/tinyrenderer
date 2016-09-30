def read_obj(filename):
    """
    Read a Wavefront obj file. Recognized lines are vertices, vertex normals,
    vertex textures and faces; all other lines are ignored
    Note that no error checking or special logic is implemented and files
    containing partial information (e.g. no entries for vertex textures) will
    not be parsed correctly.

    :param filename: the path to the Wavefront object file
    :return: a tuple of lists (vertices, vertex_textures, vertex_normals,
             faces) in which the first three lists consist of (x, y, z)
             coordinates and faces consists of 3-tuple of indexes (with each
             index being a 3-tuple itself) pointing to the elements inside
             vertices, vertex_textures and vertex_normals building the face.
    """
    vertices = []
    vertex_textures = []
    vertex_normals = []
    faces = []

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            # Skip empty and comment lines
            if not line or line.startswith("#"):
                pass
            elif line.startswith("vt"):
                vertex_textures.append(parse_vertex(line))
            elif line.startswith("vn"):
                vertex_normals.append(parse_vertex(line))
            elif line.startswith("v"):
                vertices.append(parse_vertex(line))
            elif line.startswith("f"):
                faces.append(parse_face(line))
            else:
                print "Skipping line '{}'".format(line)

    return vertices, vertex_textures, vertex_normals, faces


def parse_vertex(line):
    """
    Parse a vertex from a line in a Wavefront obj file
    :param line: a line from a Waverfron obj file
    :return: 3-tuple of (x, y, z) coordinates of the vertex
    """
    return tuple(float(x) for x in line.split()[1:])


def parse_face(line):
    """
    Parse a face from a line in a Wavefront obj file.

    :param line: a line from a Wavefront obj file containing a face
    :return: tuple of 3-tuples, with each 3-tuple containing the vertex
             indices corresponding to the geometry, texture and normals,
             respectively
    """
    # Remove the leading 'f' from the line
    x_vertices, y_vertices, z_vertices = line.split()[1:]
    to_index = lambda x: int(x) - 1
    return tuple(zip(map(to_index, x_vertices.split("/")),
                     map(to_index, y_vertices.split("/")),
                     map(to_index, z_vertices.split("/"))))


def face_to_vertices(face, vertices):
    """
    Given the indices of a face and the complete set of vertices from the
    Wavefront obj file descriging it, returns the vertices corresponding to the
    geometry of the face.
    :param face: a 3-tuple of 3-tuples of indices as returned by read_obj
    :param vertices: a list of 3-tuples containing the (x, y, z) coordinates of
                     all vertices from the Waveform obj file descriging the
                     face
    """
    vertex_indices, _, _ = face
    return tuple(vertices[i] for i in vertex_indices)


if __name__ == "__main__":
    print parse_face("f 1/2/3 4/5/6 7/8/9")
    print parse_vertex("vn 43.2 12.01 0.1234")
    print face_to_vertices(
        ((1, 0, 2), (0, 0, 1), (1, 2, 3)),
        ((0, 0, 0), (1, 1, 1), (2, 2, 2)))
