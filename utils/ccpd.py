import os
import random
import shutil

source_images_directory = "../DectPlateData/CCPD_Data/images"
source_labels_directory = "../DectPlateData/CCPD_Data/labels"
destination_directory = './Pro_Data'

max_test_files = 64
max_train_files = 1024
max_val_files = 128


def process():
    # 确保目标文件夹存在
    if not os.path.exists(source_images_directory):
        print('Source image directory does not exist!')

    if not os.path.exists(source_labels_directory):
        print('Source labels directory does not exist!')

    if not os.path.exists(destination_directory):
        os.makedirs(os.path.join(destination_directory, 'train', 'images'))
        os.makedirs(os.path.join(destination_directory, 'train', 'labels'))
        os.makedirs(os.path.join(destination_directory, 'val', 'images'))
        os.makedirs(os.path.join(destination_directory, 'val', 'labels'))
        os.makedirs(os.path.join(destination_directory, 'test', 'images'))
        os.makedirs(os.path.join(destination_directory, 'test', 'labels'))

    test_files = []
    train_files = []
    val_files = []

    # 随机采样数据
    for filename in os.listdir(source_images_directory):
        rand_num = random.randint(1, 64)

        if len(train_files) >= max_train_files and len(test_files) >= max_test_files and len(
                val_files) >= max_val_files:
            break

        if 1 <= rand_num <= 8 and len(train_files) < max_train_files:
            train_files.append(filename[0:-4])
            img_source = os.path.join(source_images_directory, filename)
            destination = os.path.join(destination_directory, 'train', 'images', filename)
            shutil.copyfile(img_source, destination)
            lab_source = os.path.join(source_labels_directory, filename[0:-4] + ".txt")
            destination = os.path.join(destination_directory, 'train', 'labels', filename[0:-4] + ".txt")
            shutil.copyfile(lab_source, destination)

        elif 9 <= rand_num <= 16 and len(test_files) < max_test_files:
            test_files.append(filename[0:-4])
            img_source = os.path.join(source_images_directory, filename)
            destination = os.path.join(destination_directory, 'test', 'images', filename)
            shutil.copyfile(img_source, destination)
            lab_source = os.path.join(source_labels_directory, filename[0:-4] + ".txt")
            destination = os.path.join(destination_directory, 'test', 'labels', filename[0:-4] + ".txt")
            shutil.copyfile(lab_source, destination)

        elif 17 <= rand_num <= 28 and len(val_files) < max_val_files:
            val_files.append(filename[0:-4])
            img_source = os.path.join(source_images_directory, filename)
            destination = os.path.join(destination_directory, 'val', 'images', filename)
            shutil.copyfile(img_source, destination)
            lab_source = os.path.join(source_labels_directory, filename[0:-4] + ".txt")
            destination = os.path.join(destination_directory, 'val', 'labels', filename[0:-4] + ".txt")
            shutil.copyfile(lab_source, destination)
        else:
            pass


if __name__ == '__main__':
    process()
