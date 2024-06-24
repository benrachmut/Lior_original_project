from MoralAgent import MoralAgent
import math
import random


# moral licensing -> +
# moral compensation -> -
# dictionary[assignment] = [improvement for me, local changes for neighbours]

# _______________________________________________________________________________________________________________
class SimpleAgent(MoralAgent):

    # PHASE 2 - Debits - Choose the option that is most beneficial for the society
    def strategy_moral_compensation(self, indications):
        neighbours_preferences = self.neighbours_preferences(indications)
        if neighbours_preferences:  # not empty
            criterion = -math.inf
            for assignment in neighbours_preferences:
                social_gain = neighbours_preferences[assignment][1]
                if social_gain > criterion:
                    criterion = social_gain
                    next_assignment = assignment
            self.alterValue = next_assignment
        else:
            self.alterValue = self.assignment

    # PHASE 2 - Credits - Choose the option that is most beneficial to him
    def strategy_moral_licensing(self, indications):
        beneficial_to_me = self.beneficial_to_myself(indications)
        if beneficial_to_me:  # not empty
            criterion = -math.inf
            for assignment in beneficial_to_me:
                my_gain = beneficial_to_me[assignment][0]
                if my_gain > criterion:
                    criterion = my_gain
                    next_assignment = assignment
            self.alterValue = next_assignment
        else:
            self.alterValue = self.assignment

    def __str__(self):
        s = "Simple, utility: " + str(round(self.utility)) + ", EI: " + str(self.cumulative_environmental_impact) + \
            ", assignment: " + str(self.assignment)
        return s


# _______________________________________________________________________________________________________________
class CarefulAgent(MoralAgent):

    # PHASE 2 - Debits - from the neighbours’ preferences
    # choose the option that will least distance him from the balance
    def strategy_moral_compensation(self, indications):
        neighbours_preferences = self.neighbours_preferences(indications)
        if neighbours_preferences:  # not empty
            criterion = math.inf
            for assignment in neighbours_preferences:
                distance_from_balance = abs(neighbours_preferences[assignment][1].item() + self.cumulative_environmental_impact)
                if assignment == self.assignment:
                    temperature = self.totalIterations - self.iteration
                    metropolis = math.exp(-self.iteration / temperature)
                    test = random.uniform(0, 1)
                    if test < metropolis:
                        distance_from_balance = math.inf
                if distance_from_balance < criterion:
                    criterion = distance_from_balance
                    self.alterValue = assignment
        else:
            self.alterValue = self.assignment

    # PHASE 2 - Credits - from the options that are beneficial to him
    # choose the option that will least distance him from the balance
    def strategy_moral_licensing(self, indications):
        beneficial_to_me = self.beneficial_to_myself(indications)
        if beneficial_to_me:  # not empty
            criterion = math.inf
            for assignment in beneficial_to_me:
                distance_from_balance = abs(beneficial_to_me[assignment][1].item() + self.cumulative_environmental_impact)
                if assignment == self.assignment:
                    temperature = self.totalIterations - self.iteration
                    metropolis = math.exp(-self.iteration / temperature)
                    test = random.uniform(0, 1)
                    if test < metropolis:
                        distance_from_balance = math.inf
                if distance_from_balance < criterion:
                    criterion = distance_from_balance
                    self.alterValue = assignment
        else:
            self.alterValue = self.assignment

    def __str__(self):
        s = "Careful, utility: " + str(round(self.utility)) + ", EI: " + str(self.cumulative_environmental_impact) + \
            ", assignment: " + str(self.assignment)
        return s


# _______________________________________________________________________________________________________________
class GenerousAgent(MoralAgent):

    # PHASE 2 - Debits - from the neighbours’ preferences
    # Choose the option that is most beneficial for the society
    def strategy_moral_compensation(self, indications):
        neighbours_preferences = self.neighbours_preferences(indications)
        if neighbours_preferences:  # not empty
            criterion = -math.inf
            for assignment in neighbours_preferences:
                social_gain = neighbours_preferences[assignment][1].item()
                if social_gain > criterion:
                    criterion = social_gain
                    next_assignment = assignment
            self.alterValue = next_assignment
        else:
            self.alterValue = self.assignment

    # PHASE 2 - Credits - from the options that are beneficial to him
    # choose according to neighbours’ preferences
    def strategy_moral_licensing(self, indications):
        beneficial_to_me = self.beneficial_to_myself(indications)
        if beneficial_to_me:  # not empty
            # print(beneficial_to_me)
            criterion = -math.inf
            for assignment in beneficial_to_me:
                social_gain = beneficial_to_me[assignment][1].item()
                if social_gain > criterion:
                    criterion = social_gain
                    next_assignment = assignment
            self.alterValue = next_assignment
        else:
            self.alterValue = self.assignment

    def __str__(self):
        s = "Generous, utility: " + str(round(self.utility)) + ", EI: " + str(self.cumulative_environmental_impact) + \
            ", assignment: " + str(self.assignment)
        return s


