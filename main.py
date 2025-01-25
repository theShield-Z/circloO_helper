import video_processing as vp
import video_to_circloO as vc

video_path = 'bad_apple.mp4'
pixels_per_row = 50
pixels_per_col = 50
threshold = 128
skip_frames = 0

mats = vp.process_video_frames(video_path, pixels_per_row, pixels_per_col, threshold, skip_frames)

vc.generate_file("bad_apple.txt", mats)
