# coding=utf-8

# 中国科学技术大学 信息科学技术学院 电子工程与信息科学系 2018
# 本科生《多媒体技术》课程实验：Android手机上使用TensorFlow模型
# 示例代码仅用于教学，代码中对网络上已有代码引用时做了标注。
# cxh@ustc.edu.cn,20181022

# 本代码配合实验项目《Android手机上使用TensorFlow模型》

import tensorflow as tf
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from keras.layers import TFSMLayer

# 模型路径 (SavedModel format)
model_path = 'model/saved_model'  # Use the SavedModel directory instead of .pb

# 测试图片
# 测试图片 test_image2.jpg 为博客专家 pan_jinquan代码中附带的图片
# 测试图片 test_image7.jpg 为后期制作的测试图片
# 测试图片 test_image8.jpg 为后期制作的测试图片
#test_image_path = "Mnist_data/test_image2.jpg"
#test_image_path = "Mnist_data/test_image7.jpg"
test_image_path = "Mnist_data/test_image8.jpg"

# 加载测试图片
test_image = Image.open(test_image_path)

# 加载保存的模型
print("Loading the model...")
loaded_model = TFSMLayer(model_path, call_endpoint='serving_default')

# 对图片进行预处理
test_image = test_image.convert('L')  # 转为灰度图
test_image = test_image.resize((28, 28))  # 调整图片大小为 28x28
test_input = np.array(test_image)  # 转为 numpy 数组
test_input = test_input / 255.0  # 归一化到 [0, 1]
test_input = test_input.reshape(1, 28 * 28)  # 展平为 (1, 784)

# 利用加载的模型预测结果
print("Running the model...")
predictions = loaded_model(test_input)  # 预测
print(f"Predictions: {predictions}")
predicted_label = np.argmax(predictions['output_0'].numpy(), axis=1)  # 获取预测的标签
print(f"模型预测结果为：{predicted_label}")

# 显示测试的图片
plt.imshow(np.array(test_image), cmap='binary')  # 显示图片
plt.title(f"Prediction result: {predicted_label}")
plt.show()