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
        self.DEFAULT_COL = "default"

        #try loading collectio from default file
        self.load_collection(self.DEFAULT_COL)

    #turns a problem's properties into a dictionary form
    def prob_to_dict(self, problem):
        pat1 = {
                "content" : problem.pat_1.content,
                "pat_type" : problem.pat_1.pat_type,
                "media" : problem.pat_1.media
                }
        
        pat2 = {
                "content" : problem.pat_2.content,
                "pat_type" : problem.pat_2.pat_type,
                "media" : problem.pat_2.media
                }

        return {
                "id" : problem.id,
                "pat_1" : pat1,
                "pat_2" : pat2,
                "topics" : problem.topics,
                "mast_lvl" : problem.mast_lvl,
                "ratings" : problem.ratings,
                "answ_hist" : problem.answ_hist
                }

    #turns the collection object's properties into a dictionary
    def col_to_dict(self):
        problems_D = {problem_id : self.prob_to_dict(problem)\
                for problem_id, problem in self.problems.items()}
        return {
            "col_name" : self.name,
            "problems" : problems_D
                }

    def load_collection(self, col_name):
        with open(f'{col_name}_col.json', 'r') as json_file:
            col_dict = json.load(json_file)
            self.name = col_dict['col_name']
            for prob_id, data in col_dict['problems'].items():
                self.add_problem(data["topics"], Pattern(**data["pat_1"]),\
                        Pattern(**data["pat_2"]), data["id"],\
                        data["mast_lvl"], data["ratings"], data["answ_hist"])
                id_counter = data["id"]
            self.top_id = id_counter 

    def save_collection(self, col_name):
        with open(f'{col_name}_col.json', 'w') as json_file:
            json.dump(self.col_to_dict(), json_file, indent=4)

        #create json for topics and problems
        
    def create_backup(self, col_name):
        pass

        #add topics and topic groups
        #add problems
        
    def close_collection(self):
        #write back_up?

        #save collection:
        self.save_collection(self.DEFAULT_COL)

    def add_problem(self, topics, pat_1, pat_2,  prob_id=None, mastery_lvl=0,\
            ratings=[], answ_hist=[], time_answ_cor=0):
        if prob_id == None:
            self.top_id += 1
            prob_id = self.top_id
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

