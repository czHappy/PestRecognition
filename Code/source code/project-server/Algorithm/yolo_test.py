import torch

# Model
print('h1')
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5x, custom
print('h2')
# Images
img = 'https://ultralytics.com/images/zidane.jpg'  # or file, PIL, OpenCV, numpy, multiple

# Inference
results = model(img)

# Results
results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
