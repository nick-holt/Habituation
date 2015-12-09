currentTime = Clock.CurrentTime
trialOnset = Event4.OnsetTime # Exact time at beginning of trial
keyState = 0 # State of the numpad5 key: 0 = not pressed, 1 = pressed
keyPressed = 0 
keyReleased = 0
onePress = 0
timedOut = 0
lookingTime = 0
lT1 = 0
lT2 = 0
lTWrite = 0
noLookOnset = 0
noLookDuration = 0
repTrialNum = 0
lTList = list()

while timedOut == 0:
	keyState = win32api.GetKeyState(win32con.VK_NUMPAD5) & 0x8000
	currentTime = Clock.CurrentTime
	if (keyState == 0):
			keyPressed = 0
	if keyState != 0:
			keyPressed = 1
			DataLogger.Add("KeyPressDetected", str(currentTime))
	if keyPressed == 0: 
		noLookOnset = currentTime
	while keyPressed == 0 and timedOut == 0:
		keyState = win32api.GetKeyState(win32con.VK_NUMPAD5) & 0x8000
		currentTime = Clock.CurrentTime
		if (keyState == 0):
			keyPressed = 0
		if keyState != 0:
			keyPressed = 1
			DataLogger.Add("KeyPressDetected", str(currentTime))
		noLookDuration = currentTime - noLookOnset
		if onePress == 1 and lookingTime > 1000 and noLookDuration > 1000: # Defines 1 sec Look Away to end trial
			DataLogger.Add("InfantQuitLookingFor1second?", "True")
			DataLogger.Add("LookingTime", str(lookingTime))
			timedOut = 1
		while onePress == 1 and lTWrite == 0 and singleLook > 1000: # Calculates Looking Time into List
			lTList.append(singleLook)
			DataLogger.Add("numberOfLooks", str(len(lTList)))
			DataLogger.Add("listLT", str(sum(lTList)))
			lTWrite = 1
		lookingTime = sum(lTList) # Defines Looking time as sum of all looks
		if onePress == 1 and lookingTime > 20000: # Ends trial if LT exceeds 20 seconds
			DataLogger.Add("MaxTrialLengthTimeout", "True")
			DataLogger.Add("LookingTime", str(lookingTime))
			timedOut = 1
		if onePress == 0 and noLookDuration > 10000: # If no looking for 10 seconds, repeat trial
			repTrialNum = counter
			counter = counter - 1
			lookingTime = 0
			DataLogger.Add("lookingTime",str(lookingTime))
			DataLogger.Add("No Looking for 10 seconds","True")
			timedOut = 1
		if keyState != 0: # Ends loop when key pressed
			keyPressed = 1
			
	if keyPressed != 0:
		lT1 = currentTime
		singleLook = 0
		onePress = 1
		lTWrite = 0

	while keyPressed != 0 and timedOut == 0:
		keyState = win32api.GetKeyState(win32con.VK_NUMPAD5) & 0x8000
		currentTime = Clock.CurrentTime
		lT2 = currentTime
		singleLook = (lT2 - lT1)
		if singleLook > 20000:
			lookingTime = 20000
			DataLogger.Add("MaxTrialLengthTimeout", "True")
			DataLogger.Add("LookingTime", str(lookingTime))
			timedOut = 1
		if (lookingTime + singleLook) > 20000:
			lookingTime = 20000
			DataLogger.Add("MaxTrialLengthTimeout", "True")
			DataLogger.Add("LookingTime", str(lookingTime))
			timedOut = 1
		if keyState != 0:
			keyPressed = 1
		if (keyState == 0):
			keyReleased = currentTime
			keyPressed = 0

counter = counter + 1
DataLogger.Add("Counter", str(counter))
if counter == 2:
	critTrialTime1 = lookingTime
	critTrialTime2 = 0
if counter == 3:
	critTrialTime2 = lookingTime
trialTime2 = trialTime1
trialTime1 = lookingTime

habCrit = ((.5)*((critTrialTime2 + critTrialTime1)/2))
DataLogger.Add("habCrit", str(habCrit))
if counter == 3 or counter == 5 or counter == 7 or counter == 11 or counter == 13 or counter == 15 or counter == 17:
		habCheck = ((trialTime1 + trialTime2)/2)
		DataLogger.Add("habCheck", str(habCheck))
		if habCheck < habCrit and counter >=3:
			habituated = 1
			DataLogger.Add("Habituated", str(habituated))
			Experiment.JumpToEvent("Test1") # Must be changed to fit cell

Clock.Reset()
Display1.ClearScreen()