import argparse, copy


class PuzzleBoard():

	def __init__(self, board_length, board_width):
		self.l = board_length
		self.w = board_width
		self.state = [[0 for _ in range(board_width)] for _ in range(board_length)]

	# Input: point - tuple cotaining (row_index, col_index) of point in self.state
	# Returns true if point is out of bounds; otherwise, returns false
	def __out_of_bounds(self, point):
		# TODO: Implement this function
		return False

	# Finds the next available open space in the PuzzleBoard (looking from the top-left in row-major order)
	def __next(self):
		for i in range(len(self.state)) :
			for j in range(len(self.state[0])):
				if (self.state[i][j] == 0):
					return (i, j)
		return False

	# Input: piece - PuzzlePiece object
	# Check if piece fits in the next available space (determined by __next method above)
	def fits(self, piece):

		position = self.__next()
		if not position:
			return False

		#TODO: Check if any part of the piece is out of bounds


		#TODO: Check if piece can be placed without intersecting another placed piece
		

		return True

	# Input: piece - PuzzlePiece object
	# Insert piece into the next available position on the board and update state
	def place(self, piece):
		# TODO: Bug in this function. Pieces not being placed correctly.
		position = self.__next()
		for i in range(position[0], position[0] + piece.w):
			for j in range(position[1], position[1] + piece.w):
				self.state[j][i] = piece.id
		return position

	# Returns whether the board has been filledwith pieces
	def completed(self):
		return True if not self.__next() else False

	def copy(self):
		copied = PuzzleBoard(self.l, self.w)
		copied.state = copy.deepcopy(self.state)
		return copied

class PuzzlePiece():

	def __init__(self, pid, length, width):
		self.id = pid
		self.l = length
		self.w = width

	def rotate(self):
		#TODO: Bug in this function. Pieces are not rotating correctly
		self.l = self.w
		self.w = self.l

	def orientation(self):
		return "H" if self.w >= self.l else "V"

	def __str__(self):
		return f"ID: {self.id}, LENGTH: {self.l}, WIDTH: {self.w}, ROTATED: {self.rotated}"

def parse_input(filepath) :
	#TODO: Bug in this function. Error raised when called
	parsed = {'board' : {}, 'pieces' : {}}
	with open(filepath) as f:
		file_contents = f.read().strip().split("\n")
		board_length, board_width = file_contents[0].strip().split(",")
		parsed['board']['length'] = int(board_length)
		parsed['board']['width'] = int(board_width)
		for i in range(len(file_contents)):
			pid, l, w = file_contents[i].strip().split(",")
			pid, l, w = int(pid), int(l), int(w)
			parsed['pieces'][pid] = {}
			parsed['pieces'][pid]['length'] = l
			parsed['pieces'][pid]['width'] = w
	return parsed


def helper(board, pieces):
	used_pieces = []
	for piece in pieces:
		if board.fits(piece):
			position = board.place(piece)
			used_pieces.append((piece, position))
		else:
			return False
	return board, used_pieces

def solve5(board, pieces):
	if len(pieces) != 5:
		return False
	for i1 in range(len(pieces)):
		piece1 = pieces[i1]
		for _ in range(2):
			piece1.rotate()
			for i2 in range(len(pieces)):
				if i2 == i1:
					continue
				piece2 = pieces[i2]
				for _ in range(2):
					piece2.rotate()
					for i3 in range(len(pieces)):
						if i3 in [i1,i2]:
							continue
						piece3 = pieces[i3]
						for _ in range(2):
							piece3.rotate()
							for i4 in range(len(pieces)):
								if i4 in [i1, i2, i3]:
									continue  
								piece4 = pieces[i4]
								for _ in range(2):
									piece4.rotate()
									for i5 in range(len(pieces)):
										if i5 in [i1, i2, i3, i4]:
											continue
										piece5 = pieces[i5]
										for _ in range(2):
											piece5.rotate()
											solved = helper(board.copy(), [piece1, piece2, 
																	piece3, piece4, piece5])
											if solved:
												new_board, used_pieces = solved
												if new_board.completed():
													return new_board, used_pieces
	return False

def solve(board, remaining, used_pieces=[]):
	# TODO: Implement a solution for a variable amount of pieces and puzzle board size.
	# HINT: Recursion might help.
	pass

def main():
	#TODO: Bug in this function. Positions are not correct after solution is found.
	parser = argparse.ArgumentParser()
	parser.add_argument('input')
	args = parser.parse_args()
	parsed = parse_input(args.input)
	board = PuzzleBoard(parsed['board']['length'], parsed['board']['width'])
	pieces = []
	for k, v in parsed['pieces'].items():
		pieces.append(PuzzlePiece(k, v['length'], v['width']))
	solved = solve5(board, pieces)
	if not solved:
		print("No solution found for given input.")
	else:
		print("Solution found.")
		board, used_pieces = solved
		for u, position in used_pieces:
			print(f"Piece ID: {u.id}, Position:{position}, Orientation: {u.orientation()}")

if __name__ == "__main__":
	main()
