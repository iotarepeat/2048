from main import Main


class Bot(Main):
	def __init__(self):
		super().__init__()
		self.puzzle.bind("<Return>", self.key_mod)
		self.puzzle.bind("<Key>", self.key)

	def key_mod(self, event):
		move = "<%s>" % (self.bestMove(self.board,2)[0])
		print(move)
		self.puzzle.event_generate(move)
		self.display()

	def predict(self, board, direction):
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
			new_board = transpose(new_board)

		elif direction == "Up":
			transpose = lambda l_of_l: [list(l) for l in zip(*l_of_l)]
			new_board = list(map(self.perform_move, transpose(board)))
			new_board = transpose(new_board)
		board = [i.copy() for i in old]
		return new_board
	@staticmethod
	def issorted(board):
		score = 0
		for i in board:
			x = sum(map(lambda x, y: abs(x - y), i, sorted(i))) 
			if x==0:
				score+=1
		for i in zip(*board):
			x = sum(map(lambda x, y: abs(x - y), i, sorted(i))) 
			if x==0:
				score+=1
		return score

	def bestMove(self, board, depth=2):
		moves = ["Up", "Down", "Left", "Right"]
		predictions = {}
		for move in moves:
			predictions[move] = self.predict(board, move)
			for i, j in zip(board, predictions[move]):
				if i != j: break
			else:
				del predictions[move] 
		if depth == 0:
			l = []
			for move in predictions:
				merge = self.tiles_merged(self.board,predictions[move])+self.issorted(predictions[move])
				m = (move,merge)
				l.append(m)
			return max(l,key=lambda x:x[1])
		l=[]
		for move in predictions:
			y = self.bestMove(predictions[move],depth-1)[1]
			l.append((move,y))
		return max(l,key=lambda x:x[1])

	@staticmethod
	def tiles_merged(prev, curr):
		count = lambda board: sum([1 for i in board for j in i if j != 0])
		return abs(count(curr) - count(prev))


if __name__ == "__main__":
	b = Bot()
	b.spawn()
	b.display()
	b.root.mainloop()