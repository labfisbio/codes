# -*- coding: utf-8 -*-
"""
Module for testing statistical distributions

@author: Andre Thomaz (athomaz@ifi.unicamp.br) @ 2022-02-14
"""


import scipy.stats as sts



############# Test for Gaussian ###############################
def test_gaussian(sample):
    print("Testing to check if the data is Gaussian")
    stat, p = sts.shapiro(sample)
    print('Statistics=%.3f, p=%.6f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
        print('Sample **LOOKS** Gaussian (fail to reject H0) - GAUSSIAN')
        return True
    else:
        print('Sample **DOES NOT** look Gaussian (reject H0) - NOT GAUSSIAN')
        return False
###############################################################        

### Statistical Test for Gaussian Distribution ################        
def test_t(sample1, sample2):
    print("Testing statistical significance by Test T for Gaussian Distributions")
    stat, p = sts.ttest_ind(sample1, sample2)
    print('Statistics=%.3f, p=%.3f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
        print('Same distributions (fail to reject H0)')
    else:
    	print('Different distributions (reject H0)')
###############################################################

### Statistical Test for Non-Gaussian Distribution ############

#Mann-Whitneyu
def mannwhitneyu(sample1, sample2):
    print("Testing statistical significance by Mann-Whitneyu for Non-Gaussian Distributions")
    stat, p = sts.mannwhitneyu(sample1, sample2)
    print('Statistics=%.3f, p=%.6f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
    	print('p: Same distribution (fail to reject H0)')
    else:
    	print('p: Different distribution (reject H0)')
        
#two-sample Kolmogorov-Smirnov        
def ks_2samp(sample1, sample2):
    print("Testing statistical significance by two-sample Kolmogorov-Smirnov test for Non-Gaussian Distributions")
    stat, p = sts.ks_2samp(sample1, sample2, alternative='two-sided', mode='auto')
    print('Statistics=%.3f, p=%.6f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
    	print('p: Same distribution (fail to reject H0)')
    else:
    	print('p: Different distribution (reject H0)')        
###############################################################
   
