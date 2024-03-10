import os
import cv2
from tqdm import tqdm


def get_imgs_pos(img_w, img_h, cut_w, cut_h, w_stride, h_stride):
    imgs_pos = []
    for beg_w in range(0, img_w, w_stride):
        for beg_h in range(0, img_h, h_stride):
            x0, y0 = beg_w, beg_h  # 左上角的点
            x1, y1 = beg_w + cut_w, beg_h + cut_h
            if x1 > img_w:  # x轴上超出图像边界
                x1 = img_w
                x0 = img_w - cut_w
            if y1 > img_h:  # y轴上超出图像边界
                y1 = img_h
                y0 = img_h - cut_h
            imgs_pos.append([x0, y0, x1, y1])
            if y1 == img_h:  # 如果超出边界
                break
    return imgs_pos


def save_subimg(cv_img, pos, img_save_dir, img_name, idx):
    x0, y0, x1, y1 = pos
    crop_img = cv_img[y0:y1, x0:x1]
    cv2.imwrite(os.path.join(img_save_dir, img_name[0:-4] + "_" + "{:04d}".format(idx) + ".jpg"), crop_img)


def save_sublabs(sub_labels, label_save_dir, img_name, idx):
    lab_path = os.path.join(label_save_dir, img_name[0:-4] + "_" + "{:04d}".format(idx) + ".txt")
    with open(lab_path, 'w') as fw:
        for lab in sub_labels:
            line = " ".join(str(num) for num in lab)
            fw.write(line + "\n")


def read_labels(txt_path):
    pos = []
    with open(txt_path, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            if not lines:
                break
                pass
            p_tmp = [float(i) for i in lines.split(' ')]
            pos.append(p_tmp)  # 添加新读取的数据
            pass
    return pos


def get_sublabels(pos, labels, img_w, img_h, cut_w, cut_h):
    x0, y0, x1, y1 = pos  # 得到该子图在大图上的位置，左上角和右下角的坐标
    sub_labs = []
    for lab in labels:
        cx, cy, w, h = lab[1] * img_w, lab[2] * img_h, lab[3] * img_w, lab[4] * img_h  # 换算得到真实的中心点及宽高,注意第一个是标签的类别
        if x0 < cx < x1 and y0 < cy < y1:  # 如果该标签的中心点落到了子图上
            # 如果当前的标签落到了子图像的边界上, 处理该标签在子图上的宽的问题
            if cx - x0 < w / 2:
                w = w / 2 + (cx - x0)
            if x1 - cx < w / 2:
                w = w / 2 + (x1 - cx)
            # 如果当前的标签落到了子图像的边界上, 处理该标签在子图上的高的问题
            if cy - y0 < h / 2:
                h = h / 2 + (cy - y0)
            if y1 - cy < h / 2:
                h = h / 2 + (y1 - cy)
            cx, cy = cx - x0, cy - y0  # 将当前的坐标换算到子图上(宽高不变，只是中心点的位置发生了改变)
            sub_labs.append([int(lab[0]), cx / cut_w, cy / cut_h, w / cut_w, h / cut_h])  # 重新归一化
    return sub_labs


if __name__ == '__main__':
    img_dir = ""
    img_list = os.listdir(img_dir)
    img_save_dir = ""

    cut_w = 640  
    cut_h = 640
    w_stride = 630
    h_stride = 630
    count = 0
    for img_name in tqdm(img_list):
        sub_count = 0
        if img_name.endswith((".jpg", ".JPG")):
            img_path = os.path.join(img_dir, img_name)
            cv_img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
            img_w, img_h = cv_img.shape[1], cv_img.shape[0]
            if img_w > cut_w and img_h > cut_h:  # 如果原图的大小是大于需要裁剪的图像大小
                imgs_pos = get_imgs_pos(img_w, img_h, cut_w, cut_h, w_stride, h_stride)
                if len(imgs_pos):  # 如果原图像被拆分为了多个子图像
                    for idx, pos in enumerate(imgs_pos):  # 逐个对所有子图像寻找其图上的子lables
                        sub_count += 1
                        save_subimg(cv_img, pos, img_save_dir, img_name, idx)  # 保存该子图像
        count += sub_count
    print("Generate total images is:", count)