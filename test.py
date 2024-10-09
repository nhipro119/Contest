import nibabel
import cv2
import matplotlib.pyplot as plt
import numpy as np
imgs = nibabel.load("D:\\QT_project\\CT_SCAN\\Contest\\data\\output.nii.gz")
in_imgs = nibabel.load("D:\\QT_project\\CT_SCAN\\Contest\\data\\input.nii.gz")
pixdim = imgs.header["pixdim"][1:4]
pixdim = pixdim[0]*pixdim[1]*pixdim[2]

imgs = imgs.get_fdata()
img64 = imgs[:,:,38]
img64  = img64.astype(np.uint8)

# img64 = cv2.bitwise_not(img64)
img64 = np.where(img64 == 1, 0, 1)

plt.imshow(img64)
plt.show()
in_img = in_imgs.get_fdata()[:,:,38]
in_img = in_img*img64
in_img *= 255
in_img = in_img.astype(np.uint8)
in_img = cv2.cvtColor(in_img, cv2.COLOR_GRAY2BGR)
plt.imshow(in_img)
plt.show()

# num_p = np.count_nonzero(imgs)
# print(num_p*pixdim/1000)
# img64 = imgs[:,:,64]
# img64 = img64.astype(np.uint8)
# # img64 *=255
# ret, labels = cv2.connectedComponents(img64)
# full_imgs = []
# in_img = in_imgs[:,:,38]
# img
# imgs = imgs.astype(np.uint8)

# for i in range(128):
#     area = []
#     img = imgs[:,:,i]
#     ret, labels = cv2.connectedComponents(img)
#     for lb in range(1,ret):
#         area.append(np.count_nonzero(labels == lb))
#     full_imgs.append(area)
# plt.imshow(imgs[:,:,39])
# plt.show()
# print(full_imgs)


# max_length = len(max(full_imgs, key=len))
# print(max_length)
# img_np = []
# for im in full_imgs:
#     z = np.zeros(max_length-len(im))
#     m = np.asarray(im)
#     img_np.append(np.concatenate([m,z], axis=0))
# img_np = np.asarray(img_np)

# full_volume = np.sum(img_np,axis=0)
# print(full_volume)
# print(sum(full_volume)*pixdim)
img64 = imgs[:,:,38]
img64  = img64.astype(np.uint8)
img64 = img64*255
ret, labels = cv2.connectedComponents(img64)
label_hue = np.uint8(179 * labels / np.max(labels))
blank_ch = 255 * np.ones_like(label_hue)
labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
labeled_img[label_hue == 0] = 0

# plt.subplot(222)
# plt.title('Objects counted:'+ str(ret-1))
plt.imshow(labeled_img)
print('objects number is:', ret-1)
plt.show()

labeled_img = labeled_img + in_img
plt.imshow(labeled_img)
print('objects number is:', ret-1)
plt.show()
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
