def read_obj(filename):
    vertices = []
    texture_vertices = []
    normal_vertices = []
    faces = []

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            # Skip empty and comment lines
            if not line or line.startswith("#"):
                pass
            elif line.startswith("vt"):
                texture_vertices.append(parse_vertex(line))
            elif line.startswith("vn"):
                normal_vertices.append(parse_vertex(line))
            elif line.startswith("v"):
                vertices.append(parse_vertex(line))
            elif line.startswith("f"):
                faces.append(parse_face(line))
            else:
                print "Skipping line '{}'".format(line)

    return vertices, texture_vertices, normal_vertices, faces


def parse_vertex(line):
    return tuple(float(x) for x in line.split()[1:])


def parse_face(line):
    # Remove the leading 'f' from the line
    x_vertices, y_vertices, z_vertices = line.split()[1:]
    to_index = lambda x: int(x) - 1
    return tuple(zip(map(to_index, x_vertices.split("/")),
                     map(to_index, y_vertices.split("/")),
                     map(to_index, z_vertices.split("/"))))


def face_to_vertices(face, vertices):
    vertex_indices, _, _ = face
    return tuple(vertices[i] for i in vertex_indices)


if __name__ == "__main__":
    print parse_face("f 1/2/3 4/5/6 7/8/9")
    print parse_vertex("vn 43.2 12.01 0.1234")
    print face_to_vertices(
        ((1, 0, 2), (0, 0, 1), (1, 2, 3)),
        ((0, 0, 0), (1, 1, 1), (2, 2, 2)))
