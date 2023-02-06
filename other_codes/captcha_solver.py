import os
from PIL import Image, ImageOps
import numpy as np
from keras_preprocessing.sequence import pad_sequences

from keras.layers import Dense, LSTM, Reshape, BatchNormalization, Input, Conv2D, MaxPool2D, Lambda, Bidirectional
from keras.models import Model
import keras.backend as K
from keras.callbacks import ModelCheckpoint

filenames = []
for dirname, _, files in os.walk('D:/hiweb/exports/temp'):
    for f in files:
        filenames = np.append(filenames, f)

num_samples = len(filenames)
print('number of samples: ', num_samples)

char_list = "0123456789"


def encode_to_labels(txt):
    # encoding each label into list of digits
    encoded_list = []
    for char in txt:
        encoded_list.append(char_list.index(char))

    return encoded_list


path = r'D:/hiweb/exports/temp/'

# lists for training dataset
training_img = []  # the images for training the model
training_txt = []  # the labels
train_input_length = []  # the input of LSTM part of the model
train_label_length = []  # the label's length (4 to 7)
train_orig_txt = []

# lists for validation dataset
valid_img = []
valid_txt = []
valid_input_length = []
valid_label_length = []
valid_orig_txt = []

max_label_len = 0  # max length for our labels (in this case 7)

for file in filenames:
    raw = Image.open(path + file)
    gray = ImageOps.grayscale(raw)
    img = np.array(gray)
    img = np.expand_dims(img, axis=2)
    img = img / 255.

    txt = file.split('.')[0]

    if len(txt) > max_label_len:
        max_label_len = len(txt)

    # split the dataset (85% train, 15% test)
    if np.random.rand() >= 0:
        valid_orig_txt.append(txt)
        valid_label_length.append(len(txt))
        valid_input_length.append(75)
        valid_img.append(img)
        valid_txt.append(encode_to_labels(txt))
    else:
        train_orig_txt.append(txt)
        train_label_length.append(len(txt))
        train_input_length.append(75)
        training_img.append(img)
        training_txt.append(encode_to_labels(txt))

train_padded_txt = pad_sequences(training_txt, maxlen=max_label_len, padding='post', value=len(char_list))
valid_padded_txt = pad_sequences(valid_txt, maxlen=max_label_len, padding='post', value=len(char_list))


def ctc_lambda_func(args):
    y_pred, labels, input_length, label_length = args

    return K.ctc_batch_cost(labels, y_pred, input_length, label_length)


training_img = np.array(training_img)
train_input_length = np.array(train_input_length)
train_label_length = np.array(train_label_length)

valid_img = np.array(valid_img)
valid_input_length = np.array(valid_input_length)
valid_label_length = np.array(valid_label_length)

training_txt = np.array(training_txt)
valid_txt = np.array(valid_txt)

inputs = Input(shape=(64, 306, 1))

conv_1 = Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
pool_1 = MaxPool2D(pool_size=(2, 2), strides=2)(conv_1)

conv_2 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool_1)
pool_2 = MaxPool2D(pool_size=(2, 2), strides=2)(conv_2)

conv_3 = Conv2D(256, (3, 3), activation='relu', padding='same')(pool_2)
conv_4 = Conv2D(256, (3, 3), activation='relu', padding='same')(conv_3)
pool_4 = MaxPool2D(pool_size=(2, 1))(conv_4)

conv_5 = Conv2D(512, (3, 3), activation='relu', padding='same')(pool_4)
batch_norm_5 = BatchNormalization()(conv_5)

conv_6 = Conv2D(512, (3, 3), activation='relu', padding='same')(batch_norm_5)
batch_norm_6 = BatchNormalization()(conv_6)
pool_6 = MaxPool2D(pool_size=(2, 1))(batch_norm_6)

conv_7 = Conv2D(512, (3, 3), activation='relu', padding='same')(pool_6)
batch_norm_7 = BatchNormalization()(conv_7)
pool_7 = MaxPool2D(pool_size=(2, 1))(batch_norm_7)

conv_8 = Conv2D(512, (2, 2), activation='relu')(pool_7)

squeezed = Lambda(lambda x: K.squeeze(x, 1))(conv_8)

blstm_1 = Bidirectional(LSTM(128, return_sequences=True, dropout=0.2))(squeezed)
blstm_2 = Bidirectional(LSTM(128, return_sequences=True, dropout=0.2))(blstm_1)

outputs = Dense(len(char_list) + 1, activation='softmax')(blstm_2)
prediction_model = Model(inputs, outputs)
# load the model weights
prediction_model.load_weights('model_weights_V1_1413data.hdf5')

# predict outputs on validation images
prediction = prediction_model.predict(valid_img[:20])

# use CTC decoder
out = K.get_value(K.ctc_decode(prediction, input_length=np.ones(prediction.shape[0]) * prediction.shape[1],
                               greedy=True)[0][0])

# see the results
i = 0
for x in out:
    print("original_text =  ", valid_orig_txt[i])
    print("predicted text = ", end='')
    for p in x:
        if int(p) != -1:
            print(char_list[int(p)], end='')
    print('\n')
    i += 1
