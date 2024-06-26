from Problems import DCOP
from enums import *







def create_dcops(numAgents,domainSize,density,environment,special_agent_type,special_agent_amount):
    for dcop_id in range(1,amount_reps+1):
        dcop = DCOP(dcop_id,numAgents,domainSize,density,environment,special_agent_type,special_agent_amount)


if __name__ == '__main__':
    amount_reps = 100
    numAgents = 50
    domainSize = 10
    densities = [0.2, 0.7]
    environments = list(AgentEnvironment)
    specials = list(AgentSpecial)
    specials_amount = [1, 2, 10]

    for density in densities:
        for environment in environments:
            for special_agent_type in specials:
                for special_agent_amount in specials_amount:
                    dcops = create_dcops(numAgents,domainSize,density,environment,special_agent_type,special_agent_amount)



    # run_simulations_sm_environment(amount_reps)
    # run_simulations_altru_environment(amount_reps)
    #run_simulations_ego_environment(amount_reps)