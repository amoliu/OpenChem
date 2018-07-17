import torch.nn as nn
import math

from utils.utils import check_params


class OpenChemMLP(nn.Module):
    """Base class for MLP module"""
    def __init__(self, params):
        super(OpenChemMLP, self).__init__()
        check_params(params, self.get_required_params(),
                     self.get_optional_params())
        self.params = params
        self.hidden_size = self.params['hidden_size']
        self.input_size = [self.params['input_size']] + self.hidden_size[:-1]
        self.n_layers = self.params['n_layers']
        self.activations = self.params['activations']
        self.dropouts = self.params['dropouts']
        self.layers = nn.ModuleList([])
        self.bn = nn.ModuleList([])
        for i in range(self.n_layers):
            self.bn.append(nn.BatchNorm1d(self.input_size[i]))
            self.layers.append(Linear(in_features=self.input_size[i],
                                      out_features=self.hidden_size[i],
                                      dropout=self.dropouts[i]))

    @staticmethod
    def get_required_params():
        return {
            'input_size': int,
            'n_layers': int,
            'hidden_size': list,
            'activations': list,
            'dropouts': list
        }

    @staticmethod
    def get_optional_params():
        return {}

    def forward(self, inp):
        output = inp
        for i in range(self.n_layers):
            output = self.bn[i](output)
            output = self.layers[i](output)
            output = self.activations[i](output)
        return output


def Linear(in_features, out_features, dropout=0):
    """Weight-normalized Linear layer (input: N x T x C)"""
    m = nn.Linear(in_features, out_features)
    nn.init.normal_(m.weight, mean=0,
                    std=math.sqrt((1 - dropout) / in_features))
    nn.init.constant_(m.bias, 0)
    return nn.utils.weight_norm(m)

