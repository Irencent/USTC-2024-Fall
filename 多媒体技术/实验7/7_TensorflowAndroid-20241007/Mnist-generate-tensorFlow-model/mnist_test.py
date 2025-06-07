# coding=utf-8

# --------------------- 
# 作者：数据架构师 
# 来源：CSDN 
# 原文：https://blog.csdn.net/luanpeng825485697/article/details/79100008 
# 版权声明：本文为博主原创文章，转载请附上博文链接！

# 中国科学技术大学 信息科学技术学院 电子工程与信息科学系 2018
# 本科生《多媒体技术》课程实验：Android手机上使用tensorflow模型
# 示例代码仅用于教学，代码中对网络上已有代码引用时做了标注。
# cxh@ustc.edu.cn,20181022

import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.utils import to_categorical

# Load MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalize the images to [0, 1] range
x_train = x_train / 255.0
x_test = x_test / 255.0

# Convert labels to one-hot encoding
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# Define the model
model = Sequential([
    Flatten(input_shape=(28, 28)),  # Flatten 28x28 images to 1D vectors
    Dense(10, activation='softmax')  # Output layer with 10 classes
])

# Compile the model
model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.5),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(x_train, y_train, batch_size=100, epochs=10)

# Evaluate the model
test_loss, test_accuracy = model.evaluate(x_test, y_test)
print(f"Test accuracy: {test_accuracy}")