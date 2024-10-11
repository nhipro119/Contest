import nibabel
import cv2
import numpy as np
import matplotlib.pyplot as plt
out_img = nibabel.load("D:\\QT_project\\c1\\data\\output.nii.gz")
out_imgs = out_img.get_fdata()
out_imgs = out_imgs.astype(np.uint8)
out_imgs *= 255
areas = []
num_area = 1
pi = 3.14156
# ret,labels = cv2.connectedComponents(out_imgs[:,:,40])
# new_area = np.where(labels == 1)

# new_area = new_area[0]+pi*new_area[1]
# new_area = new_area.tolist()
# plt.imshow(labels)
# plt.show()
# print(new_area)
# print(new_area.shape)
class Area:
    def __init__(self, ar, area_idx):
        self.ar = ar
        self.continous = True
        self.area_idx = area_idx
        self.NOP = len(ar)
    def translate_area(self, new_area):
        self.ar = new_area
        self.NOP += len(new_area)
        self.continous = True
    def discontinous(self):
        self.continous = False

def create_area(ar):
    area = {"area":ar,"continue":True}
    return area
for i in range(128):
    # print("hinh",i,":",end=" ")
    ret, labels = cv2.connectedComponents(out_imgs[:,:,i])
    # new_area = np.where(labels == 1)
    
    # print(new_area)
    
    new_areas = []
    area_each_image = {}
    for dem1 in range(len(areas)):
        areas[dem1].discontinous()
    for r in range(1,ret):
        check_overlap = False
        new_area = np.where(labels == r)
        new_area = new_area[0]+pi*new_area[1]
        new_area = new_area.tolist()
        
        for idx,ar in enumerate(areas):
            overlap = set(ar.ar).intersection(set(new_area))
            if len(overlap) > 0:
                areas[idx].translate_area(new_area)
                check_overlap = True
                area_each_image[r] = areas[idx].area_idx

                break
            else:
                pass
                # areas[idx].discontinous()
            
        if not check_overlap:
            
            new_areas.append([new_area,r])

        

    for dem2 in range(len(areas)):
        if not areas[dem2].continous:
            areas[dem2].ar = []
    for new_area in new_areas:
        areas.append(Area(new_area[0],num_area))
        area_each_image[new_area[1]] = num_area
        num_area += 1
    for aai in area_each_image.keys():
        labels = np.where(labels == aai, area_each_image[aai],labels)
    print("hinh ",i,":",np.unique(labels))
    if (np.max(labels) > 0):
        plt.title(i)
        plt.imshow(labels)
        plt.show()
    


print(len(areas))