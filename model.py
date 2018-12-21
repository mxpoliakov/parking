from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping
import numpy as np

def train(input, out, rows=235, cols=135, epochs=25):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=(rows, cols, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(units=128, activation='relu'))
    model.add(Dense(units=1, activation='sigmoid'))
    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

    train_generator = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
    test_generator = ImageDataGenerator(rescale=1./255)

    train = train_generator.flow_from_directory(input + '/train', target_size=(rows, cols), class_mode='binary')
    test = test_generator.flow_from_directory(input + '/test', target_size=(rows, cols), class_mode='binary')
    callbacks = [EarlyStopping(monitor='val_loss', patience=2)]

    model.fit_generator(train, epochs=epochs, 
                    steps_per_epoch=train.samples // 32, 
                    validation_data=test, validation_steps=test.samples // 32,
                    class_weight={0:1, 1:3}, callbacks=callbacks)
    
    validation = test_generator.flow_from_directory(input + '/validation', target_size=(rows, cols), class_mode='binary')

    score = model.evaluate_generator(validation, validation.samples // 32, workers=12)
    print('Validation accuracy:', score[1])
    model.save(out)
    print('Model saved')

def predict_one(model, img):
    return model.predict_classes(np.expand_dims(img, axis=0) / 255)[0][0]