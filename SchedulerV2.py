from Problems import DCOP
from enums import *







def create_dcops(amount_iterations,numAgents,domainSize,density,environment,special_agent_type,special_agent_amount):
    ans = []
    for dcop_id in range(1,amount_reps+1):
        dcop = DCOP(dcop_id,numAgents,domainSize,density,environment,special_agent_type,special_agent_amount,amount_iterations)
        dcop.create_neighbors()
        ans.append(dcop)
    return ans


def calculate_data(dcops,amount_iterations):
    all_iterations = {}
    for k in dcops[0].data.keys():
        all_iterations[k] = {}
        for i in range(amount_iterations):
            all_iterations[k][i] = []

    for dcop in dcops:
        for k,v in dcop.data.items():
            for iteration,util in v.items():
                all_iterations[k][iteration].append(util)





if __name__ == '__main__':
    amount_reps = 2
    amount_iterations =100
    numAgents = 50
    domainSize = 10
    densities = [ 0.2]
    environments = list(AgentEnvironment)
    specials = list(AgentSpecial)
    specials_amount = [1]

    for density in densities:
        for environment in environments:
            for special_agent_type in specials:
                for special_agent_amount in specials_amount:
                    dcops = create_dcops(amount_iterations,numAgents,domainSize,density,environment,special_agent_type,special_agent_amount)
                    for dcop in dcops:
                        dcop.initiate_dcop()
                    #static_data = {"density":density,"environment":environment.name,"special agent type":special_agent_type.name}
                    calculate_data(dcops,amount_iterations)


