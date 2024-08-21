#problem.py - module that implements the Problem class. The problem concists
#Every problem has a unique id that does not change. A problem can be part of 
#multiple topics. Mastery level tells how 
#well the user has mastered the problem and influences how frequently the 
#question is asked from the user. Ratings keep track of right(1) and wrong(0) answers
#answer history keeps track of answers and the time of an answer. Time from last
#correct answer is also followed. Promenance is priority value for the problem, 
#that influences how likely the problem will be presented to the user. It can have
#values between 0-1.

from math import log
import datetime

from pattern import Pattern

class Problem():
    def __init__(self, prob_id, topics, pat_1, pat_2, mast_lvl=0,\
            ratings=[], answ_hist=[], time_answ_cor=None):
        self.id = prob_id 
        self.pat_1 = pat_1
        self.pat_2 = pat_2
        self.topics = topics
        self.mast_lvl = mast_lvl
        self.ratings = ratings
        self.answ_hist = answ_hist
        self.time_answ_cor = time_answ_cor 
        self.MAX_PROMINANCE = 100000
        self.prominance = self.MAX_PROMINANCE
        self.total_mastery = False

    #calculates time between the last time the problem was solved correctly
    #and the current time in days
    def time_diff_days(self):
        return (datetime.datetime.now() - self.time_answ_cor).total_seconds() / 86400
   
    def calc_prominance(self): #time(days)²/5^mast_lvl
        #check if the question has meaningful datetime
        if self.time_answ_cor == None:
            self.prominance = self.MAX_PROMINANCE
            return
        
        #if there is atleast one rating
        if self.ratings:
            #if previous answer was false --> increase the prominance
            prev_wrong_mult = 100 if self.ratings[-1] == 0 else 1
            self.prominance = prev_wrong_mult\
                * self.time_diff_days()**2/5**self.mast_lvl

    def calc_mast_lvl(self):
        if 1 not in self.ratings[-3:]: #last 3 answers were correct
            self.mast_lvl += 1
            #problem has been complitely mastered
            if self.mast_lvl > 9:
                self.total_mastery == True
                
        elif self.ratings[-1] == 0: #last answer was failure
            if self.mast_lvl > 0 :
                self.mast_lvl -= 1 
