#!/usr/bin/python3

import jetson.inference
import jetson.utils
import time


classify_input="/home/james/processed_input/cropped_images/anomaly_1_0.jpg"
classifymodelpath="/home/james/jetson-inference/python/training/classification/models/class_hump_blue/"
classifymodelname="resnet18.onnx"
classifylabelspath="/home/james/jetson-inference/python/training/classification/models/class_hump_blue/"
labelsname="labels.txt"

while True:

    img = jetson.utils.loadImage(filepath)
    net = jetson.inference.imageNet(argv=[f'--model={classifymodelpath}{classifymodelname}', f'--labels={classifylabelspath}{labelsname}', '--input-blob=input_0', '--output-blob=output_0'])
    class_idx, confidence = net.Classify(img)
    class_desc = net.GetClassDesc(class_idx)
    print("image is recognized as '{:s}' (class #{:d}) with {:f}% confidence".format(class_desc, class_idx, confidence * 100))
    print(class_idx,confidence)
    time.sleep(10)