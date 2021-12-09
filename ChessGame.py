import numpy as np
import random
import tkinter as tk
import easygui as g
choice = g.choicebox(msg="游戏模式", title = '请选择游戏模式', choices=['双人游戏','AI对战'])
if choice == '双人游戏':
	choicesize = g.choicebox(msg="棋盘大小", title = '请选择棋盘大小', choices=[3,4,5])
	SIZE = int(choicesize)
else:
	choiceAI = g.choicebox(msg="落子顺序", title = '请选择落子顺序', choices=['AI先手','玩家先手'])
	SIZE = 3
EMPTY = ' '
CHESS_O = 'O'
CHESS_X = 'X'
global player
class TreeNode:
	##构造树
	def __init__(self, state): 
		self.state = state
	def getActions(self):
		state = self.state
		actions = []
		for row in range(SIZE):
			for column in range(SIZE):
				if state[row][column] == EMPTY:
					actions.append([row, column])
		return actions
	def move(self, action, chess):
		state = self.state.copy()
		row, column = action
		state[row][column] = chess
		return state

def goalTest(node):
	state = node.state
	lines = np.concatenate((state,                                          # rows
							state.T,                                        # columns
							np.diag(state).reshape((1, SIZE)),              # diag \
							np.diag(np.fliplr(state)).reshape((1, SIZE)),   # diag /
							))
	lines = lines.tolist()
	if ([CHESS_X]*SIZE in lines):
		return 2**11
	elif ([CHESS_O]*SIZE in lines):
		return -2**11
	elif (EMPTY in state):
		return None         # 继续下
	else:
		return 0            # 和局

def alphaBeta(node):
	# AI比较执行最优策略
	best_action = []
	best_value = float('-inf')
	for action in node.getActions():
		child = TreeNode(node.move(action, CHESS_X))
		value = minValue(child, float('-inf'), float('inf'))
		if (value>best_value):
			best_value = value
			best_action = action
	return best_action

