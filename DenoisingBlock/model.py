#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 21:34:35 2021

@author: at3ee
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt

    
class attentionLayer(nn.Module):
    def __init__(self, c_dim, n_frames, device):
        super(conv_attentionLayer, self).__init__()
                
        self.c_dim = c_dim # context vector dimension
        self.softmax = nn.Softmax(dim=1)  # softmax layer to calculate weights
        
        self.batch_size = 1
        self.device = device

    def forward(self, c):
        context_attention = c #b x n_frames x c_dim  
        alpha = self.softmax(context_attention)
        attention_weighted_encoding = (alpha * context_attention)

        return attention_weighted_encoding


class LSTM_model(nn.Module):
  def __init__(self, encoder_opt, decoder_opt, device, phase='train'):
    super(LSTMLayer, self).__init__()
    self.n_layers = decoder_opt['n_layers']
    self.n_frames = encoder_opt['n_frames']
    self.in_dim = decoder_opt['in_dim']
    self.c_dim = encoder_opt["c_dim"]
    self.out_dim = decoder_opt['out_dim']
    self.hid_dim = decoder_opt['hid_dim']
    
    # self.dropout = dropout
    self.scale = torch.sqrt(torch.FloatTensor([self.hid_dim]))
    self.LSTM_layer1 = nn.LSTM(self.in_dim+self.c_dim, self.hid_dim, bias=True) # decoding RNNlayer
    self.LSTM_layer2 = nn.LSTM(self.hid_dim+self.c_dim, self.out_dim, bias=True) # decoding RNNlayer
    self.attention_LSTM = conv_attentionLayer(self.c_dim, self.n_frames, device)
    self.fc_out = nn.Linear(self.hid_dim, self.out_dim)    
    # self.dropout = nn.Dropout(dropout)
    self.sigmoid = nn.Sigmoid()
    self.norm = nn.InstanceNorm1d(self.hid_dim)
    self.phase = phase
    self.batch_size = decoder_opt["batch_size"]
    self.device = device

  def init_hidden_state(self, x):
    mean_enc = x.mean(dim=-2)
    h = self.init_h(mean_enc)  # (batch_size, decoder_dim)
    c = self.init_c(mean_enc)
    return h.to(self.device), c.to(self.device)

  def forward(self, C, x):
    N = x.shape[0]
    inp_seq = x
    nframes = x.shape[1]
    
    # initialize the hidden state.
    h_t1 = torch.randn(1, nframes, self.hid_dim).to(self.device)
    c_t1 = torch.randn(1, nframes, self.hid_dim).to(self.device)
    

    h_t2 = torch.randn(1, nframes, self.out_dim).to(self.device)
    c_t2 = torch.randn(1, nframes, self.out_dim).to(self.device)
    
    att_seq = self.attention_LSTM(C)

    enc_seq, (h_t1, c_t1) = self.LSTM_layer1(inp_seq, (h_t1, c_t1))    
    out_seq, (h_t2, c_t2) = self.LSTM_layer2(torch.cat((enc_seq, att_seq), -1), (h_t2, c_t2))

    predictions = F.softmax(predictions, dim = -1)
    
    
    return out_seq, att_seq


