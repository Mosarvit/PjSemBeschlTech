# -*- coding: utf-8 -*-
"""
Created on Sun June 3 2018
@author: Jonas
"""
from helpers.apply_K import apply_K
from helpers.K_helper import invert_K


def compute_Uin_from_Uquest(Uquest, K_Uin_to_Uquest, verbosity=False):

    K_Uquest_to_Uin = invert_K(K_Uin_to_Uquest)
    Uquest, Uin = apply_K(K_Uquest_to_Uin, Uquest, verbosity)

    return Uin, Uquest


