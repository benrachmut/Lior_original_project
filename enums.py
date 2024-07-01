from enum import Enum


class AgentEnvironment(Enum):
    PC = 1
    Altruistic = 2
    Egoistic = 3

class AgentSpecial(Enum):
    Egoist = 1
    Altruist = 2
    Simple = 3
    Careful = 4
    Generous = 5
    Selfish = 6
    Random = 7