from stockfish import Stockfish
import chess.pgn

import random

def describe_move(classification, best_move, current_move, accuracy):
    descriptions = {
        'blunder': [
            f'The move {current_move} could be improved.',
            f'{current_move} was not the optimal choice.',
            f'There were better alternatives to {current_move}.'
        ],
        'mistake': [
            f'{current_move} was a bit off mark.',
            f'The move {current_move} was a misstep.',
            f'There were better moves than {current_move}.'
        ],
        'miss': [
            f'{current_move} missed a better opportunity.',
            f'The move {current_move} overlooked a better play.',
            f'{current_move} was not the best option.'
        ],
        'good': [
            f'{current_move} was a solid move.',
            f'The move {current_move} was good.',
            f'{current_move} maintained a strong position.'
        ],
        'excellent': [
            f'{current_move} was excellent.',
            f'Excellent move with {current_move}.',
            f'{current_move} was a great choice.'
        ],
        'best': [
            f'{current_move} was the best move.',
            f'Best move with {current_move}.',
            f'{current_move} was optimal.'
        ]
    }
    description = random.choice(descriptions.get(classification, ['']))
    # return description + f' Accuracy: {min(accuracy, 1) * 100:.2f}%.'
    return description

# Example usage:
# print(describe_move('blunder', 'e2e4', 0.75))


def classify_move(score):
    if score > 900:
        return 'blunder'
    elif score > 400:
        return 'mistake'
    elif score > 150:
        return 'miss'
    elif score > 50:
        return 'good'
    elif score > 20:
        return 'excellent'
    else:
        return 'best'

# def describe_move(classification, best_move, current_move, accuracy):
#     descriptions = {
#         'blunder': f'The best move was {best_move} but the played move was {current_move}.',
#         'mistake': f'The best move was {best_move} but the played move was {current_move}.',
#         'miss': f'The best move was {best_move} but the played move was {current_move}.',
#         'good': 'A good move maintains or improves the position.',
#         'excellent': 'An excellent move gives a significant advantage.',
#         'best': 'The best move is the optimal move in the current position.'
#     }
#     return descriptions.get(classification, '') + f' The accuracy of the move is {min(accuracy, 1) * 100:.2f}%.'

def classify_moves(pgn_file, stockfish_path):
    stockfish = Stockfish(stockfish_path)
    
    with open(pgn_file) as pgn:
        game = chess.pgn.read_game(pgn)
        
    board = game.board()
    moves_made = []
    total_accuracy = {'white': 0, 'black': 0}
    total_moves = {'white': 0, 'black': 0}
    stages = ['opening', 'midgame', 'endgame']
    total_accuracy_stages = {stage: {'white': 0, 'black': 0} for stage in stages}
    total_moves_stages = {stage: {'white': 0, 'black': 0} for stage in stages}

    for i, move in enumerate(game.mainline_moves()):
        # Add the move to the list of moves made
        moves_made.append(str(move))

        # Set the position using the list of moves made
        stockfish.set_position(moves_made)

        # Get the best move and its score
        best_move = stockfish.get_best_move()
        best_score = stockfish.get_evaluation()['value']

        # Make the move and get its score
        board.push(move)
        stockfish.set_fen_position(board.fen())
        score = stockfish.get_evaluation()['value']

        # Calculate the accuracy of the move
        accuracy = min(score / best_score if best_score != 0 else 1, 1)

        classification = classify_move(score)
        description = describe_move(classification, best_move, move, accuracy)
        print(description)

        # Classify the stage of the game based on the number of moves made by each player
        player = 'white' if i % 2 == 0 else 'black'
        if total_moves[player] < len(moves_made) / 6:
            stage = 'opening'
        elif total_moves[player] < len(moves_made) / 3:
            stage = 'midgame'
        else:
            stage = 'endgame'

        # Count the moves and sum the accuracies for each player and stage
        total_moves[player] += 1
        total_moves_stages[stage][player] += 1
        total_accuracy[player] += accuracy
        total_accuracy_stages[stage][player] += accuracy

    # Calculate and print the mean accuracy for each player and stage
    for player in ['white', 'black']:
        print(f"\nMean accuracy for {player}:")
        for stage in stages:
            if total_moves_stages[stage][player] > 0:
                mean_accuracy = total_accuracy_stages[stage][player] / total_moves_stages[stage][player]
                print(f"{stage.capitalize()}: {min(mean_accuracy, 1) * 100:.2f}%")
        if total_moves[player] > 0:
            mean_accuracy = total_accuracy[player] / total_moves[player]
            print(f"Overall: {min(mean_accuracy, 1) * 100:.2f}%")

classify_moves("./game.pgn", "./stockfish/stockfish-ubuntu-x86-64-modern")
