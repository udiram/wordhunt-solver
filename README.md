# Word Hunt / Boggle Solver

## Overview
This project is a **Word Hunt/Boggle** solver that provides a **Tkinter GUI** to find and score valid words from a 4×4 board. It uses a **curated ENABLE word list** and an efficient **DFS algorithm with prefix pruning** to quickly discover all possible words.

## Features
- **4×4 Board Input**: Users can enter letters in a 4×4 grid.
- **Curated ENABLE Word List**: Dynamically downloads ~172,000 words from a GitHub repository.
- **Optimized DFS Algorithm**: Uses prefix pruning to improve efficiency.
- **Standard Boggle Scoring**:
  - 3-4 letters: +1 point
  - 5 letters: +2 points
  - 6 letters: +3 points
  - 7 letters: +5 points
  - 8+ letters: +11 points
- **Graphical User Interface (GUI)**:
  - Input board manually
  - View found words and scores
  - See the total score of all words found

## Installation
### Prerequisites
- **Python 3.7+** (Recommended: 3.9+)
- **pip** (for package installation)
- **Internet connection** (for dictionary download on first run)
- **Tkinter** (included in most Python installations)
- **Requests library** (for downloading the word list)

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/<your-username>/word-hunt-solver.git
   cd word-hunt-solver
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   If `requirements.txt` is missing:
   ```bash
   pip install requests
   ```
3. **Run the solver**:
   ```bash
   python word_hunt_solver.py
   ```

## Usage
1. **Enter letters** in each cell of the 4×4 grid.
2. **Click "Solve"** to find all possible words.
3. **View results**:
   - Words sorted by descending score.
   - The total score at the bottom of the window.

## Example
### Input Board:
```
W  O  R  D
H  U  N  T
S  O  L  V
T  A  R  E
```
### Output:
```
WORDS FOUND:
  - HUNT (1)
  - SOLVER (3)
  - WORLD (2)
  - ...
TOTAL SCORE: 18
```

## Code Structure
- **`boggle_score(word)`** – Calculates Boggle scores.
- **`load_enable_word_list()`** – Downloads the ENABLE dictionary.
- **`build_prefix_set(words)`** – Optimizes DFS by precomputing valid prefixes.
- **`dfs(...)`** – Recursively explores the board to find words.
- **`solve_board(board, words_set)`** – Solves the given 4×4 board.
- **`WordHuntSolverGUI`** – Tkinter-based graphical interface.

## Troubleshooting
- **Dictionary not loading**: Check your internet connection.
- **Tkinter import error**:
  - Linux users may need to install `python3-tk`.
  - Windows/Mac users should have Tkinter by default.
- **No words found**:
  - Ensure valid letters are entered.
  - Some boards may not yield words.

## License
This project is licensed under the [MIT License](LICENSE).

## Contribution
Feel free to submit issues or pull requests for improvements.

---
**Happy Word Hunting!** 🎯

