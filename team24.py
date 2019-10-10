import random
import math
import copy

class Player24(object):
	"""Bot implementation for UT3 tournament: Player 24"""

	def __init__(self):
		self.INF = 10000000000
		self.HeuristicArray = [[0, -1, -10, -100], [1, 0, 0], [10, 0], [100]]
		self.Threes = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

		self.Heuristic = [0]*19683

		self.mapper = {'d': 0, '-': 0, 'x': 1, 'o': 2}

		# States
		# 0 -> d
		# 0 -> -
		# 1 -> x
		# 2 -> o

		def setHeu(num):

			#Assumes x is my character. If not multiply with -1 in getHeuristic
			
			a = num/6561
			b = (num/2187) % 3
			c = (num/729) % 3
			d = (num/243) % 3
			e = (num/81) % 3
			f = (num/27) % 3
			g = (num/9) % 3
			h = (num/3) % 3
			i = num % 3

			stat = [a, b, c, d, e, f, g, h, i]

			heuristic = 0
			for three in self.Threes:
				myCnt = 0
				othCnt = 0
				for j in three:
					if stat[j] == 1:
						myCnt += 1
					elif stat[j] == 2:
						othCnt += 1

				heuristic += self.HeuristicArray[myCnt][othCnt]

			self.Heuristic[num] = heuristic

		mx = 19683
		for i in xrange(mx):
			setHeu(i)


	def get_valid_cells(self, current_board_game, board_stat, move_by_opponent):

		row = move_by_opponent[0]%3
		column = move_by_opponent[1]%3

		valid_blocks = []

		if row==0 and column==0:
			valid_blocks.extend([0, 1, 3])
		elif row==0 and column==2:
			valid_blocks.extend([1, 2, 5])
		elif row==2 and column==0:
			valid_blocks.extend([3, 6, 7])
		elif row==2 and column==2:
			valid_blocks.extend([5, 7, 8])

		else:
			valid_blocks.append(3*row + column)

		valid_cells = []
		for i in valid_blocks:
			
			if board_stat[i] != '-':
				continue
			
			row = (i/3)*3
			column = (i%3)*3
			for j in xrange(0, 3):
				for k in xrange(0, 3):
					r = row + j
					c = column + k
					if current_board_game[r][c] == '-':
						valid_cells.append((r, c))

		#print valid_cells

		if len(valid_cells) == 0:
			for i in xrange(0, 9):
				for j in xrange(0, 9):
					if board_stat[(i/3)*3 + j/3] == '-' and current_board_game[i][j] == '-':
						valid_cells.append((i, j))

		#print valid_cells
		
		#print valid_cells

		#remove free move giving cells
		free_move_cells = []
		for i in valid_cells:
			if board_stat[(i[0]%3)*3 + i[1]%3] != '-':
				valid_cells.remove(i)
				free_move_cells.append(i)
		
		random.shuffle(valid_cells)

		valid_cells.extend(free_move_cells)

		return valid_cells


	def isTerminalState(self, board_stat):
		for i in xrange(0, 9):
			if board_stat[i] == '-':
				return False
		return True


	def getHeuristic(self, board_game, board_stat):

		def getHeu(lista, a, listb, b, listc, c):
			num = self.mapper[lista[a]]*9 + self.mapper[lista[a+1]]*3 + self.mapper[lista[a+2]] 
			num = num*27 + self.mapper[listb[b]]*9 + self.mapper[listb[b+1]]*3 + self.mapper[listb[b+2]] 
			num = num*27 + self.mapper[listc[c]]*9 + self.mapper[listc[c+1]]*3 + self.mapper[listc[c+2]] 

			return self.Heuristic[num]

		heuristic = 0

		heuristic = 100*getHeu(board_stat, 0, board_stat, 3, board_stat, 6)

		for i in xrange(0, 3):
			for j in xrange(0, 3):
				heuristic += getHeu(board_game[3*i], 3*j, board_game[3*i+1], 3*j, board_game[3*i+2], 3*j)

		if self.myChar == 'o':
			heuristic *= -1

		return heuristic

	def getUtility(self, board_stat):
		
		for i in self.Threes:
			myCnt = 0
			othCnt = 0
			for j in i:
				if board_stat[j] == self.myChar:
					myCnt += 1
				elif board_stat[j] == self.Other:
					othCnt += 1

			if myCnt == 3:
				return self.INF
			elif othCnt == 3:
				return -self.INF

		return 0


	def alpha_beta(self, board_game, board_stat, depth, alpha, beta, flag, node):
		
		self.nodecount += 1
		self.nextCount += 1

		if self.isTerminalState(board_stat):
			return self.getUtility(board_stat)

		children = self.get_valid_cells(board_game, board_stat, node)

		if depth == 0:
			self.nextCount += len(children)
			return self.getHeuristic(board_game, board_stat)

		if flag:
			value = -self.INF
			for child in children:

				self.update_board_stat(board_game, board_stat, child, self.myChar if flag else self.Other)
				
				value = max(value, self.alpha_beta(board_game, board_stat, depth-1, alpha, beta, False, child))
				alpha = max(alpha, value)
				
				board_game[child[0]][child[1]] = '-'
				board_stat[3*(child[0]/3) + child[1]/3] = '-'

				if beta <= alpha:
					break
			return value

		else:
			value = self.INF
			for child in children:
				
				self.update_board_stat(board_game, board_stat, child, self.myChar if flag else self.Other)
				
				value = min(value, self.alpha_beta(board_game, board_stat, depth-1, alpha, beta, True, child))
				beta = min(beta, value)
				
				board_game[child[0]][child[1]] = '-'
				board_stat[3*(child[0]/3) + child[1]/3] = '-'
				
				if beta <= alpha:
					break
			return value


	def update_board_stat(self, board_game, board_stat, move, flag):
		board_game[move[0]][move[1]] = flag

		block_no = (move[0]/3)*3 + move[1]/3
		row = (block_no/3) * 3
		column = (block_no%3) * 3
		is_won = 0
		if board_stat[block_no] == '-':
			if board_game[row][column] == board_game[row+1][column+1] and board_game[row+1][column+1] == board_game[row+2][column+2] and board_game[row+1][column+1] != '-':
				is_won = 1
			if board_game[row+2][column] == board_game[row+1][column+1] and board_game[row+1][column+1] == board_game[row][column+2] and board_game[row+1][column+1] != '-':
				is_won = 1
			if is_won != 1:
				for i in xrange(column, column+3):
					if board_game[row][i] == board_game[row+1][i] and board_game[row+1][i] == board_game[row+2][i] and board_game[row][i] != '-':
						is_won = 1
						break
			if is_won != 1:
				for i in xrange(row, row+3):
					if board_game[i][column] == board_game[i][column+1] and board_game[i][column+1] == board_game[i][column+2] and board_game[i][column] != '-':
						is_won = 1
						break

			if is_won == 1:
				board_stat[block_no] = flag

			empty_cells = []
			for i in xrange(row, row+3):
				for j in xrange(column, column+3):
					if board_game[i][j] == '-':
						empty_cells.append((i, j))
			if len(empty_cells) == 0 and is_won != 1:
				board_stat[block_no] = 'd'


	def move(self, board_game, board_stat, move_by_opponent, flag):

		self.myChar = flag
		if flag=='x':
			self.Other = 'o'
		else:
			self.Other = 'x'

		valid_cells = self.get_valid_cells(board_game, board_stat, move_by_opponent)

		self.nodecount = 0
		ind = [valid_cells[0]]
		bestVal = -self.INF
		depth = 0

		while bestVal != self.INF and depth < 40:

			depth += 1
			self.nextCount = 0
			bestVal = -self.INF

			for i in valid_cells:

				self.update_board_stat(board_game, board_stat, i, flag)
				
				tmp = self.alpha_beta(board_game, board_stat, depth, -self.INF, self.INF, False, i)
				if tmp > bestVal:
					bestVal = tmp
					ind = [i]
				elif tmp == bestVal:
					ind.append(i)
				
				board_game[i[0]][i[1]] = '-'
				board_stat[3*(i[0]/3) + i[1]/3] = '-'

			if self.nodecount + self.nextCount > 120000:
				break

		if len(ind) > 1 and self.nodecount < 50000:

			valid_cells = ind

			ind = [valid_cells[0]]
			bestVal = -self.INF
			depth = 0

			while bestVal != self.INF and depth < 40:

				depth += 1
				self.nextCount = 0
				bestVal = -self.INF

				for i in valid_cells:

					self.update_board_stat(board_game, board_stat, i, flag)
					
					tmp = self.alpha_beta(board_game, board_stat, depth, -self.INF, self.INF, False, i)
					if tmp > bestVal:
						bestVal = tmp
						ind = [i]
					elif tmp == bestVal:
						ind.append(i)
					
					board_game[i[0]][i[1]] = '-'
					board_stat[3*(i[0]/3) + i[1]/3] = '-'

				if self.nodecount + self.nextCount > 120000:
					break


		move = ind[0]

		print self.nodecount, self.nodecount + self.nextCount, depth
		print move
		
		return move

