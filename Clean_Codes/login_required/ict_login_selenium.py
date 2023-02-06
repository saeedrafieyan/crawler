#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import urllib.request
from unidecode import unidecode

import os
from PIL import Image, ImageOps
import numpy as np
from keras_preprocessing.sequence import pad_sequences

from keras.layers import Dense, LSTM, Reshape, BatchNormalization, Input, Conv2D, MaxPool2D, Lambda, Bidirectional
from keras.models import Model
import keras.backend as K
from keras.callbacks import ModelCheckpoint

import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from unidecode import unidecode


# In[2]:


def captcha_solver(address):
    filenames = []
    for dirname, _, files in os.walk(address):
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


    path = r'/temp/'

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
    pred = ''
    for x in out:
    #     print("original_text =  ", valid_orig_txt[i])
    #     print("predicted text = ", end='')
        for p in x:
            if int(p) != -1:

                pred += str(p)
    #             print(char_list[int(p)], end='')
        print('\n')
        i += 1
    return((pred))


# In[3]:


driver = webdriver.Chrome("r'/chromedriver_win32")


# In[4]:


# head to github login page
driver.get("https://adsl.tci.ir/panel/")


# In[5]:


img = driver.find_element(By.ID,'loginCaptchaImage')
# driver.find_element(By.XPATH,'/html/body/div/div[2]/div[1]/div/div[2]/form/div[4]/img')
src = img.get_attribute('src')

# download the image
urllib.request.urlretrieve(src, r"\\temp\\0000.png")


# In[6]:


from PIL import Image

element = driver.find_element(By.ID, "loginCaptchaImage")

location = element.location
size = element.size

driver.save_screenshot(r"D:\hiweb\exports\temp\0000.png")

x = location['x']
y = location['y']
w = size['width']
h = size['height']
width = x + w
height = y + h

im = Image.open(r"D:\hiweb\exports\temp\0000.png")
im = im.crop((int(x), int(y), int(width), int(height)))
im = im.resize((306, 64))
im.save(r"D:\hiweb\exports\temp\0000.png")


# In[7]:



captcha = captcha_solver('/temp')
# captcha


# In[8]:


# Github credentials
username = '2177492386'
password = '216011'


# In[9]:


# find username/email field and send the username itself to the input field
driver.find_element(By.XPATH,'/html/body/div/div[2]/div[1]/div/div[2]/form/div[2]/input').send_keys(username)

# find password input field and insert password as well
driver.find_element(By.XPATH,'/html/body/div/div[2]/div[1]/div/div[2]/form/div[3]/input').send_keys(password)

#captcha
driver.find_element(By.XPATH,'/html/body/div/div[2]/div[1]/div/div[2]/form/div[5]/input').send_keys(captcha)


# In[10]:


# click login button
driver.find_element(By.XPATH,'/html/body/div/div[2]/div[1]/div/div[2]/form/div[6]/button').click()


# In[11]:


# wait the ready state to be complete
WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)
error_message = "کد امنیتی وارد شده نادرست است."

# get the errors (if there are)
errors = driver.find_elements(By.XPATH,"/html/body/div[2]")

# if we find that error message within errors, then login is failed
if any(error_message in e.text for e in errors):
    print("[!] Login failed")
else:
    print("[+] Login successful")


# In[12]:


driver.get('https://adsl.tci.ir/panel/change-service')


# In[ ]:





# In[13]:






# from selenium.webdriver.support.ui import WebDriverWait 
# from selenium.webdriver.support import expected_conditions as EC
# items = WebDriverWait(driver,30).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "uk-card uk-card-default")]')))


# In[21]:


from unidecode import unidecode

product_type, traffic, bandwidth, duration, FCP, price = [], [], [], [], [], []
items = driver.find_elements(By.XPATH, '//div[contains(@class, "uk-card uk-card-default")]')
items = items[5:]
cards = []
for item in items:
    cards.append(item.text)
    
for card in cards:
    card = card.replace('+', '*')
    card = card.replace('-', '*')
    card = card.replace('\n', '*')
    card = card.replace('/', '*')
    card = card.split('*')
    traffic.append(card[0])
    FCP.append('TCI')
    product_type.append('سرویس')
    for i in range(len(card)):
        if 'ریال' in card[i]:
            price.append(card[i])
        if 'مگابیت در ثانیه' in card[i]:
            bandwidth.append(card[i])
        if 'قرارداد' in card[i]:
            duration.append(card[i])
            


# In[22]:


# print(items[0].text)


# In[23]:


traffic = [(x.split(' '))[0] for x in traffic]
traffic = [unidecode(x) for x in traffic]

bandwidth = [(x.split(' '))[0] for x in bandwidth]
bandwidth = [unidecode(x) for x in bandwidth]

duration = [(x.split(' '))[2] for x in duration]
duration = [unidecode(x) for x in duration]

price = [(x.split(' '))[2] for x in price]
price = [unidecode(x) for x in price]
price = [x.replace(',','') for x in price]


# In[24]:


dataset = pd.DataFrame(({'FCP':FCP,'product type':product_type, 'traffic':traffic,'bandwidth':bandwidth, 'duration':duration, 'price':price}))
# dataset


# In[25]:


date = datetime.today().strftime('%Y-%m-%d')
time = int(time.time())
dataset.to_csv(f'TCI_{date}_{time}.csv', encoding='utf-8-sig', index=False)
        




