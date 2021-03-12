#inference program to run a premade model 

import jetson.inference
import jetson.utils

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

camera = jetson.utils.videoSource("csi://0")

display = jetson.utils.videoOutput("/media/BEEA-11F9/inferenceoutput/my_video.mp4")

while display.IsStreaming():
    img = camera.Capture()

    detections = net.Detect(img)
    print(detections)
    display.Render(img)
    display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
