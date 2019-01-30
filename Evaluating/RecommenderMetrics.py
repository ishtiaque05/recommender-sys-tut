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

    def HitRate(topNPredicted, leftOutPredictions):
        hits = 0
        total = 0
        
        # For each left-out rating
        for leftOut in leftOutPredictions:
            userID = leftOut[0]
            leftOutMovieID = leftOut[1]
            # Is it in top 10 for this user
            hit = False
            for movieID, predictedRating in topNPredicted[int(userID)]:
                if(int(leftOutMovieID) == int(movieID)):
                    hit = True
                    break
            if(hit):
                hits += 1
            
            total +=1
            
            # Compute Overall Precision
            return hits/total
        
    def CumulativeHitRate(topNPredicted, leftOutPredictions, ratingCutoff=0):
        hits = 0
        total = 0
        
        # For each left-out rating
        for userID, leftOutMovieID, actualRating, estimatedRating, _ in leftOutPredictions:
            # Only look at ability to recommend things the users actually liked
            if(actualRating >= ratingCutoff):
                # Is it in the predicted top 10 for this user?
                hit = False
                for movieID, predictedRating in topNPredicted[int(userID)]:
                    if(int(leftOutMovieID) == movieID):
                        hit = True
                        break
                if(hit):
                    hits += 1
                total += 1
        # Compute overall precision
        return hits/total
                
                