# Minizinc parameters
fulloutput="1" # whether to store full output

useActSearch=0


# print current parameter details
printf '%s\n' " set |  # |   SF |   NC |   n |   m | search |    model | timeLimit | use UB"
printf '%s\n' "-----|----|------|------|-----|-----|--------|----------|-----------|--------"
printf " %3s | %2d | %4s | %4s | %3d | %3d | %6s | %8s | %9d | %d\n" "${SetNum}" ${NumInstances} "${SF}" "${NC}" ${n} ${m} "${searchAbrv}" "${model}" ${TIMELIMIT} ${useTightUB}


# define destinations for the output files
RESULTS="./results/results_set${SetNum}_sf${SF}_nc${NC}_n${n}_m${m}_$searchAbrv.txt"
STATS="./stats/stats_set${SetNum}_sf${SF}_nc${NC}_n${n}_m${m}_$searchAbrv.txt"

if [ $SetNum -eq 1 ]; then
	FIRSTSOLS="./firstSols-Set1/firstSols_best.txt"
elif [ $SetNum -eq 2 ]; then
	FIRSTSOLS="./firstSols-Set2/firstSols_best.txt"
elif [ $SetNum -eq 3 ]; then
	FIRSTSOLS="./firstSols-French-Group-1/firstSols_best.txt"
fi

# clear the files if they already exist
printf '' > "$RESULTS"
printf '' > "$STATS"

# create the first sols file if it doesnt exist
touch "${FIRSTSOLS}"

# Get all instances
# INSTANCES="$(find $SOURCE -name "inst_set${SetNum}_nc${NC}_sf${SF}_n${n}_m${m}*dzn" | sort)"
INSTANCES="$(find -name "inst_set${SetNum}_sf${SF}_nc${NC}_n${n}_m${m}*dzn" | sort)"
instNum=0	# initilise instance counter

for inst in $INSTANCES
do
	# create and clear full-output file
	FULLOUTPUT="./full-output/full-output_set${SetNum}_sf${SF}_nc${NC}_n${n}_m${m}_${searchAbrv}_0${instNum}.txt"
	printf '' > "$FULLOUTPUT"

	# only test 3 instances for each case
	if [ $instNum -ge $NumInstances ]; then
		break
	else
		true
	fi

	tmp="${inst%.dzn}"
	if [ $SetNum -eq 1 ]; then
		instPath="${tmp#*/Portuguese-Set1-mine/}"
	elif [ $SetNum -eq 2 ]; then
		instPath="${tmp#*/Portuguese-Set2-mine/}"
	elif [ $SetNum -eq 3 ]; then
		instPath="${tmp#*/French-Group-1/}"
	else
		true
	fi
	instName=${instPath##*/}

	# retrieve the new UB if we are using it, otherwise use naive UB
	if [ $useTightUB -eq 1 ]; then
		maxt=$(cat $FIRSTSOLS | grep "$inst" | awk '{a=$2;} END {print a;}')
	else
		maxt="sum(d in dur)(d)"
	fi

	# flatten the instance to fzn and send it to chuffed
	mzn2fzn -Gchuffed -D "my_search = $search; full_output = $fulloutput; maxt = $maxt;" $model.mzn $inst
	./fzn-chuffed $model.fzn --time-out "$TIMELIMIT" -a -f --verbosity 2 2> stats.txt | solns2out --output-time -o sol.txt $model.ozn

	fewStats=$(cat stats.txt | grep -v '%' | grep -v 'number of conflicts' | grep -v 'SAT' | grep -E 'propagations|nodes' | sort -k2 | cut -d' ' -f1 | tr '\n' ',')
	fewStats=${fewStats%,}
	stats=$(cat stats.txt | grep -v '%' | grep -v 'number of conflicts' | grep -E 'prop|nodes|sol|seconds|SAT|learnt|restart' | sort -k2 | cut -d' ' -f1 | tr '\n' ',')
	stats=${stats%,}
	statsNames=$(cat stats.txt | grep -v '%' | grep -v 'number of conflicts' | grep -E 'prop|nodes|sol|seconds|SAT|learnt|restart' | sort -k2 | sed -r 's/[0-9.]+ //' | sed -r 's/\(.*\)//' | tr '\n' ',')
	statsNames=${statsNames%,}


	if grep -q "makespan" sol.txt; then
		makespan_CP=$(grep "makespan" sol.txt | awk '{a=$3;} END {print a;}')

		if grep -q "==========" sol.txt; then
			status="Optimal"
			# runtime_CP=$(cut stats.txt -d, -f10 | tr -d '\n')
			runtime_CP=$(grep "search time" stats.txt | awk '{a=$1;} END {print a;}')
		else
			status="Suboptimal"
			runtime_CP="$TIMELIMIT"
		fi
	else
		makespan_CP="None"
		status="No_sol_found"
		runtime_CP="$TIMELIMIT"
	fi
	if [ $debugging -eq 1 ]; then
		echo "CP Makespan: $makespan_CP"
	else
		true
	fi
	
	firstSol=$(grep "makespan" sol.txt | head -1 | awk '{a=$3;} END {print a;}')
	timeToFirstSol=$(grep "time elapsed" sol.txt | head -1 | awk '{a=$4;} END {print a;}')

	# if using naive UB then rewrite first solution to firstSols.txt
	if [ $useTightUB -eq 0 ]; then
		# replace the previous value
		sed -i 's,'"${inst}"'.*,'"${inst}"' '"${firstSol}"',w changelog.txt' "$FIRSTSOLS"
		# if we havent processed this instance yet, append its value
		if [ -s changelog.txt ]; then
			true
		else
			printf '%s %s\n' "${inst}" "${firstSol}" >> "$FIRSTSOLS"
		fi
	else
		true
	fi

	# retrieve UB value
	UB=$(grep "maxt" ${inst} | awk '{a=$4;} END {print a;}')
	UB=${UB%;} # get rid of ";"

	LB=$(grep "mint" ${inst} | awk '{a=$3;} END {print a;}')
	LB=${LB%;} # get rid of ";"


	if [ $instNum -eq 0 ]; then
		printf 'instNum,optimal,LB,makespan,firstSol,UB,timeToFirstSol,runtime,nodes,propagations\n' >> "$RESULTS"
		printf 'optimal,search strategy,%s\n' "${statsNames}" >> "$STATS"
	else
		true
	fi

	# append results to results file
	if [ "$status" == "Optimal" ]; then
		printf '%s,1' "${instNum}" >> "$RESULTS"
	else
		printf '%s,0' "${instNum}" >> "$RESULTS"
	fi
	printf ',%s,%s,%s,%s,%s,%s,%s\n' "${LB}" "${makespan_CP}" "${firstSol}" "${UB}" "${timeToFirstSol}" "${runtime_CP}" "${fewStats}" >> "$RESULTS"

	# append stats to stats file
	if [ "$status" == "Optimal" ]; then
		printf '1,%s,%s\n' "${searchAbrv}" "${stats}" >> "$STATS"
	else
		printf '0,%s,%s\n' "${searchAbrv}" "${stats}" >> "$STATS"
	fi

	# store full output
	printf '%s\n\n%s' "$(cat sol.txt)" "$(cat stats.txt | grep -v 'number of conflicts' | grep -v '% Pruned')" >> "$FULLOUTPUT"

	if [ $debugging -eq 1 ]; then
		echo ""
	else
		if [ "${status}" == "Optimal" ]; then
			printf "1"
		else
			printf "0"
		fi
	fi
	instNum=$((instNum+1))

done