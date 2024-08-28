#collection.py
#responsible for loading, holding and managing problems and topics
import json
import copy
import os
import datetime

from problem import Problem
from pattern import Pattern

class Collection():
    def __init__(self, name='default'):
        self.name = name
        self.problems = {}
        self.topic_groups = [] #topic group: problems in a topic group
                                #must include all the topics in the topic group
        self.top_id = -1      

        #try loading collectio from default file
        self.load_collection(name)

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
                "prob_id" : problem.prob_id,
                "pat_1" : pat1,
                "pat_2" : pat2,
                "topics" : problem.topics,
                "mast_lvl" : problem.mast_lvl,
                "ratings" : problem.ratings,
                "answ_hist" : problem.answ_hist,
                "time_answ_cor" : problem.time_answ_cor.isoformat() if \
                        problem.time_answ_cor else None
                }

    #turns the collection object's properties into a dictionary
    def col_to_dict(self):
        problems_D = {prob_id : self.prob_to_dict(problem)\
                for prob_id, problem in self.problems.items()}
        return {
            "col_name" : self.name,
            "problems" : problems_D
                }

    def load_collection(self, col_name):
        #!!! ADD check if collection doesnt exist:

        with open(f'{col_name}_col.json', 'r') as json_file:
            try:
                col_dict = json.load(json_file)
                self.name = col_name
                for prob_id, data in col_dict['problems'].items():
                    self.add_problem(data["topics"], Pattern(**data["pat_1"]),\
                            Pattern(**data["pat_2"]), data["prob_id"],\
                            data["mast_lvl"], data["ratings"], data["answ_hist"],\
                            datetime.datetime.fromisoformat(data["time_answ_cor"]) if \
                                data["time_answ_cor"] != None else None)
                    id_counter = data["prob_id"]
                self.top_id = id_counter #update to highest id
            except Exception as e: 
                print(f'No data could be loaded into the collection. {e}')

    def save_collection(self, col_name):
        with open(f'{col_name}_col.json', 'w') as json_file:
            json.dump(self.col_to_dict(), json_file, indent=4)

        #create json for topics and problems
        
    def create_backup(self, col_name):
        #get current time in string format
        cur_time = datetime.datetime.now().strftime("%d-%m-%Y|%H-%M-%S")

        with open(f'./backups/{col_name}_{cur_time}_col.json', 'w') as json_file:
            json.dump(self.col_to_dict(), json_file, indent=4)
        
    def close_collection(self):
        #write back_up?
        self.create_backup(self.name)
        #save collection:
        self.save_collection(self.name)

    def add_problem(self, topics, pat_1, pat_2,  prob_id=None, mastery_lvl=0,\
            ratings=[], answ_hist=[], time_answ_cor=None):
        if prob_id == None:
            self.top_id += 1
            prob_id = self.top_id
        new_prob = Problem(prob_id, topics, pat_1, pat_2, mastery_lvl,\
                ratings, answ_hist, time_answ_cor)

        self.problems[prob_id] = new_prob
    
    def replace_problem(self, problem):
        self.problems[problem.prob_id] = problem
    
    #returns all problems from the given topic groups
    def get_problems(self, topic_groups, selection_func):
        matching_problems = []

        self.update_prominances()

        problems = self.problems
        #if all topics are included
        if not topic_groups:
            return copy.deepcopy(selection_func(self.problems))

        #when topic groups are set:
        for problem in self.problems: #!!!efficiency?!!!
            for group in topic_groups:
                #all the group's topics are found in the problems topics
                if set(group).issubset(set(problem.topics)):
                   matching_problems.append(problem)
                   break #no need to check again for an already added group

        return copy.deepcopy(selection_func(sorted(matching_problems.items())))
    
    #remove a problem from the collection
    def delete_problem(self, prob_id):
        try:
            del self.problems[prob_id]
            return True
        except KeyError: 
            return False

    #updates prominance values for problems given in parameters.
    def update_prominances(self, problems = None):
        if problems == None:
            problems = self.problems
        #!!!More efficient way for updating later
            # -update higher mastered levels less frequently 

        for problem in problems.values():
            problem.calc_prominance()

    #returns each topic and number of problems in them
    def get_topics(self):
        pass

    #returns topic groups and number of problems in each topic group
    def get_topic_group_info(self):
        pass

    #returns information about a problem or all the problems if argument
    #is not provided
    def get_problem_info(self, prob_id = None):
        self.update_prominances() 

        probs = self.problems
        #if a problem id was provided:
        if prob_id != None:
            #!!!!TRY IF IT CAN BE FOUND
            probs = {prob_id : self.problems[prob_id]}

        prob_info = []
        for prob in probs.values():
            prob_info.append(f'''problem id: {prob.prob_id} - promenance:\
 {prob.prominance} - mastery: {prob.mast_lvl}''')
        return prob_info
