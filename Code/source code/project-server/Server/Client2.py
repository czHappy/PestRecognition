import requests
import time
path = r'/home/sk49/new_workspace/dataset/2021SoftBei/A4-train-val_freshed/val/C15106005010'
t1 = time.time()

resp3 = requests.post("http://localhost:5002/predict",
                     files={"file": open('{}/14.jpeg'.format(path),'rb')})
t2 = time.time()


print(resp3.json())

print(t2 - t1)
