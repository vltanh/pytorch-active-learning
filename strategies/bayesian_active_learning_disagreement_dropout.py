import numpy as np
import torch

from .strategy import BaseStrategy


class BALDDropout(BaseStrategy):
    def __init__(self, X, Y, net, handler, args, n_drop=10):
        super().__init__(X, Y, net, handler, args)
        self.n_drop = n_drop

    def query(self, n):
        idxs_unlabeled = np.arange(self.n_pool)[~self.idxs_lb]
        probs = self.predict_prob_dropout_split(
            self.X[idxs_unlabeled], self.n_drop)
        pb = probs.mean(0)
        entropy1 = (-pb*torch.log(pb)).sum(1)
        entropy2 = (-probs*torch.log(probs)).sum(2).mean(0)
        U = entropy2 - entropy1
        return idxs_unlabeled[U.sort()[1][:n]]
