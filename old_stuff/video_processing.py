import numpy as np
import cv2
# np.set_printoptions(threshold=np.inf)


def process_video_frames(video_path, pixels_per_row, pixels_per_col, threshold, skip_frames=0):
    """
    Converts a full video into a list of binary matrices that store each desired frame of the video
    :param video_path:      path of video to convert
    :param pixels_per_row:  number of pixel groupings in each row of output matrix
    :param pixels_per_col:  number of pixel groupings in each column of output matrix
    :param threshold:       threshold point for determining whether a pixel is black or white
    :param skip_frames:     number of frames to skip between operations; helps to save on resources. For example,
                                if skip_frames = 10, frame 1 is processed, 2-10 are skipped, 11 is processed, etc.
    :return:                list of binary matrices representing the video
    """
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    processed_video_matrices = []       # List to store final matrices.

    if not cap.isOpened():
        print(f"Error: Cannot open video {video_path}")
        return

    frame_count = 0  # To keep track of the frame index

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("End of video or cannot read the frame.")
            break

        # Process every (skip_frames + 1)th frame
        if frame_count % (skip_frames + 1) == 0:
            # Convert the frame to grayscale since pixelate_and_binarize() expects a grayscale image
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Temporary image file.
            cv2.imwrite('gray_frame.png', gray_frame)

            # Call the pixelate_and_binarize function for this frame
            _, processed_frame_mat = img_to_binary_matrix('gray_frame.png', pixels_per_row, pixels_per_col, threshold)

            processed_video_matrices.append(processed_frame_mat)

        # Move to the next frame
        frame_count += 1

    # Release the video capture object
    cap.release()
    # Close all OpenCV windows
    cv2.destroyAllWindows()

    return processed_video_matrices


def img_to_binary_matrix(image_path, pixels_per_row=20, pixels_per_col=20, threshold=128):
    """
    Converts an image into a binary matrix.
    :param image_path:      path of image to convert
    :param pixels_per_row:  number of pixel groupings in each row of output matrix
    :param pixels_per_col:  number of pixel groupings in each column of output matrix
    :param threshold:       threshold point for determining whether a pixel is black or white
    :return:                binary matrix that stores the image's data
    """
    # Read the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Load as grayscale

    # Resize the image to a smaller resolution based on pixels_per_row/col.
    pixelated_img = cv2.resize(img, (pixels_per_row, pixels_per_col), interpolation=cv2.INTER_LINEAR)

    # Apply the threshold to convert the pixelated image to binary (two-tone).
    _, binary_img = cv2.threshold(pixelated_img, threshold, 255, cv2.THRESH_BINARY)

    # Convert the binary image into a matrix of ones (white) and zeros (black).
    #   binary_matrix = np.where(binary_img == 255, 1, 0)
    # Reversed black & white.
    binary_matrix = np.where(binary_img == 255, 0, 1)

    # Return the pixelated image and the binary matrix.
    return pixelated_img, binary_matrix
