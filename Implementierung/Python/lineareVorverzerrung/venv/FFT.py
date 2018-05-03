#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 15:49:32 2017

@author: Armin Galetzka, Denys Bast
Returns the FFT amplitude and the frequency vector for a given signal

Input:  singal   --------  signal in time domain
        Fns      --------  sample frequency
        
Output  frq      --------  frequency vector
        ampl     --------  vector with amplitude
        phase    --------  vector with the phase
        H        --------  vector with complex frequency domain
"""
import numpy as np

def get(signal, Fns):
    
    # -------- get FFT 
    n = signal.size
    H = np.fft.fft(signal)
    amplH = abs(H)
    
    # get frequency vector and normalize frequency domain
    fn = Fns/2
    df = Fns/n
    frq = np.arange(0,fn,df)
    ind = int(np.round(n/2))
    ampl = np.append(amplH[0]/n, amplH[1:ind]/(n/2))
    H = np.append(H[0]/n, H[1:ind]/(n/2))
    phase = np.angle(H)
    return (frq, ampl, phase, H)
