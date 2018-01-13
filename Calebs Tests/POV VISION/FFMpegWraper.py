import subprocess as sp


#the cmd>>>>>  ffmpeg -f dshow -pixel_format yuyv422 -i video="USB_Camera" -vcodec libx264 -f h264 -preset fast -tune zerolatency pipe:1

#  ffmpeg -f dshow -pixel_format yuyv422 -i video="USB_Camera" -vcodec libx264 -f h264 -preset ultrafast -tune zerolatency -threads 4  -f mpegts udp://192.168.56.1:8888

#\ -x264opts crf=20:vbv-maxrate=3000:vbv-bufsize=100:intra-refresh=1:slice-max-size=1500:keyint=30:ref=1 \
#ffmpeg -f dshow -pixel_format yuyv422 -i video="USB_Camera" -vcodec libx264 -f h264 -preset ultrafast -tune zerolatency -threads 4 \ -x264opts crf=20:vbv-maxrate=3000:vbv-bufsize=100:intra-refresh=1:slice-max-size=1500:keyint=30:ref=1 \ -f mpegts udp://192.168.56.1:8888


#  ffmpeg -f dshow -pixel_format yuyv422 -i video="USB_Camera" -vcodec libx264 -f h264 -preset ultrafast -tune zerolatency -threads 4  -f mpegts rtsp://192.168.56.1:8888

#-f rtp rtp://10.0.0.2:6005
#ffmpeg -f dshow -pixel_format yuyv422 -i video="USB_Camera" -vcodec libx264 -f h264 -preset ultrafast -tune zerolatency -threads 4 http://localhost:8090/feed1.ffm

#http://localhost:8090/feed1.ffm

#varible settings
frameRate = 30
resolutionX = 1920
resolutionY = 1080



filePath = "ffmpeg.exe"
cmd = [filePath,"-f","dshow","-video_size","1280x720","-framerate","24","-pixel_format",
        "yuyv422","-i",'video="USB_Camera"',"-vcodec","libx264","-f","h264","-preset","fast","-tune","zerolatency","pipe:1"]
