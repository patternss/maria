#collection.py
#responsible for loading, holding and managing problems and topics
import json
import copy

from problem import Problem
from pattern import Pattern

class Collection():
    def __init__(self, name='default'):
        self.name = name
        self.problems = {}
        self.topic_groups = [] #topic group: problems in a topic group
                                #must include all the topics in the topic group
        self.top_id = -1        

    def load_content(self, filename):
        pass
        #update top_id

    def save_content(self, filename):
        pass
        #create json for topics and problems
            
        #create a backup

        #save collection 


        #add topics and topic groups
        #add problems

    def add_problem(self, topics, pat_1, pat_2,  prob_id=None, mastery_lvl=0,\
            ratings=[], answ_hist=[], time_answ_cor=0):
        if prob_id == None:
            self.top_id += 1
            prob_id = self.top_id
        pat_1 = Pattern(pat_1)
        pat_2 = Pattern(pat_2)
        new_prob = Problem(prob_id, topics, pat_1, pat_2, mastery_lvl,\
                ratings, answ_hist, time_answ_cor)

        self.problems[prob_id] = new_prob
    
    #returns all problems from the given topic groups
    def get_problems(self, topic_groups, selection_func):
        matching_problems = []
        if not topic_groups: #if all topics are included:
            return copy.deepcopy(selection_func(sorted(self.problems.items())))

        for problem in self.problems: #!!!efficiency?!!!
            for group in topic_groups:
                #all the group's topics are found in the problems topics
                if set(group).issubset(set(problem.topics)):
                   matching_problems.append(problem)
                   break #no need to check again for an already added group

        return copy.deepcopy(selection_func(sorted(matching_problems.items())))
    


    #returns each topic and number of problems in them
    def get_topics(self):
        pass

    #returns topic groups and number of problems in each topic group
    def get_topic_group_info(self):
        pass

