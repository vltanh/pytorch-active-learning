import numpy as np
import torch

from .strategy import BaseStrategy


class EntropySampling(BaseStrategy):
    def __init__(self, X, Y, net, handler, args):
        super().__init__(X, Y, net, handler, args)

    def query(self, n):
        idxs_unlabeled = np.arange(self.n_pool)[~self.idxs_lb]
        probs = self.predict_prob(self.X[idxs_unlabeled])
        log_probs = torch.log(probs)
        U = (probs*log_probs).sum(1)
        return idxs_unlabeled[U.sort()[1][:n]]
