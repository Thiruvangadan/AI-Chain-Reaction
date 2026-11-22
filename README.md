# Chain Reaction

A turn-based strategy game built using **Python and Pygame**, featuring a computer opponent powered by the **Minimax algorithm with Recursion, Backtracking, and Alpha-Beta Pruning**.

The game supports local two-player gameplay and playing against the computer. It can also run directly in a web browser using Pygbag.

**Play Online:** https://thiruvangadan.github.io/chain-reaction-live/

## Game Overview

Chain Reaction is a strategy game played on a 4 × 4 grid. Players take turns placing atoms in cells, triggering chain reactions that spread to neighboring cells and capture them.

The objective is to eliminate all atoms belonging to the opponent.

## Features

- Play against a computer-controlled opponent.
- Local two-player mode.
- Chain reactions and cell explosions.
- Cell capture through neighboring explosions.
- AI opponent using recursive Minimax.
- Backtracking for exploring possible game states.
- Alpha-Beta pruning to optimize the search.
- Browser-based gameplay using Pygbag.
- Automated deployment using GitHub Actions and GitHub Pages.

## AI Decision-Making

The computer opponent uses the **Minimax algorithm** to evaluate possible moves and select an advantageous move.

### Minimax Algorithm

Minimax explores possible future game states by considering the computer's moves and the opponent's responses.

- The computer acts as the maximizing player.
- The human acts as the minimizing player.
- The algorithm evaluates possible outcomes and selects the move with the best achievable score.

### Recursion

The Minimax function calls itself to explore future moves, alternating between maximizing and minimizing players.

The initial search depth is set to **3 plies**.

### Backtracking

After exploring a possible move, the board is restored to its previous state before another move is evaluated.

This allows the algorithm to explore multiple possibilities without permanently modifying the actual game board.

### Alpha-Beta Pruning

Alpha-Beta pruning reduces unnecessary search by skipping branches that cannot influence the final decision.

- Alpha represents the best score currently guaranteed to the maximizing player.
- Beta represents the best score currently guaranteed to the minimizing player.

This improves search efficiency without changing the Minimax result for the explored depth.

### Board Evaluation

At the search-depth limit, the AI evaluates the board using factors such as:

- Number of atoms controlled by each player.
- Cell ownership.
- Cells approaching their critical mass.
- Potential threats involving neighboring opponent cells.

## Technologies Used

- Python 3.12
- Pygame CE
- Pygbag
- Minimax Algorithm
- Recursion and Backtracking
- Alpha-Beta Pruning
- Git and GitHub
- GitHub Actions
- GitHub Pages

## Run Locally

### Clone the Repository

```bash
git clone https://github.com/Thiruvangadan/chain-reaction-live.git
cd chain-reaction-live
```

### Install Dependencies

```bash
py -3.12 -m pip install pygame-ce pygbag
```

### Run the Game

```bash
py -3.12 main.py
```

## Browser Execution

This project uses Pygbag to run the Pygame application in a web browser.

To build and test the browser version locally:

```bash
py -3.12 -m pygbag .
```

Open the local URL displayed in the terminal.

The browser version is deployed through GitHub Pages using GitHub Actions.

**Play Online:** https://thiruvangadan.github.io/chain-reaction-live/

## How to Play

- Choose Play with Computer or Play with Friend.
- Select a cell to place an atom.
- Each cell has a critical mass determined by its number of neighboring cells.
- When a cell reaches its critical mass, it explodes and distributes atoms to its neighbors.
- Explosions can trigger additional chain reactions.
- Capture your opponent's cells and eliminate their atoms to win.

## Controls

| Key | Action |
|---|---|
| ESC | Return to the menu |
| R | Restart the game |
| M | Return to menu after game over |
| Q | Quit the game |

## Project Structure

```text
chain-reaction-live/
│
├── main.py
├── requirements.txt
│
└── .github/
    └── workflows/
        └── deploy.yml
```

## Future Improvements

- Experiment with deeper Minimax search.
- Improve AI evaluation and move ordering.
- Optimize AI performance for browser execution.
- Introduce additional board sizes and game variations.
- Explore online multiplayer functionality.

## Author

**Ashwanth**

[GitHub Profile](https://github.com/Thiruvangadan)

[Project Repository](https://github.com/Thiruvangadan/chain-reaction-live)