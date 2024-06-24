from statistics import mean


class Data:
    def __init__(self):
        self.utility_data = {}
        self.agent_data = {'Iteration': [], 'ID': [], 'Assignment': [], 'Utility': [], 'Expected Change in Utility': [],
                           'Cumulative Environmental Impact': [], 'Expected Impact': [], 'Base Line': [], 'Bound': []}
        self.neighbours_data = {'ID': [], 'neighbours': []}
        self.moral_agent_data = {'Iteration': [], 'ID': [], 'Assignment': [], 'Utility': [],
                                 'Expected Change in Utility': [], 'Cumulative Environmental Impact': [],
                                 'Expected Impact': []}
        self.moral_neighbours_data = {'Iteration': [], 'ID': [], 'Assignment': [], 'Utility': [], 'Base Line': [],
                                      'Bound': []}
        self.global_utility_data = {'Iteration': [], 'Global Utility': []}
        self.any_time_data = {'Iteration': [], 'Best Global Utility': []}
        # # ------------------------------------------helper for calculations:
        self.total_agents = 0
        self.helper = {'utility - start': [],
                       'utility - agent best': [],
                       'utility - finish': [],
                       'utility - global best': [],
                       'neighbours utility - start': [],
                       'neighbours utility - agent best': [],
                       'neighbours utility - finish': [],
                       'neighbours utility - global best': []}
        self.helper2 = {'Iteration': [], 'Average Utility': []}
        self.best_global_iteration = 0  # when global utility is max
        self.best_agent_iteration = 0  # when the special agent's utility is max

    def set_neighbours_data(self, data):
        for agent_id in data.keys():
            self.neighbours_data['ID'].append(agent_id)
            self.neighbours_data['neighbours'].append(data[agent_id])
            self.total_agents = len(data) - 1

        # ---------------------------------------------------------------------update num agents for utility_data cols
        for agent_id in data.keys():
            self.utility_data[agent_id] = []

    def update_data(self, data):
        # 0 - id of ME agent
        # moral_agents_neighbours:
        moral_neighbours = self.neighbours_data['neighbours'][0]
        # Iteration, ID, Assignment, Utility, Cumulative Environmental Impact, baseLine, bound
        iteration = data[0]
        id = data[1]
        assignment = data[2]
        utility = data[3]
        expected_change_utility = data[4]
        cumulative_environmental_impact = data[5]
        expected_impact = data[6]
        baseLine = data[7]
        bound = data[8]

        # ******************************************** helper:
        if iteration == 0:
            self.helper['utility - start'].append(utility)
        elif iteration == 999:
            self.helper['utility - finish'].append(utility)
        elif id == 0 and utility > max(self.moral_agent_data['Utility']):
            self.best_agent_iteration = iteration

        # _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_- helper2:
        if id in (self.neighbours_data['neighbours'][0]):
            if iteration in self.helper2['Iteration']:
                self.helper2['Average Utility'][iteration].append(utility)
            else:
                self.helper2['Iteration'].append(iteration)
                self.helper2['Average Utility'].append([])
                self.helper2['Average Utility'][iteration] = []
                self.helper2['Average Utility'][iteration].append(utility)

        # ------------------------------------------------------------------------agent_data
        self.agent_data['Iteration'].append(iteration)
        self.agent_data['ID'].append(id)
        self.agent_data['Assignment'].append(assignment)
        self.agent_data['Utility'].append(utility)
        self.agent_data['Expected Change in Utility'].append(expected_change_utility)
        self.agent_data['Cumulative Environmental Impact'].append(cumulative_environmental_impact)
        self.agent_data['Expected Impact'].append(expected_impact)
        self.agent_data['Base Line'].append(baseLine)
        self.agent_data['Bound'].append(bound)
        # ------------------------------------------------------------------------utility_data
        self.utility_data[id].append(utility)
        # ------------------------------------------------------------------------moral_agent_data
        if id == 0:
            self.moral_agent_data['Iteration'].append(iteration)
            self.moral_agent_data['Assignment'].append(assignment)
            self.moral_agent_data['Utility'].append(utility)
            self.moral_agent_data['Expected Change in Utility'].append(expected_change_utility)
            self.moral_agent_data['Cumulative Environmental Impact'].append(cumulative_environmental_impact)
            self.moral_agent_data['Expected Impact'].append(expected_impact)
        if id in moral_neighbours:
            self.moral_neighbours_data['Iteration'].append(iteration)
            self.moral_neighbours_data['ID'].append(id)
            self.moral_neighbours_data['Assignment'].append(assignment)
            self.moral_neighbours_data['Utility'].append(utility)
            self.moral_neighbours_data['Base Line'].append(baseLine)
            self.moral_neighbours_data['Bound'].append(bound)
            # # ******************************************** helper:
            if iteration == 0:
                self.helper['neighbours utility - start'].append(utility)
            elif iteration == 999:
                self.helper['neighbours utility - finish'].append(utility)
        # ------------------------------------------------------------------------global_utility_data
        if id == self.total_agents:
            self.global_utility_data['Iteration'].append(iteration)
            global_uti = 0
            for agent_id in range(self.total_agents):
                global_uti += self.utility_data[agent_id][-1]
            self.global_utility_data['Global Utility'].append(global_uti)
            if iteration == 0:
                self.any_time_data['Iteration'].append(iteration)
                self.any_time_data['Best Global Utility'].append(global_uti)
            # ------------------------------------------------------------------------any_time_data
            elif global_uti > max(self.any_time_data['Best Global Utility']):
                self.any_time_data['Iteration'].append(iteration)
                self.best_global_iteration = iteration
                self.any_time_data['Best Global Utility'].append(global_uti)

    def update_best_iteration_data(self):
        for agent_id in range(0, self.total_agents + 1):
            agent_uti_per_iteration = self.utility_data[agent_id]
            uti_global = agent_uti_per_iteration[self.best_global_iteration]
            uti_agent = agent_uti_per_iteration[self.best_agent_iteration]
            self.helper['utility - global best'].append(uti_global)
            self.helper['utility - agent best'].append(uti_agent)
            moral_neighbours = self.neighbours_data['neighbours'][0]
            if agent_id in moral_neighbours:
                self.helper['neighbours utility - global best'].append(uti_global)
                self.helper['neighbours utility - agent best'].append(uti_agent)

        # _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
        for iteration_num in self.helper2['Iteration']:
            average_uti = mean(self.helper2['Average Utility'][iteration_num])
            self.helper2['Average Utility'][iteration_num] = average_uti


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

