from models.Smiles2Label import Smiles2Label
from modules.embeddings.basic_embedding import Embedding
from modules.encoders.rnn_encoder import RNNEncoder
# from modules.encoders.cnn_encoder import CNNEncoder
from modules.mlp.openchem_mlp import OpenChemMLP
from data.smiles_data_layer import SmilesDataset

import torch.nn as nn
from torch.optim import RMSprop
from torch.optim.lr_scheduler import ExponentialLR
import torch.nn.functional as F
from sklearn.metrics import f1_score

train_dataset = SmilesDataset('/home/mpopova/Work/EAGCN/Data/HIV_updated.csv',
                              cols_to_read=[0, 2])
val_dataset = SmilesDataset('/home/mpopova/Work/EAGCN/Data/HIV_updated.csv',
                            cols_to_read=[0, 2])

use_cuda = True

model = Smiles2Label

model_params = {
    'use_cuda': use_cuda,
    'task': 'classification',
    'random_seed': 5,
    'use_clip_grad': True,
    'max_grad_norm': 10.0,
    'batch_size': 128,
    'num_epochs': 100,
    'logdir': '/home/mpopova/Work/OpenChem/logs',
    'print_every': 1,
    'save_every': 5,
    'train_data_layer': train_dataset,
    'val_data_layer': val_dataset,
    'eval_metrics': f1_score,
    'criterion': nn.CrossEntropyLoss(),
    'optimizer': RMSprop,
    'optimizer_params': {
        'lr': 0.001
    },
    'lr_scheduler': ExponentialLR,
    'lr_scheduler_params': {
        'gamma': 0.97
    },
    'mol_embedding': Embedding,
    'mol_embedding_params': {
        'num_embeddings': max(train_dataset.num_tokens, val_dataset.num_tokens),
        'embedding_dim': 256,
        'padding_idx': 0
    },
    'prot_embedding': Embedding,
    'prot_embedding_params': {
        'num_embeddings': max(train_dataset.num_tokens, val_dataset.num_tokens),
        'embedding_dim': 256,
        'padding_idx': 0
    },
    'mol_encoder': RNNEncoder,
    'mol_encoder_params': {
        'layer': "LSTM",
        'encoder_dim': 512,
        'n_layers': 2,
        'dropout': 0.3,
        'bidirectional': False
    },
    'prot_encoder': RNNEncoder,
    'prot_encoder_params': {
        'layer': "LSTM",
        'encoder_dim': 512,
        'n_layers': 2,
        'dropout': 0.3,
        'bidirectional': False
    },
    'merge': 'sum',
    'mlp': OpenChemMLP,
    'mlp_params': {
        'input_size': 512,
        'n_layers': 2,
        'hidden_size': [256, 2],
        'activations': [F.relu, F.relu],
        'dropouts': [0.3, 0.8]
    }
}
