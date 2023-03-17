import os
import sys
from moviepy.editor import VideoFileClip, concatenate_videoclips, ColorClip, CompositeVideoClip
from moviepy.editor import vfx

portrait_size = (1080,1920)
landscape_size = (1920,1080)

screen_size = portrait_size
screen_ratio = screen_size[0]/screen_size[1]
background_clip = ColorClip(screen_size, color=(0, 0, 0))
# 获取命令行参数中的文件夹路径
folder_path = sys.argv[1]

# 定义一个列表来保存视频剪辑
clips_list = []

# 遍历文件夹中的所有文件
for file_name in os.listdir(folder_path):
    # 检查文件是否为视频文件
    if file_name.endswith('.mp4') or file_name.endswith('.avi'):
        # 构造视频文件的绝对路径
        file_path = os.path.join(folder_path, file_name)
        # 加载视频文件并将其添加到clips_list列表中
        clip = VideoFileClip(file_path)
        clips_list.append(clip)

# 对所有视频剪辑应用fadein和fadeout效果，并将新的剪辑添加到新的列表中
new_clips_list = []
max_width = 0
max_height = 0
for clip in clips_list:
    # new_clip = clip.fx(vfx.fadein, 1.0)
    # new_clip = new_clip.fx(vfx.fadeout, 1.0)

    # Create a black background clip with the same size as the video clip
    if screen_ratio > 1.0:
        new_h = screen_size[1]
        new_w = int(clip.size[0] * new_h / clip.size[1])
    else:
        new_w = screen_size[0]
        new_h = int(clip.size[1] * new_w / clip.size[0])     
    new_clip = CompositeVideoClip([background_clip.set_duration(clip.duration), clip.resize((new_w,new_h)).set_position(("center", "center"))])
    new_clips_list.append(new_clip)
    # 记录最大宽度和高度
    # max_width = max(max_width, new_clip.w)
    # max_height = max(max_height, new_clip.h)

# 调整所有剪辑的大小以匹配最大的宽度和高度，并将它们添加到新的列表中
# resized_clips_list = []
# for clip in new_clips_list:
#     resized_clip = clip.resize((max_width, max_height))
#     resized_clips_list.append(resized_clip)

# 连接所有新的剪辑为一个新的剪辑
# final_clip = concatenate_videoclips(resized_clips_list, method="compose")

# 连接所有视频剪辑为新的剪辑
final_clip = concatenate_videoclips(new_clips_list)

# 输出新的剪辑为视频文件
output_file_path = os.path.join("output", 'output.mp4')
final_clip.write_videofile(output_file_path, codec="libx264", fps=clip.fps, bitrate="5000k")
