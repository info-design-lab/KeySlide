from editor import Editor
import time 
from random import randint
import math
import json
import random

editor = Editor(size=[120, 100]) # '13 macbook pro sizes
ShowSimulation = False

text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Vitae turpis massa sed elementum tempus egestas sed. Sagittis aliquam malesuada bibendum arcu vitae elementum curabitur vitae. Sit amet commodo nulla facilisi nullam vehicula ipsum a arcu. Scelerisque in dictum non consectetur a erat nam at lectus. Sit amet massa vitae tortor condimentum lacinia quis vel. Nisl suscipit adipiscing bibendum est. Ullamcorper velit sed ullamcorper morbi tincidunt ornare massa. Risus quis varius quam quisque id diam. Diam ut venenatis tellus in. Eu consequat ac felis donec et odio pellentesque diam. Sagittis id consectetur purus ut faucibus pulvinar elementum. Et netus et malesuada fames. Sed turpis tincidunt id aliquet risus feugiat in. Amet luctus venenatis lectus magna. Molestie ac feugiat sed lectus vestibulum. Nibh sit amet commodo nulla facilisi nullam vehicula ipsum a. Nisi lacus sed viverra tellus in. In tellus integer feugiat scelerisque varius morbi enim. Bibendum enim facilisis gravida neque convallis a cras. Sed pulvinar proin gravida hendrerit lectus. Mauris cursus mattis molestie a. Auctor eu augue ut lectus arcu bibendum. Ac felis donec et odio pellentesque diam volutpat commodo. Nunc congue nisi vitae suscipit tellus mauris. Tellus in hac habitasse platea dictumst vestibulum rhoncus est pellentesque. Dolor purus non enim praesent elementum facilisis. Nunc lobortis mattis aliquam faucibus purus in massa tempor. Lectus vestibulum mattis ullamcorper velit sed ullamcorper morbi tincidunt ornare. Risus sed vulputate odio ut enim. Lobortis elementum nibh tellus molestie nunc. Amet dictum sit amet justo donec. Quisque egestas diam in arcu cursus euismod. Urna nunc id cursus metus aliquam eleifend mi. Amet mattis vulputate enim nulla aliquet porttitor. Lacus luctus accumsan tortor posuere ac ut consequat. Porta nibh venenatis cras sed felis. Eleifend donec pretium vulputate sapien nec. Cras adipiscing enim eu turpis egestas pretium aenean pharetra magna. Egestas quis ipsum suspendisse ultrices gravida. Sagittis id consectetur purus ut faucibus pulvinar elementum integer enim. Metus dictum at tempor commodo ullamcorper a. Sit amet aliquam id diam. Laoreet sit amet cursus sit amet dictum sit amet justo. At risus viverra adipiscing at in tellus integer. Sollicitudin aliquam ultrices sagittis orci a scelerisque. Elementum eu facilisis sed odio morbi quis commodo odio. Pellentesque habitant morbi tristique senectus et netus et. Ut placerat orci nulla pellentesque. Amet facilisis magna etiam tempor. Feugiat scelerisque varius morbi enim. Arcu bibendum at varius vel pharetra vel turpis nunc eget. Enim ut tellus elementum sagittis vitae. Tempor id eu nisl nunc mi ipsum faucibus. Sem fringilla ut morbi tincidunt augue interdum velit. Neque volutpat ac tincidunt vitae semper quis lectus. Ullamcorper a lacus vestibulum sed arcu non odio. Neque gravida in fermentum et sollicitudin ac orci phasellus egestas. Amet justo donec enim diam vulputate ut pharetra sit amet. Sed vulputate mi sit amet mauris commodo quis imperdiet massa. Eleifend quam adipiscing vitae proin. Enim nulla aliquet porttitor lacus. Luctus venenatis lectus magna fringilla. Scelerisque mauris pellentesque pulvinar pellentesque. Accumsan sit amet nulla facilisi morbi tempus. Arcu ac tortor dignissim convallis aenean. Nunc pulvinar sapien et ligula ullamcorper malesuada proin. Diam maecenas sed enim ut sem viverra aliquet eget sit. Feugiat in ante metus dictum at tempor commodo. Lacus vel facilisis volutpat est velit egestas dui id. Nulla posuere sollicitudin aliquam ultrices sagittis orci. Amet est placerat in egestas erat imperdiet sed euismod. Tempus egestas sed sed risus pretium quam. Nisl purus in mollis nunc sed id semper. Faucibus turpis in eu mi bibendum neque egestas congue quisque. Venenatis cras sed felis eget velit aliquet sagittis. Pellentesque id nibh tortor id aliquet. Ut pharetra sit amet aliquam id diam maecenas ultricies mi. Lacinia quis vel eros donec ac odio. Aliquam nulla facilisi cras fermentum odio eu feugiat pretium nibh. Vitae proin sagittis nisl rhoncus mattis rhoncus. Malesuada fames ac turpis egestas integer. Lorem ipsum dolor sit amet consectetur adipiscing. Arcu cursus vitae congue mauris rhoncus aenean vel elit scelerisque. Amet mattis vulputate enim nulla. Felis imperdiet proin fermentum leo vel orci. Orci porta non pulvinar neque laoreet suspendisse interdum consectetur. Gravida dictum fusce ut placerat orci nulla pellentesque. Ipsum consequat nisl vel pretium. Pharetra diam sit amet nisl suscipit adipiscing bibendum est ultricies. Quam lacus suspendisse faucibus interdum posuere. Tellus molestie nunc non blandit massa. Quis risus sed vulputate odio ut enim. Varius duis at consectetur lorem donec massa sapien faucibus. Diam vel quam elementum pulvinar. Vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor. In aliquam sem fringilla ut morbi tincidunt augue interdum. Neque convallis a cras semper auctor neque. Quam quisque id diam vel quam elementum pulvinar etiam non. Sed vulputate odio ut enim blandit volutpat maecenas volutpat blandit."
for i in range(2):
	text += text
	
