# Depstech WF070 Endoscope
To have a device that won't be useless when the app inevitably disappears, here's some Python to reconstruct the mjpeg stream so that VLC can play it.

1. Connect to the depstech wifi
2. Launch `python depstech.py`
3. Point VLC to the network stream `tcp://localhost:7060/stream.mjpeg` (you can reduce video stream delay by adding `vlc --network-caching=10`)

## Technical info
A bunch of research has been done on similar devices in the past [1][2][3]. It seems our friendly developer, "Tony", has been at it with a new way to mess with the mjpeg stream. This time, rather than just flipping the middle byte, every frame has an header containing a frame sequence number which is used as a seed to calculate which byte in the frame to flip.

Another "improvement" over the previously researched devices is that the camera stream is now over UDP and requires you to periodically send a "please give me video" command.

Perhaps unsurprising but it turns out that the device also does not support 1080p as claimed. When asking the device about supported resolutions and frame rates it seems these are the supported ones:

* 1280x720 20fps
* 960x720 20fps
* 640x480 20fps

[1] https://n8henrie.com/2019/02/reverse-engineering-my-wifi-endoscope-part-4/  
[2] https://mplough.github.io/2019/12/14/borescope.html  
[3] https://mkarr.github.io/20200616_boroscope
