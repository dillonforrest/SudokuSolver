'''
Sudoku solver by Dillon Forrest.
Solves easy puzzles on www.websudoku.com
30 July 2012
'''

#!/usr/bin/python
import sys, re
from pprint import pprint

class Cell():
	_registry = []
	def __init__(self, value):
		self._registry.append(self)
		self.value = value
		self.maybe = [1,2,3,4,5,6,7,8,9] if self.value == 0 else None

class Row():
	_registry = []
	def __init__(self, large_number):
		self._registry.append(self)
		self.cells = self.createRow(large_number)
	def createRow(self, large_number):
		large_string = str(large_number)
		row_values = [ int(large_string[i]) for i in range(9) ]
		row = [ Cell(value) for value in row_values ]
		return row

class Column():
	_registry = []
	def __init__(self, rows, position):
		self._registry.append(self)
		self.cells = self.createColumn(rows, position)
	def createColumn(self, rows, pos):
		column = [ row.cells[pos] for row in rows ]
		return column

class Box():
	_registry = []
	def __init__(self, rows, i):
		self._registry.append(self)
		self.cells = self.createBox(rows, i)
	def createBox(self, rows, i):
		if   0 <= i <= 2: m = 0
		elif 3 <= i <= 5: m = 3
		elif 6 <= i <= 8: m = 6

		if   i % 3 == 0:  n = 0
		elif i % 3 == 1:  n = 3
		elif i % 3 == 2:  n = 6

		box = ( rows[ 0+m ].cells[ 0+n : 3+n] +
			rows[ 1+m ].cells[ 0+n : 3+n ] +
			rows[ 2+m ].cells[ 0+n : 3+n ] )
		return box

class Sudoku():
	def __init__(self):
		self.checkInputs()
		self.rows = self.createRows()
		self.columns = self.createColumns()
		self.boxes = self.createBoxes()
		self.buckets = [self.rows, self.columns, self.boxes]
	
	def checkInputs(self):
		for i in range(1,10):
			row = str(sys.argv[i])
			letters = re.search(r'\D+', row)
			if len(row) != 9 or letters != None:
				print "This parameter needs 9 numeric digits:", sys.argv[i]
			else: pass

	def createRows(self):
		rows_raw_data = [ sys.argv[i] for i in range(1,10) ]
		rows = [ Row(row) for row in rows_raw_data ]
		return rows
	def createColumns(self):
		columns = [ Column(self.rows, i) for i in range(9) ]
		return columns
	def createBoxes(self):
		boxes = [ Box(self.rows, i) for i in range(9) ]
		return boxes

	def solve(self):
		while True:
			self.eliminatePossibilities()
			self.isolatePossibilities()
			self.printResults()
			if self.isDone():
				self.madeMistakes()
				break					
			else:
				print "Still solving..."
				
	def updateMaybes(self, the_cell, v):
		for bucket in self.buckets:
			for container in bucket:
				if the_cell in container.cells:
					for cell in container.cells:
						if cell.maybe != None:
							cell.maybe = [ p for p in cell.maybe if p != v ]

	def updateValue(self, cell, v):
		cell.value = v
		cell.maybe = None
		self.updateMaybes(cell, v)

	def eliminatePossibilities(self):
		possibility_reductions = 0
		for bucket in self.buckets:
			for container in bucket:
				for cell in container.cells:
					if cell.value == 0:
						i = container.cells.index(cell)
						temp = container.cells[:i] + container.cells[i+1:]
						others = [ c.value for c in temp ]
						original = len(cell.maybe)
						cell.maybe = [ p for p in cell.maybe if p not in others ]
						final = len(cell.maybe)
						if len(cell.maybe) == 1:
							self.updateValue(cell, cell.maybe[0])
						if original != final: possibility_reductions += 1
					else: pass
		if possibility_reductions > 0:
			return self.eliminatePossibilities()

	def isolatePossibilities(self):
		values_added = 0
		for bucket in self.buckets:
			for container in bucket:
				maybes = [ cell.maybe for cell in container.cells ]
				for i in range(1, 10):
					maybes_with_i = [ mb for mb in maybes if mb != None and i in mb ]
					possibilities_of_i = len( maybes_with_i )
					if possibilities_of_i == 1:
						self.updateSingleNumberPossibility(i, container)
						values_added += 1
						break
		if values_added > 0:
			return self.isolatePossibilities()
	
	def updateSingleNumberPossibility(self, i, container):
		the_cell = [ cell for cell in container.cells \
			if cell.maybe != None and i in cell.maybe ][0]
		self.updateValue(the_cell, i)

	def isDone(self):
		values = [ cell.value for row in self.rows for cell in row.cells ]
		if 0 not in values: return True
		else: return False

	def printResults(self):
		results = [ [cell.value for cell in row.cells] for row in self.rows]
		pprint(results)
	
	def madeMistakes(self):
		for bucket in self.buckets:
			for container in bucket:
				values = [ cells.value for cells in container.cells ]
				for i in range(1, 10):
					if i not in values:
						print "Made some mistakes.  :("
						return True
		print "No mistakes made!  :)"
		return False

if __name__ == '__main__':
	sudoku = Sudoku()
	sudoku.solve()
	print "done"
	sys.exit()