editor.setText(text)

N = 10000
keyboardData = {}
keyslideData = {}

maxD = math.sqrt(editor.size[1]*editor.size[1] + editor.size[0]*editor.size[0])

for s in range(N):
	skip = False # skip current simulation if algorithm if not able to reach the targets
	print(s + 1) # print current simulation number

	cursorPos = editor.setCursor([randint(0, editor.size[0]), randint(0, editor.size[1])])

	correctMarkerPos = False
	# find the target location of cursor based on the 
	# cursor location, the target location is set to be
	# at random distance and angle from the cursor location
	while not correctMarkerPos:
		angle = 2 * math.pi * random.random()
		radius = maxD * math.sqrt(random.random())
		
		# set the marker at a ramdom angle and distance in the text field
		_markerPos = [cursorPos[0] + round(radius*math.cos(angle)), cursorPos[1] + round(radius*math.sin(angle))]

		# if the target locatio is outside the window, find the target location again
		if _markerPos[0] >= 0 and _markerPos[0] < editor.size[0] + 3:
			if _markerPos[1] >= 0 and _markerPos[1] < editor.size[1] + 3:
				correctMarkerPos = True

	markerPos = editor.setMarker(_markerPos)

	# Simulate keyboard shortcuts
	actionSequence = [] # stores the list of actions executed to reach the target location

	d = math.sqrt(editor.size[0]*editor.size[0] + editor.size[1]*editor.size[1])
	lastDistance = d
	oldCursorPos = [0, 0]

	while d > 0.5:
		bestAction = ""
		for a in editor.keyboardActionSpace():
			if editor.getActionReward(a) <= d:
				bestAction = a
				d = editor.getActionReward(bestAction)

		if bestAction == "" or round(lastDistance) == round(d):
			if editor.cursorPos[1] > editor.marker[1]:
				bestAction = "up_arrow"
			else:
				bestAction = "down_arrow"

		d = editor.getActionReward(bestAction)
		lastDistance = d

		_actions = [bestAction, editor.cursorPos]
		editor.performAction(bestAction)
		_actions.append(editor.cursorPos)
		actionSequence.append(_actions)

		if len(actionSequence) % 2 == 0:
			if oldCursorPos == editor.cursorPos:
				skip = True
				# stop simulation which performs repeated steps
				break
			else:
				oldCursorPos = editor.cursorPos

		if ShowSimulation:
			time.sleep(0.5)
			editor.display()
			print("len ", len(actionSequence), bestAction, editor.cursorPos, editor.marker)
			print()

	if skip:
		continue


	keyboardData[s] = {
		"cursorPos": cursorPos,
		"markerPos": markerPos,
		"actionSequence": actionSequence
	}


	# Simulate keyslide shortcuts
	cursorPos = editor.setCursor(cursorPos)
	markerPos = editor.setMarker(markerPos)
	actionSequence = []
	d = editor.markerCursorDist()
	lastDistance = d

	while d > 0.5:
		bestAction = ""
		if d > 5:
			bestAction = "keySlide"
			d = editor.getActionReward(bestAction)
		else:
			for a in editor.keyslideActionSpace():
				if editor.getActionReward(a) <= d:
					bestAction = a
					d = editor.getActionReward(bestAction)

		
		if bestAction == "" or lastDistance == d:
			if editor.cursorPos[1] > editor.marker[1]:
				bestAction = "up_arrow"
			else:
				bestAction = "down_arrow"
		
		d = editor.getActionReward(bestAction)
		lastDistance = d

		if bestAction == "keySlide":
			c, t = editor.keySlide()
		else:
			t = 0

		_actions = [bestAction, editor.cursorPos]
		editor.performAction(bestAction)
		_actions.append(editor.cursorPos)
		_actions.append(t)
		actionSequence.append(_actions)

		if ShowSimulation:
			time.sleep(0.5)
			editor.display()
			print("len ", d, len(actionSequence), bestAction, editor.cursorPos, editor.marker)
			print()

	keyslideData[s] = {
		"cursorPos": cursorPos,
		"markerPos": markerPos,
		"actionSequence": actionSequence
	}

with open('results/keyboard shortcuts.json', 'w') as outfile:
    json.dump(keyboardData, outfile)

with open('results/keyslide.json', 'w') as outfile:
    json.dump(keyslideData, outfile)

