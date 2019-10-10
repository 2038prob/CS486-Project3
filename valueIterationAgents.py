# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates(): list of all states in the MDP
              mdp.getPossibleActions(state): list of possible actions from 'state'
              mdp.getTransitionStatesAndProbs(state, action): list of (nextState, prob) pairs
              mdp.getReward(state, action, nextState): reward for the state, action, nextState transition
              mdp.isTerminal(state): true if the current state is a terminal state
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        states = mdp.getStates()
        actionVal = 0
        while iterations != 0:
            for state in states:
                stateVal = []
                actions = mdp.getPossibleActions(state)
                for action in actions:
                    transitions = mdp.getTransitionStatesAndProbs(state, action)
                    for nextState, prob in transistions:
                        actionVal += prob*(mdp.getReward(state, action, nextState)+discount*self.values[state])
                    stateVal.append(actionVal)
                    actionVal = 0
                if len(stateVal) == 0:
                    return None
                else:
                    self.values[state] = max(stateVal)
            iterations -= 1

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        actionVal = []
        transitions = self.mdp.getTransitionStatesAndProbs(state, action)
        for nextState, prob in transitions:
            actionVal.append(prob*(self.mdp.getReward(state, action, nextState)+self.discount*self.values[state]))
        return sum(actionVal)
        #util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        val = -1000
        if self.values[state] == 0:
            return None
        else:
            actions = self.mdp.getPossibleActions(state)
            for action in actions:
                actionVal = computeQValueFromValues(state, action)
                if actionVal > val:
                    val = actionVal
                    bestAction = action
        return bestAction
        #util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
