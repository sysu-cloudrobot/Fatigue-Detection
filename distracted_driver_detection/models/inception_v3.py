from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.layers import Input, Flatten, Dense, Dropout, regularizers
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D


def get_model(summary=False, img_width=150):
    # Get back the convolutional part of a VGG network trained on ImageNet
    inception_v3_model = InceptionV3(weights='imagenet',
                                     include_top=False,
                                     input_shape=(img_width, img_width, 3))
    # return inception_v3_model

    # Use the generated model
    output_inception_conv = inception_v3_model.output

    # Add the fully-connected layers

    x = GlobalAveragePooling2D(name='avg_pool')(output_inception_conv)
    x = Dropout(0.5)(x)
    x = Dense(10, activation='softmax', kernel_regularizer=regularizers.l2(0.01))(x)

    # Create your own model
    my_model = Model(input=inception_v3_model.input, output=x)
    for i in range(180):
        my_model.layers[i].trainable = False
    if summary:
        print("---------------------------------------------------------")
        for i, layer in enumerate(my_model.layers):
            print(i, layer.name)
        print("---------------------------------------------------------")
        print("---------------------------------------------------------")
        print("---------------------------------------------------------")
        my_model.summary()
    return my_model, 180, 3


# if __name__ == "__main__":
#     model, first_stage, second_stage = get_model(True, 299)
#     print('Length', len(model.layers), first_stage, second_stage)