def maxValue(node, alpha, beta):
	result = goalTest(node)
	if result != None:
		return result
	value = float('-inf')
	for action in node.getActions():
		child = TreeNode(node.move(action, CHESS_X))
		value = max(value, minValue(child, alpha, beta)//2)
		if (value >= beta):
			return value
		alpha = max(alpha, value)
	return value

def minValue(node, alpha, beta):
	result = goalTest(node)
	if result != None:
		return result
	value = float('inf')
	for action in node.getActions():
		child = TreeNode(node.move(action, CHESS_O))
		value = min(value, maxValue(child, alpha, beta)//2)
		if (value <= alpha):
			return value
		beta = min(beta, value)
	return value

def unitTest():
	##Testing
	empty_board = np.full((SIZE, SIZE), EMPTY)
	node = TreeNode(empty_board.copy())
	
	node.state = np.array(node.move([1, 1], CHESS_X))
	print('move result:', node.state, sep='\n', end='\n\n')
	print('getActions:', node.getActions(), sep='\n', end='\n\n')
	
	board = [CHESS_O]*(SIZE**2//2) + [CHESS_X]*(SIZE**2//2) + \
			[random.choice([CHESS_X, EMPTY])]
	random.shuffle(board)
	node = TreeNode(np.array(board).reshape((SIZE, SIZE)))
	print('state:', node.state, sep='\n', end='\n\n')
	print('goal test:', goalTest(node), sep='\n')

def randomBoard():
	##随机
	chess_num = random.choice(range(1, SIZE**2, 2))
	board = [CHESS_O]*(chess_num//2+1) + [CHESS_X]*(chess_num//2) + \
			[EMPTY]*(SIZE**2-chess_num)
	random.shuffle(board)
	return TreeNode(np.array(board).reshape((SIZE, SIZE)))

global count
count = 0
def main():
	##主函数
	global count
	if(choice == 'AI对战'):
		window = tk.Tk()
		# 設定視窗標題、大小和背景顏色
		window.title('Tic-Tac-Toe')
		#window.geometry('800x600')
		window.configure(background='white')
		
		
		state_label = tk.Label(window, text='Place your chess', height=2, font=("Helvetic", 30, "bold"))
		state_label.grid(row=0, column=0, columnspan=SIZE, sticky=tk.W+tk.E)
		
		board = []
		
		r = random.randint(0,2)
		c = random.randint(0,2)
			
		for row in range(SIZE):
			board.append([])
			for column in range(SIZE):
				if row == r and column == c and choiceAI == 'AI先手':
					board[row].append( tk.Button(window, text=CHESS_X, 
						 height=2, width=5, relief='groove', font=('Helvetic', 30, 'bold'), 
						 command=lambda row=row, column=column: placeChess(board, row, column, state_label)))
					board[row][column].grid(row=row+1, column=column, sticky=tk.N+tk.W+tk.E+tk.S)		
				else:
					board[row].append( tk.Button(window, text=EMPTY, 
						 height=2, width=5, relief='groove', font=('Helvetic', 30, 'bold'), 
						 command=lambda row=row, column=column: placeChess(board, row, column, state_label)))
					board[row][column].grid(row=row+1, column=column, sticky=tk.N+tk.W+tk.E+tk.S)		
		
		reset = tk.Button(window, text='Reset', height=1, relief='groove',
						  font=('Helvetic', 30, 'bold'), command=lambda:resetBoard(board, state_label))
		reset.grid(row=SIZE+1, column=0, columnspan=SIZE, sticky=tk.W+tk.E)
		
		# 主界面
		window.mainloop()
	else:
		window = tk.Tk()
		# 設定視窗標題、大小和背景顏色
		window.title('Tic-Tac-Toe')
		#window.geometry('800x600')
		window.configure(background='white')
		
		state_label = tk.Label(window, text='Place you chess', height=2, font=("Helvetic", 30, "bold"))
		state_label.grid(row=0, column=0, columnspan=SIZE, sticky=tk.W+tk.E)
		
		board = []
		for row in range(SIZE):
			board.append([])
			for column in range(SIZE):
				board[row].append(tk.Button(window, text=EMPTY, 
					 height=2, width=5, relief='groove', font=('Helvetic', 30, 'bold'), 
					 command=lambda row=row, column=column: placeChess(board, row, column, state_label)))
				board[row][column].grid(row=row+1, column=column, sticky=tk.N+tk.W+tk.E+tk.S)	
		reset = tk.Button(window, text='Reset', height=1, relief='groove',
						  font=('Helvetic', 30, 'bold'), command=lambda:resetBoard(board, state_label))
		reset.grid(row=SIZE+1, column=0, columnspan=SIZE, sticky=tk.W+tk.E)
		window.mainloop()
	
def resetBoard(board, state_label):
	count = 0
	r = random.randint(0,2)
	c = random.randint(0,2)
	for row in range(SIZE):
		for column in range(SIZE):
			if row == r and column == c and choiceAI == 'AI先手':
				board[row][column].configure(text=CHESS_X, state=tk.NORMAL)
			else:
				board[row][column].configure(text=EMPTY, state=tk.NORMAL)
	state_label.configure(text='Place your chess')

def placeChess(board, row, column, state_label):
	if choice != '双人游戏':
		board[row][column].configure(text=CHESS_O, state=tk.DISABLED)
		state = []
		for row in range(SIZE):
			state.append([])
			for column in range(SIZE):
				state[row].append(board[row][column]['text'])
		node = TreeNode(np.array(state))
		result = goalTest(node)
		if (result != None):
			gameOver(result, board, state_label)
			return
		row, column = alphaBeta(node)
		board[row][column].configure(text=CHESS_X, state=tk.DISABLED)
		node.state[row][column] = CHESS_X
		result = goalTest(node)
		if (result != None):
			gameOver(result, board, state_label)

	else:
		global count
		count+=1
		if count %2 == 0:
			board[row][column].configure(text=CHESS_O, state=tk.DISABLED)
		else:
			board[row][column].configure(text=CHESS_X, state=tk.DISABLED)
		##count += 1
		##board[row][column].configure(text=t, state=tk.DISABLED)
		state = []
		for row in range(SIZE):
			state.append([])
			for column in range(SIZE):
				state[row].append(board[row][column]['text'])
		node = TreeNode(np.array(state))
		result = goalTest(node)
		if (result != None):
			gameOver(result, board, state_label)
			return

def gameOver(result, board, state_label):
	if (result<0):
		if choice != "双人游戏":
			state_label.configure(text='You win')
		else:
			state_label.configure(text='O win')
	elif (result>0):
		if choice != "双人游戏":
			state_label.configure(text='You lose')
		else:
			state_label.configure(text='X win')
	else:
		state_label.configure(text='Drawn game')
	for row in range(SIZE):
		for column in range(SIZE):
			board[row][column].configure(state=tk.DISABLED)

if __name__ == '__main__':
	main()