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
import os
import sys
import torch.nn.functional as F
import argparse
import time

from data.time_period_dataset import TimePeriodDataset
from torch.utils.data.dataloader import DataLoader
from model.time_prd import TimePeriod


class Train:

    def __init__(self, hparams: dict, epoch_tr: bool, norm="layer", rand=False):
        self.kind = hparams['kind']  # time period, genre or band
        self.type = hparams['type']  # the specific time period, genre, or band 
        self.hparams = hparams
        self.epoch_tr = epoch_tr  # use epochs or iters (NOW: only iters supported)
        self.rand = rand
        self.norm = norm

        # document important params
        self.block_size = self.hparams['block_size']
        self.batch_size = self.hparams['batch_size']
        self.h_dim = self.hparams['hidden_dimension']
        self.n_embd = self.hparams['n_embd']
        self.num_iters = self.hparams['num_iters']

        # set up training data and dataloaders
        if self.kind == "time":
            print(self.type)
            self.train_data = TimePeriodDataset(time_prd=self.type, rand=self.rand, 
                                                train=True, block_size=self.block_size)
            self.val_data = TimePeriodDataset(time_prd=self.type, rand=self.rand, 
                                                train=False, block_size=self.block_size)
        else:
            pass # we don't have datasets for these... yet!


        self.vocab_size = len(self.train_data.itoc)  # should give same for val
        self.train_dl = DataLoader(
            dataset=self.train_data,
            batch_size= self.batch_size, 
            shuffle= True,
        )
        self.val_dl = DataLoader(
            dataset=self.val_data,
            batch_size= self.batch_size, 
            shuffle=True
        )

        self.train_iter = iter(self.train_dl)
        self.val_iter = iter(self.val_dl)

        # set up model and optimizers
        self.model = TimePeriod(
            n_embd=self.n_embd,
            vocab_size=self.vocab_size, 
            block_size=self.block_size,
            n_hidden=self.h_dim,
            norm=self.norm
        )
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=hparams['learning_rate'])
        print("num parameters", self.model.get_params())    
        print(f"length train: {len(self.train_data)} \t length val: {len(self.val_data)}")  


    def run(self, ):
        '''
        Performs training sequence
        '''

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
                        print("train ran out") 
                        self.train_iter = iter(self.train_dl)
                        x, y = next(self.train_iter)

                    # undergo evaluation as necessary
                    if i % self.hparams['eval_interval'] == 0:
                        self.model.eval()
                        self.evaluate()
                        self.model.train()

                    self.logits = self.model(x)
                    self.loss = self.model.get_loss(self.logits, y)

                    # if i % self.hparams["display_interval"] == 0:
                    #     print("Loss:   ", self.loss.item())

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
                print("evaluate train ran out") 
                self.train_iter = iter(self.train_dl)
                x_tr, y_tr = next(self.train_iter)
        
            self.logits = self.model(x_tr)
            self.loss = self.model.get_loss(self.logits, y_tr)
            self.avg_tr += self.loss

            try:
                x_val, y_val = next(self.val_iter)
            except StopIteration:
                print("evaluate val ran out") 
                self.val_iter = iter(self.val_dl)
                x_val, y_val = next(self.val_iter)

            self.logits = self.model(x_val)
            self.loss = self.model.get_loss(self.logits, y_val)
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
    parser.add_argument("-n-lay", "--num-layers", help="the number of layers the Transformer decoder block"
                        "should have", type=int)
    parser.add_argument("-block", "--block-size", help="the number of tokens taken into account as context;"
                        "by default, block-size is set to 8", type=int)
    parser.add_argument("-hdim", "--hidden-dimension", help="The dimension of the hidden layer of the MLP",
                        type=int)
    parser.add_argument("-bias", "--ffn-bias",
                        help="whether or not the feedforward part of the transformer block should include a"
                        "bias", type=bool)
    parser.add_argument("-eps", "--norm-eps", 
                        help="the epsilon for the layernorms, used to ensure that the dividing normalization"
                        "is not 0", type=float)
    parser.add_argument("-lr", "--learning-rate", help="the rate at which the network learns", type=float)
    parser.add_argument("--betas", help="betas for Adam optimizer", type=str)
    parser.add_argument("-t", "--type", help="kind of data: for time period, the time period; for genre," 
                        "the exact genre; for band, the band name")
    parser.add_argument("-k", "--kind", help="the type of MLP requested: time period, genre, or band")
    
    args = parser.parse_args()
    hparams = vars(args)

    trainer = Train(hparams, epoch_tr=False, norm="layer", rand=False)
    trainer.run()

    save_path = f"saved-models/time-prd.pth"
    torch.save(trainer.model, save_path)