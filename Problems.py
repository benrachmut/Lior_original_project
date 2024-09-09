import copy
from enums import *

from Agents import *
from random import Random


class Constraint:
    def __init__(self, D, seed, lower_bound=0, upper_bound=100, ):
        self.D = D
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.cost_rnd = Random(seed)
        self.matrix = self.create_matrix()
        # self.matrix_transpose = self.create_transpose()

    def create_matrix(self):
        ans = []
        for i in range(self.D):
            row = []
            for j in range(self.D):
                row.append(self.cost_rnd.randint(self.lower_bound, self.upper_bound))
            ans.append(row)
        return ans

    def get_matrix(self):
        return copy.deepcopy(self.matrix)
    # def create_transpose(self):
    # transpose = []
    # for i in range(self.D):
    # row = []
    # for j in range(self.D):
    # row.append(self.matrix[j][i])
    # transpose.append(row)
    # return transpose

    # def get_matrix_transpose(self):
    # return copy.deepcopy(self.matrix_transpose)


class DCOP:
    def __init__(self, dcop_id, numAgents, domainSize, density, environment, special_agent_type, special_agent_amount,
                 amount_iterations):

        self.final_iteration = amount_iterations
        self.dcop_id = dcop_id
        self.rnd_SociallyMotivated_bound = Random((self.dcop_id + 5) * 17)

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

        self.agents_special_list = []
        self.agents_non_special_list = []
        self.all_agents_list = []
        self.create_agents()
        self.agents_dict_by_role = {"Global Utility": self.all_agents_list,
                                    "Unique Agents Utility": self.agents_special_list,
                                    "Environment Agents Utility": self.agents_non_special_list,
                                    "Cumulative Environment Impact": self.agents_special_list}
        self.data = {}
        self.init_data_dict()


    def create_agents(self):
        self.all_agents_list = []
        special_agent_counter = 0
        for agent_id in range(self.numAgents):
            if special_agent_counter < self.special_agent_amount:
                agent = self.get_special_agent(agent_id)
                self.agents[agent_id] = agent
                self.agents_special_list.append(agent)
                special_agent_counter = special_agent_counter + 1
            else:
                agent = self.get_environment_agent(agent_id)
                self.agents[agent_id] = agent
                self.agents_non_special_list.append(agent)

            self.all_agents_list.append(agent)

    def get_environment_agent(self, agent_id):
        ans = None
        if self.environment == AgentEnvironment.PC:
            bound = round(self.rnd_SociallyMotivated_bound.uniform(0.05, 0.5), 2)
            ans = SociallyMotivatedAgent(agent_id, self.domainSize, bound)
        if self.environment == AgentEnvironment.Altruistic:
            ans = AltruistAgent(agent_id, self.domainSize)
        if self.environment == AgentEnvironment.Egoistic:
            ans = EgoistAgent(agent_id, self.domainSize)

        ans.is_special = False
        return ans

    def get_special_agent(self, agent_id):
        ans = None
        if self.special_agent_type == AgentSpecial.Egoist:
            ans = EgoistAgent(agent_id, self.domainSize)
        if self.special_agent_type == AgentSpecial.Altruist:
            ans = AltruistAgent(agent_id, self.domainSize)
        if self.special_agent_type == AgentSpecial.Simple:
            ans = SimpleAgent(agent_id, self.domainSize)
        if self.special_agent_type == AgentSpecial.Careful:
            ans = CarefulAgent(agent_id, self.domainSize)
        if self.special_agent_type == AgentSpecial.Generous:
            ans = GenerousAgent(agent_id, self.domainSize)
        if self.special_agent_type == AgentSpecial.Selfish:
            ans = SelfishAgent(agent_id, self.domainSize)
        if self.special_agent_type == AgentSpecial.Random:
            ans = RandomAgent(agent_id, self.domainSize)
        ans.is_special = True
        return ans

    def create_neighbors(self):
        for agent_id in self.agents.keys():
            self.neighbours[agent_id] = []
        agents = sorted(self.agents.values(), key=lambda x: x.id)
        for i in range(len(agents)):
            a1 = agents[i]
            for j in range(i + 1, len(agents)):
                a2 = self.agents[j]
                rnd_neighbors = Random(((self.dcop_id + 1) * 110 + (a1.id + 1) * 13 + (a2.id + 1)) * 17)
                rnd_neighbors.random()
                if rnd_neighbors.uniform(0.0, 1.0) < self.p1:
                    seed_first = ((self.dcop_id + 1) * 100 + (a1.id + 1) * 10 + (a2.id + 1)) * 177
                    constraint_1 = Constraint(D=self.domainSize, seed=seed_first).get_matrix()
                    a1.meet_neighbour(a2, constraint_1)

                    seed_second = ((self.dcop_id + 1) * 111 + (a1.id + 1) * 17 + (a2.id + 1)) * 1000
                    constraint_2 = Constraint(D=self.domainSize, seed=seed_second).get_matrix()
                    a2.meet_neighbour(a1, constraint_2)

    def initiate_dcop(self):

        for agent in self.agents.values():
            agent.initiate()

            # agent.init_domain()
        for i in range(self.final_iteration):
            self.record_data(i)
            while True:
                for agent in self.agents.values():
                    agent.listen()

                for agent in self.agents.values():
                    agent.reply()

                if agent.phase == 4:
                    break
        #print("DCOP",self.dcop_id,"is over")

    def record_data(self, i):

        for k, v in self.agents_dict_by_role.items():
            if k == "Cumulative Environment Impact":
                util = 0
                for agent in v:
                    if isinstance(agent,MoralAgent):
                        util = util + agent.cumulative_environmental_impact
                self.data[k][i] = util
            else:
                util = 0
                for agent in v:
                    agent_utility = self.get_agent_util(agent)
                    util = util + agent_utility
                self.data[k][i] = util

    def init_data_dict(self):
        for k in self.agents_dict_by_role.keys():
            self.data[k] = {}

    def get_agent_util(self, agent):
        agent_assignment = agent.assignment
        neighbours = agent.neighbours
        neighbors_assignments = self.get_neighbors_assignments(neighbours)
        constraints = agent.constraints
        ans = 0
        for n_id,matrix in constraints.items():
            neighbors_assignment = neighbors_assignments[n_id]
            ans = ans+matrix[agent_assignment][neighbors_assignment]
        return ans


    def get_neighbors_assignments(self,neighbours):
        ans = {}
        for n_id,obj_ in neighbours.items():
            ans[n_id]=obj_.assignment
        return ans


