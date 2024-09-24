# # # """Test GL volume tool with MRI data."""

# # # from pyqtgraph.Qt import QtGui, QtWidgets, QtCore
# # # import pyqtgraph.opengl as gl
# # # import numpy as np
# # # from nibabel import load

# # # FILENAME = r"X:\Braillic\NIFT to Volume\MR_Gd.nii\MR_Gd.nii"
# # # RENDER_TYPE = "translucent"
# # # THR_MIN = 1
# # # THR_MAX = 2000

# # # # =============================================================================
# # # # Get MRI data
# # # nii = load(FILENAME)
# # # data = np.squeeze(nii.get_fdata())

# # # data[data == 0] = THR_MIN
# # # data[data < THR_MIN] = THR_MIN
# # # data[data >= THR_MAX] = THR_MAX
# # # data -= THR_MIN
# # # data /= THR_MAX - THR_MIN

# # # # (optional) Reorient data
# # # data = data[:, ::-1, :]

# # # # Prepare data for visualization
# # # # Cropping code implemented here. Can specify how much to crop and along what axis
# # # # Prepare data for visualization

# # # half_x = data.shape[0] // 2
# # # cropped_data = data[:half_x, :, :]
# # # d2 = np.zeros(cropped_data.shape + (4,))
# # # d2[..., 3] = cropped_data**1 * 255  # alpha
# # # d2[..., 0] = d2[..., 3]  # red
# # # d2[..., 1] = d2[..., 3]  # green
# # # d2[..., 2] = d2[..., 3]  # blue

# # # # (optional) RGB orientation lines
# # # d2[:40, 0, 0] = [255, 0, 0, 255]
# # # d2[0, :40, 0] = [0, 255, 0, 255]
# # # d2[0, 0, :40] = [0, 0, 255, 255]
# # # d2 = d2.astype(np.ubyte)

# # # # =============================================================================
# # # # Create qtgui
# # # app = QtWidgets.QApplication([])
# # # w = gl.GLViewWidget()
# # # w.setGeometry(0, 0, int(1080/2), int(1920/2))
# # # w.setCameraPosition(distance=120, elevation=0, azimuth=0)
# # # w.pan(0, 0, 10)
# # # w.setWindowTitle(FILENAME)
# # # w.show()

# # # # glOptions are 'opaque', 'translucent' and 'additive'
# # # v = gl.GLVolumeItem(d2, sliceDensity=6, smooth=False, glOptions=RENDER_TYPE)
# # # v.translate(dx=-d2.shape[0]/2, dy=-d2.shape[1]/2, dz=-d2.shape[2]/3)
# # # w.addItem(v)


# # # # =============================================================================
# # # def update_orbit():
# # #     """Rotate camera orbit."""
# # #     global counter
# # #     counter += 1
# # #     w.orbit(1, 0)  # degree


# # # def stop_and_exit():
# # #     """Stop and exit program."""
# # #     app.quit()
# # #     print("Finished")


# # # # =============================================================================
# # # if __name__ == '__main__':
# # #     # Initiate timer
# # #     timer1 = QtCore.QTimer()
# # #     timer2 = QtCore.QTimer()
# # #     counter = 0
# # #     # Connect stuff
# # #     timer1.timeout.connect(update_orbit)
# # #     timer2.timeout.connect(stop_and_exit)

# # #     # Start timer (everytime this time is up connects are excuted)
# # #     NR_FRAMES = 360
# # #     FRAMERATE = 1000 // 2  # ms, NOTE: keep it high to guarantee all frames  # ms, NOTE: keep it high to guarantee all frames
# # #     timer1.start(FRAMERATE)
# # #     timer2.start((NR_FRAMES * FRAMERATE) + 2000)

# # #     # Start program
# # #     QtWidgets.QApplication.instance().exec_()
# # import urllib3
# # import base64
# # import json
# # with open("2400106729.nii.gz","rb") as f:
# #     data = f.read()
# # encode_data = base64.b64encode(data)
# # encode_data_str = encode_data.decode("ascii")

# # http = urllib3.PoolManager()
# # param = json.dumps({"filedata":encode_data_str,
# #                     "patientID":"0123456780",
# #                     "authID":"Y2hpdGhpZW4yMDI0LTA5LTIwIDE2OjE4OjAyLjg3ODE5OQ==",
# #                     "Name":"2400106729.nii.gz"})
# # res = http.request("POST","103.63.121.200:9012/upload",headers={'Content-Type': 'application/json'},body=param)
# # print(res.data)

# import nibabel
# import matplotlib.pyplot as plt
# import cv2
# import numpy as np
imgs = nibabel.load("240010729.nii.gz")

print(imgs)
print(imgs.get_fdata().shape)
img = imgs.get_fdata()
# for i in range(128):
img = img * 255
img = img.astype(np.uint8)
# area = []
# for i in range(128):
#     for
frame = cv2.cvtColor(img[:,:,64], cv2.COLOR_GRAY2RGB)
# frame = img[64]

# frame[:,:,1:] = frame[:,:,1:] * 0
r = frame[:,:,:1]
g = frame[:,:,1:2]
b = frame[:,:,2:]
r = np.where(r == 0, 1, 255)
g = np.where(g == 0, 1, 0)
b = np.where(b == 0, 1, 0)
frame = np.concatenate([r,g,b],axis=2)
# frame = np.where(frame == [255,0,0], 1, 255)
plt.imshow(frame)
plt.show()

in_img = nibabel.load("2400106729.nii.gz")

in_img = in_img.get_fdata()
# in_img = in_img *255
in_img = in_img.astype(np.uint8)

img64 = cv2.cvtColor(in_img[:,:,64], cv2.COLOR_GRAY2RGB)

total_img = img64 * frame
plt.imshow(total_img)
plt.show()
# cv2.imshow("img",frame)
# cv2.waitkey()
import urllib3
import os
import json
import base64
mri_data = open(os.path.join(os.getcwd(),"data","input.nii.gz"), "rb").read()
# mri_data = base64.b64encode(mri_data)
# mri_data = mri_data.decode("ascii")
file_data = ("input.nii.gz",mri_data)
http =urllib3.PoolManager()
rs = http.request("POST","103.63.121.200:9010/predict",fields={"file":file_data})
if rs.status == 200:
    rs_data = rs.data.decode("ascii")
    dict_data = json.loads(rs_data)
    file_data = dict_data["file"]
    volume_data = dict_data["volume"]
    file_data = file_data.encode("ascii")
    file_data = base64.b64decode(file_data)
    with open(os.path.join(os.getcwd(),"data","output.nii.gz"),"wb") as f:
        f.write(file_data)
    print(volume_data)
print(rs.status)