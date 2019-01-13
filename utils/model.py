from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping
import numpy as np


class Model(object):

    def __init__(self, model=None):
        if type(model) == str:
            self.load_model(model)
        else:
            self.model = model

    def train(self, input_dir, output_name, rows=235, cols=135, epochs=25):
        model = Sequential()
        model.add(Conv2D(32, (3, 3), input_shape=(rows, cols, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Conv2D(32, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(units=128, activation='relu'))
        model.add(Dense(units=1, activation='sigmoid'))
        model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

        train_generator = ImageDataGenerator(rescale=1. / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
        test_generator = ImageDataGenerator(rescale=1. / 255)

        train = train_generator.flow_from_directory(input_dir + '/train', target_size=(rows, cols), class_mode='binary')
        test = test_generator.flow_from_directory(input_dir + '/test', target_size=(rows, cols), class_mode='binary')
        callbacks = [EarlyStopping(monitor='val_loss', patience=2)]

        model.fit_generator(train, epochs=epochs,
                steps_per_epoch=train.samples // 32, validation_data=test,
                validation_steps=test.samples // 32, class_weight={0: 1, 1: 3},
                callbacks=callbacks)

        validation = test_generator.flow_from_directory(input_dir + '/validation',
                target_size=(rows, cols), class_mode='binary')

        score = model.evaluate_generator(validation, validation.samples // 32,
                workers=12)

        print('Validation accuracy:', score[1])

        self.model = model
        self.export_model(output_name)

    def export_model(self, output_name):
        if self.model is not None:
            self.model.save(output_name)

    def load_model(self, input_name):
        self.model = load_model(input_name)

    def predict(self, img):
        return self.model.predict_classes(np.expand_dims(img, axis=0) / 255)[0][0]
