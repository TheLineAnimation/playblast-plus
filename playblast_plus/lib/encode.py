import subprocess

"""
Full credit goes to Chris Zurbrigg for this code 

Correct Argument List -
-y -framerate 24 -i [INPUTFILE]_%04d.png -c:v libx264 -pix_fmt yuv420p 
    -crf 21 -preset ultrafast [OUTPUTFILE].mp4

Ensure -pix_fmt yuv420p is present to create playable media. 
Otherwise there will be issues with black frames
"""

FFMPEG_PATH = "../bin/ffmpeg.exe"
FFPROBE_PATH = "../bin/ffprobe.exe"

def extract_middle_image(source_path, output_path):

    ffprobe_cmd = FFPROBE_PATH
    ffprobe_cmd += ' -v error -show_entries format=duration '
    ffprobe_cmd += '-of default=noprint_wrappers=1:nokey=1 '
    ffprobe_cmd += source_path

    duration = float(subprocess.check_output(ffprobe_cmd))

    ffmpeg_cmd = FFMPEG_PATH
    ffmpeg_cmd += ' -y -i {0} -ss {1} -frames:v 1 {2}'.format(source_path, 
                                                              duration/2.0, 
                                                              output_path)
    print(ffmpeg_cmd)
    subprocess.call(ffmpeg_cmd)


def encode_image_sequence(image_seq_path, 
                            output_path, 
                            framerate=24, 
                            crf=21, 
                            preset="ultrafast", 
                            audio_path=None
                        ):

    ffmpeg_cmd = FFMPEG_PATH
    ffmpeg_cmd += ' -y '
    ffmpeg_cmd += ' -framerate {0}'.format(framerate)
    ffmpeg_cmd += ' -i {0}'.format(image_seq_path)
    if audio_path:
        ffmpeg_cmd += ' -i {0}'.format(audio_path)

    ffmpeg_cmd += ' -c:v libx264 -crf {0} -preset {1}'.format(crf, preset)
    if audio_path:
        ffmpeg_cmd += ' -c:a aac -filter_complex "[1:0] apad" -shortest'

    ffmpeg_cmd += ' {0}'.format(output_path)

    print(ffmpeg_cmd)
    subprocess.call(ffmpeg_cmd)

def image_sequence_to_ffmpeg_input():
    pass

# if __name__ == "__main__":

    # source_path = "D:/ffmpeg/ffmpeg-4.2.1/bin/bbb_shot_060.mp4"
    # output_path = "D:/ffmpeg/ffmpeg-4.2.1/bin/middle_frame.png"

    # extract_middle_image(source_path, output_path)