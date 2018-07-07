import os

from keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping

from ..config import models_dir


def learning_rate(init_lr):
    def base(epoch):
        lr = init_lr * pow(10, -epoch)
        return lr

    return base


def get_callbacks(base_name, init_lr, dyn_lr=False):
    callbacks = []
    msave = ModelCheckpoint(
        os.path.join(models_dir, "%s-{epoch:02d}-acc-{val_acc:.4f}-loss-{val_loss:.4f}.hdf5" % base_name),
        monitor='val_acc', verbose=1, mode='min')
    callbacks.append(msave)
    if dyn_lr:
        lrs = LearningRateScheduler(learning_rate(init_lr=init_lr))
        callbacks.append(lrs)
    return callbacks
