from Agents import *
from SchedulerV2 import *


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

    def create_agents(self):
        special_agent_counter = 0
        for agent_id in self(self.numAgents):
            if special_agent_counter<special_agent_amount:
                self.agents[agent_id] = self.get_special_agent(agent_id)
            else:
                self.agents[agent_id] = self.get_environment_agent(agent_id)

    def get_environment_agent(self,agent_id):

        if self.environment == AgentEnvironment.egoist:
            #bound = round(random.uniform(0.05, 0.5), 2) TODO use random bound using agent id and dcop id
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




