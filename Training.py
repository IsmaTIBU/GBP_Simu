import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os

class FixedIndustrialVisionSystem:
    def __init__(self, img_size=(224, 224), num_classes=4):
        self.img_size = img_size
        self.num_classes = num_classes
        self.model = None
        self.class_names = ['bp1_bp2', 'bp1_gp2', 'gp1_bp2', 'gp1_gp2']
        
    def create_fixed_model(self):
        """Crear modelo más simple y estable"""
        base_model = MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(*self.img_size, 3),
            alpha=1.0
        )
        
        base_model.trainable = True
        
        inputs = tf.keras.Input(shape=(*self.img_size, 3))
        x = base_model(inputs, training=True)
        x = GlobalAveragePooling2D()(x)
        x = Dropout(0.2)(x)
        x = Dense(64, activation='relu')(x)
        x = Dropout(0.1)(x)
        outputs = Dense(self.num_classes, activation='softmax', dtype='float32')(x)
        
        model = Model(inputs, outputs)
        
        model.compile(
            optimizer=Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print(f"✅ Modelo simplificado creado: {model.count_params():,} parámetros")
        return model
    
    def create_fixed_data_generators(self, data_dir):
        """Generadores de datos con augmentación MÁS CONSERVADORA"""
        
        # Augmentation to train the model with diferent "variances"
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=15,
            width_shift_range=0.15,
            height_shift_range=0.05,
            zoom_range=0.10,
            horizontal_flip=False,
            validation_split=0.2
        )
        
        val_datagen = ImageDataGenerator(
            rescale=1./255,
            validation_split=0.2
        )
        
        train_generator = train_datagen.flow_from_directory(
            data_dir,
            target_size=self.img_size,
            batch_size=15,
            class_mode='categorical',
            subset='training',
            shuffle=True
        )
        
        val_generator = val_datagen.flow_from_directory(
            data_dir,
            target_size=self.img_size,
            batch_size=16,
            class_mode='categorical',
            subset='validation',
            shuffle=False
        )
        
        return train_generator, val_generator
    
    def get_conservative_callbacks(self):
        """Callbacks más conservadores"""
        return [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-8,
                verbose=1
            ),
            tf.keras.callbacks.ModelCheckpoint(
                'best_model_fixed.keras',
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            )
        ]
    
    def diagnose_data(self, data_dir):
        """Diagnosticar problemas en los datos"""
        print("\n=== DIAGNÓSTICO DE DATOS ===")
        
        for class_name in self.class_names:
            class_dir = os.path.join(data_dir, class_name)
            if os.path.exists(class_dir):
                count = len([f for f in os.listdir(class_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
                print(f"{class_name}: {count} imágenes")
            else:
                print(f"❌ {class_name}: Carpeta no encontrada")
        
        test_gen = ImageDataGenerator(rescale=1./255)
        sample_gen = test_gen.flow_from_directory(
            data_dir,
            target_size=self.img_size,
            batch_size=1,
            class_mode='categorical',
            shuffle=False
        )
        return True

def train_with_fixes(data_dir="data/"):
    """Entrenar con todas las correcciones aplicadas"""
    
    system = FixedIndustrialVisionSystem(img_size=(224, 224))
    
    system.diagnose_data(data_dir)
    
    model = system.create_fixed_model()
    system.model = model
    
    train_gen, val_gen = system.create_fixed_data_generators(data_dir)
    
    print(f"\n=== CONFIGURACIÓN CORREGIDA ===")
    print(f"Datos entrenamiento: {train_gen.samples}")
    print(f"Datos validación: {val_gen.samples}")
    print(f"Clases: {train_gen.class_indices}")
    
    callbacks = system.get_conservative_callbacks()
    
    print(f"\n=== INICIANDO ENTRENAMIENTO CORREGIDO ===")
    history = model.fit(
        train_gen,
        epochs=10,
        validation_data=val_gen,
        callbacks=callbacks,
        verbose=1
    )
    
    return model, history

if __name__ == "__main__":
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '1'
    
    model, history = train_with_fixes()
    
    print("\n=== ENTRENAMIENTO COMPLETADO ===")
    print("Modelo guardado como 'best_model_fixed.keras'")