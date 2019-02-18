#!/usr/bin/python

import pickle
from gib_detect_train import avg_transition_prob

model_data = pickle.load(open('gib_model.pki', 'rb'))


def check(str_to_chk):
    model_mat = model_data['mat']
    threshold = model_data['thresh']
    print(avg_transition_prob(str_to_chk, model_mat) > threshold)
