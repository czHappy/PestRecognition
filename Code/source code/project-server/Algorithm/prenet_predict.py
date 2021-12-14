import os
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import Algorithm.models as models
import functools
import time
from conf.config import config
from Algorithm.resnet_model import resnet50

config = config.cfg
path = config['pre_model']['path']  # 模型路径
device = torch.device('cuda')
os.environ['CUDA_VISIBLE_DEVICES'] = config['GPU']['CUDA_VISIBLE_DEVICES']
from PIL import Image

transform_pre = transforms.Compose([
    transforms.Resize((224, 224)),
    # transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    # transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
])


@functools.lru_cache(None)
def pre_process():
    model = resnet50(pretrained=False)
    model = torch.nn.DataParallel(model)
    model.load_state_dict(torch.load(path))
    print("Loading prenet model complete!")
    model.eval()
    model.to(device)
    return model

def predict(img, model):
    print(type(img))
    #print(img.size())
    img = img.convert("RGB")

    image = transform_pre(img).unsqueeze(0) #增加一个维度变成4Dtensor

    with torch.no_grad():
        image.to(device)
        output = model(image)
        output = nn.functional.softmax(output, dim=1)
        _, output = torch.max(output, 1)
        # print("output = ", output)
    return output.cpu().numpy()[0]

if __name__ == '__main__':
    img1 = Image.open(os.path.join(config['dataset']['val_path'], '0/C223590400608.jpg'))
    img2 = Image.open(os.path.join(config['dataset']['val_path'], '0/C223590400609.jpg'))
    img4 = Image.open(os.path.join(config['dataset']['val_path'], '1/C223601900058.jpg'))
    img3 = Image.open(os.path.join(config['dataset']['val_path'], '2/C223590400606.jpg'))
    t1 = time.time()
    model = pre_process()

    t2 = time.time()
    res1 = predict(img1, model)
    t3 = time.time()
    res2 = predict(img2, model)
    t4 = time.time()
    res3 = predict(img3, model)
    t5 = time.time()
    res4 = predict(img4, model)
    t6 = time.time()
    res5 = predict(img4, model)
    t7 = time.time()

    print(t2 - t1, t3 - t2, t4 - t3, t5 - t4, t6 - t5, t7 - t6)

    print(res1, res2, res3, res4, res5)

