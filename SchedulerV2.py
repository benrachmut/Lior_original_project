from enums import *


amount_reps = 100
numAgents = 50
domainSize = 10
connectivity = [0.2,0.7]
environments = list(AgentEnvironment)
specials = list(AgentSpecial)
specials_amount = [1,2,10]




if __name__ == '__main__':


    # run_simulations_sm_environment(amount_reps)
    # run_simulations_altru_environment(amount_reps)
    run_simulations_ego_environment(amount_reps)