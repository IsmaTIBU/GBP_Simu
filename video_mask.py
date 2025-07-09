from PIL import Image
import numpy as np
import cv2

cap = cv2.VideoCapture('Simu_Kepar.mp4')
# print(img.size)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"width:{width}, height:{height}")

mask1 = np.zeros((height, width), dtype=np.uint8)
mask2 = np.zeros((height, width), dtype=np.uint8)

xa1, ya1 = 290, 700
xa2, ya2 = 780, 825

xb1, yb1 = 1350, 550
xb2, yb2 = 1750, 650

mask1[ya1:ya2, xa1:xa2] = 255
mask2[yb1:yb2, xb1:xb2] = 255
mask = np.maximum(mask1, mask2)
mask_img = Image.fromarray(mask)


# Mask -> 3D for RGB
mask_3d = np.stack([mask_img] * 3, axis=-1)

DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720


output_filename = 'Output/output_masked_video.avi'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_filename, fourcc, 30.0, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    masked_frame = np.where(mask_3d == 255, frame, 0)

    resized_frame = cv2.resize(masked_frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    cv2.imshow('Masked Video', resized_frame)

    out.write(resized_frame)

    # ESC to exit
    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()