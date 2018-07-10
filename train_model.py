from distracted_driver_detection.train import train

def getopts():
    from sys import argv
    opts = {}
    while argv:
        if argv[0][0] == '-':
            opts[argv[0]] = argv[1]
        argv = argv[1:]
    return opts

if __name__ == "__main__":
    opts = getopts()
    num_of_epochs = int(opts.get('--epochs', '20'))
    print_summary = opts.get('--summary', 'False') == 'True'
    skip_first_stage = opts.get('--skip_first_stage', 'False') == 'True'
    batch_size = int(opts.get('--batch', '32'))
    lr = float(opts.get('--lr', '5e-5'))
    weight_path = opts.get('--weight_path', None)
    dyn_lr = opts.get('--dyn_lr', 'False') == 'True'
    initial_epoch = int(opts.get('--initial_epoch', 0))
    train(num_of_epochs, img_width=299, print_summary=print_summary,
          batch_size=batch_size, learning_rate=lr, weight_path=weight_path,
          dyn_lr=dyn_lr, initial_epoch=initial_epoch,
          skip_first_stage=skip_first_stage)