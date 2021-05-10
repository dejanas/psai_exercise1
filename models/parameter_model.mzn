include "disjunctive.mzn";
include "redefinitions.mzn";
include "cumulative.mzn";

0..1: full_output;

% ------------------------------------- PARAMETERS -------------------------------------%

int: nActs; % total number of activities (N) including source and sink
int: nSkills; % total number of skills (K)
int: nResources; % total number of resources (M)
int: nPrecs; % total number of precedence relations between two activities

set of int: ACT = 1..nActs;
set of int: SKILL = 1..nSkills;
set of int: RESOURCE = 1..nResources;
set of int: PREC = 1..nPrecs;

array[ACT] of int: dur; % duration of each activity
array[ACT,SKILL] of int: sreq; % required resources of each skill for each activity
array[RESOURCE,SKILL] of bool: mastery; % skills mastered by each resource
array[PREC] of ACT: pred; % predecessor activity of the corresponding precedence relation
array[PREC] of ACT: succ; % successor activity of the corresponding precedence relation

% ------------------------------------- REDUNDANT PARAMETERS -------------------------------------%

int: mint;  % minumum makespan
int: maxt;  % maximum makespan
int: nUnrels; % number of unrelated activites wrt to the precedence graph

set of int: UNREL = 1..nUnrels;
set of int: TIME = 0..maxt;

array[UNREL] of ACT: unpred; % unrelated predecessor activity
array[UNREL] of ACT: unsucc; % unrelated successor activity

array[ACT] of set of RESOURCE: USEFUL_RES; % set of resources that are useful per activity
array[RESOURCE] of set of ACT: POTENTIAL_ACT; % set of activities that the resource may be assigned to

array[SKILL] of 0..nResources: skill_capacity = [sum(r in RESOURCE)(bool2int(mastery[r,s])) | s in SKILL]; % capacity for each skill


% ------------------------------------- DECISION VARIABLES -------------------------------------%

array[ACT] of var TIME: start; % start time of activity
array[UNREL] of var bool: overlap; %  unrelated activities overlapping
array[ACT, RESOURCE] of var bool: assign; % assignment of resources to activities
array[ACT, RESOURCE, SKILL] of var bool: contrib; % contribution

var TIME: makespan = start[nActs];  % makespan

% ------------------------------------- CONSTRAINTS -------------------------------------%


% Precedence relation constraint (2)
constraint forall(p in PREC)(
    start[pred[p]] + dur[pred[p]] <= start[succ[p]]
);

% Skill requirements constraint (3)
constraint forall(a in ACT, s in SKILL where sreq[a,s]>0)(
  sum(r in USEFUL_RES[a])(contrib[a,r,s]) == sreq[a,s]
);


% Skill possesment constraint (4)
constraint forall(a in ACT, r in USEFUL_RES[a], s in SKILL)(
  contrib[a,r,s] <= bool2int(mastery[r,s])
);

% Resource non-overlapping constraint (5)
constraint
  forall ( 
    u in UNREL
  )(
  let {int: i = unpred[u],
       int: j = unsucc[u]} in
        if exists( s in SKILL )( sreq[i,s] + sreq[j,s] > skill_capacity[s] ) then
             (     overlap[u]  -> start[i] + dur[i] <= start[j] ) /\
             ( not(overlap[u]) -> start[j] + dur[j] <= start[i] )
        else
            (
              not(overlap[u]) <-> (start[i] + dur[i] <= start[j] \/
                                   start[j] + dur[j] <= start[i])
            ) /\ (
              forall(
                r in USEFUL_RES[i] intersect USEFUL_RES[j]
              )(
                (assign[i,r] /\ assign[j,r]) -> not(overlap[u])
              )
            )
        endif
  );

% Max one contribution per activity constraint
constraint forall(a in ACT, r in USEFUL_RES[a])(
  sum(s in SKILL where mastery[r,s]==true /\ sreq[a,s]>0)
     (contrib[a,r,s]) <= 1
);

% Resources contribute only to their assigned activities
constraint forall(a in ACT, r in USEFUL_RES[a], s in SKILL where sreq[a,s]>0) (
  contrib[a,r,s] <= bool2int(assign[a,r])
);

% ------------------------------------- SEARCH STRATEGIES -------------------------------------%

ann: start_search = int_search(start, first_fail, indomain_min, complete);
% ann: assign_search = bool_search([ assign[a,r] | a in ACT, r in RESOURCE ],
                          %  input_order, indomain_max, complete);
% ann: contrib_search = bool_search([ contrib[a,r,s] 
%                            | a in ACT, r in RESOURCE, s in SKILL ],
%                            input_order, indomain_max, complete);

ann: search_strategy = start_search;


% ------------------------------------- SOLVE -------------------------------------%

solve :: search_strategy
minimize makespan;

% --------------------------------- OUTPUT RESULTS ---------------------------------%

output
if full_output == 0 then    
  ["makespan = " ++ show(makespan) ++ "\n"]
elseif full_output == 1 then
  ["makespan = " ++ show(makespan) ++ "\n"] ++
  ["start times = " ++ show(start) ++ "\n"] ++
  ["assignment = " ++ show(assign) ++ "\n"] ++
  ["contribution = " ++ show(contrib) ++ "\n"] 
else
  [""]
endif
;

