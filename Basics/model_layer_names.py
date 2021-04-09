##gives the names of input and output layers for a onnx model

import onnx

model = onnx.load("/home/james/jetson-inference/python/training/classification/models/class_hump_blue/resnet18.onnx")

output =[node.name for node in model.graph.output]

input_all = [node.name for node in model.graph.input]
input_initializer =  [node.name for node in model.graph.initializer]
net_feed_input = list(set(input_all)  - set(input_initializer))

print('Inputs: ', net_feed_input)
print('Outputs: ', output)