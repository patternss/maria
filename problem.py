#problem.py - module that implements the problems offered by Maria

class Problem():
    def __init__(self, prob_id, topic, description, thing):
        self.id = prob_id
        self.description = description
        self.thing = thing
        self.topic = topic


