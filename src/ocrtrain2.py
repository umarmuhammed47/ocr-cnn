import tensorflow as tf
import numpy as np
import pandas as pd
import cv2
import time
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.models import Sequential

trainingData = pd.read_csv('../datasets/data/trainingRecords.csv')
testData = pd.read_csv('../datasets/data/validationRecords.csv')
x_train = trainingData.loc[:, trainingData.columns != 'label']
y_train = trainingData['label']
x_test = testData.loc[:, testData.columns != 'label']
y_test = testData['label']
# print(x_train.loc[[0]])
x_train = x_train.to_numpy()
y_train = y_train.to_numpy()
x_test = x_test.to_numpy()
y_test = y_test.to_numpy()

print(x_train.shape)
x_train = np.reshape(x_train, (y_train.shape[0], 28, 28, 1))
x_test = np.reshape(x_test, (y_test.shape[0], 28, 28, 1))
print(x_train.shape)

# x_train, x_test = x_train / 255.0, x_test / 255.0

# cv2.imshow("image", x_train[0])
# cv2.waitKey(2000)

print(x_train.shape)
NAME = "{}-conv-{}-nodes-{}-dense{}".format(5, 128, 3, int(time.time()))
print('Name:', NAME)
tensorboard = TensorBoard(log_dir='logs/{}'.format(NAME))
model = Sequential()

model.add(Conv2D(filters=32, kernel_size=(3, 3), activation='relu', kernel_initializer='he_uniform', padding='same', input_shape=(28, 28, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(BatchNormalization())

# model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(BatchNormalization())

# model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
# model.add(BatchNormalization())

model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dense(384, activation='relu'))
model.add(Dense(256, activation='relu'))
model.add(Dense(192, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(62, activation='softmax'))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()
model.fit(x_train, y_train, epochs=50, batch_size=32, validation_split=0.2, callbacks=[tensorboard])
model.evaluate(x_test, y_test)
model.save("../finalModel5.hdf5")
