# TODO: packed variable length sequence

import numpy as np

from torch.utils.data import Dataset

from data.utils import read_smiles_property_file
from data.utils import sanitize_smiles, pad_sequences, seq2tensor
from data.utils import tokenize


class SmilesProteinDataset(Dataset):
    def __init__(self, filename, cols_to_read, delimiter=',', mol_tokens=None,
                 prot_tokens=None, pad=True):
        super(SmilesProteinDataset, self).__init__()
        data = read_smiles_property_file(filename, cols_to_read, delimiter)
        smiles = data[0]
        proteins = np.array(data[1])
        target = np.array(data[2], dtype='float')
        clean_smiles, clean_idx = sanitize_smiles(smiles)
        self.target = target[clean_idx]
        proteins = list(proteins[clean_idx])
        if pad:
            clean_smiles = pad_sequences(clean_smiles)
            proteins = pad_sequences(proteins)
        self.mol_tokens, self.mol_token2idx, self.mol_num_tokens = \
            tokenize(clean_smiles, mol_tokens)
        self.prot_tokens, self.prot_token2idx, self.prot_num_tokens = \
            tokenize(proteins, prot_tokens)
        clean_smiles = seq2tensor(clean_smiles, self.mol_tokens)
        proteins = seq2tensor(proteins, self.prot_tokens)
        self.molecules = clean_smiles
        self.proteins = proteins
        assert len(self.molecules) == len(self.proteins)
        assert len(self.molecules) == len(self.target)

    def __len__(self):
        return len(self.target)

    def __getitem__(self, index):
        sample = {'tokenized_smiles': self.molecules[index],
                  'tokenized_protein': self.proteins[index],
                  'labels': self.target[index]}
        return sample
