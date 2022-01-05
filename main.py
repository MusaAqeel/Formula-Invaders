#Imports
import pygame
import sys, os, time
import random

#Initializing
pygame.init()
main_clock = pygame.time.Clock()
pygame.font.init()

#Display
WIDTH, HEIGHT = 750,750
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

#Text and Font
main_font = os.path.join("FinalAssets/Fonts", "RetronoidItalic-8Xg2.ttf")
body_font = os.path.join("FinalAssets/Fonts", "Comic Sans MS Bold.ttf")
body_font_2 = os.path.join("FinalAssets/Fonts", "Comic Sans MS.ttf")

#Loading images
UFO= pygame.image.load(os.path.join("FinalAssets/Enemy", "UFO.png"))
soft_laser = pygame.image.load(os.path.join("FinalAssets/Tires", "SoftTire.png"))
med_laser = pygame.image.load(os.path.join("FinalAssets/Tires", "MedTire.png"))
hard_laser = pygame.image.load(os.path.join("FinalAssets/Tires", "HardTire.png"))
background = pygame.image.load(os.path.join("FinalAssets", "BG.png"))

hamilton_punk = pygame.transform.scale(pygame.image.load(os.path.join("FinalAssets/Drivers/Hamilton", "LewisPUNK.png")), (100,100))
verstappen_punk = pygame.transform.scale(pygame.image.load(os.path.join("FinalAssets/Drivers/Verstappen", "VerstappenPUNK.png")), (100,100))
leclerc_punk = pygame.transform.scale(pygame.image.load(os.path.join("FinalAssets/Drivers/Leclerc", "LeclercPUNK.png")), (100,100))
calderon_punk = pygame.transform.scale(pygame.image.load(os.path.join("FinalAssets/Drivers/Calderon", "CalderonPUNK.png")), (100,100))
norris_punk = pygame.transform.scale(pygame.image.load(os.path.join("FinalAssets/Drivers/Norris", "NorrisPUNK.png")), (100,100))

soft_tire_menu_image = pygame.image.load(os.path.join("FinalAssets/Tires", "SoftTireMenu.png"))
med_tire_menu_image = pygame.image.load(os.path.join("FinalAssets/Tires", "MedTireMenu.png"))
hard_tire_menu_image = pygame.image.load(os.path.join("FinalAssets/Tires", "HardTireMenu.png"))

soft_tire_laser = pygame.image.load(os.path.join("FinalAssets/Tires", "SoftTire.png"))
med_tire_laser = pygame.image.load(os.path.join("FinalAssets/Tires", "MedTire.png"))
hard_tire_laser = pygame.image.load(os.path.join("FinalAssets/Tires", "HardTire.png"))

gas_can_img = pygame.transform.scale(pygame.image.load(os.path.join("FinalAssets", "gasCan.png")), (50,50))

laser_sound = pygame.mixer.Sound(os.path.join("FinalAssets/Audio", "Beep.mp3"))

background = pygame.image.load(os.path.join("FinalAssets", "BG.png"))

white = (255,255,255)
black = (0,0,0)
grey = (64,64,64)
red = (255,0,0)
green = (0,255,0)
orange = (205,130,35)

#Create Text
def text_format(text, font, size, colour):
	new_font = pygame.font.Font(font, size)
	new_text = new_font.render(text, 0, colour)
	return new_text

#Checks for collisions
def collide(obj1, obj2):
	offset_x = obj2.x_coord - obj1.x_coord
	offset_y = obj2.y_coord - obj1.y_coord
	return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

