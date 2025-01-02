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




def calculate_data(dcops,amount_iterations,static_data,file_name):
    cumulative_measures = get_all_utils_per_measure(dcops,amount_iterations)
    #avg_measures = add_avg_per_agent(cumulative_measures)
    measures = {**cumulative_measures}#,**avg_measures}
    measures_avg_over_runs = get_average_over_runs(measures)
    measures_avg_over_runs_reformat = change_format_of_data(measures_avg_over_runs,amount_iterations)
    format_static_data = get_formatted_static_data(static_data,amount_iterations)
    ans_dict = {**format_static_data,**measures_avg_over_runs_reformat}
    df = pd.DataFrame(ans_dict)
    df.to_csv(file_name+".csv", index=False)
    return(df)


if __name__ == '__main__':


    amount_reps = 10#100
    amount_iterations = 10#1000
    numAgents = 50
    domainSize = 10
    densities = [0.2,0.7]
    environments = [AgentEnvironment.Egoistic]#list(AgentEnvironment)
    specials = [AgentSpecial.Altruist]#list(AgentSpecial)
    specials_amount = [1]

    # amount_of_agents_dict= {"Global Utility": numAgents,"Unique Agents Utility": None,"Environment Agents Utility": None,"Cumulative Environment Impact":None}
    for density in densities:
        for environment in environments:
            for special_agent_type in specials:
                for special_agent_amount in specials_amount:
                    print("density:",density,"_environment:",environment,"_special_agent_type:",special_agent_type)
                    dcops = create_dcops(amount_iterations,numAgents,domainSize,density,environment,special_agent_type,special_agent_amount)
                    for dcop in dcops:
                        dcop.agents_dict_by_role["Environment Agents Utility"] = dcop.connected_to_special_id_dict.values()
                        dcop.agents_dict_by_role["Environment Agents Utility Average"] = dcop.connected_to_special_id_dict.values()
                        dcop.initiate_dcop()
                    file_name = "SM_DCOP_"+str(density)+"_"+environment.name+"_"+special_agent_type.name+"_"+str(special_agent_amount)
                    static_data = {"Density": density, "Environment": environment.name,
                                   "Strategy Unique Agent": special_agent_type.name,"special agent amount":special_agent_amount }
                    df = calculate_data(dcops,amount_iterations,static_data,file_name,)
                    df.to_pickle(file_name+".pkl")





