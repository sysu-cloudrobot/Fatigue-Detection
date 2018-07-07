from . import inception_v3


def get_model(modelType, img_width, print_summary=False):
    if modelType == 'inception_v3':
        return inception_v3.get_model(print_summary, img_width)
    return None
