from enum import Enum


class AgentEnvironment(Enum):
    socially_motivated = 1
    altruist = 2
    egoist = 3

class AgentSpecial(Enum):
    egoist = 1
    altruist = 2
    simple = 3
    careful = 4
    generous = 5
    selfish = 6
    random = 7