#Create Buttons Class
class button():
	def __init__(self, colour, x_coord, y_coord, width, height, text_colour=None, text_size=None, font=None, text=''):
		self.colour = colour
		self.x = x_coord
		self.y = y_coord
		self.width = width
		self.height = height
		self.text = text
		self.text_colour = text_colour
		self.text_size = text_size
		self.font = font
	
	#Check if certain coordinates are over
	def isOver(self, pos):
		if pos[0] > self.x and pos[0] < self.x + self.width:
			#Checked for the x coordinate
			if pos[1] > self.y and pos[1] < self.y + self.height:
				#Check for the x and y coordinate
				return True
		return False

	#Draws the button on the screen
	def draw(self, win, outline=None):
		# Call this method to draw the button on the screen
		if outline:
			pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
		
		pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height), 0)


		#Draws the text if any
		if self.text != '':
			text = text_format(self.text, self.font, self.text_size, self.text_colour)
			text_x = self.x + (self.width / 2 - text.get_width() / 2)
			text_y = self.y + (self.height / 2 - text.get_height() / 2)
			win.blit(text, (text_x, text_y))

		

#Laser class
class Laser:
	def __init__(self, x_coord, y_coord, img):
		self.x_coord = x_coord
		self.y_coord = y_coord
		self.img = img
		self.mask = pygame.mask.from_surface(self.img)

	#Draw the laser
	def draw(self, window):
		window.blit(self.img, (self.x_coord, self.y_coord))

	#Move the laser
	def move(self, vel):
		self.y_coord+=vel

	#Checks if the laser is off screen
	def off_screen(self, height):
		return not (self.y_coord <= height and self.y_coord >=0)

	#Checks for collisions
	def collision(self, obj):
		return collide(self, obj)

class Ship:
	#Cooldown in frames
	COOLDOWN = 30

	def __init__(self, x_coord, y_coord, health=100):
		self.x_coord = x_coord
		self.y_coord = y_coord
		self.health = health
		self.ship_img = None
		self.laser_img = None
		self.lasers = []
		self.cooldown_counter = 0

	#Drawing the ship and lasers
	def draw(self, window):
		#Drawing the ship
		window.blit(self.ship_img, (self.x_coord, self.y_coord))
		
		#Iterarating through every laser
		for laser in self.lasers:
			laser.draw(window)

	#Move the laser and handle the collisions
	def move_lasers(self, vel, obj):
		self.cooldown()
		
		#Iterarating through every laser
		for laser in self.lasers:
			laser.move(vel)
			if laser.off_screen(HEIGHT):
				#Removes the laser if it goes off screen
				self.lasers.remove(laser)
			elif laser.collision(obj):
				#Laser hits object, lower obj health and remove laser
				obj.health -=10
				self.lasers.remove(laser)

	def cooldown(self):
		#Laser cooldown so user can't spam
		if self.cooldown_counter >= self.COOLDOWN:
			self.cooldown_counter = 0
		elif self.cooldown_counter > 0:
			self.cooldown_counter += 1

	def shoot(self):
		#Handles shooting a laser
		if self.cooldown_counter == 0:
			laser = Laser(self.x_coord, self.y_coord, self.laser_img)
			self.lasers.append(laser)
			#Sets the cooldown
			self.cooldown_counter = 1

	def get_width(self):
		#Returning the width of the ship
		return self.ship_img.get_width()

	def get_height(self):
   		#Returning the height of the ship
		return self.ship_img.get_height()

