#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 22:21:20 2019

@author: Syed Ishtiaque Ahmad
"""

import itertools

from surprise import accuracy
from collections import defaultdict

class RecommenderMetrics:
    
    def MAE(predictions):
        return accuracy.mae(predictions, verbose=False)
    
    def RMSE(predictions):
        return accuracy.rmse(predictions, verbose=False)
    
    def GetTopN(predictions, n=0, minimumRating=4.0):
        topN = defaultdict(list)
        
        for userID, movieID, actualRating, estimatedRating, _ in predictions:
            if(estimatedRating >= minimumRating):
                topN[int(userID)].append((int(movieID), estimatedRating))
                
        for userID, ratings in topN.items():
            ratings.sort(key=lambda x: x[1], reverse=True)
            topN[int(userID)] = ratings[:n]
         
        return topN    