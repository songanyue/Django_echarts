import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from matplotlib import ticker

from tensorflow import keras
from tensorflow.keras.layers import *

# 堆叠LSTM
def encoder_decoder_LSTM_train(n_input, n_out, n_features, epochs_num, train_data, train_label, vaild_data, vaild_label):
    model = keras.Sequential()
    model.add(LSTM(16, activation='tanh', return_sequences=True, input_shape=(n_input, n_features)))
    model.add(LSTM(16, activation='tanh', return_sequences=True, dropout=0.2, recurrent_dropout=0.2))
    model.add(LSTM(16, activation='tanh', dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(n_out))

    # 模型编译
    model.compile(optimizer='adam', loss='mse')
    model.fit(train_data, train_label, epochs=epochs_num, batch_size=None, shuffle=False, validation_data=(vaild_data, vaild_label))
    return model

# 根据输入数据个数，输出数据个数，步长，特征数，将原始的时间序列数据制作成为训练数据和标签；
def to_supervised(data, n_input, n_out, n_features, step):
    X, y = [], []
    in_start = 0  # in_start：当前训练数据的首位数据的位置。
    for _ in range(len(data)):  # 遍历原始数据
        in_end = in_start + (n_input - 1) * step  # inend：当前训练数据的最后一位数据的位置
        out_end = in_end + step * n_out  # out_end：当前标签的最后一位数据的位置
        if out_end <= len(data):  # 若作为标签的最后一位数据在原始数据的范围内，则可以划分一组训练数据和标签
            tmp_x = []
            for i in range(n_input):
                if n_features == 1:  # 当特征数为1，即只有单特征时间序列数据
                    element_x = []
                    element_x.append(data[in_start + i * step])  # 根据开始和结束位置存入训练数据（例如：[3,3,2,4,1]）
                    tmp_x.append(element_x)  # 再存入容器中,这样与多特征的格式统一(格式变为：[[3,3,2,4,1]])
                else:
                    tmp_x.append(data[in_start + i * step,
                                 0:n_features])  # 多特征的时序数据，训练数据也存入多特征(例如3特征的时序数据：[[3,2,1],[4,7,5],[9,5,2]])
            X.append(tmp_x)  # 再将该组时序数据的容器存入训练数据的容器
            y.append(data[in_end:in_end + step * n_out])  # 该组的标签存入标签容器中
        in_start += 1  # 更新起始位置
    return np.array(X), np.array(y)

n_input = 7  # 输入的数据个数
n_output = 7  # 输出的数据个数
n_features = 1  # 每个数据含有的特征数量
step_lenth = 1  # 步长（时间序列的组合方式：若为1，表示1，2，3的方式组合；若为2，表示1，3，5的方式组合）
epochs_num = 500  # 训练的迭代次数

# 载入数据集
file_path = 'WHO-COVID-19-data.csv'
covid_df = pd.read_csv(file_path)
date = covid_df['date'].tolist()
new_cases = covid_df['new_cases'].tolist()

# # 归一化
max_val = max(new_cases)  # 取最大值
case_count = []  # 存储归一化后病例数的容器
for case in new_cases:
    tmp = case / max_val  # 将所有病例数据都控制在0~1之间
    case_count.append(tmp)  # 添加归一化后病例数

# 制作训练集序列
case_count = np.array(case_count)  # 转换为numpy.array格式

# 将数据制作成训练数据和标签
case_data, case_label = to_supervised(case_count, n_input, n_output, n_features, step_lenth)

# 划分训练集和验证集。这里表示将后三组的训练数据和标签划为验证集
train_data = case_data[:-3]
train_label = case_label[:-3]
valid_data = case_data[-3:]
valid_label = case_label[-3:]

# 模型训练
model = encoder_decoder_LSTM_train(n_input, n_output, n_features, epochs_num, train_data, train_label, valid_data, valid_label)

# 保存模型的权重
model.save_weights('my_model_weights.h5')

# 模型预测
org_test_data = case_count[-n_input:]
test_data = []
tmp = []
for case in org_test_data:
    element_x = [case]
    tmp.append(element_x)

test_data.append(tmp)
test_data = np.array(test_data)

y_hat = model.predict(test_data).reshape((-1))
y_hat *= max_val
print("最终预测结果：", y_hat)
#print("实际值：", new_cases[-n_output:])

# 图像展示
# fig, ax = plt.subplots(1, 1)
#
# plt.plot(
#     date[:-n_output],
#     new_cases[:-n_output],
#     label='Historical Daily Cases'
# )
# plt.plot(
#     date[-n_output:],
#     new_cases[-n_output:],
#     label='Real Daily Cases'
# )
# plt.plot(
#     date[-n_output:],
#     y_hat,
#     label='Predicted Daily Cases'
# )
#
# ax.xaxis.set_major_locator(ticker.MultipleLocator())
#
# for lobj in ax.get_xticklabels():
#     lobj.set_rotation(30)
#     lobj.set_size(8)
#
# plt.legend()
# plt.show()
#
# plt.plot(
#     date[-n_output:],
#     new_cases[-n_output:],
#     label='Real Daily Cases'
# )
# plt.plot(
#     date[-n_output:],
#     y_hat,
#     label='Predicted Daily Cases'
# )
#
# ax.xaxis.set_major_locator(ticker.MultipleLocator())
#
# for lobj in ax.get_xticklabels():
#     lobj.set_rotation(30)
#     lobj.set_size(8)
#
# plt.legend()
# plt.show()