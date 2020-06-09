import pyautogui
import pynput
import time
import json

class Controller:
	def __init__(self):
            with open("config.json") as config_file:
                config = json.load(config_file)
                self.controls = config["controls"]
               	self.os = config["os"]
            
            self.screen = pyautogui.size()
            self.window = [-1,-1,-1,-1]
    
            if self.os == 'Windows':
                # import fails while using Linux
                import pygetwindow as gw
                window = gw.getAllTitles()
                for title in window:
                    if "Super" in title or "Dolphin" in title:
                        window = title

                        window = gw.getWindowsWithTitle(window)[0]
                        window.moveTo(5, 5)
                        window.resizeTo(600, 500)

                        self.window[0], self.window[1] = window.topleft
                        self.window[2], self.window[3] = window.bottomright

            elif self.os == 'Linux':
                if "window" not in config:
                    print("Linux OS requires game window calibration")
                    self.calibrate_screen()
                    print("Calibration complete")
                    with open("config.json", "wb") as config_file:
                        json.dump(self.window, config_file)
                else:
                    print(config["window"])
                    
	def click(self):
		pyautogui.click()

	def moveTo(self, x, y):
		pyautogui.moveTo(x,y)

	def calibrate_screen(self):
		print("Move mouse to top left of game window and click")

		# capture mouse location when clicked
		with pynput.mouse.Listener(on_click=self.find_window) as listener:
			listener.join()
		print("Move mouse to bottom of game window and click")

		with pynput.mouse.Listener(on_click=self.find_window) as listener:
			listener.join()

		print("Screen calibrated to ", self.window)


	def find_window(self, x, y, button, pressed):
		if pressed:
			# set the pixel range of the game window
			if self.window[0] ==  -1:
				self.window[0] = x
			elif self.window[2] == -1:
				self.window[2] = x

			if self.window[1] == -1:
				self.window[1] = y
			elif self.window[3] == -1:
				self.window[3] = y

			# Release listener
			return False

	def win_press(self, x):
		directkeys.PressKey(x)

	def win_release(self, x):
		directkeys.ReleaseKey(x)

	def press(self, key):
		pyautogui.press(key)

	def keyDown(self, key):
		press_time = 0.5
		pyautogui.keyDown(key)
		time.sleep(press_time)
		pyautogui.keyUp(key)

	def keyUp(self, key):
		pyautogui.keyUp(key)


	def center(self):
		centerx = ((self.window[2] - self.window[0]) / 2) + self.window[0]
		centery = ((self.window[3] - self.window[1]) / 2) + self.window[1]
		pyautogui.moveTo(centerx, centery)


	# takes in a list of controls and controls game
	def play(self, move):
		# control state looks something like this
		for m in reversed(move.moves):
			pyautogui.keyDown(controls[m])

		for m in move.moves:
			pyautogui.keyUp(controls[m])

		return


# idk if we need a class to handle it, but this is working for now
class MoveSet:
	def __init__(self, moves):
		# just keeping basic controls for now
		controls = ["a", "b", "x", "y", "start", "up", "down", "left", "right"]
		self.moves = []

		# assign moves based on input
		for i in range(len(moves)):
			if moves[i] == True:
				self.moves.append(controls[i])

		print(self.moves)


def main():

	controller = Controller()

	# sorry for the spam, probably a better way to handle this

	#                 ["a", "b", "x", "y", "start", "up", "down", "left", "right"]
	right_a = MoveSet([True, False, False, False, False, False, False, False, True])
	left_a = MoveSet([True, False, False, False, False, False, False, True, False])
	up_a = MoveSet([True, False, False, False, False, True, False, False, False])
	down_a = MoveSet([True, False, False, False, False, False, True, False, False])
	jump = MoveSet([True, False, False, False, False, True, False, False, False])

	# aerials
	r_air = MoveSet([True, False, True, False, False, True, False, False, True])
	l_air = MoveSet([True, False, True, False, False, False, False, True, False])
	n_air = MoveSet([True, False, True, False, False, False, True, False, False])
	d_air = MoveSet([True, False, True, False, False, True, False, False, False])

	up_b = MoveSet([False, True, True, False, False, True, False, False, False])
	down_b = MoveSet([False, True, True, False, False, False, True, False, False])
	right_b = MoveSet([False, True, True, False, False, False, False, False, True])
	left_b = MoveSet([False, True, True, False, False, False, False, True, False])

	test_moves = [right_a, left_a, up_a, down_a, jump]
	aerials = [r_air, l_air, n_air, d_air]
	b_attacks = [up_b, down_b, right_b, left_b]

	for m in b_attacks:
		for i in range(1):
			controller.play(m)
			time.sleep(2)

if __name__=="__main__":
	main()
