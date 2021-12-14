"""Run inference with a YOLOv5 model on images, videos, directories, streams

Usage:
    $ python path/to/detect.py --source path/to/img.jpg --weights yolov5s.pt --img 640
"""

import argparse
import sys
import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn

FILE = Path(__file__).absolute()
sys.path.append(FILE.parents[0].as_posix())  # add yolov5/ to path

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, colorstr, non_max_suppression, \
    apply_classifier, scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path, save_one_box
from utils.plots import colors, plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized
import os

def pre_process():
    weights = r'/home/sk49/new_workspace/cz/SoftCup/ckpts/yolo.pt' # model.pt path(s)
    device = '2'
    device = select_device(device)
    return attempt_load(weights, map_location=device).eval() , device # load FP32 model


@torch.no_grad()
def run(model,
        device,
        sql_helper,
        source='./example.jpg',  # file/dir/URL/glob, 0 for webcam
        imgsz=640,  # inference size (pixels)
        conf_thres=0.25,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        save_txt=True,  # save results to *.txt
        save_conf=False,  # save confidences in --save-txt labels

        nosave=False,  # do not save images/videos
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        update=False,  # update all models
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference

        ):
    save_img = True  # save inference images
    webcam = False
    half = True  # half precision only supported on CUDA

    # Load model
    # model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check image size
    names = model.module.names if hasattr(model, 'module') else model.names  # get class names

    if half:
        model.half()  # to FP16

    # Set Dataloader
    vid_path, vid_writer = None, None
    if webcam:
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride)
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # Run inference

    model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    t0 = time.time()
    txt_path = r'./run/detect.txt'
    if os.path.exists(txt_path):
        os.remove(txt_path)  # 清空
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = time_synchronized()
        pred = model(img, augment=augment)[0]

        # Apply NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        t2 = time_synchronized()

        # Apply Classifier
        #if classify:
        #    pred = apply_classifier(pred, modelc, img, im0s)

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            if webcam:  # batch_size >= 1
                p, s, im0, frame = path[i], f'{i}: ', im0s[i].copy(), dataset.count
            else:
                p, s, im0, frame = path, '', im0s.copy(), getattr(dataset, 'frame', 0)

            s += '%gx%g ' % img.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh

            if len(det):
                print("in det")
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string


                # Write results

                for *xyxy, conf, cls in reversed(det):
                    if conf < 0.4:
                        continue
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        c = int(cls)  # integer class
                        line = (names[c], *xywh, conf) if save_conf else (names[c], *xywh)  # label format
                        with open(txt_path, 'a') as f:#直接写到固定 追加
                            f.write(('%s ' * len(line)).rstrip() % line + '\n')

                    if save_img:  # Add bbox to image
                        c = int(cls)  # integer class
                        code = names[c]
                        insect_name = sql_helper.get_name_by_code(code)
                        print(insect_name)
                        #label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                        label = None if hide_labels else (insect_name if hide_conf else f'{insect_name} {conf:.2f}')
                        im0 = plot_one_box(xyxy, im0, label=label, color=colors(c, True), line_thickness=line_thickness)

            # Print time (inference + NMS)
            print(f'{s}Done. ({t2 - t1:.3f}s)')

            # Save results (image with detections)
            save_path = r'./run/img.png'
            if save_img:
                if dataset.mode == 'image':
                    cv2.imwrite(save_path, im0) #这里考虑少写一次
                else:  # 'video' or 'stream'
                    if vid_path != save_path:  # new video
                        vid_path = save_path
                        if isinstance(vid_writer, cv2.VideoWriter):
                            vid_writer.release()  # release previous video writer
                        if vid_cap:  # video
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        else:  # stream
                            fps, w, h = 30, im0.shape[1], im0.shape[0]
                            save_path += '.mp4'
                        vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                    vid_writer.write(im0)



    print(f'Done. ({time.time() - t0:.3f}s)')




def main():
    model,device = pre_process()
    run(model, device)


if __name__ == "__main__":

    main()
