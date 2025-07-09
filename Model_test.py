import cv2
import numpy as np
import tensorflow as tf

# 1. LOAD TRAINED MODEL
print("Cargando modelo...")
model = tf.keras.models.load_model('best_model_fixed.keras')
class_names = ['bp1_bp2', 'bp1_gp2', 'gp1_bp2', 'gp1_gp2']
print("✅ Modelo cargado")

def predict_frame(frame):
    """Toma un frame del video y predice la clase"""
    
    frame_small = cv2.resize(frame, (224, 224))
    
    frame_normalized = frame_small.astype(np.float32) / 255.0
    
    frame_batch = np.expand_dims(frame_normalized, axis=0)
    
    predictions = model.predict(frame_batch, verbose=0)
    
    confidence = np.max(predictions)
    predicted_class_idx = np.argmax(predictions)
    predicted_class = class_names[predicted_class_idx]
    
    return predicted_class, confidence

# 3. Rectangle drawings on the frame
def draw_indicators(frame, predicted_class, confidence):
    """Dibuja cuadrados de colores según la detección"""
    
    height, width = frame.shape[:2]
    
    pos1_start = (190, 465)
    pos1_end = (520, 550)
    pos2_start = (900, 365) 
    pos2_end = (1168, 435)
    
    # BGR format for OpenCV
    green_color = (0, 255, 0)
    red_color = (0, 0, 255)
    
    if predicted_class in ['gp1_gp2', 'gp1_bp2']:  # gp1 = good position 1, bp2 = bad position 2
        cv2.rectangle(frame, pos1_start, pos1_end, green_color, 3)
    else:
        cv2.rectangle(frame, pos1_start, pos1_end, red_color, 3)
    
    if predicted_class in ['gp1_gp2', 'bp1_gp2']:  # gp2 = good position 2, bp1 = bad position 1
        cv2.rectangle(frame, pos2_start, pos2_end, green_color, 3)
    else:
        cv2.rectangle(frame, pos2_start, pos2_end, red_color, 3)
    
    text_y = height - 60
    cv2.putText(frame, f"Deteccion: {predicted_class}", (20, text_y), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f"Confianza: {confidence:.2f}", (20, text_y + 25), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    return frame

def process_video(video_path, output_path=None, show_video=True):
    """Procesa el video frame por frame con indicadores visuales"""
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"❌ No se pudo abrir el video: {video_path}")
        return
    
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    out = None
    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        print(f"   Guardando video procesado en: {output_path}")
    
    frame_count = 0
    results = []
    current_prediction = None
    current_confidence = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Predict for every 10 frames
        if frame_count % 10 == 0:
            current_prediction, current_confidence = predict_frame(frame)
            
            if frame_count % fps == 0:
                timestamp = frame_count / fps
                results.append({
                    'tiempo': timestamp,
                    'clase': current_prediction,
                    'confianza': current_confidence
                })
                print(f"   {timestamp:6.1f}s: {current_prediction} ({current_confidence:.2f})")
        
        if current_prediction:
            frame = draw_indicators(frame, current_prediction, current_confidence)
        
        if out:
            out.write(frame)
        
        if show_video:
            cv2.imshow('Video Industrial - Detección de Posiciones', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("   Saliendo...")
                break
            elif key == ord(' '):
                print("   Pausado - Presiona ESPACIO para continuar")
                while True:
                    if cv2.waitKey(1) & 0xFF == ord(' '):
                        break
        
        frame_count += 1
    
    cap.release()
    if out:
        out.release()
    if show_video:
        cv2.destroyAllWindows()
    
    print(f"✅ Completed process")
    return results

# 4. ANALIZAR RESULTADOS
def analyze_results(results):
    """Analiza los resultados del video"""
    
    if not results:
        print("❌  No results to analyze")
        return
    
    class_counts = {}
    high_confidence_count = 0
    
    for result in results:
        clase = result['clase']
        confianza = result['confianza']
        
        if clase not in class_counts:
            class_counts[clase] = 0
        class_counts[clase] += 1
        
        if confianza > 0.8:
            high_confidence_count += 1
    
    print(f"\nACCURACY:")
    reliable_percentage = (high_confidence_count / len(results)) * 100
    print(f"   Good accuracy (>80%): {high_confidence_count}/{len(results)} ({reliable_percentage:.1f}%)")

def main():
    """Función principal del programa"""
    
    video_path = "Output/output_masked_video.avi"
    
    output_path = "Output/Model_processed_video.mp4"
    
    print(f"Processing: {video_path}")
    
    # Processing
    results = process_video(video_path, output_path=output_path, show_video=True)
    
    print("\n¡Processing finished!")
    print(f"📁 Video saved in: {output_path}")

if __name__ == "__main__":
    main()