#!/usr/bin/python
import sys, re, copy
from pprint import pprint

class Cell():
	def __init__(self, value):
		self.value = value
		self.maybe = [1,2,3,4,5,6,7,8,9] if self.value == 0 else None

class Sudoku():
	def __init__(self):
		self.checkInputs()
		self.rows = self.createRows()
		self.columns = self.createColumns()
		self.boxes = self.createBoxes()
		self.buckets = [self.rows, self.columns, self.boxes]

	def checkInputs(self):
		for i in range(1, 10):
			row = str(sys.argv[i])
			letters = re.search(r'\D+', row)
			if len(row) != 9 or letters != None:
				print "This parameter needs 9 numeric digits:", sys.argv[i]
			else: pass
	
	def createRows(self):
		row_data = [ str(sys.argv[i]) for i in range(1, 10) ]
		ints = [ [ int(row[i]) for i in range(9) ] for row in row_data ]
		rows = [ [ Cell(value) for value in row ] for row in ints ]
		return rows
	def createColumns(self):
		columns = [ [ row[i] for row in self.rows ] for i in range(9) ]
		return columns
	def createBoxes(self):
		def createBox(i, rows):
			if   0 <= i <= 2: m = 0
			elif 3 <= i <= 5: m = 3
			elif 6 <= i <= 8: m = 6
			if   i % 3 == 0:  n = 0
			elif i % 3 == 1:  n = 3
			elif i % 3 == 2:  n = 6
			box = ( rows[ 0+m ][ 0+n : 3+n ] +
				rows[ 1+m ][ 0+n : 3+n ] +
				rows[ 2+m ][ 0+n : 3+n ] )
			return box
		boxes = [ createBox(i, self.rows) for i in range(9) ]
		return boxes

##########
	def updateValue(self, cell, v):
		cell.value = v
		cell.maybe = None
		self.updateMaybes(cell, v)
	def updateMaybes(self, the_cell, v):
		for bucket in self.buckets:
			for container in bucket:
				if the_cell in container:
					other_cells = [ c for c in container if c != the_cell ]
					for cell in other_cells:
						if cell.maybe != None:
							cell.maybe = [ p for p in cell.maybe if p != v ]

##########
	def eliminatePossibilities(self):
		possibility_reductions = 0
		for bucket in self.buckets:
			for container in bucket:
				for cell in container:
					if cell.value == 0:
						i = container.index(cell)
						other_cells = container[:i] + container[i+1:]
						other_vals = [ c.value for c in other_cells ]
						original = len(cell.maybe)
						cell.maybe = [ p for p in cell.maybe if p not in other_vals ]
						final = len(cell.maybe)
						if len(cell.maybe) == 1:
							self.updateValue(cell, cell.maybe[0])
						if original != final: 
							possibility_reductions += 1
					else: pass
		if possibility_reductions > 0:
			self.findSharedPossibilities()
			self.eliminatePossibilities()

##########
	def isolatePossibilities(self):
		
		#@@@@
		def updateSingleNumberPossibility(self, i, cont):
			#print "test 1"
			#print [ c for c in cont if c.maybe!= None and i in c.maybe ]
			the_cell = [ c for c in cont if c.maybe!= None and i in c.maybe ][0]
			self.updateValue(the_cell, i)

		values_added = 0
		for bucket in self.buckets:
			for container in bucket:
				for i in range(1, 10):
					maybes = [ cell.maybe for cell in container ]
					maybes_with_i = [ mb for mb in maybes if mb != None and i in mb ]
					possibilities_with_i = len(maybes_with_i)
					if possibilities_with_i == 1:
						updateSingleNumberPossibility(self, i, container)
						values_added += 1
		if values_added > 0:
			self.findSharedPossibilities()
			self.isolatePossibilities()

