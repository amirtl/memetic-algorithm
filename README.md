# memetic-algorithm
Solving TSP with memetic algorithm.
# explanation
- the TSP problem with memetic algorithm is similar with genetic algorithm but with a local search.
- in my code (TSP-memetic.py) i solve the problem with berlin59 dataset.
# executation
run with python 3.
# algorithm
- Individual: We put each person in the society in a permutation from 1 to the number of cities, the first and last of which is zero. (Starts from city zero and returns to city zero.).
- Initial population: Like a genetic algorithm, the number of first population is randomly generated.
- Recombination: In each generation with a probability of two people, a child is produced, which is the recombination method of tow points.
- Mutation: occurs with a probability on the offspring in each generation and moves with the offspring. The mutation is performed as follows:
From the index "i" through "j" are all reversed.
- Local search: In each generation, it goes to all the people in all the neighborhoods and exchanges the best with a possible one with the original person. 
- Neighborhood: Both people who are different in only two cities are considered neighbors: 
That is, he put only the "i" index of the first  in the "j" index og the second  and vice versa.
- New generation selection: In each generation, N% of the top are selected.
- End of algorithm: After en point load does not change the best fit stops.
