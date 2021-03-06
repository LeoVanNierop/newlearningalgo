#put imports here
import numpy as np

class Brain(object):
    random_state = np.random.RandomState(666) # maintain shared randomstate for reproducibility

    neurons = []
    sensors = [] # neurons that fire based on inputs (eg, 'vision')
    actuators = [] # neurons that fire to signal outputs (eg classifications)





class Neuron(object):
    ''' a class representing a single neuron in a brain. It has input dendrites, 
    and a single output dendrite. Multiple other neurons can have an input dendrite
    listening to the output.
    A neuron can grow new dendrites, strengthen or weaken its input dendites, and connect
    a dendrite to a random neuron (proximity based??).
    These actions are performed in response to "pleasure" or "pain" signals coming back down
    the output dendrite (pain/pleasure treshold to allow small mistakes to only affect a few
    neurons?)
    A neuron that for some reason has all connected neurons absolute weight too small should
    atrophy and be killed off'''
    
    output = 0 # always zero or 1
    _update_output = 0 # used to update all neurons simultaneously: first calculate this, then assign them all to their outputs
    alive = True
    pain_treshold = 0.1
    pleasure_treshold = 0.1
    
    brain = None # a link to the brain object containing this neuron
    _bias = 1 # this sets the turnover point, if inputs==bias, firing probability is 1/2
    inputs = [
        {
            'weight': 1,
            'link': None,
            'time_idle': 0
        }
    ] # a new neuron receives a single unconnnected input dendride with unit weight. 
      # this can be modified at spawning time (helper function? __init__?)
   
    _settable = [
            'pain_treshold',
            'pleasure_treshold',
            'brain',
            'inputs',
        ]
   
    def __init__(self, data={}):
        for item in data:
            if item in self._settable:
                setattr(self, item, data[item])
                
    
    def prepare_output(self, random_state):
        in_value = sum([x['weight']*x['link'].output for x in inputs if x['link'] is not None])
        prob = 0.5+0.5*np.sinh(in_value - _bias)
        if prob > random_state.rand():
            _update_output = 1
        else:
            _update_output = 0
    
    def apply_output(self):
        ouput = _update_output
        
    def grow_input(self, initial_weight=1, initial_link=None):
        inputs.append({
            'weight': initial_weight,
            'link': initial_link,
            'time_idle': None
            })
            
    def link_dangling_inputs(self, random_state):
        if brain is None:
            return
        else:
            for dendrite in inputs:
                if dendrite['link'] == None:
                    dendrite['link'] = random_state.choice(self.brain.neurons)
                    #yes, this could create self-reinforcing neurons
                    #no, that is not per se a bad thing.
    
    def atrophy(self, minweight=0.1):
    #the default minimum needs experimentation
        self.inputs = [x for x in self.inputs if x['weight']>minweight]
        if len(self.inputs) == 0:
            self.alive = False
        
    def happiness_feedback(pleasure=0, pain=0):
        if pain > self.pain_treshold:
            for input in self.inputs:
                if input.output == 0:
                    input['weight'] += pain-self.pain_treshold
                else:
                    input['weight'] -= pain-self.pain_treshold
                    input.happiness_feedback(pain=pain)
        if pleasure > self.pleasure_treshold:
            for input in self.inputs:
                if input.output == 1:
                    input['weight'] += pleasure-self.pleasure_treshold
                else:
                    input['weight'] -= pleasure-self.pleasure_treshold
                    input.happiness_feedback(pleasure=pleasure)
                    
    def __repr__(self):
        data = {x: getattr(self, x, None) for x in self._settable}
        rep = "Neuron({})".format(data)
        return rep
        
    
    
    
    
    
      
    
