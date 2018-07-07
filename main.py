from distracted_driver_detection.detect import detect
from distracted_driver_detection.train import train
from keras import backend as K
K.clear_session()


def getopts():
    from sys import argv
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts


if __name__ == "__main__":
    opts = getopts()
    mode = opts['--mode']

    if mode == "train":
        num_of_epochs = int(opts.get('--epochs', '20'))
        width = int(opts.get('--width', '299'))
        print_summary = opts.get('--summary', 'False') == 'True'
        skip_first_stage = opts.get('--skip_first_stage', 'False') == 'True'
        batch_size = int(opts.get('--batch', '32'))
        lr = float(opts.get('--lr', '5e-5'))
        weight_path = opts.get('--weight_path', None)
        dyn_lr = opts.get('--dyn_lr', 'False') == 'True'
        initial_epoch = int(opts.get('--initial_epoch', 0))
        train(num_of_epochs=num_of_epochs, img_width=width, print_summary=print_summary,
            batch_size=batch_size, learning_rate=lr, weight_path=weight_path,
            dyn_lr=dyn_lr, initial_epoch=initial_epoch,
            skip_first_stage=skip_first_stage)
    
    if mode == "detect":
        path_to_model = opts.get('--path_to_model')
        print('[INFO] Model: ', path_to_model)
        image_path = opts.get('--path_to_image')
        model_type = opts.get('--model', 'simple')
        width = int(opts.get('--width', '299'))
        fc_layers = int(opts.get('--fc', 2))
        fc_width = int(opts.get('--fc_dim', 4096))
        dropout = float(opts.get('--dropout', 0.5))
        result = detect(path_to_model, image_path, model_type, img_width=width)
        print(result)
