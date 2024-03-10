import os
import random
import shutil

"""
https://blog.csdn.net/weixin_42182534/article/details/129288927
该脚本实现了将原始数据集自动划分为yolo训练数据集排列形式 (目录排序如下)
old_root:
    dataset
        images
        yolo_labels

new_root:
    dataset
        test
            images
            labels
        train
            images
            labels  
        val
            images
            labels          
"""


# 文件的递归删除(清空path文件夹下的所有文件，但不会删除空文件夹)
def del_dir(path):
    for i in os.listdir(path):
        path_file = os.path.join(path, i)

        # 如果是一个文件就删除，不然继续递归文件夹。
        if os.path.isfile(path_file):
            os.remove(path_file)

        elif os.path.isdir(path_file):
            file = os.listdir(path_file)
            if len(file) == 0:
                os.rmdir(path_file)
            else:
                del_dir(path_file)
                os.rmdir(path_file)


def remake_dir(path):
    if os.path.exists(path):
        os.mkdir(os.path.join(path, "images"))
        os.mkdir(os.path.join(path, "labels"))
    else:
        os.mkdir(path)
        os.mkdir(os.path.join(path, "images"))
        os.mkdir(os.path.join(path, "labels"))


def copy_files(old_root, new_root):
    # 保证随机可复现
    # 这保证了每次调用copy_files函数时的随机值是相同的
    random.seed(0)

    file_lists = os.listdir(old_root)

    all_files = []
    train_files = []
    val_files = []
    test_files = []

    for file in file_lists:
        all_files.append(file)

    L = len(all_files)
    train_num = int(0.8 * L)
    val_num = int(0.2 * L)
    test_num = L - train_num - val_num

    # 随机选取训练数据
    for i in range(train_num):
        temp = random.choice(all_files)
        train_files.append(temp)
        all_files.remove(temp)
    # 随机选取验证数据
    for i in range(val_num):
        temp = random.choice(all_files)
        val_files.append(temp)
        all_files.remove(temp)
    # 随机选取测试数据
    for i in range(test_num):
        temp = random.choice(all_files)
        test_files.append(temp)
        all_files.remove(temp)

    # 拷贝对应的训练集数据
    for file_name in train_files:

        if ".png" in file_name or ".jpg" in file_name:
            t_name = str("train\\images")
        else:
            t_name = str("train\\labels")

        old_file_path = os.path.join(old_root + str("\\") + file_name)
        new_file_path = os.path.join(new_root + str("\\") + t_name + str("\\") + file_name)

        shutil.copy(old_file_path, new_file_path)

    # 拷贝对应的验证集数据
    for file_name in val_files:

        if ".png" in file_name or ".jpg" in file_name:
            t_name = str("val\\images")
        else:
            t_name = str("val\\labels")

        old_file_path = os.path.join(old_root + str("\\") + file_name)
        new_file_path = os.path.join(new_root + str("\\") + t_name + str("\\") + file_name)

        shutil.copy(old_file_path, new_file_path)

    # 拷贝对应的测试集数据
    # for file_name in test_files:
    #
    #     if ".png" in file_name or ".jpg" in file_name:
    #         t_name = str("test\\images")
    #     else:
    #         t_name = str("test\\labels")
    #
    #     old_file_path = os.path.join(old_root + str("\\") + file_name)
    #     new_file_path = os.path.join(new_root + str("\\") + t_name + str("\\") + file_name)
    #
    #     shutil.copy(old_file_path, new_file_path)

    return


def main():
    old_root = r""

    new_root = r""

    path_list = ["train", "val","test"]

    # 该部分循环实现了若文件夹存在则删除文件夹下的所有文件，并创建"images"和"labels"
    # 若文件夹不存在，则创建该文件，并创建子文件夹"images"和"labels"
    # 注释该部分则程序不会对文件是否存在进行判断，直接进行copy操作
    for path in path_list:
        path = os.path.join(new_root, path)
        if os.path.exists(path):
            del_dir(path)
            remake_dir(path)

        else:
            remake_dir(path)

    # 该部分实现对原始数据集的划分
    order_list = ["images", "labels"]
    for root in order_list:
        order_root = os.path.join(old_root, root)

        copy_files(order_root, new_root)


if __name__ == '__main__':
    main()
