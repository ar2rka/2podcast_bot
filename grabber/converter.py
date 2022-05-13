from moviepy.editor import *
import os


FILE_PATH = 'media/'
BITRATE = '64k'


def mp4_to_mp3(mp4_file, mp3_file):
    video = AudioFileClip(FILE_PATH + mp4_file)
    mp3_filename = mp3_file + '.mp3'
    video.write_audiofile(filename=FILE_PATH + mp3_filename,
                          bitrate=BITRATE)
    os.remove(FILE_PATH + mp4_file)
    return mp3_filename
