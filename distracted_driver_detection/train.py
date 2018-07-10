from keras.optimizers import RMSprop
from .models import get_model
from .models.callbacks import get_callbacks
from keras.preprocessing.image import ImageDataGenerator
from .config import train_dir, validation_dir, test_dir, data_path, normalize_zero

num_of_imgs = 21794


def get_train_datagen(img_width, batch_size=32):
    train_datagen = ImageDataGenerator(rescale=1.0 / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
    train_generator = train_datagen.flow_from_directory(train_dir, target_size=(img_width, img_width),
                                                        batch_size=batch_size, class_mode='categorical', shuffle=True)
    return train_generator


def get_validation_datagen(img_width, batch_size=32):

    test_datagen = ImageDataGenerator(rescale=1.0 / 255)
    validation_generator = test_datagen.flow_from_directory(validation_dir, target_size=(img_width, img_width),
                                                            batch_size=batch_size,
                                                            class_mode='categorical', shuffle=True)
    return validation_generator


def train(num_of_epochs, img_width=299, print_summary=False,
          batch_size=32, learning_rate=5e-5, weight_path=None,
          dyn_lr=False, initial_epoch=0, skip_first_stage=False):
    model_type = 'inception_v3'
    model, second_stage, first_stage = get_model(model_type, img_width, print_summary)
    # Run first stage
    if first_stage is not None and second_stage is not None:
        for layer in model.layers[:-first_stage]:
            layer.trainable = False
        for layer in model.layers[-first_stage:]:
            layer.trainable = True
    
    if weight_path is not None and len(weight_path) > 0:
        print('[INFO] loading weights')
        model.load_weights(weight_path)
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    train_generator = get_train_datagen(img_width, batch_size)
    validation_generator = get_validation_datagen(img_width, batch_size)

    # train the convolutional neural network  
    if not skip_first_stage:
        print('[INFO] Start first stage')
        model.fit_generator(generator=train_generator, epochs=2,
                            steps_per_epoch= 33 / batch_size,
                            validation_steps= 33 / batch_size,
                            validation_data=validation_generator,
                            callbacks=get_callbacks(model_type, 0.001, False),
                            initial_epoch=0)
    # Run second stage
    if first_stage is not None and second_stage is not None:
        for layer in model.layers[:second_stage]:
            layer.trainable = False
        for layer in model.layers[second_stage:]:
            layer.trainable = True

    model_opt = RMSprop(lr=learning_rate)
    model.compile(loss='categorical_crossentropy', optimizer=model_opt, metrics=['accuracy'])

    print('[INFO] Run train process')
    # train the convolutional neural network
    model.fit_generator(generator=train_generator, epochs=num_of_epochs + 2,
                        steps_per_epoch=18304 / batch_size,
                        validation_steps=3328 / batch_size,
                        validation_data=validation_generator,
                        callbacks=get_callbacks(model_type, learning_rate, dyn_lr),
                        initial_epoch=2 + initial_epoch)
    print('[INFO] End train process')

