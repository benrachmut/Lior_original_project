import copy

from Agents import *
from SchedulerV2 import *
from random import Random


class Constraint:
    def __init__(self,D,seed,lower_bound=0,upper_bound=100,):
        self.D = D
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.cost_rnd = Random(seed)
        self.matrix = self.create_matrix()
        self.matrix_transpose = self.create_transpose()

    def create_matrix(self):
        ans = []
        for i in range(self.D):
            row = []
            for j in range(self.D):
                row.append(self.cost_rnd.randint(self.lower_bound,self.upper_bound))
            ans.append(row)
        return ans

    def create_transpose(self):
        transpose = []
        for i in range(self.D):
            row = []
            for j in range(self.D):
                row.append(self.matrix[j][i])
            transpose.append(row)
        return transpose

    def get_matrix(self):
        return copy.deepcopy(self.matrix)

    def get_matrix_transpose(self):
        return copy.deepcopy(self.matrix_transpose)

class DCOP:
    def __init__(self,dcop_id,numAgents,domainSize,density,environment,special_agent_type,special_agent_amount):
        self.dcop_id = dcop_id
        self.p1 = density
        self.numAgents = numAgents
        self.domainSize = domainSize
        self.environment = environment
        self.special_agent_type = special_agent_type
        self.special_agent_amount = special_agent_amount
        # _________________________________creations
        self.agents = {}  # { key: id, value: agent}
        self.neighbours = {}  # { key: id, value: all his neighbours}
        self.constraints = {}
        self.create_agents()
        self.rnd_SociallyMotivated_bound = Random((self.dcop_id+5)*17)

    def create_agents(self):
        special_agent_counter = 0
        for agent_id in self(self.numAgents):
            if special_agent_counter<special_agent_amount:
                self.agents[agent_id] = self.get_special_agent(agent_id)
            else:
                self.agents[agent_id] = self.get_environment_agent(agent_id)

    def get_environment_agent(self,agent_id):

        if self.environment == AgentEnvironment.egoist:
            bound = round( self.rnd_SociallyMotivated_bound.uniform(0.05, 0.5), 2)
            return  SociallyMotivatedAgent(agent_id, self.domainSize, bound)
        if self.environment == AgentEnvironment.altruist:
            return AltruistAgent(agent_id, self.domainSize)
        if self.environment == AgentEnvironment.altruist:
            return EgoistAgent(agent_id, self.domainSize)

    def get_special_agent(self,agent_id):
        if self.special_agent_type == AgentSpecial.egoist:
            return EgoistAgent(agent_id, self.domainSize)
        if self.special_agent_type == AgentSpecial.altruist:
            return AltruistAgent(agent_id, self.domainSize)
        if self.special_agent_type == AgentSpecial.simple:
            return SimpleAgent(agent_id, self.domainSize)
        if self.special_agent_type == AgentSpecial.careful:
            return CarefulAgent(agent_id, self.domainSize)
        if self.special_agent_type == AgentSpecial.generous:
            return GenerousAgent(agent_id, self.domainSize)
        if self.special_agent_type == AgentSpecial.selfish:
            return SelfishAgent(agent_id, self.domainSize)
        if self.special_agent_type == AgentSpecial.random:
            return RandomAgent(agent_id, self.domainSize)

    def create_neighbors(self):
        for agent_id in self.agents.keys():
            self.neighbours[agent_id] = []
        agents = sorted(self.agents.values(), key= lambda x:x.id)
        for i in range(len(agents)):
            a1 = agents[i]
            for j in range(i+1,len(agents)):
                a2 = self.agents[j]
                if self.rnd_neighbors.uniform(0.0, 1.0)<self.p1:
                    seed = ((self.dcop_id+1)*100+(a1.id+1)*10+(a2.id+1))*177
                    constraint = Constraint(D=self.domainSize,seed =seed)
                    constraint_matrix_a1_row_a2_col = constraint.get_matrix()
                    a1.meet_neighbor(a2.id,constraint_matrix_a1_row_a2_col) # need todo this, complete lior neighbors and constraints like lior ask about transpose
                    constraint_matrix_a2_row_a1_col = constraint.get_matrix_transpose()
                    a2.meet_neigbor(a1.id,constraint_matrix_a2_row_a1_col)