class SimulationData:
    def __init__(self):
        self.line_chart_personal_data = {'Simple': [], 'Careful': [], 'Generous': [], 'Selfish': [], 'Random': [],
                                         'Egoist': [], 'Altruist': []}
        self.line_chart_neighbors_data = {'Simple': [], 'Careful': [], 'Generous': [], 'Selfish': [], 'Random': [],
                                          'Egoist': [], 'Altruist': []}
        self.line_chart_global_data = {'Simple': [], 'Careful': [], 'Generous': [], 'Selfish': [], 'Random': [],
                                       'Egoist': [], 'Altruist': []}
        self.line_chart_impact_data = {'Simple': [], 'Careful': [], 'Generous': [], 'Selfish': [], 'Random': [],
                                       'Egoist': [], 'Altruist': []}
        self.line_chart_ex_utility_data = {'Simple': [], 'Careful': [], 'Generous': [], 'Selfish': [], 'Random': [],
                                           'Egoist': [], 'Altruist': []}

    def update_data(self, data, agent_type):
        self.line_chart_personal_data[agent_type].extend(data.moral_agent_data['Utility'])
        self.line_chart_neighbors_data[agent_type].extend(data.helper2['Average Utility'])
        self.line_chart_global_data[agent_type].extend(data.global_utility_data['Global Utility'])
        self.line_chart_impact_data[agent_type].extend(data.moral_agent_data['Expected Impact'])
        self.line_chart_ex_utility_data[agent_type].extend(data.moral_agent_data['Expected Change in Utility'])


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
class AllSimulationData:
    def __init__(self, sims_list):
        self.num_iterations = 1000
        self.all_simulations = sims_list
        self.agent_types = ['Simple', 'Careful', 'Generous', 'Selfish', 'Random', 'Egoist', 'Altruist']

        # _-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
        self.line_chart_personal_list_data = {'Simple': [], 'Careful': [], 'Generous': [], 'Selfish': [],
                                              'Random': [], 'Egoist': [], 'Altruist': []}
        self.line_chart_neighbors_list_data = {'Simple': [], 'Careful': [], 'Generous': [], 'Selfish': [],
                                               'Random': [], 'Egoist': [], 'Altruist': []}
        self.line_chart_global_list_data = {'Simple': [], 'Careful': [], 'Generous': [], 'Selfish': [],
                                            'Random': [], 'Egoist': [], 'Altruist': []}
        self.line_chart_personal_mean_data = {'Simple': [], 'Careful': [], 'Generous': [], 'Selfish': [],
                                              'Random': [], 'Egoist': [], 'Altruist': []}
        self.line_chart_neighbors_mean_data = {'Simple': [], 'Careful': [], 'Generous': [], 'Selfish': [],
                                               'Random': [], 'Egoist': [], 'Altruist': []}
        self.line_chart_global_mean_data = {'Simple': [], 'Careful': [], 'Generous': [], 'Selfish': [],
                                            'Random': [], 'Egoist': [], 'Altruist': []}
        self.line_chart_impact_list_data = {'Simple': [], 'Careful': [], 'Generous': [], 'Selfish': [],
                                            'Random': [], 'Egoist': [], 'Altruist': []}
        self.line_chart_impact_mean_data = {'Simple': [], 'Careful': [], 'Generous': [], 'Selfish': [],
                                            'Random': [], 'Egoist': [], 'Altruist': []}
        self.line_chart_ex_utility_list_data = {'Simple': [], 'Careful': [], 'Generous': [], 'Selfish': [], 'Random': [],
                                           'Egoist': [], 'Altruist': []}
        self.line_chart_ex_utility_mean_data = {'Simple': [], 'Careful': [], 'Generous': [], 'Selfish': [], 'Random': [],
                                           'Egoist': [], 'Altruist': []}
        self.impact_utility_coordinates_data = {'Simple_impact': [], 'Simple_e_utility': [], 'Simple_r_utility': [],
                                                'Careful_impact': [], 'Careful_e_utility': [], 'Careful_r_utility': [],
                                                'Generous_impact': [], 'Generous_e_utility': [],
                                                'Generous_r_utility': [],
                                                'Selfish_impact': [], 'Selfish_e_utility': [], 'Selfish_r_utility': [],
                                                'Random_impact': [], 'Random_e_utility': [], 'Random_r_utility': []}

    def update_data(self):
        for agent_type in self.agent_types:
            for iteration in range(self.num_iterations):
                self.line_chart_personal_list_data[agent_type].append([])
                self.line_chart_personal_list_data[agent_type][iteration] = []
                self.line_chart_neighbors_list_data[agent_type].append([])
                self.line_chart_neighbors_list_data[agent_type][iteration] = []
                self.line_chart_global_list_data[agent_type].append([])
                self.line_chart_global_list_data[agent_type][iteration] = []
                self.line_chart_impact_list_data[agent_type].append([])
                self.line_chart_impact_list_data[agent_type][iteration] = []
                self.line_chart_ex_utility_list_data[agent_type].append([])
                self.line_chart_ex_utility_list_data[agent_type][iteration] = []
        for agent_type in self.agent_types:
            for data in self.all_simulations:
                for iteration in range(self.num_iterations):
                    cell_p = data.line_chart_personal_data[agent_type][iteration]
                    cell_n = data.line_chart_neighbors_data[agent_type][iteration]
                    cell_g = data.line_chart_global_data[agent_type][iteration]
                    cell_im = data.line_chart_impact_data[agent_type][iteration]
                    cell_eu = data.line_chart_ex_utility_data[agent_type][iteration]
                    self.line_chart_personal_list_data[agent_type][iteration].append(cell_p)
                    self.line_chart_neighbors_list_data[agent_type][iteration].append(cell_n)
                    self.line_chart_global_list_data[agent_type][iteration].append(cell_g)
                    self.line_chart_impact_list_data[agent_type][iteration].append(cell_im)
                    self.line_chart_ex_utility_list_data[agent_type][iteration].append(cell_eu)
        for agent_type in self.agent_types:
            for iteration in range(self.num_iterations):
                list_cell_p = self.line_chart_personal_list_data[agent_type][iteration]
                list_cell_n = self.line_chart_neighbors_list_data[agent_type][iteration]
                list_cell_g = self.line_chart_global_list_data[agent_type][iteration]
                list_cell_im = self.line_chart_impact_list_data[agent_type][iteration]
                list_cell_eu = self.line_chart_ex_utility_list_data[agent_type][iteration]
                mean_cell_p = mean(list_cell_p)
                mean_cell_n = mean(list_cell_n)
                mean_cell_g = mean(list_cell_g)
                mean_cell_im = mean(list_cell_im)
                mean_cell_eu = mean(list_cell_eu)
                self.line_chart_personal_mean_data[agent_type].append(mean_cell_p)
                self.line_chart_neighbors_mean_data[agent_type].append(mean_cell_n)
                self.line_chart_global_mean_data[agent_type].append(mean_cell_g)
                self.line_chart_impact_mean_data[agent_type].append(mean_cell_im)
                self.line_chart_ex_utility_mean_data[agent_type].append(mean_cell_eu)
        self.agent_types = ['Simple', 'Careful', 'Generous', 'Selfish', 'Random']
        for agent_type in self.agent_types:
            column_impact = agent_type + "_impact"
            column_e_utility = agent_type + "_e_utility"
            column_r_utility = agent_type + "_r_utility"
            for iteration in range(self.num_iterations-1):
                iteration_impact = self.line_chart_impact_mean_data[agent_type][iteration]
                iteration_e_utility = self.line_chart_ex_utility_mean_data[agent_type][iteration]
                iteration_r_utility = self.line_chart_personal_mean_data[agent_type][iteration+1] - self.line_chart_personal_mean_data[agent_type][iteration]
                self.impact_utility_coordinates_data[column_impact].append(iteration_impact)
                self.impact_utility_coordinates_data[column_e_utility].append(iteration_e_utility)
                self.impact_utility_coordinates_data[column_r_utility].append(iteration_r_utility)

