import tkinter as tk
import random, time


# board = [[0] * 4] * 4
class Main:
	def __init__(self):
		self.board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
		self.root = tk.Tk()
		self.root.bind("<KeyPress>", self.key)

	@staticmethod
	def perform_move(l):
		for i in range(3):
			try:
				l.remove(0)
			except ValueError:
				break
			l.append(0)
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
		prev_board = []
		prev_board = self.board
		if event.keysym == "Left":
			self.board = list(map(self.perform_move, self.board))

		if event.keysym == "Right":
			self.board = list(
			    map(lambda x: self.perform_move(x[::-1])[::-1], self.board))
		if event.keysym == "Down":
			transpose = lambda l_of_l: [list(l) for l in zip(*l_of_l)]
			self.board = list(
			    map(lambda x: self.perform_move(x[::-1])[::-1],
			        transpose(self.board)))
			self.board = transpose(self.board)

		if event.keysym == "Up":
			transpose = lambda l_of_l: [list(l) for l in zip(*l_of_l)]
			self.board = list(map(self.perform_move, transpose(self.board)))
			self.board = transpose(self.board)
		for i, j in zip(prev_board, self.board):
			if i != j:
				self.spawn()
				break
		self.display()

	def display(self):
		for i in range(len(self.board)):
			for j in range(len(self.board)):
				tk.Label(
				    self.root,
				    text=self.board[i][j] if self.board[i][j] else None,
				    height=5,
				    width=10,
				    borderwidth=2,
				    relief="ridge").grid(
				        row=i, column=j)
		self.root.update()

	def spawn(self):
		'''
			Randomly sets a single zero element in board to 2,4 or 8
		'''
		num = random.choice([2] * 8 + [4] * 2)
		index = [(i, j) for i in range(len(self.board))
		         for j in range(len(self.board)) if self.board[i][j] == 0
		         ]  # Generate all possible rows and columns
		if len(index) > 0:
			index = random.choice(index)
			self.board[index[0]][index[1]] = num
		else:
			# Board is full
			pass


m = Main()
m.spawn()
m.display()
m.root.mainloop()