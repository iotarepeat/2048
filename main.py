import tkinter as tk
import random, time


# board = [[0] * 4] * 4
class Main:
	board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

	def __init__(self):
		self.prev_board = []
		self.score = 0
		self.root = tk.Tk()
		self.root.title("2048")
		self.puzzle = tk.Frame(self.root)
		for i in ["Left", "Right", "Up", "Down"]:
			self.puzzle.bind("<" + i + ">", self.key)
		self.puzzle.bind("<u>", self.undo)
		self.puzzle.focus_set()
		self.puzzle.grid()
		self.puzzle.focus_set()
		self.color = {
			0: "#ccc",
			2: "#eee4da",
			4: "#ede0c8",
			8: "#f2b179",
			16: "#f59563",
			32: "#f67c5f",
			64: "#f65e3b",
			128: "#edcf72",
			256: "#edcc61",
			512: "#edc850",
			1024: "#edc53f",
			2048: "#edc22e"
		}

	def undo(self, event):
		self.board = [i.copy() for i in self.prev_board]
		self.display()

	def perform_move(self, l):
		'''
			Perform move assuming left on given row
			EG: 2,2,2,0 becomes 4,2,0,0
		'''
		# Append all zero to extreme right
		for i in range(3):
			try:
				l.remove(0)
				l.append(0)
			except ValueError:
				break
		'''
			l is original list,
			n stores next elements corresponding to original
			EG
			if l = [1,2,3,4] then n = [2,3,4,0]

			if there exists an index i such that,
			l[i] ==  n[i]
			set l[i+1] = 0
			Again move the zero to extreme right
		'''
		for ind, i in enumerate(l[:-1]):
			n = l[1:] + [0]
			if i == n[ind]:
				self.score += l[ind]
				l[ind] *= 2
				l[ind + 1] = 0
				n[ind + 1] = 0
				l.remove(0)
				l.append(0)
		return l

	def key(self, event):
		'''
			Perform move based on the key pressed
		'''
		prev_board = [i.copy() for i in self.board]
		transpose = lambda l_of_l: [list(l) for l in zip(*l_of_l)]
		if event.keysym == "Left":
			# Apply move to every row
			self.board = list(map(self.perform_move, self.board))

		elif event.keysym == "Right":
			# Reverse and apply move to every row and reverse the result
			self.board = list(
				map(lambda x: self.perform_move(x[::-1])[::-1], self.board))
		elif event.keysym == "Up":
			# Transpose and apply move to every row and Transpose the result
			self.board = list(map(self.perform_move, transpose(self.board)))
			self.board = transpose(self.board)
		elif event.keysym == "Down":
			# Transpose + Reverse
			self.board = list(
				map(lambda x: self.perform_move(x[::-1])[::-1],
					transpose(self.board)))
			self.board = transpose(self.board)
		'''
			Check if any further moves are possible before
			spawing
			
		'''
		zero = False
		for i, j in zip(prev_board, self.board):
			if 0 in j:
				zero = True
			if i != j:
				self.prev_board = prev_board
				self.spawn()  #If there's change in the board spawn
				self.display()
				break
		# Check if there are any empty squares
		if not zero:
			# Check if game is over  Check if any possible moves like left ,up or down can be performed
			if not self.game_over():
				self.display()
			else:
				self.root.focus_set()
				tk.Label(
					self.root,
					text="Game Over  Your score is: " + str(
						self.score)).grid()

	def display(self):
		for i in range(len(self.board)):
			for j in range(len(self.board)):
				# Do not display a number for zero,
				# If non zero choose background color from  dictionary
				tk.Label(
					self.puzzle,
					text=self.board[i][j] if self.board[i][j] else None,
					bg=self.color[self.board[i][j]],
					height=5,
					width=10,
					borderwidth=2,
					relief="ridge").grid(
						row=i, column=j)
		tk.Label(
			self.root,
			text="Score: " + str(self.score),
		).grid(
			row=5, column=0, sticky="nsew", rowspan=4)
		self.puzzle.update()

	def game_over(self):
		'''
			Checks if there are any two adjacent tiles
			horizontally and vertically
		'''
		for i in self.board:
			prev = i[0]
			for j in i[1:]:
				if prev == j:
					return False
				prev = j
		for i in list(zip(*self.board)):
			prev = i[0]
			for j in i[1:]:
				if prev == j:
					return False
				prev = j
		return True

	def spawn(self):
		'''
			Randomly sets a single zero element in board to 2,4 or 8
		'''
		num = random.choice([2] * 8 + [4] * 2)
		index = [(i, j) for i in range(len(self.board))
				 for j in range(len(self.board)) if self.board[i][j] == 0
				 ]  # Generate all possible rows and columns
		if len(index) > 0:
			x, y = random.choice(index)
			self.board[x][y] = num


if __name__ == "__main__":
	b = Main()
	b.spawn()
	b.display()
	b.root.mainloop()