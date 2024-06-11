# Blackjack MonteCarlo
 

# Solving Blackjack with Monte Carlo methods
This project is an implementation of the algorithm provided in the book ***Reinforcement Learning An Introduction by Barto and Sutton, Example 5.3.*** 

The algorithm uses policy iteration to average the returns for all state action pairs to find the best move given a state of blackjack described by:

- The two cards the agent is holding
- The card that the dealer is holding
- Whether the agent has an ace in hand

## Installation
1. Clone the repository
2. Make sure numpy is installed
3. Run the file. *While in the cloned project's directory, paste this command into the terminal `python BlackjackMC.py`* :thumbsup:

## Notes
Currently, the agent is training on 5 million episodes which does *almost* a perfect job at finding the optimal policy. I believe that by increasing the number of episodes, the alorgorithm **will** converge to the optimal policy show below.
![Optimal policy for blackjack](../Images/blackjackOptimalPolicy.PNG)
If you wish to train the agent on more episodes, simply change the #episodes in `findOptimalPolicy(#episodes)`  located at the end of the code :smile: