import copy
from enums import *

from Agents import *
from random import Random


class Constraint:
    def __init__(self,D,seed,lower_bound=0,upper_bound=100,):
        self.D = D
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.cost_rnd = Random(seed)
        self.matrix = self.create_matrix()
        #self.matrix_transpose = self.create_transpose()

    def create_matrix(self):
        ans = []
        for i in range(self.D):
            row = []
            for j in range(self.D):
                row.append(self.cost_rnd.randint(self.lower_bound,self.upper_bound))
            ans.append(row)
        return ans

    def get_matrix(self):
        return copy.deepcopy(self.matrix)
    #def create_transpose(self):
        #transpose = []
        #for i in range(self.D):
            #row = []
            #for j in range(self.D):
                #row.append(self.matrix[j][i])
            #transpose.append(row)
        #return transpose


    #def get_matrix_transpose(self):
        #return copy.deepcopy(self.matrix_transpose)

class DCOP:
    def __init__(self,dcop_id,numAgents,domainSize,density,environment,special_agent_type,special_agent_amount,amount_iterations):


        self.final_iteration = amount_iterations
        self.dcop_id = dcop_id
        self.rnd_SociallyMotivated_bound = Random((self.dcop_id+5)*17)

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
    def create_agents(self):
        special_agent_counter = 0
        for agent_id in range(self.numAgents):
            if special_agent_counter<self.special_agent_amount:
                self.agents[agent_id] = self.get_special_agent(agent_id)
                special_agent_counter = special_agent_counter+1
            else:
                self.agents[agent_id] = self.get_environment_agent(agent_id)

    def get_environment_agent(self,agent_id):
        ans = None
        if self.environment == AgentEnvironment.socially_motivated:
            bound = round( self.rnd_SociallyMotivated_bound.uniform(0.05, 0.5), 2)
            ans =  SociallyMotivatedAgent(agent_id, self.domainSize, bound)
        if self.environment == AgentEnvironment.altruist:
            ans = AltruistAgent(agent_id, self.domainSize)
        if self.environment == AgentEnvironment.egoist:
            ans = EgoistAgent(agent_id, self.domainSize)

        ans.is_special = False
        return ans
    def get_special_agent(self,agent_id):
        ans = None
        if self.special_agent_type == AgentSpecial.egoist:
            ans = EgoistAgent(agent_id, self.domainSize)
        if self.special_agent_type == AgentSpecial.altruist:
            ans = AltruistAgent(agent_id, self.domainSize)
        if self.special_agent_type == AgentSpecial.simple:
            ans = SimpleAgent(agent_id, self.domainSize)
        if self.special_agent_type == AgentSpecial.careful:
            ans = CarefulAgent(agent_id, self.domainSize)
        if self.special_agent_type == AgentSpecial.generous:
            ans = GenerousAgent(agent_id, self.domainSize)
        if self.special_agent_type == AgentSpecial.selfish:
            ans = SelfishAgent(agent_id, self.domainSize)
        if self.special_agent_type == AgentSpecial.random:
            ans = RandomAgent(agent_id, self.domainSize)
        ans.is_special = True
        return ans


    def create_neighbors(self):
        for agent_id in self.agents.keys():
            self.neighbours[agent_id] = []
        agents = sorted(self.agents.values(), key= lambda x:x.id)
        for i in range(len(agents)):
            a1 = agents[i]
            for j in range(i+1,len(agents)):
                a2 = self.agents[j]
                rnd_neighbors = Random(((self.dcop_id+1)*110+(a1.id+1)*13+(a2.id+1))*17)
                rnd_neighbors.random()
                if rnd_neighbors.uniform(0.0, 1.0)<self.p1:
                    seed_first = ((self.dcop_id+1)*100+(a1.id+1)*10+(a2.id+1))*177
                    constraint_1 = Constraint(D=self.domainSize,seed =seed_first).get_matrix()
                    a1.meet_neighbour(a2,constraint_1)

                    seed_second = ((self.dcop_id + 1) * 111 + (a1.id + 1) * 17 + (a2.id + 1)) * 1000
                    constraint_2 = Constraint(D=self.domainSize, seed=seed_second).get_matrix()
                    a2.meet_neighbour(a1,constraint_2)


    def initiate_dcop(self):

        for agent in self.agents.values():
            agent.initiate()

        for i in range(self.final_iteration):
            while True:
                for agent in self.agents.values():
                    agent.listen()

                for agent in self.agents.values():
                    agent.reply()

                    if agent.phase == 4 and agent.is_special:
                        print(type(agent), i, agent.utility)
                if agent.phase == 4:
                    break


                #if agent.phase == 4:
                    #break
                    #data.update_data(agent.get_data())  # save data here
                    #up = True
            #if up:
                #i = i + 1

        #print("#################### finished DCOP",self.dcop_id)

        #data.update_best_iteration_data()
