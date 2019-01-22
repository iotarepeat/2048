import tkinter as tk
import random, time


# board = [[0] * 4] * 4
class Main:
	def __init__(self):
		self.board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
		self.root = tk.Tk()
		self.puzzle = tk.Frame(self.root)
		for i in ["Left","Right","Up","Down"]:
			self.puzzle.bind("<"+i+">", self.key)
		self.puzzle.focus_set()
		self.puzzle.grid()
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

	@staticmethod
	def perform_move(l):
		for i in range(3):
			try:
				l.remove(0)
				l.append(0)
			except ValueError:
				break
		for ind, i in enumerate(l[:-1]):
			n = l[1:] + [0]
			if i == n[ind]:
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
		if event.keysym == "Left":
			self.board = list(map(self.perform_move, self.board))

		elif event.keysym == "Right":
			self.board = list(
			    map(lambda x: self.perform_move(x[::-1])[::-1], self.board))
		elif event.keysym == "Down":
			transpose = lambda l_of_l: [list(l) for l in zip(*l_of_l)]
			self.board = list(
			    map(lambda x: self.perform_move(x[::-1])[::-1],
			        transpose(self.board)))
			self.board = transpose(self.board)

		elif event.keysym == "Up":
			transpose = lambda l_of_l: [list(l) for l in zip(*l_of_l)]
			self.board = list(map(self.perform_move, transpose(self.board)))
			self.board = transpose(self.board)
		m = 2
		zero = False
		for i, j in zip(prev_board, self.board):
			m = max(m, *j)
			if 0 in j:
				zero = True
			if i != j:
				self.spawn()  #If there's no change in the board,do not spawn
				self.display()
				break
		if not zero:
			if not self.game_over():  # Check if any possible moves like left ,up or down can be performed
				self.display()
			else:
				self.root.focus_set()
				tk.Label(
				    self.root,
				    text="Game Over  Your score is: " + str(m)).grid()

	def display(self):
		for i in range(len(self.board)):
			for j in range(len(self.board)):
				tk.Label(
				    self.puzzle,
				    text=self.board[i][j] if self.board[i][j] else None,
				    bg=self.color[self.board[i][j]],
				    height=5,
				    width=10,
				    borderwidth=2,
				    relief="ridge").grid(
				        row=i, column=j)
		self.puzzle.update()

	def game_over(self):
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


m = Main()
m.spawn()
m.display()
m.root.mainloop()