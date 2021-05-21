import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from queue import PriorityQueue
import threading
import time


class Maze(tk.Tk):
	def __init__(self):
		self.start = None
		self.finish = None
		self.blocked =  []
		self.maze = []
		self.grid = []
		self.visited = []
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
		self.a_star_button = ttk.Button(self, text="A*", command=self.a_star)
		self.a_star_button.place(relx=0.30, rely=0.6, relwidth=0.2)
		self.gbfs_button = ttk.Button(self, text="GBFS", command=self.gbfs)
		self.gbfs_button.place(relx=0.50, rely=0.6, relwidth=0.2)
		self.reset_button = ttk.Button(self, text="Reset", command=self.reset)
		self.reset_button.place(relx=0.30, rely=0.67, relwidth=0.2)
		self.simulate_button = ttk.Button(self, text="Simulate", state='disabled',command=self.simulate)
		self.simulate_button.place(relx=0.50, rely=0.67, relwidth=0.2)

	def generate_grid(self):
		for i in range(7):
			inner_grid = []
			inner_maze = []
			for j in range(12):
				g = tk.Button(self.base, text=0, height=1, width=3, background='#696969')
				g.bind('<Button-1>', lambda event, g=g, i=i, j=j: self.start_clicked(g, i, j))
				g.bind('<Button-3>', lambda event, g=g, i=i, j=j: self.finish_clicked(g, i, j))
				g.bind('<Shift-Button-1>', lambda event, g=g, i=i, j=j: self.blocked_clicked(g, i, j))
				g.grid(row=i, column=j)
				inner_grid.append(g)
				inner_maze.append([0, None])
			self.grid.append(inner_grid)
			self.maze.append(inner_maze)
		for gr in self.grid[0]:
			gr.grid(pady=(100, 0))
		for gr in self.grid:
			gr[0].grid(padx=(65, 0))
	
	def start_clicked(self, button: tk.Button, i: int, j: int):
		if self.start:
			print("Start Already Set")
		elif self.finish == (i, j):
			print("Start and Finish point cannot be same")
		elif not self.start:
			self.start = (i, j)
			button.config(bg='#2E8B57')
			button.config(text='1')
			self.maze[i][j][0] = 1

	def finish_clicked(self, button: tk.Button, i: int, j: int):
		if self.finish:
			print("Finish Already Set")
		elif self.start == (i, j):
			print("Start and Finish point cannot be same")
		elif not self.finish:
			self.finish = (i, j)
			button.config(bg='#DC143C')
			button.config(text='2')
			self.maze[i][j][0] = 1
	
	def blocked_clicked(self, button: tk.Button, i: int, j: int):
		self.blocked.append((i, j))
		button.config(bg='#4682B4')
		button.config(text='-1')
		self.maze[i][j][0] = -1

	def reset(self):
		self.maze = []
		self.grid = []
		self.blocked = []
		self.visited = []
		self.start = None
		self.finish = None
		self.a_star_button.config(state="normal")
		self.gbfs_button.config(state="normal")
		self.simulate_button.config(state='disabled')
		for widget in self.base.winfo_children():
			widget.destroy()
		self.generate_grid()

	def simulate(self):
		t = threading.Thread(target=self._simulate)
		t.setDaemon(True)
		t.start()

	def _simulate(self):
		# Generating Top level Window
		simulate_window = tk.Toplevel(self)
		simulate_window.geometry('500x300')
		sim_frame = ttk.Frame(simulate_window)
		sim_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
		
		# Generating Grid
		simulate_grid = []
		for i in range(7):
			inner_grid = []
			for j in range(12):
				g = tk.Button(sim_frame, text=0, height=1, width=3, background='#696969')
				g.grid(row=i, column=j)
				if self.maze[i][j][0] == -1:
					g.config(bg="#4682B4", text='-1')
				inner_grid.append(g)
			simulate_grid.append(inner_grid)
		for gr in simulate_grid[0]:
			gr.grid(pady=(70, 0))
		for gr in simulate_grid:
			gr[0].grid(padx=(65, 0))

		# Marking Start and Finish
		simulate_grid[self.start[0]][self.start[1]].config(bg='#2E8B57', text='start')
		simulate_grid[self.finish[0]][self.finish[1]].config(bg='#DC143C', text='stop')

		for node in self.visited:
			simulate_grid[node[0]][node[1]].config(bg='#FFDAB9', text='P')
			time.sleep(0.2)

	@staticmethod
	def get_heuristics(a, b):
		(x1, y1) = a
		(x2, y2) = b
		return abs(x1-x2) + abs(y1-y2)

	def gbfs(self):
		if not self.start and not self.finish:
			return
		opened = PriorityQueue()
		visited = []
		cost = 0
		estimation = Maze.get_heuristics(self.start, self.finish)
		opened.put((estimation, self.start))
		while not opened.empty():
			estimation, dequeued_node = opened.get()
			self.grid[dequeued_node[0]][dequeued_node[1]].config(text=estimation)
			self.grid[dequeued_node[0]][dequeued_node[1]].config(bg='#FFDAB9')
			# print(f'{dequeued_node=}')
			if dequeued_node == self.finish:
				break
			else:
				if dequeued_node not in visited:
					if dequeued_node[1] + 1<=12-1 and self.maze[dequeued_node[0]][dequeued_node[1] + 1][0] != -1:
						estimation = Maze.get_heuristics((dequeued_node[0], dequeued_node[1]+1), self.finish)
						opened.put((estimation, (dequeued_node[0], dequeued_node[1]+1)))
					if dequeued_node[1] - 1 >= 0 and self.maze[dequeued_node[0]][dequeued_node[1] - 1][0] != -1:
						estimation = Maze.get_heuristics((dequeued_node[0], dequeued_node[1]-1), self.finish)
						opened.put((estimation, (dequeued_node[0], dequeued_node[1]-1)))
					if dequeued_node[0] - 1 >= 0 and self.maze[dequeued_node[0] - 1][dequeued_node[1]][0] != -1:
						estimation = Maze.get_heuristics((dequeued_node[0]-1, dequeued_node[1]), self.finish)
						opened.put((estimation, (dequeued_node[0]-1, dequeued_node[1])))
					if dequeued_node[0] + 1<=7-1 and self.maze[dequeued_node[0] + 1][dequeued_node[1]][0] != -1:
						estimation = Maze.get_heuristics((dequeued_node[0]+1, dequeued_node[1]), self.finish)
						opened.put((estimation, (dequeued_node[0]+1, dequeued_node[1])))
					visited.append(dequeued_node)
					cost += 1
		
		self.visited = visited
		self.grid[self.start[0]][self.start[1]].config(bg='#2E8B57')
		self.grid[self.start[0]][self.start[1]].config(text='start')
		self.grid[self.finish[0]][self.finish[1]].config(bg='#DC143C')
		self.grid[self.finish[0]][self.finish[1]].config(text='stop')
		self.a_star_button.config(state="disabled")
		self.gbfs_button.config(state="disabled")
		self.simulate_button.config(state='normal')

	def a_star(self):
		if not self.start and not self.finish:
			return
		opened = PriorityQueue()
		visited = []
		self.maze[self.start[0]][self.start[1]][1] = 0
		estimation = Maze.get_heuristics(self.start, self.finish) + 0
		opened.put((estimation, self.start))
		while not opened.empty():
			estimation, dequeued_node = opened.get()
			self.grid[dequeued_node[0]][dequeued_node[1]].config(bg='#FFDAB9')
			self.grid[dequeued_node[0]][dequeued_node[1]].config(text=estimation)
			if dequeued_node == self.finish:
				break
			else:
				if dequeued_node not in visited:
					# Directions
					current_g = self.maze[dequeued_node[0]][dequeued_node[1]][1]
					left, right, down, up = None, None, None, None
					if dequeued_node[0] - 1 >= 0:
						left = self.maze[dequeued_node[0] - 1][dequeued_node[1]]
					if dequeued_node[0] + 1<=7-1:
						right = self.maze[dequeued_node[0] + 1][dequeued_node[1]]
					if dequeued_node[1] + 1<=12-1:
						up = self.maze[dequeued_node[0]][dequeued_node[1] + 1]
					if dequeued_node[1] - 1 >= 0:
						down = self.maze[dequeued_node[0]][dequeued_node[1] - 1]
					# Comparison
					if left and left[0] != -1:
						if not left[1]:
							new_g = current_g + 1
							left[1] = new_g
						estimation = Maze.get_heuristics((dequeued_node[0]-1, dequeued_node[1]), self.finish) + left[1]
						opened.put((estimation, (dequeued_node[0]-1, dequeued_node[1])))
					if right and right[0] != -1:
						if not right[1]:
							new_g = current_g + 1
							right[1] = new_g
						estimation = Maze.get_heuristics((dequeued_node[0]+1, dequeued_node[1]), self.finish) + right[1]
						opened.put((estimation, (dequeued_node[0]+1, dequeued_node[1])))
					if up and up[0] != -1:
						if not up[1]:
							new_g = current_g + 1
							up[1] = new_g
						estimation = Maze.get_heuristics((dequeued_node[0], dequeued_node[1]+1), self.finish) + up[1]
						opened.put((estimation, (dequeued_node[0], dequeued_node[1]+1)))
					if down and down[0] != -1:
						if not down[1]:
							new_g = current_g + 1
							down[1] = new_g
						estimation = Maze.get_heuristics((dequeued_node[0], dequeued_node[1]-1), self.finish) + down[1]
						opened.put((estimation, (dequeued_node[0], dequeued_node[1]-1)))
					visited.append(dequeued_node)

		self.visited = visited
		self.grid[self.start[0]][self.start[1]].config(bg='#2E8B57')
		self.grid[self.start[0]][self.start[1]].config(text='start')
		self.grid[self.finish[0]][self.finish[1]].config(bg='#DC143C')
		self.grid[self.finish[0]][self.finish[1]].config(text='stop')
		self.a_star_button.config(state="disabled")
		self.gbfs_button.config(state="disabled")
		self.simulate_button.config(state='normal')

if __name__ =='__main__':
	root = Maze()
	root.title('Nucleotic\'s Maze')
	root.geometry('500x500')
	style = ThemedStyle(root)
	style.set_theme('equilux')
	root.resizable(False, False)
	root.mainloop()