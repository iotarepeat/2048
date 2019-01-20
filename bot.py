from main import Main


class Bot(Main):
	def __init__(self):
		super().__init__()
		self.puzzle.bind("<Return>", self.key_mod)
		self.puzzle.bind("<Key>", self.key)

	def key_mod(self, event):
		move = "<%s>" % (self.bestMove({
		    "Up": 0,
		    "Down": 0,
		    "Left": 0,
		    "Right": 0
		}))
		print(move)
		self.puzzle.event_generate(move)

	def predict(self,board, direction):
		old = [i.copy() for i in board]
		if direction == "Left":
			new_board = list(map(self.perform_move, board))

		elif direction == "Right":
			new_board = list(
			    map(lambda x: self.perform_move(x[::-1])[::-1], board))
		elif direction == "Down":
			transpose = lambda l_of_l: [list(l) for l in zip(*l_of_l)]
			new_board = list(
			    map(lambda x: self.perform_move(x[::-1])[::-1],
			        transpose(board)))
			new_board = transpose(board)

		elif direction == "Up":
			transpose = lambda l_of_l: [list(l) for l in zip(*l_of_l)]
			new_board = list(map(self.perform_move, transpose(board)))
			new_board = transpose(board)
		board = [i.copy() for i in old]
		return new_board

	def bestMove(self, score):
		board = [i.copy() for i in self.board]
		prev_board = [i.copy() for i in board]
		for i in range(3):
			for move in ["Up", "Down", "Left", "Right"]:
				board = self.predict(board,move)
				for i, j in zip(self.board, board):
					if i != j:
						break
				else:
					score[move]-=1
					continue
				score[move] += self.tiles_merged(prev_board, board)
				prev_board = board
		return max(score, key=lambda x: score[x])

	@staticmethod
	def tiles_merged(prev, curr):
		count = lambda board: sum([1 for i in board for j in i if j != 0])
		return -(count(curr) - count(prev) - 1)


if __name__ == "__main__":
	m = Bot()
	m.spawn()
	m.display()
	m.puzzle.mainloop()