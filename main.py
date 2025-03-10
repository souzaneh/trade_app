# -*- coding: utf-8 -*-
"""Trade_App_Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vPbMwfwmdHWPZcu9acS20YWlikrIAI-J

# import liberary  // data _prepration
"""

import tensorflow as tf
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#import  sklearn
from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential
from keras.layers import Dense, SimpleRNN,LSTM, GRU

#!pip install yfinance

import yfinance as yf

import datetime
# Set the end date to the current date
now = datetime.datetime.now()
end_date = now .strftime('%Y-%m-%d')
start_date = (now - datetime.timedelta(days=20)).strftime('%Y-%m-%d')
ms = yf.download('GOOGL', start=start_date , end=end_date, progress=False)
df = ms [['Open','Close', 'High', 'Low']].round(3)
df

x_step = 10
y_step = 2
train_ratio = 1

# prepration data(train/validation splite, return sequences)

def sequence_data (df, x_step, y_step,train_ratio):

#train/val split:
  h = int(train_ratio*len(df))
  train = df[: h]
  val = df [h-(x_step+y_step):]

  train_C = train.Close.values
  val_C = val.Close.values
  print ('train_C.shape:',train_C.shape)
  print ('val_C.shape:',val_C.shape)
  sc = MinMaxScaler(feature_range=(0,1))
  train_C_s = sc.fit_transform(train_C)


  #train sequences
  x_seq = []
  y_seq = []
  for i in range(x_step, len(train_C)-y_step+1):
    x_seq.append(train_C_s[i-x_step:i,0]) # 0: make (n,1) to (n,) shape, convert from culomn/vertically display to row/horizontally display
    y_seq .append (train_C_s[i:i+y_step,0])

  x_train= np.array(x_seq)
  x_train = x_train .reshape(x_train.shape[0],x_train.shape[1],1)
  y_train= np.array(y_seq)

  #val sequences
  val_C_s = sc.transform(val_C)
  x_seq = []
  y_seq = []
  for i in range(x_step, len(val_C)-y_step+1):
    x_seq.append(val_C_s[i-x_step:i,0])
    y_seq .append (val_C_s[i:i+y_step,0])

  x_val= np.array(x_seq)
  x_val = x_val .reshape(x_val.shape[0],x_val.shape[1],1)
  y_val= np.array(y_seq)


  return x_train, y_train, x_val, y_val,sc,  train_C,val_C,

# prepration data(train/validation splite, return sequences)
x_train,  y_train , x_val, y_val, sc,train_C_df,val_C_df = sequence_data(df, x_step, y_step,train_ratio)

from tensorflow.keras.models import load_model

# Part 1: Data extraction/preprocessing
#def prepare_data():
    # Your code to fetch and clean data
  #  return processed_data

# Part 2: Load model and predict
def run_prediction():
    model = load_model("LSTM_GRU_model.keras")
   # data = prepare_data()
    predictions = sc.inverse_transform(model.predict(x_train) )
   # predictions = model.predict(data)
    pd.DataFrame(predictions).to_csv("predictions.csv", index=False)


if __name__ == "__main__":
    run_prediction()

