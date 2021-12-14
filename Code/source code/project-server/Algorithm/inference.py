import os
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import Algorithm.models as models
from conf.config import config
config = config.cfg

print(config['GPU']['CUDA_VISIBLE_DEVICES'])
os.environ['CUDA_VISIBLE_DEVICES'] = config['GPU']['CUDA_VISIBLE_DEVICES']
datadir = config['dataset']['val_path']  # 测试集
path = config['model']['path']  # 模型路径
device = torch.device('cuda')
size = config['model']['size']

transform_test = transforms.Compose([
    transforms.Resize((size, size)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
])

testset = torchvision.datasets.ImageFolder(datadir, transform_test)
testloader = torch.utils.data.DataLoader(testset, batch_size=1, shuffle=False, num_workers=2)
classname = testset.classes

if __name__ == '__main__':

    model = models.KNOWN_MODELS['BiT-M-R101x1'](head_size=99, zero_head=True)
    model = torch.nn.DataParallel(model)

    with torch.no_grad():
        model.load_state_dict(torch.load(path))
        print("loading model compelte!")
        correct = 0
        total = 0
        model.eval()
        model.to(device)
        for i, data in enumerate(testloader):
            images, label = data
            images, label = images.to(device), label.to(device)
            outputs = model(images)
            outputs = nn.functional.softmax(outputs, dim=1)
            # 取得分最高的那个类 (outputs.data的索引号)
            score, predicted = torch.max(outputs.data, 1)
            score, predicted = score.cpu().numpy(), predicted.cpu().numpy()
            # print(score)

            # print("idx = {}, probability = {} ".format(predicted[0], score[0]))
            total += label.size(0)
            flag = False
            if predicted[0] == label.cpu().numpy()[0]:
                correct += 1
                flag = True
            print("idx = {}, class = {}, probability = {}, flag = {} ".format(predicted[0], classname[predicted[0]], score[0], flag))
        print('done!')

    print("avg correct : ", correct / total)



