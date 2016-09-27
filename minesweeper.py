#!/usr/bin/python
'''
 This is a random program I wrote to play Minesweeper through the console. NOTE: Work in progress!
'''
import sys
import random
from datetime import datetime as dt


class Cell:

	def __init__(self, mine_flag=False, hide=True):
		self.set_as_mine(mine_flag)
		self.num = 0
		self.__flag = None
		self.hidden = hide

	def is_mine(self):
		return self.__mine

	def set_as_mine(self, boolean):
		self.__mine = boolean

	def get_flag(self):
		return self.__flag

	def set_flag(self, boolean=True):
		self.__flag = boolean


class Minesweeper:

	def __init__(self):
		self.__board = None
		self.__mines = None
		self.__found = None
		self.__flag_ctr = None
		self.start_time = dt.now()

	def __check_win(self):
		return self.__mines == self.__found

	def __set_board_nums(self, xdim, ydim):
		for i in xrange(0, xdim):
			for j in xrange(0, ydim):
				if self.__board[i][j].is_mine():
					if((i == 0) and (j == 0)):
						self.__board[0][1].num += 1
						self.__board[1][0].num += 1
						self.__board[1][1].num += 1
					elif((i == xdim - 1) and (j == 0)):
						self.__board[xdim - 2][0].num += 1
						self.__board[xdim - 2][1].num += 1
						self.__board[xdim - 1][1].num += 1
					elif((i == 0) and (j == ydim - 1)):
						self.__board[1][ydim - 2].num += 1
						self.__board[1][ydim - 2].num += 1
						self.__board[1][ydim - 1].num += 1
					elif((i == xdim - 1) and (j == ydim - 1)):
						self.__board[xdim - 2][ydim - 2].num += 1
						self.__board[xdim - 2][ydim - 1].num += 1
						self.__board[xdim - 1][ydim - 2].num += 1
					elif((i == 0) and ((j > 0) and (j < ydim - 1))):
						for k in xrange(j - 1, j + 2):
							self.__board[i + 1][k].num += 1
							if(k != j):
								self.__board[i][k].num += 1
					elif((i == xdim - 1) and ((j > 0) and (j < ydim - 1))):
						for k in xrange(j - 1, j + 2):
							self.__board[i - 1][k].num += 1
							if(k != j):
								self.__board[i][k].num += 1
					elif(((i > 0) and (i < xdim - 1)) and (j == 0)):
						for k in xrange(i - 1, i + 2):
							self.__board[k][j + 1].num += 1
							if(k != i):
								self.__board[k][j].num += 1
					elif(((i > 0) and (i < xdim - 1)) and (j == ydim - 1)):
						for k in xrange(i - 1, i + 2):
							self.__board[k][j - 1].num += 1
							if(k != i):
								self.__board[k][j].num += 1
					elif(((i < xdim - 1) and (i > 0)) and ((j < ydim - 1) and (j > 0))):
						for k in xrange(j - 1, j + 2):
							self.__board[i - 1][k].num += 1
							self.__board[i + 1][k].num += 1
							if(k != j):
								self.__board[i][k].num += 1

	def __disp_board(self):
		# Use the below print for debugging.
		#print "Mines Left:\t", self.__flag_ctr, "\tActually Found:\t", self.__found, "\tTime:\t", (dt.now() - self.start_time).seconds
		print "Mines Left:\t", self.__flag_ctr, "\tTime:\t", (dt.now() - self.start_time).seconds
		print "_____" * len(self.__board[0])
		for row in self.__board:
			for cell in row:
				if cell.get_flag():
					x = "F"
				elif cell.hidden:
					x = " "
				else:
					x = cell.num
				print "| ", x,
			print "|\n", "_____" * len(row)

	def __get_neighbors(self, i, j, n, s):
		ydim = len(self.__board[0])
		xdim = len(self.__board)
		candidates = []
		if((i == 0) and (j == 0)):
			candidates = [(0, 1), (1, 0), (1, 1)]
		elif((i == xdim - 1) and (j == 0)):
			candidates = [(i - 1, 0), (i - 1, 1), (i, 1)]
		elif((i == 0) and (j == ydim - 1)):
			candidates = [(1, ydim - 2), (1, ydim - 2), (1, ydim - 1)]
		elif((i == xdim - 1) and (j == ydim - 1)):
			candidates = [(xdim - 2, ydim - 2), (xdim - 2, ydim - 1), (xdim - 1, ydim - 2)]
		elif((i == 0) and ((j > 0) and (j < ydim - 1))):
			for k in xrange(j - 1, j + 2):
				candidates.append((i + 1, k))
				if(k != j):
					candidates.append((i, k))
		elif((i == xdim - 1) and ((j > 0) and (j < ydim - 1))):
			for k in xrange(j - 1, j + 2):
				candidates.append((i - 1, k))
				if(k != j):
					candidates.append((i, k))
		elif(((i > 0) and (i < xdim - 1)) and (j == 0)):
			for k in xrange(i - 1, i + 2):
				candidates.append((k, j + 1))
				if(k != i):
					candidates.append((k, j))
		elif(((i > 0) and (i < xdim - 1)) and (j == ydim - 1)):
			for k in xrange(i - 1, i + 2):
				candidates.append((k, j - 1))
				if(k != i):
					candidates.append((k, j))
		elif(((i < xdim - 1) and (i > 0)) and ((j < ydim - 1) and (j > 0))):
			for k in xrange(j - 1, j + 2):
				candidates.append((i - 1, k))
				candidates.append((i + 1, k))
				if(k != j):
					candidates.append((i, k))
		for c in candidates:
			if c not in s:
				n.append(c)
				s.add(c)

	def __open_up_board(self, x, y):
		stack = [(x, y)]
		seen = set(stack)
		while(len(stack) != 0):
			xy = stack.pop()
			if not self.__board[xy[0]][xy[1]].is_mine():
				self.__board[xy[0]][xy[1]].hidden = False
				if(self.__board[xy[0]][xy[1]].num == 0):
					self.__get_neighbors(xy[0], xy[1], stack, seen)

	def __left_click(self, x, y):
		cell = self.__board[x][y]
		if cell.get_flag():
			print "Flag set. First unset the flag."
			return True
		if cell.is_mine():
			return False
		n = self.__board[x][y].num
		if(n != 0):
			self.__board[x][y].hidden = False
			return True
		self.__open_up_board(x, y)
		return True

	def __right_click(self, x, y):
		if not self.__board[x][y].hidden:
			return
		flag = self.__board[x][y].get_flag()
		if not flag:
			self.__board[x][y].set_flag(True)
			self.__flag_ctr -= 1
			if self.__board[x][y].is_mine():
				self.__found += 1
		else:
			self.__board[x][y].set_flag(False)
			self.__flag_ctr += 1
			if self.__board[x][y].is_mine():
				self.__found -= 1
		return

	def play_game(self, cmd):
		cmd = cmd.strip()
		try:
			x = int(cmd[1])
			y = int(cmd[2])
		except:
			print "Invalid Input. Format:\t <L/R> <x coordinate> <y coordinate>"
			return -2
		if((x < 0) or (x >= len(self.__board)) or (y < 0) or (y >= len(self.__board[0]))):
			print "Indices out of bounds! Make sure your x index is between [0,", len(self.__board), ") and your y index is between [0,", len(self.__board[0]), ")"
			return -2
		lr = cmd[0]
		if((lr == "L") or (lr == "l")):
			res = self.__left_click(x, y)
			if not res:
				print "Oops! You hit a mine!"
				return -1
		elif((lr == "R") or (lr == "r")):
			self.__right_click(x, y)
		else:
			print "Invalid Input. Format:\t <L/R> <x coordinate> <y coordinate>"
			return -2
		self.__disp_board()
		if self.__check_win():
			print "You Win!"
			return 1
		return 0

	def generate_board(self, xdim=8, ydim=8, mines=10, config=None):
		if((xdim <= 0) or (ydim <= 0) or (mines >= xdim * ydim)):
			return False
		self.__board = []
		if config is not None:
			with open(config, "r") as f:
				self.__mines = 0
				for line in f:
					line = line.strip().split(",")
					row = []
					for c in line:
						if(c == "X"):
							self.__mines += 1
							row.append(Cell(True))
						else:
							row.append(Cell())
					self.__board.append(row)
		else:
			self.__board = [[Cell() for _ in xrange(0, ydim)] for _ in xrange(0, xdim)]
			mine_cntr = 0
			while(mine_cntr < mines):
				x = random.randint(0, xdim - 1)
				y = random.randint(0, ydim - 1)
				if not self.__board[x][y].is_mine():
					self.__board[x][y].set_as_mine(True)
					mine_cntr += 1
			self.__mines = mines
		self.__found = 0
		self.__flag_ctr = self.__mines
		self.__set_board_nums(xdim, ydim)
		self.__disp_board()
		return True

	def final_display(self):
		print "_____" * len(self.__board[0])
		for row in self.__board:
			for cell in row:
				if cell.is_mine():
					if cell.get_flag():
						x = "X"
					else:
						x = "*"
				elif cell.get_flag():
					x = "F"
				elif cell.hidden:
					x = " "
				else:
					x = cell.num
				print "| ", x,
			print "|\n", "_____" * len(row)


def main():
	M = Minesweeper()
	if not M.generate_board():
		print "Error in board generation."
		return
	res = 0
	while((res != -1) and (res != 1)):
		try:
			res = M.play_game(input("Enter your command:\t"))
		except KeyboardInterrupt:
			sys.exit()
		except:
			print "Error"
	M.final_display()


if __name__ == "__main__":
	main()
