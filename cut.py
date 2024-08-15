
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip

def split_video(input_file, num_pieces, output_dir):
    # Get the duration of the video
    video = VideoFileClip(input_file)
    duration = video.duration
    piece_duration = duration / num_pieces
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(num_pieces):
        start_time = i * piece_duration
        end_time = start_time + piece_duration
        output_file = os.path.join(output_dir, f"output_{i+1}.mp4")
        
        ffmpeg_extract_subclip(input_file, start_time, end_time, targetname=output_file)
        print(f"Created: {output_file}")

    print("Video splitting completed.")

if __name__ == "__main__":

    input_file = input("Enter the path to the video file: ")
    num_pieces = int(input("Enter the number of pieces to split the video into: "))
    output_dir = input("Enter the output directory: ")
    
    split_video(input_file, num_pieces, output_dir)