# coding=utf-8

# 中国科学技术大学 信息科学技术学院 电子工程与信息科学系 2018
# 本科生《多媒体技术》课程实验：Android手机上使用TensorFlow模型
# 原有《多媒体技术》课程的实验的各个项目都是在Microsoft Visual Studio的Visual C++ 6.0下开发，可以运行在Windows操作系统下。
# 随着智能手机在诸多场合取代了PC机的作用，我们重新考虑原有课程实验项目设置的合理性。
# 2018年尝试性将Android下多媒体技术开发的内容放入课程实验。
# 示例代码仅用于教学，代码中对网络上已有代码引用时做了标注。
# cxh@ustc.edu.cn,20181022

# 本代码内容根据 https://blog.csdn.net/guyuealian/article/details/79672257 代码整理
# 在此感谢博客专家 pan_jinquan 的分享，希望同学们通过对本例程的学习了解利用TensorFlow生成并保存模型的基本步骤

# 本代码配合实验项目《Android手机上使用TensorFlow模型》

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
import os

print(f'TensorFlow Version: {tf.__version__}')

# 加载 MNIST 数据集
# 下载 http://yann.lecun.com/exdb/mnist/ 的库，把压缩包解压后放在子目录Mnist_data中
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train / 255.0  # 归一化到 [0, 1]
x_test = x_test / 255.0

# 转换标签为 one-hot 编码
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# 创建模型
model = Sequential([
    Flatten(input_shape=(28, 28), name='input'),  # 输入层
    Dense(10, activation='softmax', name='output')  # 输出层
])

# 编译模型
model.compile(optimizer=SGD(learning_rate=0.01),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 训练模型
model.fit(x_train, y_train, batch_size=100, epochs=10)

# 测试模型准确率
loss, accuracy = model.evaluate(x_test, y_test)
print(f'Accuracy: {accuracy}')

# Save the model in Keras format (recommended for most use cases)
model.save('model/mnist_model.keras')

# Alternatively, if you want to save in HDF5 format
# model.save('model/mnist_model.h5')

# To save in the TensorFlow SavedModel format (for TFLite conversion, TensorFlow Serving, etc.)
tf.saved_model.save(model, 'model/saved_model')

# Convert to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_saved_model('model/saved_model')
tflite_model = converter.convert()

# Save the TFLite model
tflite_model_file = 'model/mnist_model.tflite'
with open(tflite_model_file, 'wb') as f:
    f.write(tflite_model)

print(f'Model saved successfully in multiple formats:')
print(f'- Keras format: model/mnist_model.keras')
print(f'- TensorFlow SavedModel format: model/saved_model')
print(f'- TensorFlow Lite format: model/mnist_model.tflite')