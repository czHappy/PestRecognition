import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
from torch.optim.lr_scheduler import *
import torchvision.transforms as transforms
import torchvision as tv
import numpy as np
import os
import argparse
from Algorithm.resnet_model import resnet50
import Algorithm.ranger as ranger
from conf.config import config
config = config.cfg # 读取配置文件



parser=argparse.ArgumentParser()
parser.add_argument('--num_workers',type=int,default=4)
parser.add_argument('--batchSize',type=int,default=32)
parser.add_argument('--nepoch',type=int,default=40)
parser.add_argument('--lr',type=float,default=0.001)
parser.add_argument('--gpu',type=str,default='0,1,3')
opt=parser.parse_args()
print(opt)
os.environ["CUDA_VISIBLE_DEVICES"]=opt.gpu

transform_train=transforms.Compose([
	transforms.Resize((224,224)),
	# transforms.RandomHorizontalFlip(),
	transforms.ToTensor(),
	# transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))
    transforms.Normalize((0.485,0.456,0.406),(0.229,0.224,0.225))
])

transform_val=transforms.Compose([
	transforms.Resize((224,224)),
	transforms.ToTensor(),
	# transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5)),
    transforms.Normalize((0.485,0.456,0.406),(0.229,0.224,0.225)),
])

# datadir = '/home/sk49/new_workspace/dataset/2021SoftBei/A4-basebone'
datadir = config['dataset']['train_path']
trainset = tv.datasets.ImageFolder(os.path.join(datadir, "train"), transform_train)
valset = tv.datasets.ImageFolder(os.path.join(datadir, "val"), transform_val)


trainloader = torch.utils.data.DataLoader(trainset, batch_size=opt.batchSize,shuffle=True,num_workers=opt.num_workers)
valloader = torch.utils.data.DataLoader(valset, batch_size=len(valset),shuffle=False,num_workers=opt.num_workers)

model=resnet50(pretrained=True)

model = torch.nn.DataParallel(model)

print(model)

model.cuda()
# optimizer=torch.optim.SGD(model.parameters(), lr=opt.lr, momentum=0.9, weight_decay=5e-4)
optimizer = ranger.Ranger(model.parameters())
#optimizer=torch.optim.Adam(model.parameters(),lr=opt.lr)
scheduler=StepLR(optimizer, step_size=5, gamma=0.2)
criterion=nn.CrossEntropyLoss()
criterion.cuda()


def train(epoch):
    print('\nEpoch: %d' % epoch)
    model.train()
    for batch_idx,(img,label) in enumerate(trainloader):
        image = Variable(img.cuda())
        label = Variable(label.cuda())
        optimizer.zero_grad()
        out = model(image)
        loss = criterion(out, label)
        loss.backward()
        optimizer.step()
        print("Epoch:%d [%d|%d] loss:%f" %(epoch,batch_idx,len(trainloader),loss.mean()))

    scheduler.step()

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import sklearn.metrics as sm

def val(epoch):
    print("\nValidation Epoch: %d" %epoch)
    model.eval()
    total=0
    correct=0
    with torch.no_grad():
        for batch_idx,(img,label) in enumerate(valloader):
            image=Variable(img.cuda())
            label=Variable(label.cuda())
            out = model(image)
            _,predicted=torch.max(out.data,1)
            print(label.shape)
            print(out.shape)
            ot = torch.argmax(out, 1)
            ot = ot.view(len(ot), 1)
            cm = confusion_matrix(label.data.cpu().numpy(), ot.data.cpu().numpy())
            print(cm)
            r = sm.classification_report(label.data.cpu().numpy(), ot.data.cpu().numpy())
            print('分类报告为：', r, sep='\n')
            total+=image.size(0)
            a = predicted.data.eq(label.data).cpu().sum()
            correct += a
            # if a == 1:
            #     sample_fname, _ = valloader.dataset.samples[batch_idx]
    acc = 1.0 * correct.numpy() / total
    print("Acc: %f "% (acc))
    if acc > 0.973 and epoch > 25:
        print("save! ", acc)
        torch.save(model.state_dict(), './model_{}_{}_{}_{}.pth'.format(50, opt.batchSize, acc, epoch))

for epoch in range(opt.nepoch):
    train(epoch)
    # scheduler.step()
    val(epoch)

