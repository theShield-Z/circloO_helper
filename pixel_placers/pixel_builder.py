"""Imports matrix as an array of pixels."""


def build(arr: list, obj='b', start_x=1500, start_y=1500, size=1, extras='0', line_nums=False, start_line=0):
    """
    Convert a binary matrix into a pixel display in circloO
    :param arr:     Matrix to be converted
    :param obj:     circloO object; default 'b' is solid rectangle
    :param start_x: Initial x value (left)
    :param start_y: Initial y value (top)
    :param size:    Size of each pixel
    :param extras:  If using objects other than default rectangles, add the extra attributes here
    :param line_nums:   Choose whether to enumerate lines in level file
    :param start_line:  Starting value of line enumeration
    :return:    String of circloO objects (w/o header)
    """
    text = []
    xpos = 0
    ypos = 0
    cur_line = start_line

    for r in arr:
        for c in r:
            if c == 1:
                text.append(f'{obj} {xpos + start_x} {ypos + start_y} {size} {size} {extras}\n')

                if line_nums:
                    text.append(f'< {cur_line}\n')
                    cur_line += 1

            xpos += 2 * size

        xpos = 0
        ypos += 2 * size

    return ''.join(text)


# EXAMPLE CODE #########################################################################################################

mat_1 = [[1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
         [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
         [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
         [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
         [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1]]

mat_2 = [[0, 1, 0, 1, 0],
         [0, 0, 0, 0, 0],
         [1, 0, 0, 0, 1],
         [0, 1, 1, 1, 0]]

print(build(mat_1, size=5, start_y=1700))
print(build(mat_2, obj='tmb', size=10, extras='0 -1 0 -1 6 0 0\nfixrot\nnoanim'))
