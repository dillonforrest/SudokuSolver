'''
Sudoku solver by Dillon Forrest.
Supposed to solve  puzzles on www.websudoku.com, but presently incomplete.
31 July 2012
'''

#!/usr/bin/python
import sys, re, copy
from pprint import pprint

class Cell():
	def __init__(self, value):
		self.value = value
		self.maybe = [1,2,3,4,5,6,7,8,9] if self.value == 0 else None

class Row():
	def __init__(self, large_number):
		def createRow(self, large_number):
			large_string = str(large_number)
			row_values = [ int(large_string[i]) for i in range(9) ]
			row = [ Cell(value) for value in row_values ]
			return row
		self.cells = createRow(self, large_number)

class Column():
	def __init__(self, rows, position):
		def createColumn(self, rows, pos):
			column = [ row.cells[pos] for row in rows ]
			return column
		self.cells = createColumn(self, rows, position)

class Box():
	def __init__(self, rows, i):
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
		
		self.cells = createBox(self, rows, i)

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

##########
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

##########
	def isolatePossibilities(self):
		
		def updateSingleNumberPossibility(self, i, container):
			the_cell = [ cell for cell in container.cells \
				if cell.maybe != None and i in cell.maybe ][0]
			self.updateValue(the_cell, i)

		values_added = 0
		for bucket in self.buckets:
			for container in bucket:
				maybes = [ cell.maybe for cell in container.cells ]
				for i in range(1, 10):
					maybes_with_i = [ mb for mb in maybes if mb != None and i in mb ]
					possibilities_of_i = len( maybes_with_i )
					if possibilities_of_i == 1:
						updateSingleNumberPossibility(self, i, container)
						values_added += 1
						break
		if values_added > 0:
			return self.isolatePossibilities()

##########
	def findSharedPossibilities(self, initial=None):
		
		def isSharedMaybe(n, cells):
			sharers = [ c for c in cells if c.maybe != None and n in c.maybe ]
			if 2 <= len(sharers) <= 3: return sharers
			else:	return None

		def cutOtherMaybes(self, n, sharers, cells):
			def eliminate(n, sharers, cells):
				for cell in cells:
					if cell not in sharers and cell.maybe!=None and n in cell.maybe:
						shared_maybes = [ c.maybe for c in sharers ]
						cell.maybe = [ p for p in cell.maybe if p != n ]
						if len(cell.maybe) == 1:
							self.updateValue(cell, cell.maybe[0])
			for bucket in self.buckets:
				for container in bucket:
					all_present = all( [ c in container.cells for c in sharers ] )
					if container.cells != cells and all_present:
						eliminate(n, sharers, container.cells)


		for bucket in self.buckets:
			for container in bucket:
				for n in range(1, 10):
					sharers = isSharedMaybe(n, container.cells)
					if sharers:
						cutOtherMaybes(self, n, sharers, container.cells)
		final = self.checkBoard()
		if initial != final:
			return self.findSharedPossibilities(initial=final)

##########
	def doTrialAndError(self):
		self.ascertained_values = self.makeCopy(self.buckets)
		# pick out blank cells with only 2 possible candidate values
		candidates = [ c for row in self.buckets[0] \
			for c in row.cells if c.maybe!=None and len(c.maybe) == 2 ]
		marker = [ copy.deepcopy(c) for c in candidates ]
		pprint( [c.maybe for c in candidates] )
		for i in range(len(candidates)):
			for p in marker[i].maybe:
				pprint( [ c.maybe for c in marker ] )
				if self.solve(trial_and_error=True): return
				self.buckets = self.makeCopy(self.ascertained_values)

##########
	def makeCopy(self, buckets):
		all_cells = [copy.deepcopy(c) for row in buckets[0] for c in row.cells]
		all_cells = [ [ all_cells[i*9:(i+1)*9] ] for i in range(9) ]
		pprint(all_cells)
		rows = [ Row(123456789) for _ in range(9) ]
		for i in range(9):
			rows[i].cells = all_cells[i*9:(i+1)*9]
		columns = [ Column(rows, i) for i in range(9) ]
		boxes = [ Box(rows, i) for i in range(9) ]
		new_copy = [rows, columns, boxes]
		return new_copy

##########
	def checkBoard(self, to_print=False):
		numbers = [ [cell.value for cell in row.cells] for row in self.rows]
		maybes = [ [cell.maybe for cell in row.cells] for row in self.rows]
		if to_print: pprint(numbers)
		return numbers, maybes
	
##########
	def solve(self, initials=None, trial_and_error=False):
		
		def isDone(self):
			values = [ cell.value for row in self.rows for cell in row.cells ]
			if 0 not in values: return True
			else: return False

		def isMistake(self):
			for bucket in self.buckets:
				for container in bucket:
					values = [ cell.value for cell in container.cells ]
					for i in range(1, 10):
						number_count = [ v for v in values if v == i ]
						if len(number_count) > 1:
							print "Made some mistakes.  :("
							return True
			print "No mistakes made!  :)"
			return False

		self.eliminatePossibilities()
		self.isolatePossibilities()
		self.findSharedPossibilities()
		finals = self.checkBoard(to_print=True)
		if isMistake(self):
			if not trial_and_error:
				sys.exit()
			else:
				print "Trying something new... blarghh... @_@"
				return
		if isDone(self):
			print "I'M FINISHED!!!!!!! Vn_n"
			if not trial_and_error: return
			else: 
				return True
		else:
			if initials == finals:
				print "Got stuck!  I couldn't fill any blanks!  :("
				if not trial_and_error:
					print "Running by trial and error now... gahhh... >_<"
					self.doTrialAndError()
				else:
					print "Trying something new... blarghh... @_@"
					return
			else:
				print "Still solving... hm... B("
				return self.solve(initials = finals, 
					trial_and_error=trial_and_error)

if __name__ == '__main__':
	sudoku = Sudoku()
	sudoku.solve()
	print "done"
	sys.exit()
