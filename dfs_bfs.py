import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle


class Maze(tk.Tk):
	def __init__(self):
		self.start = None
		self.finish = None
		self.blocked =  []
		self.maze = []
		self.grid = []
        # -------------- Tkinter Declaration ----------------------------
		tk.Tk.__init__(self)
		self.base = ttk.Frame(self)
		self.base.place(relheight=1, relwidth=1)
		self.generate_grid()
        # -------------- Main Buttons ----------------------------
		l = ttk.Label(self, text='Press Left mouse button to select Start location', foreground='#2E8B57')
		l.place(relx=0.24, rely=0.03)
		l = ttk.Label(self, text='Press Right mouse button to select Finish location', foreground='#DC143C')
		l.place(relx=0.24, rely=0.06)
		l = ttk.Label(self, text='Press Shift-Left mouse button to select Blocked location', foreground='#4682B4')
		l.place(relx=0.20, rely=0.09)
		self.bfs_button = ttk.Button(self, text="BFS", command=self.bfs)
		self.bfs_button.place(relx=0.30, rely=0.6, relwidth=0.2)
		self.dfs_button = ttk.Button(self, text="DFS", command=self.dfs)
		self.dfs_button.place(relx=0.50, rely=0.6, relwidth=0.2)
		self.reset_button = ttk.Button(self, text="Reset", command=self.reset)
		self.reset_button.place(relx=0.40, rely=0.67, relwidth=0.2)

	def generate_grid(self):
		for i in range(7):
			inner_grid = []
			inner_maze = []
			for j in range(6):
				g = tk.Button(self.base, text=0, height=1, width=3, background='#696969')
				g.bind('<Button-1>', lambda event, g=g, i=i, j=j: self.start_clicked(g, i, j))
				g.bind('<Button-3>', lambda event, g=g, i=i, j=j: self.finish_clicked(g, i, j))
				g.bind('<Shift-Button-1>', lambda event, g=g, i=i, j=j: self.blocked_clicked(g, i, j))
				g.grid(row=i, column=j)
				inner_grid.append(g)
				inner_maze.append(0)
			self.grid.append(inner_grid)
			self.maze.append(inner_maze)
		for gr in self.grid[0]:
			gr.grid(pady=(100, 0))
		for gr in self.grid:
			gr[0].grid(padx=(160, 0))
	
	def start_clicked(self, button: tk.Button, i: int, j: int):
		if self.start:
			print("Start Already Set")
		elif self.finish == (i, j):
			print("Start and Finish point cannot be same")
		elif not self.start:
			self.start = (i, j)
			button.config(bg='#2E8B57')
			button.config(text='1')
			self.maze[i][j] = 1

	def finish_clicked(self, button: tk.Button, i: int, j: int):
		if self.finish:
			print("Finish Already Set")
		elif self.start == (i, j):
			print("Start and Finish point cannot be same")
		elif not self.finish:
			self.finish = (i, j)
			button.config(bg='#DC143C')
			button.config(text='2')
			self.maze[i][j] = 1
	
	def blocked_clicked(self, button: tk.Button, i: int, j: int):
		self.blocked.append((i, j))
		button.config(bg='#4682B4')
		button.config(text='-1')
		self.maze[i][j] = -1

	def reset(self):
		self.maze = []
		self.grid = []
		self.blocked = []
		self.start = None
		self.finish = None
		self.bfs_button.config(state="normal")
		self.dfs_button.config(state="normal")
		for widget in self.base.winfo_children():
			widget.destroy()
		self.generate_grid()

	def bfs(self):
		if not self.start and not self.finish:
			return
		q = []
		q.append(self.start)
		visited = []
		while q:
			current = q.pop(0)
			if current == self.finish:
				break
			else: 
				if current not in visited:
					if current[0] + 1 <= 7 - 1: 
						if self.maze[current[0] + 1][current[1]] != -1:
							q.append((current[0] + 1, current[1]))
							if (current[0] + 1, current[1]) != self.finish:
								self.maze[current[0] + 1][current[1]] = 0.4
							
					if current[1] + 1 <= 6 - 1:
						if self.maze[current[0]][current[1] + 1] != -1:
							q.append((current[0], current[1] + 1))
							if (current[0], current[1] + 1) != self.finish:
								self.maze[current[0]][current[1] + 1] = 0.4

					if current[0] - 1 >= 0: 
						if self.maze[current[0] - 1][current[1]] != -1:
							q.append((current[0] - 1, current[1]))
							if (current[0] - 1, current[1]) != self.finish:
								self.maze[current[0] - 1][current[1]] = 0.4

					if current[1] - 1 >= 0:
						if self.maze[current[0]][current[1] - 1] != -1:
							q.append((current[0], current[1] - 1))
							if (current[0], current[1] - 1) != self.finish:
								self.maze[current[0]][current[1] - 1] = 0.4
				visited.append(current)

		for i in range(7):
			for j in range(6):
				if self.maze[i][j] == 0.4:
					self.grid[i][j].config(bg='#FFDAB9')
					self.grid[i][j].config(text='P')
		self.grid[self.start[0]][self.start[1]].config(bg='#2E8B57')
		self.grid[self.start[0]][self.start[1]].config(text='1')
		self.bfs_button.config(state="disabled")
		self.dfs_button.config(state="disabled")

	def dfs(self):
		s = []
		s.append(self.start)
		visited = []
		while s:
			current = s.pop()
			if current == self.finish:
				break
			else: 
				if current not in visited:
							
					if current[1] + 1 <= 6 - 1:
						if self.maze[current[0]][current[1] + 1] != -1:
							s.append((current[0], current[1] + 1))
							if (current[0], current[1] + 1) != self.finish:
								self.maze[current[0]][current[1] + 1] = 0.4

					if current[1] - 1 >= 0:
						if self.maze[current[0]][current[1] - 1] != -1:
							s.append((current[0], current[1] - 1))
							if (current[0], current[1] - 1) != self.finish:
								self.maze[current[0]][current[1] - 1] = 0.4

					if current[0] - 1 >= 0: 
						if self.maze[current[0] - 1][current[1]] != -1:
							s.append((current[0] - 1, current[1]))
							if (current[0] - 1, current[1]) != self.finish:
								self.maze[current[0] - 1][current[1]] = 0.4

					if current[0] + 1 <= 7 - 1: 
						if self.maze[current[0] + 1][current[1]] != -1:
							s.append((current[0] + 1, current[1]))
							if (current[0] + 1, current[1]) != self.finish:
								self.maze[current[0] + 1][current[1]] = 0.4
			visited.append(current)

		for i in range(7):
			for j in range(6):
				if self.maze[i][j] == 0.4:
					self.grid[i][j].config(bg='#FFDAB9')
					self.grid[i][j].config(text='P')
		self.grid[self.start[0]][self.start[1]].config(bg='#2E8B57')
		self.grid[self.start[0]][self.start[1]].config(text='1')
		self.bfs_button.config(state="disabled")
		self.dfs_button.config(state="disabled")

if __name__ =='__main__':
	root = Maze()
	root.title('Nucleotic\'s Maze')
	root.geometry('500x500')
	style = ThemedStyle(root)
	style.set_theme('equilux')
	root.resizable(False, False)
	root.mainloop()