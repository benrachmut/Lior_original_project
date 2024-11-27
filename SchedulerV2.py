from Problems import DCOP
from enums import *
from data_functions import *
import pandas as pd







def create_dcops(amount_iterations,numAgents,domainSize,density,environment,special_agent_type,special_agent_amount):
    ans = []
    for dcop_id in range(1,amount_reps+1):
        dcop = DCOP(dcop_id,numAgents,domainSize,density,environment,special_agent_type,special_agent_amount,amount_iterations)
        dcop.create_neighbors()
        dcop.create_special_agent_neighbor_list()
        ans.append(dcop)

    return ans




def calculate_data(dcops,amount_iterations,amount_of_agents_dict,static_data,file_name):
    cumulative_measures = get_all_utils_per_measure(dcops,amount_iterations)
    avg_measures = add_avg_per_agent(cumulative_measures,amount_of_agents_dict)
    measures = {**cumulative_measures,**avg_measures}
    measures_avg_over_runs = get_average_over_runs(measures)
    measures_avg_over_runs_reformat = change_format_of_data(measures_avg_over_runs,amount_iterations)
    format_static_data = get_formatted_static_data(static_data,amount_iterations)
    ans_dict = {**format_static_data,**measures_avg_over_runs_reformat}
    df = pd.DataFrame(ans_dict)
    df.to_csv(file_name+".csv", index=False)
    return(df)


if __name__ == '__main__':


    amount_reps = 5
    amount_iterations = 1000
    numAgents = 50
    domainSize = 10
    densities = [0.2,0.7]
    environments = list(AgentEnvironment)
    specials = list(AgentSpecial)
    specials_amount = [1]

    amount_of_agents_dict = {"Global Utility": numAgents,
                             "Unique Agents Utility": None,
                             "Environment Agents Utility": None, # change only to the special agent neighbor
                             "Cumulative Environment Impact":None} # I calculate to my self how much did i harm to
    for density in densities:
        for environment in environments:
            for special_agent_type in specials:
                for special_agent_amount in specials_amount:
                    amount_of_agents_dict["Unique Agents Utility"]=special_agent_amount #
                    amount_of_agents_dict["Cumulative Environment Impact"] = special_agent_amount
                    dcops = create_dcops(amount_iterations,numAgents,domainSize,density,environment,special_agent_type,special_agent_amount)
                    for dcop in dcops:
                        dcop.agents_dict_by_role["Environment Agents Utility"] = dcop.connected_to_special_id_dict.values()
                        dcop.initiate_dcop()
                    file_name = "SM_DCOP_"+str(density)+"_"+environment.name+"_"+special_agent_type.name+"_"+str(special_agent_amount)
                    static_data = {"Density": density, "Environment": environment.name,
                                   "Strategy Unique Agent": special_agent_type.name,"special agent amount":special_agent_amount }
                    df = calculate_data(dcops,amount_iterations,amount_of_agents_dict,static_data,file_name,)
                    df.to_pickle(file_name+".pkl")





