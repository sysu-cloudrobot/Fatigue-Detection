from .config import test_dir
from keras.preprocessing import image
from keras.applications.inception_v3 import preprocess_input
import numpy as np
import os

from .models import get_model

class_info = [
    '安全驾驶',
    '右手打字',
    '右手打电话',
    '左手打字',
    '左手打电话',
    '调收音机',
    '喝饮料',
    '拿后面的东西',
    '整理头发和化妆',
    '和其他乘客说话'
]


def load_model(path_to_model, model_type='inception_v3', img_width=299):
    model = get_model(modelType=model_type, print_summary=False, img_width=img_width)
    if (isinstance(model, tuple)):
        model = model[0]
    model.load_weights(path_to_model)
    return model

def detect(path_to_image, img_width=299):
    # model = load_model(path_to_model, model_type, img_width=img_width)

    # 加载图像
    img = image.load_img(path_to_image, target_size=(img_width, img_width))

    # 图像预处理
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    print(x.shape)

    x = preprocess_input(x)

    print(x.shape)

    # 对图像进行分类
    result = model.predict(x)

    # 输出预测概率
    print('Predicted:', result)

    label = np.where(result[0] == max(result[0]))

    print(label)

    return class_info[int(label[0][0])]

path_to_model = './models/inception_v3-07-acc-0.9934-loss-0.2515.hdf5'
model = load_model(path_to_model=path_to_model, model_type='inception_v3', img_width=299)
print(detect('./img_1.jpg'))