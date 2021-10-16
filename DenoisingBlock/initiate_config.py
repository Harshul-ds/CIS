import json

config = {}

config['root_dir'] = './'
config['device'] = 'cpu'
config['model'] = []
config['model'].append({
    'batch_size':3,
    'n_layers':1,
    'n_frames':321,
    'in_dim':1025,
    'c_dim':33,
    'att_dim':64,
    'out_dim':1025,
    'hid_dim':4096,
    })
config['specs'] = []
config['specs'].append({
    'fs': 4096,
    'win_length': 512,
    'hop_length': 64,
    'n_fft': 2048,

    })


with open('config.json5', 'w') as outfile:
    json.dump(config, outfile, indent=2, sort_keys=False)
