from Message import Message
import numpy as np
import random


class Agent:
    # neighbours - list of agent Ai’s neighbours { key: id, value: neighbour}
    # constraints - set of agent Ai’s constraint matrixes with his neighbours { key: neighbour_id, value: matrix}
    def __init__(self, id, domainSize, privacyLevel):
        self.id = id
        self.domainSize = domainSize
        self.privacyLevel = privacyLevel
        self.assignment = 0
        self.utility = 0
        # -------------------initialise phase
        self.neighbours = {}
        self.constraints = {}
        self.domain = []
        # -------------------information
        self.alterValue = 0
        self.my_local_change = 0
        self.offered_local_changes = []
        self.LocalView = {}
        self.taboos = {}  # my taboos
        # -------------------messages
        self.message_box = []
        # -------------------data
        self.phase = 0
        self.iteration = 0
        self.totalIterations = 1000

    # __________________________________________________________________initiate:
    # neighbours - { key: id, value: neighbour}
    def init_neighbours(self, neighbours):
        self.neighbours = neighbours

    # constraints - { key: neighbour id, value: matrix}
    def init_constraints(self, constraints):
        self.constraints = constraints

    # by domain size
    def init_domain(self):
        for i in range(self.domainSize):
            self.domain.append(i)

    # _____________________________________________________________________________PRIVET METHODS:
    # _______________________________________________________________message_boxes:
    # ------------clear
    # PHASE 1 - value
    # PHASE 2 - pref
    # PHASE 3 - alternative_value_and_improvement
    # PHASE 4 - taboo
    def clear_message_box(self):
        self.message_box = []

    # ------------collect
    # PHASE 1 - value
    # PHASE 2 - pref
    # PHASE 3 - alternative_value_and_improvement
    # PHASE 4 - taboo
    def collect_messages(self, msg):
        self.message_box.append(msg)

    # ------------send
    # PHASE 1 - pref
    # PHASE 2 - alternative_value_and_improvement
    # PHASE 3 - taboo
    # PHASE 4 - value
    def send_messages(self, messages_to_send):
        # messages_to_send = {key: neighbour_id, value: msg}
        for neighbour_id in messages_to_send:
            neighbour = self.neighbours[neighbour_id]
            msg = messages_to_send[neighbour_id]
            neighbour.collect_messages(msg)

    # ------------make
    # PHASE 1 - pref
    def make_pref_messages(self):
        messages_to_send = {}
        if self.privacyLevel == 2:
            pass
        elif self.privacyLevel == 3:
            pass
        else:
            for neighbour_id in self.neighbours:
                pref_list = self.privacy_level_1_full_information(neighbour_id)
                content = pref_list
                sender = self.id
                receiver = neighbour_id
                msg = Message(sender, receiver, content)
                messages_to_send[neighbour_id] = msg
        return messages_to_send

    # PHASE 2 - alternative_value_and_improvement
    # def make_alternative_value_and_improvement_messages(self, indications):
    #     socialGain = self.calculate_social_gain_for_alter_value(indications)
    #     messages_to_send = {}
    #     content = [self.alterValue, socialGain]
    #     sender = self.id
    #     for neighbour_id in self.neighbours:
    #         receiver = neighbour_id
    #         msg = Message(sender, receiver, content)
    #         messages_to_send[neighbour_id] = msg
    #     return messages_to_send

    # PHASE 2 - alternative_value
    def make_alternative_value_local_change_messages(self):
        messages_to_send = {}
        content = [self.alterValue, self.my_local_change]
        sender = self.id
        for neighbour_id in self.neighbours:
            receiver = neighbour_id
            msg = Message(sender, receiver, content)
            messages_to_send[neighbour_id] = msg
        return messages_to_send

    # PHASE 3 - taboo
    def make_taboo_messages(self):
        # send taboo if passed the threshold
        # send smaller_social_gain if my improvement is better than the neighbour's
        pass

    # PHASE 4 - value
    def make_value_messages(self):
        messages_to_send = {}
        content = self.assignment
        sender = self.id
        for neighbour_id in self.neighbours:
            receiver = neighbour_id
            msg = Message(sender, receiver, content)
            messages_to_send[neighbour_id] = msg
        return messages_to_send

    # _______________________________________________________________calculate:
    # ----------------------------PHASE 1 - pref messages
    # potential change in utility for each assignment in the domain
    def privacy_level_1_full_information(self, neighbour_id):
        indications_list = np.zeros(self.domainSize, dtype=int)
        constraint_matrix_with_n = self.constraints[neighbour_id]
        # find permanent part of utility
        perm_uti = self.only_one_change_assignment(neighbour_id)
        for index in range(len(indications_list)):
            potential_utility = perm_uti + constraint_matrix_with_n[self.assignment][index]
            indications_list[index] = potential_utility - self.utility
        return indications_list

    # (potential change in utility/ total utility) for each assignment in the domain
    def privacy_level_2_relative_information(self, neighbour_id):  # *************************** fix!!!
        indications_matrix = np.zeros((self.domainSize, self.domainSize))
        constraint_matrix_with_n = self.constraints[neighbour_id]
        for row in indications_matrix:
            for column in row:
                potential_utility = constraint_matrix_with_n[row][column]
                indications_matrix[row][column] = (potential_utility - self.utility) / self.utility
        return indications_matrix

    # which assignment in the neighbor’s’ domain of is the most preferable to me, and by how much (potential change in utility)
    def privacy_level_3_preferences(self, neighbour):
        pass

    # ----------------------------calculate utility:
    def calculate_utility(self, assignment):
        utility = 0
        for neighbour_id in self.neighbours:
            # column for constraint matrix
            neighbour_assignment = self.LocalView[neighbour_id]
            constraint_matrix_with_n = self.constraints[neighbour_id]
            uti = constraint_matrix_with_n[assignment][neighbour_assignment]
            utility = utility + uti
        return utility

    # ----------------------------calculate social gain for alter value:
    def calculate_local_change_for_alter_value(self, indications):
        my_change = self.calculate_utility(self.alterValue) - self.utility
        n_local_change = 0
        for neighbour_id in self.neighbours:
            # local changes for neighbours:
            indications_list_from_n = indications[neighbour_id]
            n_change = indications_list_from_n[self.alterValue]
            n_local_change = n_local_change + n_change
        self.my_local_change = my_change + n_local_change

    # ----------------------------calculate perm uti:
    def only_one_change_assignment(self, neighbour_id):
        # perm uti = utility - relative utility of this neighbour
        # potential_utility = perm uti + utility per assignment of neighbour
        # indications = potential_utility - current utilitys
        constraint_matrix_with_n = self.constraints[neighbour_id]
        # find permanent part of utility
        neighbour_assignment = self.LocalView[neighbour_id]
        perm_uti = self.utility - constraint_matrix_with_n[self.assignment][neighbour_assignment]
        return perm_uti

    def __str__(self):
        s = "agent ID: " + str(self.id) + ", utility: " + str(self.utility)
        return s
