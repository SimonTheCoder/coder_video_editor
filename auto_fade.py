import os
import sys
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.editor import vfx

FADEIN_TIME=0.75
FADEOUT_TIME=0.75

# 获取命令行参数中的文件夹路径
folder_path = sys.argv[1]

# Check if ./faded exists
if os.path.exists("./faded"):
    # If yes, rename it to faded_<current_date>
    import datetime
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    # If faded_{current_date} exists, skip renaming
    if not os.path.exists(f"./faded_{current_date}"):
        os.rename("./faded", f"faded_{current_date}")

#check if ./faded exist.
#if not ,create it.# Check if ./faded exists
if not os.path.exists("./faded"):
    # If not, create it
    os.makedirs("./faded")
    


# 定义一个列表来保存视频剪辑
clips_list = []
count = 0
# 遍历文件夹中的所有文件
for file_name in os.listdir(folder_path):
    # 检查文件是否为视频文件
    if file_name.endswith('.mp4') or file_name.endswith('.avi'):
        # 构造视频文件的绝对路径
        file_path = os.path.join(folder_path, file_name)
        print(f"processing: {file_path}")
        # 加载视频文件并将其添加到clips_list列表中
        try:
            clip = VideoFileClip(file_path)
            bitrate = int(clip.fps * clip.size[0] * clip.size[1] * 0.0001)+1
            

            # file_size = os.path.getsize(clip.filename)
            # duration = clip.duration
            # bitrate = int(file_size / duration * 0.01)

            bitrate_str = f"{bitrate}k"
            # Print bitrate_str as info
            print(f"bitrate_str: {bitrate_str}")

            print(clip.duration)
            clips_list.append(clip)
            new_clip = clip.fx(vfx.fadein, FADEIN_TIME)
            new_clip = new_clip.fx(vfx.fadeout, FADEOUT_TIME)
            # file_name = "test.mp4"
            output_file_path = os.path.join("faded", file_name)
            new_clip.write_videofile(output_file_path,codec="libx264", fps=clip.fps ,bitrate=bitrate_str)
            count=count+1
        except Exception as e:
            print(e)
            print("continue to next.")    

print(f"{count} processed.")