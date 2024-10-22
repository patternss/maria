#problem.py - module that implements the Problem class. 
#Every problem has a unique id that does not change. A problem can be part of 
#multiple topics. Mastery level tells how 
#well the user has mastered the problem and influences how frequently the 
#question is asked from the user. Ratings keep track of right(1) and wrong(0) answers
#answer history keeps track of answers and the time of an answer. Time from last
#correct answer is also followed. Prominance is priority value for the problem, 
#that influences how likely the problem will be presented to the user.

import datetime
import random

from pattern import Pattern

class Problem():
    def __init__(self, prob_id, topics, pat_1, pat_2, mast_lvl=0,\
            ratings=[], answ_hist=[], time_answ_cor=None, lock = None):
        self.prob_id = prob_id 
        self.pat_1 = pat_1
        self.pat_2 = pat_2
        self.topics = topics
        self.mast_lvl = mast_lvl
        self.ratings = ratings
        self.answ_hist = answ_hist
        self.time_answ_cor = time_answ_cor 
        self.lock = lock
        self.MAX_PROMINENCE = 100000
        self.prominence = self.MAX_PROMINENCE
        self.total_mastery = False

    #calculates time between the last time the problem was solved correctly
    #and the current time in days
    def time_diff_days(self):
        return (datetime.datetime.now() - self.time_answ_cor).total_seconds() / 86400
   
    def calc_prominence(self): #time(days)²/5^mast_lvl
        #if the question has not been answered correctly
        if self.time_answ_cor == None:
            self.prominence = self.MAX_PROMINENCE
            return
        
        #if there is atleast one rating
        if self.ratings:
            #if previous answer was false --> increase the prominence
            #this is done so that the question will be prompted quickly again.
            prev_wrong_mult = 100 if self.ratings[-1] == 0 else 1
            self.prominence = prev_wrong_mult\
                * self.time_diff_days()**2/5**self.mast_lvl +\
                round(random.uniform(0,0.25)) #add a little bit of randomness

    def calc_mast_lvl(self):
        #if there are {correct} answers and the last {correct} were right: 
        correct = 3 #number of consecutive correct answers before lvl up
        if len(self.ratings) >= correct and 0 not in self.ratings[-correct:]:
            #if mastery progression is locked and lock level has been reached
            if self.lock != None and self.lock == self.mast_lvl:
                return
            self.mast_lvl += 1
            #if problem has been complitely mastered
            if self.mast_lvl > 7:
                self.total_mastery == True
                
        #if last answer was wrong. Drop mastery level by 1
        elif self.ratings[-1] == 0 and self.mast_lvl > 0: #last answer was failure
            self.mast_lvl -= 1
            


