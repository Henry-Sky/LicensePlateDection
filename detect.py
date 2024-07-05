import os
import shutil
import threading
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2

yolo_detect_scrip = ['python', 'yolov5/detect.py',
                     '--weights', 'yolov5/weights/best.pt',
                     '--img', "720",
                     '--source', 'cache/target/text.jpg',
                     '--save-txt'
                     ]

crnn_detect_scrip = ['python', 'crnn/demo.py',
                     '-m', 'crnn/weights/netCRNN.pth',
                     '-i', 'cache/target/text_cropped.jpg',
                     '-o', 'cache',
                     ]


def run_script(script):
    try:
        # 使用subprocess模块执行外部Python脚本
        subprocess.run(script, check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"执行失败: {e}")


def read_yolo_results(txt_file_path):
    results = []
    with open(txt_file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 5:
                class_id, center_x, center_y, width, height = map(float, parts)
                results.append((class_id, center_x, center_y, width, height))
    return results


def process_yolo_result(yolo_results):
    # 读取原图像
    image = cv2.imread('cache/target/text.jpg')
    h, w = image.shape[:2]
    # 遍历检测结果
    for i, (class_id, center_x, center_y, width, height) in enumerate(yolo_results):
        # 转换归一化坐标到像素坐标
        x = int((center_x - width / 2) * w)
        y = int((center_y - height / 2) * h)
        width = int(width * w)
        height = int(height * h)
        # 裁剪检测框
        buffer = 6
        cropped_image = image[y - buffer:y + height + buffer, x - buffer:x + width + buffer]
        # 保存裁剪后的图像
        cv2.imwrite("cache/target/text_cropped.jpg", cropped_image)
        print("缓存车牌聚焦图像")


def detect(source_img):
    if os.path.exists('cache'):
        shutil.rmtree('cache')
    if os.path.exists('output'):
        shutil.rmtree('output')
    os.mkdir('cache')
    os.mkdir("output")
    os.mkdir('cache/target')
    shutil.copy(source_img, 'cache/target/text.jpg')
    # 创建YOLOv5识别线程
    thread = threading.Thread(target=run_script, args=[yolo_detect_scrip])
    thread.start()
    thread.join()
    # 读取检测结果
    if os.path.isdir("yolov5/runs/detect"):
        shutil.move("yolov5/runs/detect", "cache")
        yolo_result = read_yolo_results("cache/detect/exp/labels/text.txt")
        process_yolo_result(yolo_result)
        print("成功获取检测结果")
    else:
        raise FileNotFoundError("错误！检测车牌位置结果不存在")
    # 创建C-RNN线程检测车牌内容线程
    thread = threading.Thread(target=run_script, args=[crnn_detect_scrip])
    thread.start()
    thread.join()
    # 读取检测结果
    result = "licenseplate"
    if os.path.exists("cache/results.txt"):
        print("成功获取车牌内容")
        with open("cache/results.txt", 'r', encoding='utf-8') as file:
            result = file.readline().strip()
        tmp = ""
        for i, chr in enumerate(result):
            if i == 1:
                tmp += chr + '-'
            else:
                tmp += chr
        result = tmp
        print("检测车牌结果: {}".format(result))
    # 输出结果图像
    shutil.copy("cache/target/text_cropped.jpg", "output/cropped_image.jpg")
    image = cv2.imread("cache/target/text.jpg")
    height, width, _ = image.shape
    # YOLO检测框信息 (class, x_center, y_center, width, height)
    for box in yolo_result:
        class_id, x_center, y_center, box_width, box_height = box
        # 计算实际坐标
        x_center = int(x_center * width)
        y_center = int(y_center * height)
        box_width = int(box_width * width)
        box_height = int(box_height * height)
        # 计算左上角和右下角坐标
        x1 = int(x_center - box_width / 2)
        y1 = int(y_center - box_height / 2)
        x2 = int(x_center + box_width / 2)
        y2 = int(y_center + box_height / 2)
        # 绘制矩形框
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 64, 0), 2)
        # 打上标签
        pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)
        font = ImageFont.truetype("simsun.ttc", 40, encoding="utf-8")
        draw.text((x1, y1 - 40), result, (0, 0, 0),
                  spacing=1, stroke_width=2, stroke_fill=(255, 128, 0), font=font)
        image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    cv2.imwrite('output/labeled_image.jpg', image)


if __name__ == "__main__":
    detect("source/text.jpg")
