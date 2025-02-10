import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading


# ------------------------------------------------------------------------------
# 1) Boggle/Word Hunt Scoring Function
# ------------------------------------------------------------------------------
def boggle_score(word):
    length = len(word)
    if length < 3:
        return 0
    elif length == 3 or length == 4:
        return 1
    elif length == 5:
        return 2
    elif length == 6:
        return 3
    elif length == 7:
        return 5
    else:  # length >= 8
        return 11


# ------------------------------------------------------------------------------
# 2) Download a curated “ENABLE” word list (no proper nouns / fewer obscure words)
# ------------------------------------------------------------------------------
def load_enable_word_list():
    """
    Grabs the ENABLE word list from a known GitHub source.
    This list is ~172,806 words, excluding most proper nouns & super obscure terms.
    """
    url = "https://raw.githubusercontent.com/dolph/dictionary/master/enable1.txt"
    response = requests.get(url)
    response.raise_for_status()

    words = set()
    for line in response.text.splitlines():
        w = line.strip().upper()
        # Basic extra check: ignore lines that seem obviously invalid or are too short
        if w and len(w) >= 2:
            words.add(w)
    return words


# ------------------------------------------------------------------------------
# 3) Build a prefix set for quick “does any word start with this prefix?” checks
# ------------------------------------------------------------------------------
def build_prefix_set(words):
    prefix_set = set()
    for w in words:
        for i in range(1, len(w) + 1):
            prefix_set.add(w[:i])
    return prefix_set


# ------------------------------------------------------------------------------
# 4) DFS to explore all paths from a given cell (row, col)
# ------------------------------------------------------------------------------
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1)
]


def dfs(board, row, col, visited, current_word, results, prefix_set, words_set):
    current_word += board[row][col]

    # If no words start with this prefix, prune search.
    if current_word not in prefix_set:
        return

    # If it's a valid word of >= 3 letters, add it
    if current_word in words_set and len(current_word) >= 3:
        results.add(current_word)

    # Explore all 8 neighbors
    for dr, dc in DIRECTIONS:
        r_new = row + dr
        c_new = col + dc
        if 0 <= r_new < 4 and 0 <= c_new < 4 and (r_new, c_new) not in visited:
            visited.add((r_new, c_new))
            dfs(board, r_new, c_new, visited, current_word, results, prefix_set, words_set)
            visited.remove((r_new, c_new))


# ------------------------------------------------------------------------------
# 5) Solve the 4x4 board using the dictionary
# ------------------------------------------------------------------------------
def solve_board(board, words_set):
    prefix_set = build_prefix_set(words_set)
    results = set()

    for row in range(4):
        for col in range(4):
            visited = {(row, col)}
            dfs(board, row, col, visited, "", results, prefix_set, words_set)

    return results


# ------------------------------------------------------------------------------
# 6) Tkinter GUI
# ------------------------------------------------------------------------------
class WordHuntSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Hunt Solver (ENABLE Dictionary)")
        self.root.resizable(False, False)

        # Frame for dictionary loading status
        self.loading_frame = ttk.Frame(self.root)
        self.loading_frame.pack(padx=10, pady=10, fill="x")

        self.loading_label = ttk.Label(
            self.loading_frame, text="Loading curated dictionary (ENABLE)...", anchor="center"
        )
        self.loading_label.pack()

        # Start loading dictionary in a background thread, so UI remains responsive
        self.words_set = set()
        self.load_thread = threading.Thread(target=self.load_dictionary)
        self.load_thread.start()

        # Frame for the 4x4 board
        self.grid_frame = ttk.Frame(self.root)

        self.entries = []
        for r in range(4):
            row_entries = []
            for c in range(4):
                e = ttk.Entry(self.grid_frame, width=3, justify="center", font=("Arial", 14))
                e.grid(row=r, column=c, padx=3, pady=3)
                row_entries.append(e)
            self.entries.append(row_entries)

        # Solve button
        self.solve_button = ttk.Button(self.root, text="Solve", command=self.solve_board_ui)

        # Results label
        self.results_label = ttk.Label(self.root, text="Found Words (sorted by score):")

        # Listbox for displaying found words + their scores
        self.results_listbox = tk.Listbox(self.root, width=35, height=15, font=("Courier", 10))

        # Total score label
        self.total_score_label = ttk.Label(self.root, text="Total Score: 0")

        # Periodically check if the dictionary has finished loading
        self.root.after(100, self.check_load_complete)

    def load_dictionary(self):
        try:
            self.words_set = load_enable_word_list()
        except Exception as ex:
            self.words_set = set()
            print("Error loading dictionary:", ex)

    def check_load_complete(self):
        if self.load_thread.is_alive():
            # Dictionary still loading, check again in 100 ms
            self.root.after(100, self.check_load_complete)
        else:
            # Loading done
            if len(self.words_set) == 0:
                self.loading_label.config(text="Failed to load dictionary!")
                messagebox.showerror(
                    "Error",
                    "Could not load the ENABLE dictionary.\n"
                    "Please check your internet connection or the dictionary URL."
                )
                return
            else:
                self.loading_label.config(text="Dictionary loaded successfully!")

            # Now that the dictionary is loaded, show the rest of the UI
            self.grid_frame.pack(padx=10, pady=10)
            self.solve_button.pack(pady=(0, 5))
            self.results_label.pack()
            self.results_listbox.pack(padx=10, pady=5)
            self.total_score_label.pack(pady=(0, 10))

    def solve_board_ui(self):
        # Build the board from the entries
        board = []
        for r in range(4):
            row_letters = []
            for c in range(4):
                val = self.entries[r][c].get().strip().upper()
                # Default to a blank if user hasn't typed anything
                row_letters.append(val if val else " ")
            board.append(row_letters)

        # Solve
        found_words = solve_board(board, self.words_set)

        # Clear old results
        self.results_listbox.delete(0, tk.END)

        # Score each word and sort by descending score, then alphabetical
        scored_words = []
        total_score = 0

        for w in found_words:
            pts = boggle_score(w)
            scored_words.append((w, pts))
            total_score += pts

        scored_words.sort(key=lambda x: (-x[1], x[0]))  # sort by score desc, then word asc

        # Populate listbox
        for word, pts in scored_words:
            self.results_listbox.insert(tk.END, f"{word:<15} {pts:>2}")

        # Update total
        self.total_score_label.config(text=f"Total Score: {total_score}")


def main():
    root = tk.Tk()
    app = WordHuntSolverGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