# _______________________________________________________________________________________________________________
class SelfishAgent(MoralAgent):

    # PHASE 2 - Debits - if all neighbours_preferences bad - choose what best for myself
    def strategy_moral_compensation(self, indications):
        neighbours_preferences = self.neighbours_preferences(indications)
        if neighbours_preferences:  # not empty
            criterion = -math.inf
            for assignment in neighbours_preferences:
                my_gain = neighbours_preferences[assignment][0]
                if my_gain > criterion:
                    criterion = my_gain
                    next_assignment = assignment
            profitability = criterion - (self.totalIterations - self.iteration)
            if profitability > 0:
                self.alterValue = next_assignment
            elif (math.exp(profitability / (self.iteration + 10))) < random.uniform(0, 1):
                self.strategy_moral_licensing(indications)
            else:
                self.alterValue = next_assignment
        else:
            self.strategy_moral_licensing(indications)

    # PHASE 2 - Credits - Choose the option that is most beneficial to him
    def strategy_moral_licensing(self, indications):
        beneficial_to_me = self.beneficial_to_myself(indications)
        if beneficial_to_me:  # not empty
            criterion = -math.inf
            for assignment in beneficial_to_me:
                my_gain = beneficial_to_me[assignment][0]
                if my_gain > criterion:
                    criterion = my_gain
                    next_assignment = assignment
            self.alterValue = next_assignment
        else:
            self.alterValue = self.assignment

    def __str__(self):
        s = "Selfish, utility: " + str(round(self.utility)) + ", EI: " + str(self.cumulative_environmental_impact) + \
            ", assignment: " + str(self.assignment)
        return s


# _______________________________________________________________________________________________________________
class RandomAgent(MoralAgent):

    # PHASE 2 - Debits - Choose at random from the options that are beneficial for the society
    def strategy_moral_compensation(self, indications):
        neighbours_preferences = self.neighbours_preferences(indications)
        if neighbours_preferences:  # not empty
            next_assignment = random.choice(list(neighbours_preferences))
            self.alterValue = next_assignment
        else:
            self.alterValue = self.assignment

    # PHASE 2 - Credits - Choose at random from the options that are beneficial to him
    def strategy_moral_licensing(self, indications):
        beneficial_to_me = self.beneficial_to_myself(indications)
        if beneficial_to_me:  # not empty
            next_assignment = random.choice(list(beneficial_to_me))
            self.alterValue = next_assignment
        else:
            self.alterValue = self.assignment

    def __str__(self):
        s = "Random Agent, utility: " + str(round(self.utility)) + ", EI: " + str(self.cumulative_environmental_impact) + \
            ", assignment: " + str(self.assignment)
        return s


# _______________________________________________________________________________________________________________
class CalculatedAgent(MoralAgent):

    # PHASE 2 - Debits - calculate the weigh:
    # how much the assignment will bring me closer to balance and how much he will “pay” for it,
    # choose the with the highest social benefit and minimum harm to the utility
    def strategy_moral_compensation(self, indications):
        neighbours_preferences = self.neighbours_preferences(indications)
        if neighbours_preferences:  # not empty
            criterion = -math.inf
            for assignment in neighbours_preferences:
                social_gain = neighbours_preferences[assignment][1].item()
                my_gain = neighbours_preferences[assignment][0]
                cumulative_gain = social_gain + my_gain
                if cumulative_gain > criterion:
                    criterion = cumulative_gain
                    next_assignment = assignment
            self.alterValue = next_assignment
        else:
            self.alterValue = self.assignment

    # PHASE 2 - Credits - calculate the weigh:
    # how much the assignment will distance it from balance and how much he will gain from it,
    # choose the assignment with the highest benefit and minimum distance.
    def strategy_moral_licensing(self, indications):
        beneficial_to_me = self.beneficial_to_myself(indications)
        if beneficial_to_me:  # not empty
            criterion = -math.inf
            for assignment in beneficial_to_me:
                social_gain = beneficial_to_me[assignment][1].item()
                my_gain = beneficial_to_me[assignment][0]
                cumulative_gain = (0.5-(self.iteration/(2*self.totalIterations)))*social_gain + (0.5+(self.iteration/(2*self.totalIterations)))*my_gain
                if cumulative_gain > criterion:
                    criterion = cumulative_gain
                    next_assignment = assignment
            self.alterValue = next_assignment
        else:
            self.alterValue = self.assignment

    def __str__(self):
        s = "Calculated, utility: " + str(round(self.utility)) + ", EI: " + str(self.cumulative_environmental_impact) +\
            ", assignment: " + str(self.assignment)
        return s
