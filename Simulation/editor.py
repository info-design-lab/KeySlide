import math
import numpy as np 


class Editor(object):
	'''
	A virtual editor class
	'''
	def __init__(self, size=[30, 10], cursor=[0, 0]):
		self.size = size
		self.cursorPos = cursor
		self.marker = None
		self.columnWidth = 10
		self.rowHeight = 25
		self.keyboardActions = [
	    	"right_arrow", "left_arrow", "up_arrow", "down_arrow", 
	    	"eol", # end of line
	    	"bol", # beginning of line
	    	"text_bottom", # bottom of text entry field
	    	"text_top", # top of text entry field
	    	"word_jump_right",
	    	"word_jump_left"
	    	]

		self.keySlideActions = [
			"right_arrow", "left_arrow", "up_arrow", "down_arrow", 
	    ]
		self.keySlideSpeed = 1.9 # average speed of Keyslide Cursor

		self.keyCoord = {"Tilda": {"x": 0.0, "y": 0.0}, "Digit1": {"x": 37.72, "y": 0.0}, "Digit2": {"x": 75.39, "y": 0.0}, "Digit3": {"x": 113.008, "y": 0.0}, "Digit4": {"x": 150.658, "y": 0.0}, "Digit5": {"x": 188.308, "y": 0.0}, "Digit6": {"x": 225.958, "y": 0.0}, "Digit7": {"x": 263.608, "y": 0.0}, "Digit8": {"x": 301.258, "y": 0.0}, "Digit9": {"x": 338.908, "y": 0.0}, "Digit0": {"x": 376.558, "y": 0.0}, "Minus": {"x": 414.208, "y": 0.0}, "Equal": {"x": 451.858, "y": 0.0}, "KeyQ": {"x": 56.533, "y": -36.76}, "KeyW": {"x": 94.222, "y": -36.76}, "KeyE": {"x": 131.872, "y": -36.76}, "KeyR": {"x": 169.522, "y": -36.76}, "KeyT": {"x": 207.172, "y": -36.76}, "KeyY": {"x": 244.822, "y": -36.76}, "KeyU": {"x": 282.472, "y": -36.76}, "KeyI": {"x": 320.122, "y": -36.76}, "KeyO": {"x": 357.772, "y": -36.76}, "KeyP": {"x": 395.422, "y": -36.76}, "BracketLeft": {"x": 433.072, "y": -36.76}, "BracketRight": {"x": 470.722, "y": -36.76}, "Backslash": {"x": 508.372, "y": -36.76}, "KeyA": {"x": 65.984, "y": -73.472}, "KeyS": {"x": 103.629, "y": -73.472}, "KeyD": {"x": 141.129, "y": -73.472}, "KeyF": {"x": 178.629, "y": -73.472}, "KeyG": {"x": 216.129, "y": -73.472}, "KeyH": {"x": 253.629, "y": -73.472}, "KeyJ": {"x": 291.129, "y": -73.472}, "KeyK": {"x": 328.629, "y": -73.472}, "KeyL": {"x": 366.129, "y": -73.472}, "Semicolon": {"x": 403.629, "y": -73.472}, "besideColon": {"x": 441.129, "y": -73.472}, "KeyZ": {"x": 84.793, "y": -109.565}, "KeyX": {"x": 122.293, "y": -109.565}, "KeyC": {"x": 159.793, "y": -109.565}, "KeyV": {"x": 197.293, "y": -109.565}, "KeyB": {"x": 234.793, "y": -109.565}, "KeyN": {"x": 272.293, "y": -109.565}, "KeyM": {"x": 309.793, "y": -109.565}, "Comma": {"x": 347.293, "y": -109.565}, "Period": {"x": 384.793, "y": -109.565}, "Slash": {"x": 422.293, "y": -109.565}}
		self.keyWidth = 35 
		self.keyHeight = 34 
		self.displayDebug = True # doesnt display text if true

		self.columnRanges = [] # length of text in each column
		self.text = None # text of the entire text document
		self.rowText = [] 
		for i in range(self.size[1]):
	   		self.rowText.append("|"*self.size[0])

	def setCursor(self, pos):
		self.cursorPos = pos
		if pos[0] < 0 or pos[1] < 0:
			if pos[1] < 0:
				self.cursorPos[1] = 0
			if pos[0] < 0:
				self.cursorPos[0] = 0
		if pos[1] > self.size[1] - 1:
			self.cursorPos[1] = self.size[1] - 1
		if pos[0] > self.columnRanges[self.cursorPos[1]] - 1:
			self.cursorPos[0] = self.columnRanges[self.cursorPos[1]] - 1
		return self.cursorPos

	def setMarker(self, pos=[0, 0]):
		self.marker = pos
		if pos[1] > self.size[1] - 1:
			self.marker[1] = self.size[1] - 1
		if pos[0] > self.columnRanges[self.marker[1]] - 1:
			self.marker[0] = self.columnRanges[self.marker[1]] - 1
		return self.marker

	def getMarker(self):
		return self.marker

	def keyboardActionSpace(self):
		return self.keyboardActions

	def keyslideActionSpace(self):
		return self.keySlideActions

	def markerCursorDist(self):
		dx = self.cursorPos[0] - self.marker[0]
		dy = self.cursorPos[1] - self.marker[1]
		return math.sqrt(dx*dx + dy*dy)

	def getActionReward(self, a):
		# returns the reward by an action without changing
		# the actual cursor position
		c = self.cursorPos
		self.performAction(a)
		reward = self.markerCursorDist()
		self.cursorPos = c
		return reward

	def performAction(self, a):
		if a == "right_arrow":
			self.right_arrow()
		elif a == "left_arrow":
			self.left_arrow()
		elif a == "up_arrow":
			self.up_arrow()
		elif a == "down_arrow":
			self.down_arrow()
		elif a == "eol":
			self.eol()
		elif a == "bol":
			self.bol()
		elif a == "text_bottom":
			self.text_bottom()
		elif a == "text_top":
			self.text_top()
		elif a == "word_jump_right":
			self.word_jump_right()
		elif a == "word_jump_left":
			self.word_jump_left()
		elif a == "keySlide":
			c, t = self.keySlide()
			self.setCursor(c)
		else:
			raise Exception("Invalid Action " + a)

	def display(self):
		for i in range(len(self.rowText)):
			s = ""
			for j in range(self.columnRanges[i]):
				if j == self.cursorPos[0] and i == self.cursorPos[1]:
					s += "X"
				elif not self.displayDebug:
					s += self.rowText[i][j]
				elif self.displayDebug:
					s += "_"

				if self.marker:
					if j == self.marker[0] and i == self.marker[1]:
						s = s[:-1]
						s += "*"
			print(s)

	def setText(self, t):
		self.text = t.split()
		self.setColumnRanges()

	def setColumnRanges(self):
		self.columnRanges = []

		row = 0
		col = 0
		string = ""
		for i in self.text:
			if col + len(i) > self.size[0]:
				self.columnRanges.append(col - 1)
				self.rowText[row] = string + " "*(self.size[0] - len(string))

				col = 0
				row += 1
				string = ""

				if row > self.size[1] - 1:
					break

			col += len(i) + 1
			string += i + " "

	def right_arrow(self):
		col, row = self.cursorPos

		if col == self.columnRanges[row] - 1:
			if row == len(self.columnRanges) - 1:
				return
			col = 0
			row += 1
		else: 
			col += 1

		self.cursorPos = [col, row]

	def left_arrow(self):
		col, row = self.cursorPos

		if col == 0:
			if row == 0:
				return
			else: 
				row -= 1
				col = self.columnRanges[row] - 1
		else:
			col -= 1				

		self.cursorPos = [col, row]

	def up_arrow(self):
		col, row = self.cursorPos
		if row == 0:
			col = 0
		else:
			row -= 1
			if self.columnRanges[row] - 1 < col:
				col = self.columnRanges[row] - 1

		self.cursorPos = [col, row]
		

	def down_arrow(self):
		col, row = self.cursorPos

		if row == len(self.columnRanges) - 1:
			col = self.columnRanges[row] - 1
		else:
			row += 1
			if self.columnRanges[row] - 1 < col:
				col = self.columnRanges[row] - 1

		self.cursorPos = [col, row]

	def eol(self):
		col, row = self.cursorPos
		col = self.columnRanges[row] - 1 
		self.cursorPos = [col, row]

	def bol(self):
		col, row = self.cursorPos
		col = 0
		self.cursorPos = [col, row]

	def text_bottom(self):
		row = len(self.columnRanges) - 1
		col = self.columnRanges[row] - 1 
		self.cursorPos = [col, row]

	def text_top(self):
		self.cursorPos = [0, 0]

	def word_jump_right(self):
		self.right_arrow()
		col, row = self.cursorPos

		while self.rowText[row][col] != " ":
			self.right_arrow()
			col, row = self.cursorPos

			if row == len(self.columnRanges) - 1 and col == self.columnRanges[row] - 1:
				break

	def word_jump_left(self):
		self.left_arrow()
		col, row = self.cursorPos

		while self.rowText[row][col] != " ":
			self.left_arrow()
			col, row = self.cursorPos

			if row == 0 and col == 0:
				break

	def keySlide(self):
		Mx = (self.marker[0] - self.cursorPos[0])*self.columnWidth
		My = (self.marker[1] - self.cursorPos[1])*self.rowHeight

		norm = math.sqrt(Mx*Mx + My*My)
		Mx = Mx/norm
		My = My/norm
		
		keys = []
		if Mx > 0 and My > 0:
			# top left to bottom right
			keys = self.getKeyslideKeys("Digit3", Mx, My)
		elif Mx > 0 and My < 0:
			# bottom left to top right
			keys = self.getKeyslideKeys("KeyZ", Mx, My)
		elif Mx < 0 and My > 0:
			# top right to bottom left
			keys = self.getKeyslideKeys("Digit8", Mx, My)
		elif Mx < 0 and My < 0:
			# bottom right to top left
			keys = self.getKeyslideKeys("KeyM", Mx, My)
		else:
			if Mx > 0:
				keys = ['KeyA', 'KeyS', 'KeyD', 'KeyF', 'KeyG', 'KeyH']
			else:
				keys = ['KeyH', 'KeyG', 'KeyF', 'KeyD', 'KeyS', 'KeyA']

		slope = self.calculateSlope(keys)
		cursor, time = self.pointProjectionOnLine(slope)
		time = max(time, len(keys)*50)
		return cursor, time

	def getKeyslideKeys(self, key, Mx, My):
		rectMaxDist = self.dist(0, 0, self.keyWidth/2, self.keyHeight/2) + 15
		startKey = self.keyCoord[key]

		pressedKeys = []
		for i in self.keyCoord:
			# get intersection of line with all the keys
			a = {'x': self.keyCoord[i]['x'] - startKey['x'], 'y': self.keyCoord[i]['y'] - startKey['y']}
			a_ = [a['x'], -a['y'], 0]
			b_ = [Mx, My, 0]
			perpendDist = np.cross(a_, b_)[2]

			if perpendDist < 0:
				continue
			elif perpendDist > rectMaxDist:
				continue
			else:
				pressedKeys.append(i)

		pressedKeys.sort(key= lambda x: self.dist(self.keyCoord[x]['x'], self.keyCoord[x]['y'], startKey['x'], startKey['y']))
		return pressedKeys

	def calculateSlope(self, keys):
		# caluclate the slope based on the key coordinates
		if(len(keys) > 1):
			thetas = []
			weights = []

			for i in range(1, len(keys)):
				thetas.append(math.atan2(
					self.keyCoord[keys[i]]['y'] - self.keyCoord[keys[0]]['y'], 
					self.keyCoord[keys[i]]['x'] - self.keyCoord[keys[0]]['x']
					))
				weights.append(i/len(keys))
			
			num = 0
			denom = 0

			for i in range(len(thetas)):
				num += thetas[i]*weights[i]
				denom += weights[i]

			t = num/denom

			Mx = math.cos(t)
			My = math.sin(t)

			norm = math.sqrt(Mx*Mx + My*My)
			Mx = Mx/norm
			My = My/norm

			return [Mx, My]

	def pointProjectionOnLine(self, slope):
		# calculates the projection of target point on
		# the line from the cursor position with give slope
		col, row = self.cursorPos
		a = [
			(self.marker[0] - col)*self.columnWidth,
			-(self.marker[1] - row)*self.rowHeight,
		]

		projection = a[0]*slope[0] + a[1]*slope[1]

		col += projection*slope[0]/self.columnWidth
		row -= projection*slope[1]/self.rowHeight

		time = projection/self.keySlideSpeed

		return [round(col), round(row)], time

	def dist(self, x1, y1, x2, y2):
		dx = x2 - x1
		dy = y2 - y1
		return math.sqrt(dx*dx + dy*dy)