#Formula 1 car class
class Player(Ship):
	def __init__(self, x_coord, y_coord, health=101):
		super().__init__(x_coord, y_coord, health)
		self.ship_img = F1_Car
		self.laser_img = player_laser
		self.mask = pygame.mask.from_surface(self.ship_img)
		self.max_health = health
		self.score = 0
		self.fuel = 100
		self.max_fuel = 100

	#Moving the laser
	def move_lasers(self, vel, objs):
		#Checking the cooldown
		self.cooldown()
		#Iterating through every laser
		for laser in self.lasers:
			#Moving the laser
			laser.move(vel)
			if laser.off_screen(HEIGHT):
				#Removing the laser if it goes off screen
				self.lasers.remove(laser)
			else:
				#Iterating through every object
				for obj in objs:
					if laser.collision(obj):
						#Removing the object if the laser collides
						objs.remove(obj)
						#Increasing the score
						self.score+=10
						if laser in self.lasers:
							#Removing the laser that collided with the object
							self.lasers.remove(laser)

	#Draws the car and healthbar
	def draw(self, window):
		super().draw(window)
		self.healthbar(window)
		self.fuelbar(window)

	#Handles the healthbar
	def healthbar(self, window):
		#Red part of health bar
		pygame.draw.rect(window, red, (self.x_coord, self.y_coord + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
		#Green part of healthbar
		pygame.draw.rect(window, green, (self.x_coord, self.y_coord + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health),10))

	def fuelbar(self, window):
		#Green part of healthbar
		pygame.draw.rect(window, green, (WIDTH/2 - 100, 10, 200, 10))
		#Orange part of fuel
		pygame.draw.rect(window, orange, (WIDTH/2 - 100, 10, 200 * (self.fuel / self.max_fuel), 10))
		#Text
		text = text_format("Fuelbar", body_font, 12, black)
		WIN.blit(text, (WIDTH/2 - text.get_width()/2, 25))

	#Returning the score gotten by killing enemies
	def return_score(self):
		return self.score


#Enemy ships class
class Enemy(Ship):
	#Map for each tire laser type
	TIRE_MAP = {
		"soft": (UFO, soft_laser),
		"med": (UFO, med_laser),
		"hard": (UFO, hard_laser),
		"gas_tank": (gas_can_img)
	}

	def __init__(self, x_coord, y_coord, laser_choice, refuel = False, health=100):
		super().__init__(x_coord, y_coord, health)
		if not refuel:
			self.ship_img, self.laser_img = self.TIRE_MAP[laser_choice]
		else:
			self.ship_img = self.TIRE_MAP[laser_choice]

		self.mask = pygame.mask.from_surface(self.ship_img)
		self.refuel = refuel

	#Moving the enemy ship
	def move(self, vel):
		self.y_coord +=vel

	#Having the enemy shoot
	def shoot(self):
		#Checks for cooldown
		if self.cooldown_counter == 0:
			#New laser
			laser = Laser(self.x_coord + 17, self.y_coord, self.laser_img)
			self.lasers.append(laser)
			#Setting the cooldown
			self.cooldown_counter = 1


#Starting menu (main menu)
def main_menu():
	#Buttons
	button_width = 200
	button_height = 70
	button_x_coord = WIDTH/2 - button_width/2
	button_y_coord = 300
	button_y_distance = 100
	button_text_colour = black
	button_text_size = 60
	button_font = main_font

	#Creating new buttons
	start_button = button(grey, button_x_coord, button_y_coord, button_width, button_height, button_text_colour, button_text_size, button_font, 'START')	
	quit_button = button(grey, button_x_coord, button_y_coord + button_y_distance * 1,  button_width,  button_height, button_text_colour, button_text_size, button_font, 'QUIT')	
	credits_button = button(grey, button_x_coord, button_y_coord + button_y_distance * 2, button_width,  button_height, button_text_colour, button_text_size, button_font, 'CREDITS')	
	tutorial_button = button(grey, button_x_coord, button_y_coord + button_y_distance * 3,  button_width, button_height, button_text_colour, button_text_size, button_font, 'TUTORIAL')	

	#Title
	title = text_format("FORMULA INVADERS", main_font, 77, black)
	title_x_coord = WIDTH/2 - title.get_width()/2
	title_y_coord = 80

	run = True
	pygame.display.set_caption("Start Menu")
	
	#Function to draw the updated elements
	def redraw_window():
		#Setting the background
		WIN.fill(grey)

		#Title
		WIN.blit(title, (title_x_coord, title_y_coord))

		#Buttons
		start_button.draw(WIN)
		quit_button.draw(WIN)
		credits_button.draw(WIN)
		tutorial_button.draw(WIN)

	#Game loop
	while run:
		#Redrawing the window
		redraw_window()
		pygame.display.update()

		#Checking for events
		for event in pygame.event.get():
			#Getting the mouse coordinates
			pos = pygame.mouse.get_pos()

			#Quiting the game if the user quits
			if event.type == pygame.QUIT:
				pygame.quit()
				os._exit(1)
				quit()

			#If the user clicks anywhere
			if event.type == pygame.MOUSEBUTTONDOWN:
				#Checking if they clicked on the start button
				if start_button.isOver(pos):
					#Moving to the next menu
					driver_selection_menu()
				#Checking if they clicked on the quit button
				if quit_button.isOver(pos):
					#Quiting
					pygame.quit()
					os._exit(1)
					quit()
				#Checking if they clicked on the credits button
				if credits_button.isOver(pos):
					#Going to the credits menu
					credit_menu()
				#Checking if they clicked on the tutorial button
				if tutorial_button.isOver(pos):
					#Going to the tutorial menu
					tutorial_menu()

			#Checking where the users mouse is when they move
			if event.type == pygame.MOUSEMOTION:
				#If it's over the start button, change the text to white
				if start_button.isOver(pos):
					start_button.text_colour = white
				else:
					start_button.text_colour = black
				#If it's over the quit button, change the text to white
				if quit_button.isOver(pos):
					quit_button.text_colour = white
				else:
					quit_button.text_colour = black
				#If it's over the credits button, change the text to white
				if credits_button.isOver(pos):
					credits_button.text_colour = white
				else:
					credits_button.text_colour = black
				#If it's over the tutorial button, change the text to white
				if tutorial_button.isOver(pos):
					tutorial_button.text_colour = white
				else:
					tutorial_button.text_colour = black


#Driver Selection Menu
def driver_selection_menu():
	#Text font
	driver_font_size = 12
	driver_font_colour = black
	driver_font = body_font_2
	driver_width_height = 100
	#Button and text y-coordinate
	button_y = 300
	title_y_coord = button_y + 110

	#Lewis Hamilton
	lewis_x_coord = 130
	lewis_button = button(grey, lewis_x_coord, button_y, driver_width_height, driver_width_height)
	lewis_text = text_format("Lewis Hamilton", driver_font, driver_font_size, driver_font_colour)

	#Max Verstappen
	verstappen_x_coord = 230
	verstappen_button = button(grey, verstappen_x_coord, button_y, driver_width_height, driver_width_height)
	verstappen_text = text_format("Max Verstappen", driver_font, driver_font_size, driver_font_colour)

	#Charles Leclerc
	leclerc_x_coord = 330
	leclerc_button = button(grey, leclerc_x_coord, button_y, driver_width_height, driver_width_height)
	leclerc_text = text_format("Charles Leclerc", driver_font, driver_font_size, driver_font_colour)

	#Tatiana Calderon
	calderon_x_coord = 430
	calderon_button = button(grey, calderon_x_coord, button_y, driver_width_height, driver_width_height)
	calderon_text = text_format("Tatiana Calderon", driver_font, driver_font_size, driver_font_colour)

	#Lando Norris
	norris_x_coord = 530
	norris_button = button(grey, norris_x_coord, button_y, driver_width_height, driver_width_height)
	norris_text = text_format("Lando Norris", driver_font, driver_font_size, driver_font_colour)

	#Back button
	back_button = button(grey, WIDTH-150, 50 , 100, 50, black, 22, main_font, "BACK")

	#Menu Title Text
	menu_title_size = 40
	menu_title = text_format("Select your driver", main_font, menu_title_size, driver_font_colour)
	menu_title_x = WIDTH/2 - menu_title.get_width()/2
	menu_title_y = 200

	#Instructions
	instruction_size = 15
	instruction_x = 20
	instruction_y = 600
	instruction_text = text_format("Has no effect on game mechanis", body_font, instruction_size, driver_font_colour)

	run = True
	pygame.display.set_caption("Player Selection Menu")
	#Function to update the window
	def redraw_window():
		WIN.fill(grey)

		#Lewis Hamilton
		lewis_button.draw(WIN)
		WIN.blit(hamilton_punk, (lewis_x_coord, button_y))
		WIN.blit(lewis_text, (lewis_x_coord, title_y_coord))

		#Max Verstappen
		verstappen_button.draw(WIN)
		WIN.blit(verstappen_punk, (verstappen_x_coord, button_y))
		WIN.blit(verstappen_text, (verstappen_x_coord, title_y_coord))

		#Charles Leclerc
		leclerc_button.draw(WIN)
		WIN.blit(leclerc_punk, (leclerc_x_coord, button_y))
		WIN.blit(leclerc_text, (leclerc_x_coord, title_y_coord))

		#Tatiana Calderon
		calderon_button.draw(WIN)
		WIN.blit(calderon_punk, (calderon_x_coord, button_y))
		WIN.blit(calderon_text, (calderon_x_coord, title_y_coord))

		#Lando Norris
		norris_button.draw(WIN)
		WIN.blit(norris_punk, (norris_x_coord, button_y))
		WIN.blit(norris_text, (norris_x_coord+10, title_y_coord))

		#Back Button
		back_button.draw(WIN)

		#Menu Title
		WIN.blit(menu_title, (menu_title_x, menu_title_y))

		#Instruction text
		WIN.blit(instruction_text, (instruction_x, instruction_y))

	global F1_Car
	#Event runner
	while run:
		#Updating the display
		redraw_window()
		pygame.display.update()
		#Looping through events
		for event in pygame.event.get():
			#Getting mouse coordinates
			pos = pygame.mouse.get_pos()

			#Quits the app if the user quits
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				os._exit(1)
				quit()

			#Handles button clicks
			if event.type == pygame.MOUSEBUTTONDOWN:
				#Checking if they clickled a button and proceeding to the next menu
				if lewis_button.isOver(pos):
					#Choose hamiltons car
					F1_Car = pygame.image.load(os.path.join("FinalAssets/Drivers/Hamilton", "HamiltonCar.png"))
					tire_menu()
				elif verstappen_button.isOver(pos):
					#Choose verstappens car
					F1_Car = pygame.image.load(os.path.join("FinalAssets/Drivers/Verstappen", "VerstappenCar.png"))
					tire_menu()
				elif leclerc_button.isOver(pos):
					F1_Car = pygame.image.load(os.path.join("FinalAssets/Drivers/Leclerc", "LeclercCar.png"))
					tire_menu()
				elif calderon_button.isOver(pos):
					F1_Car = pygame.image.load(os.path.join("FinalAssets/Drivers/Calderon", "CalderonCar.png"))
					tire_menu()
				elif norris_button.isOver(pos):
					F1_Car = pygame.image.load(os.path.join("FinalAssets/Drivers/Norris", "NorrisCar.png"))
					tire_menu()
				elif back_button.isOver(pos):
					main_menu()

			#Handles mouse movement
			if event.type == pygame.MOUSEMOTION:
				if back_button.isOver(pos):
					back_button.text_colour = white
				else:
					back_button.text_colour = black

				if lewis_button.isOver(pos):
					lewis_text = text_format("Lewis Hamilton", driver_font, driver_font_size, white)
				else:
					lewis_text = text_format("Lewis Hamilton", driver_font, driver_font_size, black)

				if verstappen_button.isOver(pos):
					verstappen_text = text_format("Max Verstappen", driver_font, driver_font_size, white)
				else:
					verstappen_text = text_format("Max Verstappen", driver_font, driver_font_size, black)

				if leclerc_button.isOver(pos):
					leclerc_text = text_format("Charles Leclerc", driver_font, driver_font_size, white)
				else:
					leclerc_text = text_format("Charles Leclerc", driver_font, driver_font_size, black)

				if calderon_button.isOver(pos):
					calderon_text = text_format("Tatiana Calderon", driver_font, driver_font_size, white)
				else:
					calderon_text = text_format("Tatiana Calderonn", driver_font, driver_font_size, black)

				if norris_button.isOver(pos):
					norris_text = text_format("Lando Norris", driver_font, driver_font_size, white)
				else:
					norris_text = text_format("Lando Norris", driver_font, driver_font_size, black)


def tire_menu():
	#Button properties
	tire_button_width = 145
	tire_button_height = 30
	med_choice_x = WIDTH/2 - tire_button_width/2
	tire_button_y = HEIGHT/2 - tire_button_height/2
	soft_choice_x = med_choice_x - 200
	hard_choice_x = med_choice_x + 200

	#Buttons
	back_button = back_button = button(grey, WIDTH-150, 50 , 100, 50, black, 22, main_font, "BACK")
	soft_choice_button = button(grey, soft_choice_x, tire_button_y, tire_button_width, tire_button_height, black, 22, main_font, "SOFT TIRES")
	med_choice_button = button(grey, med_choice_x, tire_button_y, tire_button_width, tire_button_height, black, 22, main_font, "MEDIUM TIRES")
	hard_choice_button = button(grey, hard_choice_x, tire_button_y, tire_button_width, tire_button_height, black, 22, main_font, "HARD TIRES")
	offset = 20

	#Menu Title
	menu_title_text = text_format("Select your tires", main_font, 40, black)
	menu_title_x = WIDTH/2 - menu_title_text.get_width()/2
	menu_title_y = 200

	#Intructions
	instruction_size = 15
	instruction_colour = black	
	instruction_x = 20
	instruction_y = 600

	instruction_text_line_1 = text_format("Depending on the tire you choose, the game difficulty chanegs as follows: ", body_font, instruction_size, instruction_colour)
	instruction_text_line_2 = text_format("Soft Tires: The easiest, has a reduced number of enemies per wave", body_font, instruction_size, instruction_colour)
	instruction_text_line_3 = text_format("Medium Tire: Standard diffuculty", body_font, instruction_size, instruction_colour)
	instruction_text_line_4 = text_format("Hard Tires: The hardest, with more enemy per waves and also a slower tire", body_font, instruction_size, instruction_colour)
	instruction_text_height = instruction_text_line_1.get_height()

	def redraw_window():
		WIN.fill(grey)
		back_button.draw(WIN)
		soft_choice_button.draw(WIN)
		med_choice_button.draw(WIN)
		hard_choice_button.draw(WIN)

		#Tires
		WIN.blit(soft_tire_menu_image, (soft_choice_x + offset, tire_button_y + tire_button_height))
		WIN.blit(med_tire_menu_image, (med_choice_x + offset, tire_button_y + tire_button_height))
		WIN.blit(hard_tire_menu_image, (hard_choice_x + offset, tire_button_y + tire_button_height))

		#Text
		WIN.blit(menu_title_text, (menu_title_x, menu_title_y))
		WIN.blit(instruction_text_line_1, (instruction_x, instruction_y))
		WIN.blit(instruction_text_line_2, (instruction_x, instruction_y + instruction_text_height))
		WIN.blit(instruction_text_line_3, (instruction_x, instruction_y + instruction_text_height*2))
		WIN.blit(instruction_text_line_4, (instruction_x, instruction_y + instruction_text_height*3))

	run = True
	pygame.display.set_caption("Tire Selection Menu")
	global player_laser
	global wave_incremeant
	global laser_vel
	
	while run:
		#Updating the display
		redraw_window()
		pygame.display.update()

		#Checks for events
		for event in pygame.event.get():
			#Gettibg mouse coordinates
			pos = pygame.mouse.get_pos()

			#Quits the app if the user quits
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				os._exit(1)
				quit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if soft_choice_button.isOver(pos):
					#If the user chooses soft choice tires
					player_laser = soft_tire_laser
					wave_incremeant = 3
					laser_vel = 5
					game()
				elif med_choice_button.isOver(pos):
					#If the user chooses the medium choice tires
					player_laser = med_tire_laser
					wave_incremeant = 5
					laser_vel = 3
					game()
				elif hard_choice_button.isOver(pos):
					#If the user chooses the hard choice tires
					player_laser = hard_tire_laser
					wave_incremeant = 7
					laser_vel = 3
					game()
				elif back_button.isOver(pos):
					driver_selection_menu()

			if event.type == pygame.MOUSEMOTION:
				if back_button.isOver(pos):
					back_button.text_colour = white
				else:
					back_button.text_colour = black

				if soft_choice_button.isOver(pos):
					soft_choice_button.text_colour = white
				else:
					soft_choice_button.text_colour = black

				if med_choice_button.isOver(pos):
					med_choice_button.text_colour = white
				else:
					med_choice_button.text_colour = black

				if hard_choice_button.isOver(pos):
					hard_choice_button.text_colour = white
				else:
					hard_choice_button.text_colour = black

def credit_menu():
	#Back button
	back_button = back_button = button(grey, WIDTH-150, 50 , 100, 50, black, 22, main_font, "BACK")

	#Title
	title_text = text_format("FORMULA INVADERS", main_font, 77, black)
	title_x_coord = WIDTH/2 - title_text.get_width()/2
	title_y_coord = 80

	#Text
	text_size = 20
	text_colour = black
	text_font = body_font
	line_1_x_coord = 10
	line_1_y_coord = 300
	line_1 = text_format("Game Developers: ", text_font, text_size, text_colour)

	def redraw_window():
		#Background colour
		WIN.fill(grey)

		#Back button
		back_button.draw(WIN)

		#Title
		WIN.blit(title_text, (title_x_coord, title_y_coord))

		#Text
		WIN.blit(line_1, (line_1_x_coord, line_1_y_coord))

	run = True
	pygame.display.set_caption("Credits Menu")

	#Game loop
	while run:
		#Updating the display
		redraw_window()
		pygame.display.update()

		#Events
		for event in pygame.event.get():
			#Getting mouse coordinates
			pos = pygame.mouse.get_pos()

			#If the user quits the app
			if event.type == pygame.QUIT:
				pygame.quit()
				os._exit(1)
				quit()

			#Handles button clicks
			if event.type == pygame.MOUSEBUTTONDOWN:
				if back_button.isOver(pos):
					#If the user clicks the back button
					main_menu()

			#Checks for mouse movement
			if event.type == pygame.MOUSEMOTION:
				if back_button.isOver(pos):
					back_button.text_colour = white
				else:
					back_button.text_colour = black


def tutorial_menu():
	#Back button
	back_button = back_button = button(grey, WIDTH-150, 50 , 100, 50, black, 22, main_font, "BACK")

	#Title
	title_text = text_format("FORMULA INVADERS", main_font, 77, black)
	title_x_coord = WIDTH/2 - title_text.get_width()/2
	title_y_coord = 80

	#Text
	line_1 = text_format('Move with "WASD"', body_font, 19, black)
	line_2 = text_format('Shoot with the spacebar', body_font, 19, black)
	line_3 = text_format('You lose lives if you let UFOs touch the ground', body_font, 19, black)
	line_4 = text_format("Do not get hit with tires or UFO's or you'll lose health", body_font, 19, black)
	line_5 = text_format('Keep on going for as long as you can and try to beat your old score', body_font, 19, black)
	line_6 = text_format('You get 10 points for killing each UFO, and 30 points for passing each level', body_font, 19, black)
	line_7 = text_format('Your score will only be displayed at the end of the game', body_font, 19, black)
	x_coord = 10
	y_coord = 200
	incrimeant = 25

	def redraw_window():
		#Window background
		WIN.fill(grey)

		#Back Button
		back_button.draw(WIN)

		#Title
		WIN.blit(title_text, (title_x_coord, title_y_coord))

		#Text
		WIN.blit(line_1, (x_coord, y_coord))
		WIN.blit(line_2, (x_coord, y_coord + incrimeant*1))
		WIN.blit(line_3, (x_coord, y_coord + incrimeant*2))
		WIN.blit(line_4, (x_coord, y_coord + incrimeant*3))
		WIN.blit(line_5, (x_coord, y_coord + incrimeant*4))
		WIN.blit(line_6, (x_coord, y_coord + incrimeant*5))
		WIN.blit(line_7, (x_coord, y_coord + incrimeant*6))

	run = True
	pygame.display.set_caption("Tutorial Menu")

	#Game loop
	while run:
		#Updating the display
		redraw_window()
		pygame.display.update()

		#Checks for events
		for event in pygame.event.get():
			#Mouse coordinates
			pos = pygame.mouse.get_pos()

			#If the user quits, the quit the app
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				os._exit(1)
				quit()

			#Handles mouse clicks
			if event.type == pygame.MOUSEBUTTONDOWN:
				if back_button.isOver(pos):
					#If the user clicks on the back button
					main_menu()

			#Handles mouse movements
			if event == pygame.MOUSEMOTION:
				if back_button.isOver(pos):
					back_button.text_colour = white
				else:
					back_button.text_colour = black


# Main game functions
def game():
	#Variables
	run = True
	FPS = 120
	level = 0
	lives = 5
	main_font = pygame.font.SysFont("comicsans", 50)
	lost_font = pygame.font.SysFont("comicsans", 60)

	enemies = []
	wave_length = 5
	enemy_vel = 1
	enemy_laser_vel = 3
	player_vel = 5
	wave_score = 0
	final_score = 0

	player = Player(300, 630)

	clock = pygame.time.Clock()

	lost = False
	lost_count = 0

	# Redraws the window
	def redraw_window():
		WIN.blit(background, (0, 0))
		# draw text
		lives_label = main_font.render(f"Lives: {lives}", 1, white)
		level_label = main_font.render(f"Level: {level}", 1, white)

		#Adds the lives and levels label to the screen
		WIN.blit(lives_label, (10, 10))
		WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

		#Draws the enemies
		for enemy in enemies:
			enemy.draw(WIN)

		#Draws the player
		player.draw(WIN)

		#Handles what to do when the player looses
		if lost:
			final_score = player.return_score() + wave_score
			lost_label = lost_font.render(f"Your Score: {final_score}", 1, white)

			WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))
		pygame.display.update()

	pygame.display.set_caption("Formula Invaders")
	
	#Event runner
	while run:
		clock.tick(FPS)
		redraw_window()
		
		#Checks if the player looses
		if lives <= 0 or player.health <= 0 or player.fuel <= 0:
			lost = True
			lost_count += 1

		#Handles if the player looses
		if lost:
			if lost_count > FPS * 3:
				run = False
			else:
				continue

		#Handles if the player beats the wave
		if len(enemies) == 0:
			level += 1
			wave_length += wave_incremeant
			wave_score +=30

			if level % 4 == 0:
				gas_tank = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), "gas_tank", True)
				enemies.append(gas_tank)

			#Spawns the enemies
			for i in range(wave_length):
				enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["soft", "med", "hard"]))
				enemies.append(enemy)

		# Checks for events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				os._exit(1)
				quit()

		#Handles movement and shooting 
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a] and player.x_coord - player_vel > 0:  # left
			player.x_coord -= player_vel
		if keys[pygame.K_d] and player.x_coord + player_vel + player.get_width() < WIDTH:  # right
			player.x_coord += player_vel
		if keys[pygame.K_w] and player.y_coord - player_vel > 0:  # up
			player.y_coord -= player_vel
		if keys[pygame.K_s] and player.y_coord + player_vel + player.get_height() + 15 < HEIGHT:  # down
			player.y_coord += player_vel
		if keys[pygame.K_SPACE]:
			player.shoot()
			player.fuel -= 0.1

			laser_sound.stop()
			# play the laser sound
			laser_sound.play()

		# Handles the enemies
		for enemy in enemies[:]:
			enemy.move(enemy_vel)
			enemy.move_lasers(enemy_laser_vel, player)

			if random.randrange(0, 2 * 60) == 1:
				if not enemy.refuel:
					enemy.shoot()

			if collide(enemy, player):
				if not enemy.refuel:
					player.health -= 10
					enemies.remove(enemy)
				elif player.fuel < player.max_fuel:
					player.fuel += 0.1
					
			elif enemy.y_coord + enemy.get_height() > HEIGHT:
				lives -= 1
				enemies.remove(enemy)

		player.move_lasers(-laser_vel, enemies)

	pygame.time.delay(5000)
	main_menu()

main_menu()