import os
import shutil


# pic_dir = './dataset/SegmentationClass'
pic_dir = './result-105'
save_dir = './dataset'

person_num = pic_dir.split('-')[1]
for img_ori in os.listdir(pic_dir):
    img_ori_temp = img_ori
    num = int(img_ori_temp.split('.png')[0].split('-')[1])
    oldname = os.path.join(pic_dir, img_ori)
    newdir = os.path.join(save_dir, str(num))
    if not os.path.exists(newdir):
        os.makedirs(newdir)
    newname = os.path.join(newdir, person_num+'-'+img_ori)
    print(oldname, '======>', newname)
    shutil.copyfile(oldname, newname)