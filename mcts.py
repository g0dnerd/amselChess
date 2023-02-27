import random
import math
import copy
import multiprocessing as mp
import numpy as np

import amsel_engine


class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.num_visits = 0
        self.total_score = 0
        self.move = None

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_valid_moves())

    def add_child(self, child_state):
        child_node = Node(child_state, self)
        self.children.append(child_node)
        return child_node

    def select_child(self):
        unexplored_children = [c for c in self.children if c.num_visits == 0]
        if unexplored_children:
            return random.choice(unexplored_children)
        else:
            return max(self.children, key=lambda c: c.total_score / c.num_visits + 1.4 * (
                    2 * math.log(self.num_visits) / c.num_visits) ** 0.5)

    def update(self, score):
        self.num_visits += 1
        self.total_score += score


def expand(node):
    # print('Expanding node')
    valid_moves = node.state.get_valid_moves()
    random.shuffle(valid_moves)
    for move in valid_moves:
        child_state = copy.deepcopy(node.state)
        child_state.make_move(move[0], move[1])
        child_node = node.add_child(child_state)
        child_node.move = move
        # print('Added child with move', move)
    return node


def backpropagation(node, score):
    while node is not None:
        if node.state.current_player == 'black':
            node.update(-score)
        else:
            node.update(score)
        # print('Updated node with moves', node.state.move_history, 'with score', score)
        node = node.parent


class Tree:
    MAX_DEPTH = 10
    MAX_SIMULATIONS = 50

    def __init__(self, state):
        self.num_simulations = 0
        self.root = Node(state)
        self.engine = amsel_engine.Engine()

    def select(self, node):
        print('Selecting node')
        max_ucb = float('-inf')
        selected_child = None
        for child in node.children:
            if child.num_visits == 0:
                return child
            else:
                ucb = child.total_score / child.num_visits + math.sqrt(
                    math.log(self.MAX_SIMULATIONS) / child.num_visits)
                if ucb > max_ucb:
                    max_ucb = ucb
                    selected_child = child
                    # print('Selected child:', selected_child.move)
        return self.select(selected_child)

    def simulation(self, node):
        print('')
        state = copy.deepcopy(node.state)
        depth = 0
        while not state.is_game_over() and depth < self.MAX_DEPTH:
            move = random.choice(state.get_valid_moves())
            # print('Randomly selected move:', move)
            state.make_move(move[0], move[1])
            depth += 1
        if state.is_game_over():
            if state.is_checkmate():
                if state.game_result == '1-0':
                    return 1
                else:
                    return 0
            else:
                # print('returning 0.5')
                return 0.5
        evaluation = self.engine.evaluate_position(state) / 100
        # print('returning', evaluation, 'after moves', state.move_history)
        return evaluation

    def find_best_move(self):
        print('')
        for _ in range(self.MAX_SIMULATIONS):
            # printout = 'Running random simulation at depth ' + str(depth + 1)
            # print(printout, end='\r')
            printout = 'Running simulation ' + str(_ + 1)
            print(printout, end='\r')
            node = self.root
            state = copy.deepcopy(node.state)

            while not node.is_fully_expanded() and node.children:
                # print('Selecting child node')
                node = node.select_child()
                state.make_move(node.move[0], node.move[1])

            if not node.is_fully_expanded():
                # print('simulating not fully expanded node')
                expand(node)
                score = self.simulation(node)
            else:
                # print('simulating fully expanded node')
                score = self.simulation(node)

            while node is not None:
                backpropagation(node, score)
                node = node.parent

            # self.num_simulations += 1

        max_visits = float('-inf')
        best_node = None
        for child in self.root.children:
            if child.num_visits > max_visits:
                max_visits = child.num_visits
                best_node = child

        return best_node.move