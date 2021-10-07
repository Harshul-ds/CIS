import json

config = {}

config['root_dir'] = './'
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
config['trainer'] = []
config['trainer'].append({
        'root_dir': './',
        'loss_function': {
        'module': 'utils',
        'main': 'mse_loss_for_variable_length_data',
        'args': {}
        },
        'scheduler': {
            'module': 'torch.optim.optim.lr_scheduler.StepLR'
            
            },
        'lr': 1e-4,
    	'epochs':500,
    	'chk_pt_freq': 5,
        'validation': {
            'interval': 1,
            'find_max': False,
            'custom': {
                'visualize_audio_limit': 5,
                'visualize_waveform_limit': 5,
                'visualize_spectrogram_limit': 5
                    }
                }
            
	})


with open('config.json5', 'w') as outfile:
    json.dump(config, outfile, indent=2, sort_keys=False)
