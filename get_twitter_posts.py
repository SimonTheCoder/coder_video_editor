
# this tool need snscrape
# this tool need run under proxychains

import snscrape.modules.twitter as sntwitter
import sys
import os
import requests
from tqdm import tqdm

import json

# Check if twitter_list.json exists, if not create it with an empty list
if not os.path.exists("twitter_list.json"):
    with open("twitter_list.json", "w") as file:
        json.dump([], file)
    print("fill your list in twitter_list.json.")    

# Read the list from twitter_list.json
with open("twitter_list.json", "r") as file:
    twitter_list = json.load(file)


since_date = sys.argv[1]
if len(sys.argv) == 3:
    until_date = sys.argv[2]
else:
    until_date = None

import os
import datetime

# Check if ./res exists and rename it to ./res_<current_date>
if os.path.exists("./res"):
    # Check if ./res_<current_date> exists
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    if not os.path.exists(f"./res_{current_date}"):
        os.rename("./res", f"./res_{current_date}")
else:
    # Create the ./res directory
    os.makedirs("./res")

posts_list = []

for user in twitter_list:
    if until_date is None:
        query = f"(from:{user}) since:{since_date}"
    else:    
        query = f"(from:{user}) since:{since_date} until:{until_date}"
    print(f"query:{query}")
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        #print(vars(tweet))
        save_file_name = f"{user}_{tweet.date}".replace(" ","_").replace(":","：")
        print(save_file_name)
        #print(tweet.media)
        if tweet.media is not None and len(tweet.media) == 1:
            video = tweet.media[0]
            #print(type(video))
            if type(video) != sntwitter.Video:
                print(f"not a video. ({type(video)})")
                continue
            #print(video.variants)
            max_bitrate = 0
            max_bitrate_video = None
            
            #find the max bitrate video variant
            for video_info in video.variants:
                if video_info.bitrate is not None and video_info.bitrate > max_bitrate:
                    max_bitrate = video_info.bitrate
                    max_bitrate_video = video_info
            # no proper video variant found
            if max_bitrate_video is None:
                continue

            
            # #requests: download video file, and save it. 
            # response = requests.get(max_bitrate_video.url,stream=True)
            # total_size = int(response.headers.get('content-length', 0))
            # block_size = 1024 # 1 Kibibyte
            # progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
            # with open(f"res/{save_file_name}.mp4","wb") as file:
            #     for data in response.iter_content(block_size):
            #         progress_bar.update(len(data))
            #         file.write(data)

            # progress_bar.close()

            # if total_size != 0 and progress_bar.n != total_size:
            #     print("下载失败")
            # else:
            #     print("下载完成")      

            #yt-dlp
            import subprocess
            subprocess.call(['proxychains','yt-dlp', '-P', 'res', tweet.url])

        else:
            print("no media")
            #print(vars(tweet))