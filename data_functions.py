import math


def get_all_utils_per_measure(dcops,amount_iterations):
    ans = {}
    for k in dcops[0].data.keys():
        ans[k] = {}
        for i in range(amount_iterations):
            ans[k][i] = []

    for dcop in dcops:
        for k, v in dcop.data.items():
            for iteration, util in v.items():
                ans[k][iteration].append(util)
    return ans


def add_avg_per_agent(cumulative_measures, ):
    ans = {}
    for k,v in cumulative_measures.items():
        #amount_of_agent = amount_of_agents_dict[k]
        new_key_name = "Average Per Agent "+ k
        ans[new_key_name] = {}
        for iteration, list_of_utils in v.items():
            list_of_avgs = []
            for util in list_of_utils:
                print()
                #if amount_of_agent !=0:
                #    list_of_avgs.append(util/amount_of_agent)
                #else:
                #    list_of_avgs.append(0)

            ans[new_key_name][iteration] = list_of_avgs
    return ans


def get_average_over_runs(measures):
    ans = {}
    for measure_name,utils_per_iterations_dict in measures.items():
        ans[measure_name]={}
        ans[measure_name+"_std"] = {}
        ans[measure_name+"_variance"] = {}

        for iteration, to_use_in_mean in utils_per_iterations_dict.items():
            mean_ = sum(to_use_in_mean) / len(to_use_in_mean)
            ans[measure_name][iteration] = mean_
            variance = sum((x - mean_) ** 2 for x in to_use_in_mean) / len(to_use_in_mean)  # Calculate variance
            ans[measure_name + "_variance"][iteration] = variance

            ans[measure_name+"_std"][iteration] = math.sqrt(variance)



            #    ans[measure_name][iteration] = 0

    return ans

def change_format_of_data(measures_avg_over_runs,amount_iterations):

    ans = {"iteration":[]}

    for iteration in range(amount_iterations):
        ans["iteration"].append(iteration)

    for measure_name in measures_avg_over_runs.keys():
        ans[measure_name] = [None] * amount_iterations

    for measure_name, dict_ in measures_avg_over_runs.items():
        for iteration, measure_value in dict_.items():
            ans[measure_name][iteration] = measure_value

    return ans

def get_formatted_static_data(static_data,amount_iterations):
    ans = {}
    for k, v in static_data.items():
        ans[k]=[]
        for _ in range(amount_iterations):
            ans[k].append(v)
    return ans





