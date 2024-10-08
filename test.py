import nibabel
import cv2
import matplotlib.pyplot as plt
import numpy as np
imgs = nibabel.load("D:\\QT_project\\CT_SCAN\\Contest\\data\\output.nii.gz")

pixdim = imgs.header["pixdim"][1:4]
pixdim = pixdim[0]*pixdim[1]*pixdim[2]

imgs = imgs.get_fdata()


num_p = np.count_nonzero(imgs)
print(num_p*pixdim/1000)
img64 = imgs[:,:,64]
img64 = img64.astype(np.uint8)
# img64 *=255
ret, labels = cv2.connectedComponents(img64)
full_imgs = []

imgs = imgs.astype(np.uint8)

for i in range(128):
    area = []
    img = imgs[:,:,i]
    ret, labels = cv2.connectedComponents(img)
    for lb in range(1,ret):
        area.append(np.count_nonzero(labels == lb))
    full_imgs.append(area)

print(full_imgs)
# label_hue = np.uint8(179 * labels / np.max(labels))
# blank_ch = 255 * np.ones_like(label_hue)
# labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
# labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
# labeled_img[label_hue == 0] = 0
# plt.subplot(222)
# plt.title('Objects counted:'+ str(ret-1))
# plt.imshow(labels)
# print('objects number is:', ret-1)
# plt.show()
# print("max lb",np.max(labels))
# area = []
# for lb in range(1,ret):
#     area.append(np.count_nonzero(labels == lb))
# print(area)
# print(len(area))
# print(ret)
# print(ret, labels.shape)
# cv2.imshow("img",img64)
# cv2.waitKey()
# plt.imshow(imgs[:,:,64])
# plt.show()