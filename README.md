# Multi-Skill Project Scheduling Problem (MSPSP)

The goal of the Multi-Skill Project Scheduling Problem (MSPSP) is to schedule the number of activities given  Ai , i ∈ {0, . . . , N} by satisfying following constraints:

  1. Each activity has a fixed duration pi and cannot be interrupted once when started
  1. Given precedence relations in format (Ai, Aj) signify that activity Aj can start only when Ai has finished.
  3. Each activity requires a certain amount of resources which must have certain skills Sk, k ∈ {1, . . . , K}. The set of available resources is Rm, m ∈ {1, . . . , M} and each      resource may possess one or several of the skills
  
  4. Resources can only be assigned to use skills that they possess
  5. No resource can work on more than one activity at the same time

A schedule consists of an assignment of starting times to each activity as well as a number of resources using a certain skill such that the total demand of the activity is met. The goal of MSPSP is to find a schedule with minimal makespan, i.e. one where the end of activity An is as early as possible
