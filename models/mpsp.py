"""Multi-Skill Project Scheduling Problem - CP model""" 

model="mspsp-07"
TIMELIMIT=600
NumInstances=6

SFList=[ 1 , 0.75, 0.5, 0 ]
NCList=[ 1.5, 1.8, 2.1 ]

setList= ['set-a', 'set-b']

SearchList=['start_s', 'assign_s', 'contrib_s']

def getSearchAbbreviation(search) :
    if search == 'start_s':
        return 's'
    elif search == 'assign_s':
        return 'as'
    elif search == 'contrib_s':
        return 'cs'

def main(): 
    print('****************************************MPSP****************************************')
    for setName in setList:
        # define number of activities based on the set number
        if setName == 'set-a':
            n=22
        elif setName == 'set-b':
            n=42

        # iterate over all specified search strategies
        for search in SearchList:
            # store abbreviation of search strategy for output files
            searchAbrv = getSearchAbbreviation(search)

            # iterate over skill factor values
            for SF in SFList:
                # calculate m array
                if n == 22:
                    if SF == 1:
                        mList=[20, 25, 30]
                    elif SF == 0.75:
                        mList=[10, 20, 25]
                    elif SF == 0.5:
                        mList=[10, 13, 15]
                    else:
                        mList=[10, 20, 25]
                elif n == 40:
                    if SF == 1:
                        mList=[40, 50, 60]
                    elif SF == 0.75:
                        mList=[30, 38, 45]
                    elif SF == 0.5:
                        mList=[20, 25, 30]
                    else:
                        mList=[30, 38, 45]

                # iterate over network complexity values
                for NC in NCList:
                    # iterate over the correct resource values
                    for m in mList:
                        # solve all instances with the given parameters
                        
                        # ./solve_instance_CP.sh $SetNum $SF $NC $n $m $search $model $TIMELIMIT $NumInstances $useTightUB $debugging

                        # print the number of instances where optimality was found
                        # results="./results/results_set${setName}_sf${SF}_nc${NC}_n${n}_m${m}_${searchAbrv}.txt"
                        # awk -F"," '{x+=$2}END{printf "-> " x}' "$results"
                        # printf "/%s optimal\n\n" ${NumInstances}
                        results = "./results/results_set{}_sf{}_nc{}_n{}_m{}_{}.txt".format(setName, SF, NC, n, m, searchAbrv)
                        print('Saved results in:', results)
                        
 
if __name__ == "__main__": 
	main() 