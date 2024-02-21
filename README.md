# Chess Coach

This Python script uses the Stockfish chess engine to analyze chess games and provide feedback on the moves made by each player.

## Features

- Analyzes each move in a game and classifies it as a blunder, mistake, miss, good, excellent, or best move.
- Calculates the accuracy of each move as a percentage of the best possible score.
- Provides a description of each move based on its classification and accuracy.
- Calculates the mean accuracy for each player in the opening, midgame, and endgame stages, as well as overall.

## Requirements

- Python 3
- python-chess library
- Stockfish chess engine

## Usage

1. Install the required Python libraries with pip:

    ```bash
    pip install python-chess
    ```

2. Download and install the Stockfish chess engine from the official website.

3. Run the script with Python:

    ```bash
    python app.py
    ```

## Disclaimer

This script is provided as an example and may not work perfectly for your specific use case. Always test code thoroughly before using it in a production environment.

## License

This project is licensed under the MIT License.
