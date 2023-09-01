import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
import yahoo_fin.stock_info as si
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard
from tensorflow.keras.layers import LSTM, Bidirectional, Dense, Dropout
from tensorflow.keras.models import Sequential


def load_stock_data(ticker, start_date, end_date):
    data = si.get_data(ticker, start_date=start_date, end_date=end_date)
    return data


def preprocess_data(data, window_size):
    data = data[["adjclose"]]
    scaler = preprocessing.MinMaxScaler()
    data = scaler.fit_transform(data)
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i : i + window_size])
        y.append(data[i + window_size])
    X = np.array(X)
    y = np.array(y)
    return X, y, scaler


def create_lstm_model(window_size):
    model = Sequential()
    model.add(LSTM(50, activation="relu", input_shape=(window_size, 1)))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mse")
    return model


ticker = "AAPL"
start_date = "2015-01-01"
end_date = "2020-01-01"
window_size = 60

data = load_stock_data(ticker, start_date, end_date)
X, y, scaler = preprocess_data(data, window_size)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = create_lstm_model(window_size)
history = model.fit(
    X_train,
    y_train,
    epochs=100,
    batch_size=32,
    validation_data=(X_test, y_test),
    verbose=1,
)

predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions)
y_test = scaler.inverse_transform(y_test)

plt.plot(y_test, label="Actual Prices")
plt.plot(predictions, label="Predicted Prices")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.show()
