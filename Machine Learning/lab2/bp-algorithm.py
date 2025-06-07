from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import datasets
from pandas import DataFrame
import numpy as np

iris = datasets.load_iris()
df = DataFrame(iris.data, columns=iris.feature_names)
df["target"] = list(iris.target)
X = df.iloc[:, 0:4]
Y = df.iloc[:, 4]
# 划分数据

"""
在此填入你的代码
"""
# 按照 8:2 划分训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0) 

sc = StandardScaler()
sc.fit(X)
standard_train = sc.transform(X_train)
standard_test = sc.transform(X_test)

'''# 构建 mlp 模型
"""
在此填入你的代码
"""
mlp = MLPClassifier(hidden_layer_sizes=(10, 10), max_iter=1000)

# 拟合数据
"""
在此填入你的代码
"""
mlp.fit(standard_train, Y_train)

# 得到预测结果
"""
在此填入你的代码
"""
result = mlp.predict(standard_test)


# 查看模型结果
print("测试集合的 y 值：", list(Y_test))
print("神经网络预测的的 y 值：", list(result))
print("预测的准确率为：", mlp.score(standard_test, Y_test))
print("层数为：", mlp.n_layers_)
print("迭代次数为：", mlp.n_iter_)
print("损失为：", mlp.loss_)
print("激活函数为：", mlp.out_activation_)

'''
# 代码的手动实现
class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        
        # 初始化权重
        self.weights1 = np.random.rand(input_size, hidden_size)
        self.weights2 = np.random.rand(hidden_size, output_size)
        
        # Initialize biases
        self.bias1 = np.zeros((1, hidden_size))
        self.bias2 = np.zeros((1, output_size))


        # 初始化偏置
        self.bias1 = np.zeros((1, hidden_size))
        self.bias2 = np.zeros((1, output_size))

    def sigmoid(self, x):  # sigmoid 计算方式
        """
        在此填入你的代码
        """
        x = 1 / (1 + np.exp(-x))
        return x

    def sigmoid_derivative(self, x):  # sigmoid 导数计算方式
        """
        在此填入你的代码
        """
        return x * (1 - x)

    def forward(self, X):
        """
        在此填入你的代码
        """
        self.z1 = np.dot(X, self.weights1) + self.bias1
        self.a1 = self.sigmoid(self.z1)
        self.z2 = np.dot(self.a1, self.weights2) + self.bias2
        output = self.sigmoid(self.z2)  
        
        return output

    def backward(self, X, y, output, learning_rate):
        """
        在此填入你的代码
        """
        output_error = output - y
        output_delta = output_error * self.sigmoid_derivative(output)

        z1_error = output_delta.dot(self.weights2.T)
        z1_delta = z1_error * self.sigmoid_derivative(self.a1)

        # Update weights and biases
        self.weights2 -= self.a1.T.dot(output_delta) * learning_rate
        self.bias2 -= np.sum(output_delta, axis=0, keepdims=True) * learning_rate
        self.weights1 -= X.T.dot(z1_delta) * learning_rate
        self.bias1 -= np.sum(z1_delta, axis=0, keepdims=True) * learning_rate

    def train(self, X, y, epochs, learning_rate):
        for epoch in range(epochs):
            output = self.forward(X)
            loss = np.mean(0.5 * (y - output) ** 2)
            self.backward(X, y, output, learning_rate)
            if epoch % 100 == 0:
                print(f"Epoch {epoch + 1}, Loss: {loss}")

    def predict(self, X):
        output = self.forward(X)
        return np.argmax(output, axis=1)


# 将标签转换为独热编码
def one_hot_encode(labels):
    num_classes = len(np.unique(labels))
    one_hot_labels = np.zeros((len(labels), num_classes))
    for i, label in enumerate(labels):
        one_hot_labels[i][label] = 1
    return one_hot_labels


# 构建神经网络
input_size = X_train.shape[1]
hidden_size = 10
output_size = len(np.unique(Y_train))  # 根据训练集标签确定输出层大小
nn = NeuralNetwork(input_size, hidden_size, output_size)

# 将标签转换为独热编码
Y_train_encoded = one_hot_encode(Y_train)

# 训练神经网络
print("training.......")
nn.train(standard_train, Y_train_encoded, epochs=1000, learning_rate=0.01)

# 预测测试集
predictions = nn.predict(standard_test)

# 计算准确率
accuracy = accuracy_score(Y_test, predictions)

# 查看模型结果
print("测试集合的 y 值：", list(Y_test))
print("神经网络预测的的 y 值：", list(predictions))
print("预测的准确率为：", accuracy)
