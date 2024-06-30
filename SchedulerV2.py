from Problems import DCOP
from enums import *







def create_dcops(amount_iterations,numAgents,domainSize,density,environment,special_agent_type,special_agent_amount):
    ans = []
    for dcop_id in range(1,amount_reps+1):
        dcop = DCOP(dcop_id,numAgents,domainSize,density,environment,special_agent_type,special_agent_amount,amount_iterations)
        dcop.create_neighbors()
        ans.append(dcop)
    return ans

if __name__ == '__main__':
    amount_reps = 2
    amount_iterations =1000
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



    # run_simulations_sm_environment(amount_reps)
    # run_simulations_altru_environment(amount_reps)
    #run_simulations_ego_environment(amount_reps)