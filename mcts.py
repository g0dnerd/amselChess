import amsel_engine
import math
import numpy as np
import random
import copy


def backpropagation(node, score):
    # Update the scores of all nodes in the path from the given node to the root
    while node is not None:
        # print("Backpropagating for node of type", type(node))
        node.score += score
        node.visits += 1
        node = node.parent


def expansion(node, game):
    # Expand the node by generating all possible moves and creating a new child node for each one.
    legal_moves = game.get_valid_moves()
    for move in legal_moves:
        new_game = copy.deepcopy(game)
        new_game.make_move(move[0], move[1])
        # print("Creating new node after move", move[0], "to", move[1], "with current player", new_game.current_player)
        new_node = Node(node, move, new_game)
        node.children.append(new_node)


class Node:
    def __init__(self, parent=None, move=None, game=None):
        self.game = game
        self.move = move
        self.engine = amsel_engine.Engine(self.game)
        self.parent = parent
        self.children = []
        self.visits = 0
        self.score = 0.0

    def add_child(self, child_game):
        child_node = Node(self, None, child_game)
        self.children.append(child_node)
        return child_node

    def update(self, score):
        self.visits += 1
        self.score += score

    def fully_expanded(self):
        return len(self.children) == len(self.engine.get_legal_moves())

    def best_child(self, exploration_value):
        choices_weights = [(c.score / c.visits) +
                           exploration_value * math.sqrt((2 * math.log(self.visits) / c.visits))
                           for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def select_child(self, exploration_value):
        # Check that all children are expanded.
        assert all(node.fully_expanded() for node in self.children)

        # Use the UCB1 formula to select a child node.
        log_total = math.log(self.visits)

        def ucb1(node):
            return node.score / node.visits + exploration_value * math.sqrt(log_total / node.visits)

        return max(self.children, key=ucb1)


class Tree:
    def __init__(self, game, max_depth=25):
        self.game = game
        self.root = Node(None, None, self.game)
        self.MAX_DEPTH = max_depth
        self.num_simulations = 100
        self.engine = amsel_engine.Engine(game)

        expansion(self.root, self.game)

    def selection(self, node):
        # Find the child node with the highest UCB1 score.
        # print("Got passed a node with ", len(node.children), " children.")
        max_ucb = float('-inf')
        selected_child = None
        for child in node.children:
            if child.visits == 0:
                # If a child hasn't been explored yet, select it
                return child
            else:
                # Calculate the UCB1 score for the child node.
                ucb = child.score / child.visits + math.sqrt(
                    2 * math.log(node.visits) / child.visits)
                if ucb > max_ucb:
                    max_ucb = ucb
                    selected_child = child
        return self.selection(selected_child)

    def simulation(self, node):
        # Select a random unexplored child node and evaluate its position.
        while node.children:
            unexplored_children = [child for child in node.children if child.visits == 0]
            if unexplored_children:
                child = random.choice(unexplored_children)
                return self.evaluate(child.game)
            else:
                # Select a child node using the UCB1 formula.
                node = self.selection(node)

                if node.depth == self.MAX_DEPTH:
                    return self.evaluate(node.game)

        # If all child nodes have been explored, simulate a random game
        return self.evaluate(node.game)

    def evaluate(self, game):
        # Evaluate the position using the evaluate_position method of the engine
        score = self.engine.evaluate_position(game)
        # Scale the score to be between -1 and 1
        return score / 100.0

    def find_best_move(self):
        for i in range(self.num_simulations):
            print("Running simulation", i)
            # Select a node to explore
            node = self.selection(self.root)
            # Expand the node
            expansion(node, node.game)
            reward = self.simulation(node)
            backpropagation(node, reward)

        # Select the best child of the root node
        best_node = self.root.children[0]
        for child in self.root.children[1:]:
            if child.visits > best_node.visits:
                best_node = child

        print("Best move is", best_node.move, "with score", best_node.score, "and visits", best_node.visits)
        return best_node.move

