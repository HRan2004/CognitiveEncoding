import os
import time

from moviepy.video.io.VideoFileClip import VideoFileClip
import math
from aip import AipSpeech
from pydub import AudioSegment
import wave
import pandas as pd

input_path = './input'  # 输入视频文件路径
videos_path = './videos'  # 输出切片视频路径
audios_path = 'middle/audios'  # 输出切片音频路径
audios_path2 = './audios2'  # 转换pcm后音频文件路径
output_path = 'middle/output'  # 输出excel文件路径
max_n = 10000000


# APP_ID = '30232056'
# API_KEY = '8eC5sdRTxK6M3EbHcmsF3dyE'
# SECRET_KEY = 'RMTfzzbJYtrwPWp8001QjJaLvTYl2c7g'

APP_ID = '55279753'
API_KEY = 'GpCXb1Xvsmm0gHOBib71jkjW'
SECRET_KEY = 'LyokG0is3GT9udiAF7nKbsXCXQ6P0iSH'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def split_video(video_path, segment_length=10):
  # 加载视频
  clip = VideoFileClip(video_path)
  duration = clip.duration  # 获取视频时长

  # 计算需要切分成多少段
  segments = math.ceil(duration / segment_length)

  # 开始切分
  for i in range(segments):
    start_time = i * segment_length
    end_time = min((i + 1) * segment_length, duration)

    # 切分视频片段
    current_clip = clip.subclip(start_time, end_time)

    # 输出视频片段
    output_filename = f"{videos_path}/segment_{i + 1}.mp4"
    current_clip.write_videofile(output_filename, codec="libx264")
    audio_filename = f"{audios_path}/segment_{i + 1}.wav"
    current_clip.audio.write_audiofile(audio_filename)

    print(f"Segment {i + 1} has been created: {output_filename}")
    if i >= max_n - 1:
      break


def get_file_content(filePath):
  with open(filePath, 'rb') as fp:
    return fp.read()



if __name__ == "__main__":
  # for file in os.listdir(input_path):
  #   print('\nParse video:', file)
  #   split_video(input_path + '/' + file, 10)
  for file in os.listdir(audios_path):
    print('\nRegenerate audio:', file)
    audio = AudioSegment.from_file(audios_path + "/" + file)
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
    with wave.open(audios_path2 + '/' + file.replace('.wav', '.pcm'), "wb") as pcm_file:
      pcm_file.setnchannels(1)
      pcm_file.setsampwidth(2)
      pcm_file.setframerate(16000)
      pcm_file.writeframes(audio.raw_data)
  data = {}
  for file in os.listdir(audios_path2):
    print('\nAnalysis audio:', file)
    result = client.asr(get_file_content(audios_path2 + '/' + file), 'pcm', 16000)
    print(result)
    if 'result' in result and len(result['result']) > 0:
      data[file] = result['result'][0]
    else:
      data[file] = ''
    time.sleep(0.1)
  print('\n')
  print(data)
  df = pd.DataFrame(list(data.items()), columns=['Key', 'Value'])
  df.to_excel(output_path + '/result.xlsx')


print('\nParse finished.\n\n')
