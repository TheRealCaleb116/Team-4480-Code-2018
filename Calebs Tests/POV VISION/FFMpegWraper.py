import subprocess as sp


#the cmd>>>>>  ffmpeg -f dshow -video_size 1280x720 -framerate 24 -pixel_format yuyv422 -i video="USB_Camera" -vcodec libx264 -f h264 -preset fast -tune zerolatency pipe:1

#varible settings
frameRate = 30
resolutionX = 1920
resolutionY = 1080



filePath = "ffmpeg.exe"
cmd = [filePath,"-f","dshow","-video_size","1280x720","-framerate","24","-pixel_format",
        "yuyv422","-i",'video="USB_Camera"',"-vcodec","libx264","-f","h264","-preset","fast","-tune","zerolatency","pipe:1"]
