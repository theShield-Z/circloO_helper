import math


def generate_file(output_path, video_matrices, center_x=1500, center_y=1500, segments=6):
    """
    :param output_path:     .txt file to output resultant level
    :param video_matrices:  list of binary matrices that store frames of a video (see video_processing.py)
    :param center_x:        center of level along x-axis
    :param center_y:        center of level along y-axis
    :param segments:        how many level segments the display will take up; one less than max works best
    :return:                None
    """
    vid_len = len(video_matrices)
    pixels_per_row = len(video_matrices[0][0])
    pixels_per_col = len(video_matrices[0])
    pixel_density = max(pixels_per_col, pixels_per_row)

    # GENERATE FILE.
    f = open(output_path, 'w')
    f.writelines("/\n"
                 "/ circloO level\n"
                 "/ Made with circloO Level Editor v1.3\n"
                 "totalCircles 8 1\n"
                 "/ EDITOR_TOOL 1 1\n"
                 "/ EDITOR_VIEW 1500 1500 0.6\n"
                 "/ EDT 3303\n"
                 "/ _SAVE_TIME_1721799879000_END\n"
                 "levelscriptVersion 7\n"
                 "COLORS 128\n"
                 "grav 0 270\n")
    label = 0  # Keeps track of line number.

    # CALCULATE PIXEL GRID.
    #   center of where each generator goes.
    #   level centre is (1500, 1500); each segment adds 100 radius
    #       for n-segment circle, corners of grid are at +/- 200n * sqrt(2)/2 + center_[x or y]

    cf = 200 * segments * math.sqrt(2) / 2
    tlc = (-cf + center_x, -cf + center_y)  # Top-left corner position

    # FILL GRID WITH GENERATORS.
    #   Generator Enumeration:
    #       first row, first gen: 0; first row, last gen: PIXEL_DENSITY
    #       last row, first gen: PD^2 + PD; last row, last gen: PD^2 + 2PD
    #       nth row, mth gen: PD * n + m (0-based)

    space = 200 * segments * math.sqrt(2) / pixel_density  # space b/w each gen.
    xpos, ypos = tlc    # positions of each gen; initialized to top left corner.
    size = 15           # size of each gen.

    for i in range(pixel_density + 1):

        for j in range(pixel_density + 1):
            f.write(f"tmc {xpos} {ypos} {size} 0 0 0 0\ndamping -1\nnoanim\noff\n")
            f.write(f"< {label}\n")

            xpos += space
            label += 1

        ypos += space
        xpos = tlc[0]   # reset xpos

    # GENERATE CONNECTIONS BASED ON 2D PROJECTION (LOGIC).

    #   MAKE TRIGGERS.
    start_tx = 900
    tx = start_tx
    ty = 300

    trigger_labels = []
    for i in range(vid_len):

        if i % 30 == 0 and i != 0:
            tx = start_tx
            ty += 51

        f.write(f"ic 'isp' {tx} {ty} 1\ntrigger\n")
        f.write(f"< {label}\n")

        trigger_labels.append(label)
        label += 1
        tx += 51

    #   CONNECT TRIGGERS.

    for j in range(vid_len):
        # Cycle through each rotation matrix.

        frame = video_matrices[j] - video_matrices[j - 1]  # Saves resources by only changing necessary gen states.
        # print(frame)
        trigger = trigger_labels[j]

        for r in range(len(frame)):
            # Cycle through the rows of current frame's matrix.

            for c in range(len(frame[r])):
                # Cycle through cols of current frame's matrix.
                index = r * (pixel_density + 1) + c  # index of generator corresponding to current row/col

                if frame[r, c] == 1:
                    f.write(f"> {trigger}\n> {index}\nspc 'NowIf'\n")

                    f.write(f"< {label}\n")
                    label += 1

                if frame[r, c] == -1:
                    f.write(f"> {trigger}\n> {index}\nspc 'Destroy'\n")

                    f.write(f"< {label}\n")
                    label += 1

    # STARTING POSITION.
    #   Due to the resource saving in l89, pixel display must be initialized to first frame of video.

    f.write(f"ic 'isp' 850 200 1\nzoomFactor -2\ntrigger\n")    ## not tested w/ zoomFactor ##
    f.write(f"< {label}\n")
    start_trigger = label
    start_frame = video_matrices[0]
    label += 1

    for r in range(len(start_frame)):

        for c in range(len(start_frame)):
            index = r * (pixel_density + 1) + c

            if start_frame[r, c] == 1:
                f.write(f"> {start_trigger}\n> {index}\nspc 'NowIf'\n")

                f.write(f"< {label}\n")
                label += 1

    # OUTPUT TO .txt FILE.

    f.write("y 850 200 .1 1 1")     # Add player
    f.close()
