"""
train.py trains both the time period neural network (MLP) and the whole dataset
neural network (Transformer) seperately. The user, in their preferences, enters
which time periods and which genres they wish to hear music from. From that, only
the required number of time period and genre NNs will be trained. 

Things to do in the near future:
TODO: Implement a learning rate schedueler, as proposed by Vaswani et al., 2017
TODO: Implement gradient clipping 
"""

import torch 
import torch.nn.functional as F
import argparse
import time

from model.time_prd import TimePeriod
from model.whole_dataset_tr import WholeDatasetTransformer
from torch.utils.data.dataloader import DataLoader
from data.whole_dataset import WholeDataset


class Train:

    def __init__(self, hparams: dict, epoch_tr: bool, rand=True):
        '''
        Initalizes the data if it was not passed in already, sets up optimizers and 
        constants, and declares the model.
        '''

        self.epoch_tr = epoch_tr
        self.rand = rand
        self.hparams = hparams
        # document important params
        self.block_size = self.hparams['block_size']
        self.batch_size = self.hparams['batch_size']
        self.n_embd = self.hparams['n_embd']
        self.num_iters = self.hparams['num_iters']

        # set up training data and dataloaders 
        self.train_data = WholeDataset(train=True, rand=self.rand, block_size=self.block_size)
        self.val_data = WholeDataset(train=False, rand=self.rand, block_size=self.block_size)
        self.vocab_size = len(self.val_data.get_vocab())

        self.train_dl = DataLoader(
            dataset=self.train_data,
            batch_size= self.batch_size, 
            shuffle= True,
        )
        self.val_dl = DataLoader(
            dataset=self.val_data,
            batch_size= self.batch_size, 
            shuffle= True,
        )

        self.train_iter = iter(self.train_dl)
        self.val_iter = iter(self.val_dl)

        # set up model and optimizers 
        self.model = WholeDatasetTransformer(
            n_embd = self.n_embd, n_layers = self.hparams['num_layers'],
            vocab_size = self.vocab_size, n_head = self.hparams['n_head'],
            h_dim = self.hparams['hidden_dimension'], 
            block_size = self.hparams['block_size'],
            dropout = self.hparams['dropout'], 
            ffn_bias = self.hparams["ffn_bias"],
            layernorm_eps = self.hparams['layernorm_eps']
        )
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=hparams['learning_rate'])
        print("num parameters", self.model.get_params())        

        # set up times
        self.start = None

        
    def run(self):
        '''
        Performs training sequence
        '''

        self.start = time.time()    # begin start time
        self.model.train()

        # if epoch_tr, train for a set number of epochs 
        if self.epoch_tr:
            pass

        # else, train for a set number of iterations
        else:
            print("Beginning iteration training...")
            self.num_iters = self.hparams['num_iters']

            try:
                for i in range(self.num_iters):
                    # check if you can get next batch
                    try:
                        x, y = next(self.train_iter)
                    except StopIteration:
                        self.train_iter = iter(self.train_dl)
                        x, y = next(self.train_iter)

                    # undergo evaluation as necessary
                    if i % self.hparams['eval_interval'] == 0:
                        self.model.eval()
                        self.evaluate()
                        self.model.train()

                    self.logits = self.model(x)
                    self.loss = self.model.get_loss(self.logits, y, lf=F.cross_entropy)

                    if i % self.hparams["display_interval"] == 0:
                        print("Loss:   ", self.loss.item())

                    self.optimizer.zero_grad(set_to_none=True)
                    self.loss.backward()
                    self.optimizer.step()


            except KeyboardInterrupt:
                print("Ending training.")


            # print(f"Fi_time = {self.end} - {self.start}")
            # print(f"Total Training Time = {self.train_time}")
            return 


    @torch.no_grad()
    def evaluate(self):
        # evaluation for train step
        self.avg_tr = 0 
        self.avg_val = 0

        for _ in range(hparams['eval_iters']):
            try:
                x_tr, y_tr = next(self.train_iter)
            except StopIteration:
                self.train_iter = iter(self.train_dl)
                x_tr, y_tr = next(self.train_iter)
        
            self.logits = self.model(x_tr)
            self.loss = self.model.get_loss(self.logits, y_tr, lf=F.cross_entropy)
            self.avg_tr += self.loss

            try:
                x_val, y_val = next(self.val_iter)
            except StopIteration:
                print("Executing here") 
                self.val_iter = iter(self.val_dl)
                x_val, y_val = next(self.val_iter)

            self.logits = self.model(x_val)
            self.loss = self.model.get_loss(self.logits, y_val, lf=F.cross_entropy)
            self.avg_val += self.loss

        self.avg_tr /= hparams['eval_iters']
        self.avg_val /= hparams['eval_iters']
        print(f"EVALUATION: \t Average Train  {self.avg_tr} \t Average Val {self.avg_val}")
        

if __name__ == "__main__":
    '''
    Users have the ability to input their own hyperparameters for increased customizability;
    if they do not enter a certain argument, a default value will be provided
    '''
    parser = argparse.ArgumentParser(
        prog='train.py',
        description = "Input arguments/hyperparameters for increased customizability during NN training."
    )

    # arguments 
    parser.add_argument("-ep", "--num-epochs", help="the number of epochs the NN should train for if planning"
                        "to train for a set number of epochs", type=int)
    parser.add_argument("-iters", "--num-iters", help="number of iterations the NN should run for", type=int)
    parser.add_argument("-ei", "--eval-iters", help="number of iterations the trainer will run during evaluation" 
                        "phase", type=int)
    parser.add_argument("-eval", "--eval-interval", help="between how many training steps should an evaluation " 
                        "phase occur. after eval-interval training steps, the program will go into evaluation " 
                        "mode", type=int)
    parser.add_argument("-di", "--display-interval", help="between how many training steps should loss and "
                        "time data be printed.", type=int)
    parser.add_argument("-d", "--device", help="the device the model should run on (cuda/cpu/mps/etc)", type=str)
    parser.add_argument("-batch", "--batch-size", help="the number of training examples that should be coupled" 
                        "during training; default=4", type=int)
    parser.add_argument("-ne", "--n-embd", help="dimensionality that inputs are encoded in; default = 32", 
                        type=int)
    parser.add_argument("-nh", "--n-head", help="number of parallel-processed heads that perform multi-"
                        "headed attention.", type=int)
    parser.add_argument("-n-lay", "--num-layers", help="the number of layers the Transformer decoder block"
                        "should have", type=int)
    parser.add_argument("-block", "--block-size", help="the number of tokens taken into account as context;"
                        "by default, block-size is set to 8", type=int)
    parser.add_argument("-bias", "--ffn-bias",
                        help="whether or not the feedforward part of the transformer block should include a"
                        "bias", type=bool)
    parser.add_argument("-eps", "--layernorm-eps", 
                        help="the epsilon for the layernorms, used to ensure that the dividing normalization"
                        "is not 0", type=float)
    parser.add_argument("-drop", "--dropout", help="percentage of neurons set to 0 during training", type=float)
    parser.add_argument("-h-dim", "--hidden-dimension", 
                        help="the size of the hidden layer for the feedforward NN; default set to 4*n_embd", 
                        type=int)
    parser.add_argument("-lr", "--learning-rate", help="the rate at which the network learns", type=float)
    parser.add_argument("--betas", help="betas for Adam optimizer", type=str)
    
    args = parser.parse_args()
    hparams = vars(args)


    trainer = Train(hparams, bool(hparams['num_epochs']), False)
    trainer.run()

    save_path = "saved-models/model.pth"
    torch.save(trainer.model, save_path)

