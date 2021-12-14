import os
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import Algorithm.models as models
import functools
import time
from conf.config import config
config = config.cfg
# path = config['model']['path']  # 模型路径

device = torch.device('cuda')
os.environ['CUDA_VISIBLE_DEVICES'] = config['GPU']['CUDA_VISIBLE_DEVICES']
from PIL import Image
transform_pre = transforms.Compose([
    transforms.Resize((480, 480)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
])

@functools.lru_cache(None)
def pre_process(flag=0):
    model_path = 'path' + '_' + str(flag)
    model_path = config['model'][model_path]
    model = models.KNOWN_MODELS['BiT-M-R101x1'](head_size=config['dataset']['classes'+'_'+str(flag)], zero_head=True)
    model = torch.nn.DataParallel(model)

    model.load_state_dict(torch.load(model_path))
    print("Loading model complete!")
    model.eval()
    model.to(device)
    return model

def predict(img, model, class_list):
    img = img.convert("RGB")
    image = transform_pre(img).unsqueeze(0)
    with torch.no_grad():
        image.to(device)
        output = model(image)
        output = nn.functional.softmax(output, dim=1)
        val, idx = torch.topk(output, 3)
        val, idx = val.cpu().numpy()[0], idx.cpu().numpy()[0]
        top1_p, top1_code = round(val[0] * 100, 2), class_list[idx[0]][2:-1:]
        top2_p, top2_code = round(val[1] * 100, 2), class_list[idx[1]][2:-1:]
        top3_p, top3_code = round(val[2] * 100, 2), class_list[idx[2]][2:-1:]
    return [[top1_p, top2_p, top3_p], [top1_code, top2_code, top3_code]]

if __name__ == '__main__':
    img1 = Image.open(os.path.join(config['dataset']['val_path'], 'C22360210010/6.jpg'))
    img2 = Image.open(os.path.join(config['dataset']['val_path'], 'C22360210010/7.jpg'))
    img4 = Image.open(os.path.join(config['dataset']['val_path'], 'C22360210010/8.jpg'))
    img3 = Image.open(os.path.join(config['dataset']['val_path'], 'C22360210010/9.jpg'))
    t1 = time.time()
    model, class_list = pre_process()

    t2 = time.time()
    res1 = predict(img1, model, class_list)
    t3 = time.time()
    res2 = predict(img2, model, class_list)
    t4 = time.time()
    res3 = predict(img3, model, class_list)
    t5 = time.time()
    res4 = predict(img4, model, class_list)
    t6 = time.time()
    res5 = predict(img4, model, class_list)
    t7 = time.time()

    print(t2 - t1, t3 - t2, t4 - t3, t5 - t4, t6 - t5, t7 - t6)

    print(res1, res2)