##########
	def findSharedPossibilities(self, initial=None):
		
		#@@@@
		def isSharedMaybe(i, cells):
			sharers = [ c for c in cells if c.maybe != None and i in c.maybe ]
			if 2 <= len(sharers) <= 3: return sharers
			else: return None

		#@@@@
		def cutOtherMaybes(self, n, sharers, cells):
			#$$$$
			def eliminate(i, sharers, cells):
				others = [ c for c in cells if c not in sharers ]
				filtered = [ c for c in others if c.maybe!=None and i in c.maybe ]
				for cell in filtered:
					cell.maybe = [ p for p in cell.maybe if p != i ]
					if len(cell.maybe) == 1:
						self.updateValue(cell, cell.maybe[0])
			for bucket in self.buckets:
				for container in bucket:
					all_present = all( [ c in container for c in sharers ] )
					if container != cells and all_present:
						eliminate(i, sharers, container)

		for bucket in self.buckets:
			for container in bucket:
				for i in range(1, 10):
					sharers = isSharedMaybe(i, container)
					if sharers:
						cutOtherMaybes(self, i, sharers, container)
		final = self.checkBoard(to_print=False)
		if initial != final:
			self.findSharedPossibilities(initial=final)

##########
	def doTrialAndError(self):

		#@@@@
		def makeExpanded(self, cell):
			for i in range(9):
				for j in range(9):
					if self.buckets[0][i][j] == cell:
						return cell.value, cell.maybe, i, j

		self.asc_val = copy.deepcopy(self.buckets) # asc_val = ascertained
		# pick out blank cells with only 2 possible candidate values
		cells = [ c for row in self.buckets[0] for c in row ]
		candidates = [ c for c in cells if c.maybe!= None and len(c.maybe)==2 ]
		candidates_copy = copy.deepcopy(candidates)
		expanded = [ makeExpanded(self, c) for c in candidates ]
		for c in expanded:
			for p in c[1]:
				self.updateValue(self.buckets[0][ c[2] ][ c[3] ], p)
				does_it_work = self.solve(trial_and_error=True)
				if does_it_work == False or does_it_work == None:
					self.buckets = copy.deepcopy(self.asc_val)
				else:
					return

##########
	def checkBoard(self, to_print=False):
		values = [ [ cell.value for cell in row ] for row in self.buckets[0] ]
		maybes = [ [ cell.maybe for cell in row ] for row in self.buckets[0] ]
		if to_print: pprint(values)
		return values, maybes

##########
	def solve(self, start=None, trial_and_error=False):
		solving_message = "Solving... hmm... B("
		victory_message = "I'M FINISHED!!!!!!!!!  Vn_n"
		trial_and_error_message = "I'm stuck!  Now trial-and-error...  @_@"
		try_again_message = "Gah!  Got stuck!  Gonna try again...  >_<"

		#@@@@
		def isDone(self):
			values = [ cell.value for row in self.buckets[0] for cell in row ]
			if 0 not in values: return True
			else: return False
				
		#@@@@
		def checkForMistakes(self, to_print=False, trial_and_error=False):
			mistake_message = "Mistakes were made.  T-T"
			for bucket in self.buckets:
			 	for container in bucket:
					values = [ cell.value for cell in container ]
					if not trial_and_error:
						if not all( [ i in values for i in range(1, 10) ] ):
							if to_print: print mistake_message
							return False
					else:
						for i in range(1, 10):
							value_count = len([ v for v in values if v == i ])
							if value_count > 1:
								if to_print: print mistake_message
								return False
			if to_print: print "No mistakes made!  :)"
			return True

		print solving_message
		print "BEFORE"
		self.checkBoard(to_print=True)
		self.eliminatePossibilities()
		self.isolatePossibilities()
		checkForMistakes(self, trial_and_error=False)
		end = self.checkBoard(to_print=True)
		if isDone(self):
			checkForMistakes(self, to_print=True, 
				trial_and_error=trial_and_error)
			print victory_message
			if trial_and_error: return True
		elif start != end and not trial_and_error:
			self.solve(start=end)
		elif start != end and trial_and_error:
			self.solve(start=end, trial_and_error=True)
		elif start == end and not trial_and_error:
			print trial_and_error_message
			self.doTrialAndError()
		elif start == end and trial_and_error:
			print try_again_message
			return False

##########
##########
##########

if __name__ == '__main__':
	sudoku = Sudoku()
	sudoku.solve()
	print "done"
	sys.exit()
