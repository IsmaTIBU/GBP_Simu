import cv2
import os

VIDEO = "Output/output_masked_video.avi"
CARPETA = "data"

os.makedirs(CARPETA, exist_ok=True)

cap = cv2.VideoCapture(VIDEO)
frame_num = 0

print("🎬 Extrayendo fotogramas...")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    cv2.imwrite(f"{CARPETA}/frame_{frame_num:05d}.jpg", frame)
    frame_num += 1
    
    if frame_num % 100 == 0:
        print(f"📸 {frame_num} frames procesados...")

cap.release()
print(f"✅ ¡Listo! {frame_num} fotogramas en carpeta '{CARPETA}'")