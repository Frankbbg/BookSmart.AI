import customtkinter as ctk
import importlib 
import datetime  
from classes.Database import engine as db_engine, get_session
from ai import StoryGPT
from PIL import Image 
from tkinter import messagebox
import pickle, os
from classes.models import User
from classes.user_service import get_user_by_username
from config import (
    PROJECT_ROOT, 
    ICON_FILE, 
    IMAGES_SUBDIRECTORY, 
    THEME_COLORS, 
    LAST_USER_PICKLE_FILE
)


'''
+ Header: Tkinter frame that represents the header of the application 

Constructor:
- master (App): 'App' Class instance

Attributes/Variables:
- master (App): 'App' class instance
- sidebar (CTkFrame): Inner frame that that contains the label and the contains the container for the nav buttons
- navLabel (CTkLabel): Label that shows the text of the sidebar 
- navBtnFrame (CTkFrame): Tkinter frame/container that has the buttons in the nav
- navBtns (Array): List that contains all of the tkinter buttons that are contained in the nav bar
- navBtnMap (Object/Map): Object/map that contains the text of the buttons (keys) and the name of the class/page that 
	the button is linked to. This allows buttons to link open certain pages when clicked

Methods:
- updateNavBtns(self): Adjusts the accessibility of the nav buttons based on their login state. 
- disableNavBtns(self): Disables the nav buttons from being used
'''

class Sidebar(ctk.CTkFrame):
	def __init__(self, master):
		# Put Sidebar in the master frame
		self.master = master
		super().__init__(master, fg_color=self.master.theme["main_clr"], corner_radius=0)
		sidebarFrame = ctk.CTkFrame(self, fg_color=self.master.theme["main_clr"], corner_radius=0)
		sidebarFrame.pack(expand=True)

		sidebar_bg = ctk.CTkImage(light_image=Image.open(os.path.join(self.master.image_path, "sidebar_bg_light.jpg")),
													 dark_image=Image.open(os.path.join(self.master.image_path, "sidebar_bg_dark.jpg")), size=((300), (850)))
		sidebar_bgPanel = ctk.CTkLabel(sidebarFrame, image=sidebar_bg, text=" ")
		sidebar_bgPanel.grid(row=0, column=0, sticky="ns")

		navbarBGFrame = ctk.CTkFrame(sidebarFrame, fg_color=self.master.theme["sub_clr"])
		navbarBGFrame.grid(row=0, column=0, sticky='nse')
		navbarBGFrame.grid_rowconfigure(6, weight=1)

		logo_image = ctk.CTkImage(Image.open(os.path.join(self.master.image_path, "BookSmartLogo.png")), size=(150, 150))
		sidebar_logo = ctk.CTkLabel(navbarBGFrame, text=" ", fg_color="transparent", image=logo_image, font=ctk.CTkFont(size=40, weight="bold"))
		sidebar_logo.grid(row=0, column=0, padx=20, pady=20)

		currentYear = datetime.datetime.now().year
		copyrightDateLabel = ctk.CTkLabel(navbarBGFrame, text=f"BookSmart {currentYear}", bg_color="transparent", fg_color="transparent", text_color=self.master.theme["label_clr"], font=("Helvetica", 20))
		copyrightDateLabel.grid(row=1, column=0)

		# List of all buttons in the sidebar
		self.navBtns = [] 

		buttons = {
			"Home": {
				"image_name": "glass_home_btn.png",
				"command": lambda: self.master.openPage("homePage"),
			},
			"AI Settings": {
				"image_name": "glass_settings_btn.png",
				"command": lambda: self.master.openPage("AISettingsPage"),
			},
			"My Library": {
				"image_name": "glass_library_btn.png",
				"command": lambda: self.master.openPage("storyLibraryPage"),
			},
			"My Account": {
				"image_name": "glass_account_btn.png",
				"command": lambda: self.master.openPage("userAccountPage"),
			},
			"Toggle Theme": {
				"image_name": "glass_theme_btn.png",
				"command": lambda: self.master.themeManager.toggleTheme(),
			},
			"Logout": {
				"image_name": "glass_logout_btn.png",
				"command": lambda: self.master.userSessionManager.confirmLogout(),
			}
		}
		
		for i, (btn_name, btn_info) in enumerate(buttons.items(), start=2):
			btn_image = ctk.CTkImage(Image.open(os.path.join(self.master.image_path, btn_info["image_name"])),
				size=(100, 100))
			
			navBtn = ctk.CTkButton(navbarBGFrame, image=btn_image, bg_color='transparent', fg_color='transparent', 
						  text=btn_name, hover_color=self.master.theme["hover_clr"], anchor="w", corner_radius=0, height=5, border_spacing=5,
				font=("Helvetica", 16, "bold"), text_color=self.master.theme["btn_text_clr"], command=btn_info["command"])
			
			navBtn.grid(row=i+1, column=0)

			self.navBtns.append(navBtn)  # Store the button with its name as the key

	def disableSidebarButtons(self):
		'''Disables all nav buttons'''
		for button in self.navBtns:
			button.configure(state="disabled")

	def updateSidebar(self):
		'''
		- Update the navigation buttons based on the user's login state.
		If the user is logged in:
		1. Enable sidebar.
		2. Allow users to click on the buttons to navigate to their respective places.

		Else the user is not logged in:
		1. Disable all navigation buttons that aren't the toggle theme button.
		2. Prevent users from clicking on those buttons, ensuring they cannot navigate to other pages until they log in.

		NOTE: 
		- The toggleThemeBtn is special as, it shouldn't be disabled even when the user 
			is logged out. So we make sure that we exclude it from being disabled. However we 
			will leave it so that this function can enable this button again in case it 
			was disabled by disableNavButtons.
		'''

		# Disable/Re-enable buttons based on login state; toggle theme is an exception as it always stays enabled.
		for button in self.navBtns:
			if (self.master.loggedInUser): 
				button.configure(state="standard")
			elif button.cget("text") != "Toggle Theme":
				button.configure(state="disabled")

		# Render sidebar depending on login state
		if (self.master.loggedInUser):
			self.master.enableSidebar()
		else:
		 	self.master.disableSidebar()
			 
'''
+ Themebar: Tkinter frame that represents the method to change themes of the application

Constructor:
- master (App): 'App' Class instance

Attributes/Variables:
- toggleThemeBtn (CTkButton): Button that allows user to change themes of the application
'''


'''
+ App: Root window of the tkinter or GUI application. It's our Main application window and it contains 
	data that we want to persist through different pages of the application.

Attributes/Variables:
- width (int): The viewport width of the client.
- height (int): The viewport height of the client. 
- currentPage (CTkFrame): The page that the application is currently rendering 
- loggedInUser (User): Represents the user that is currently logged into the application. If no user is logged in then
	this value is None.
- currentStory (Story): Can represent the saved story object that the user is continuing to write, or it represents the story
	that the user is using to remix off of. 
- isSavedStory (Bool): If true, currentStory is the story the user is continuing. Else, this means isRemixed story is True or False
- isRemixedStory (Bool): If true, currentStory is the story the user is using to remix off of. Note as a result their remixed story 
	isn't saved in the database yet. Else, this means isSavedStory is true or false.

NOTE: If both isSavedStory and isRemixedStory are false, then the user is not remixing a story and they aren't continuing a saved story.
	Basically it means the user is writing a brand new story that hasn't been saved into the database yet.

- unsavedStoryMessages (Array): Array of 'Message' objects that the user and AI have generated for a story, but they haven't been
	saved and linked to a story object in the database yet. These would represent the messages in their most recent chat session.
- engine (SqlAlchemy Engine): Sqlalchemy engine object that helps us connect to the database
- Session (SqlAlchemy Session Maker): Customized constructor that makes session objects for our database 
- session (SqlAlchemy Session): Session class instance that's used to interact with the database 
- header (CTkFrame): Header of the application
- footer (CTkFrame): Footer of the application

Methods:
- getPage(self, pageName): Searches for and returns a class/module with name pageName. This class is a tkinter frame and 
	is an individual page in our GUI application. 
- openPage(self, pageName, *args): Opens and loads a page in our tkinter application that has the name pageName.
	It passes, the 'App' class and then any potential arguments that the pageName class may take as parameters
- logoutUser(self): Logs out the currently logged in user from our application.
'''

# SECURITY NOTE: The UserSessionManager uses Python's `pickle` module to store the last logged-in
# user's username in 'last_user.pkl'. While this approach is convenient for a local desktop
# application to remember the last user, it's important to be aware of the security implications
# of `pickle`. Deserializing pickle files from untrusted sources can be dangerous and may lead to
# arbitrary code execution. 
# For this local application, the risk is mitigated as the file is written and read by the
# application itself on the user's machine. However, if this application were to be web-based
# or require higher security (e.g., handling sensitive data or multi-user environments not
# strictly local), this pickle-based session management would need to be replaced with more
# robust and secure methods. Such methods could include:
#   - Secure, http-only cookies with random session tokens.
#   - Server-side session management with encrypted session data.
#   - Use of industry-standard authentication libraries or frameworks.
class UserSessionManager:
	def __init__(self, app):
		self.app = app
		self.loggedInUser = None
		
	def saveLoginAs(self, userAccount, Username):	
		# Assign the new logged in user
		self.app.loggedInUser = userAccount
		self.app.loggedInUser.username = Username

		# Update the nav buttons now that the user is logged in
		# so that they actually work and aren't disabled
		self.app.sidebar.updateSidebar() 

		# Redirect the user to the 'My Account' or the 'user account page'
		self.app.openPage("userAccountPage") 
  
	def logoutUser(self):
		# loggedInUser is none because we are logging out the user
		self.loggedInUser = None
		# Remove the login authentication token because we are logging out the user
		# Use config for pickle file path
		pickle_path = os.path.join(PROJECT_ROOT, LAST_USER_PICKLE_FILE)
		if os.path.exists(pickle_path):
			os.remove(pickle_path)
		
		# Wipe currentStory and reset booleans for the new user. This is so the new user starts on a blank slate
		self.app.unsavedStoryMessages = [] 
		self.app.currentStory = None
		self.app.isSavedStory = False
		self.app.isRemixedStory = False

		# Clear AI knowledge of any stories the user is currently writing, if any, which prevents the user from logging back in and getting unexpected output
		# NOTE: More specifically when they login and 'continue' an unsaved story, it prevents AI from having knowledge of an interaction from another user or session.
		self.app.storyGPT.chatHistory.clear()

		# Redirect the user to the login page
		self.app.openPage("userLoginPage")

		# Update nav buttons so that user can't access the pages associated with them
		self.app.sidebar.updateSidebar()
  
	def confirmLogout(self):
		response = messagebox.askquestion('Log out?', f'Are you sure you want to logout {self.app.loggedInUser.username}?')
		if response == 'yes':
			self.logoutUser()  # Calls the function for quitting the app
		elif response == 'no':
			pass
		else:
			messagebox.showwarning('error', 'Something went wrong!')
   
	def checkForPrevUser(self):
		try:
			# Use config for pickle file path
			pickle_path = os.path.join(PROJECT_ROOT, LAST_USER_PICKLE_FILE)
			if os.path.exists(pickle_path):
				with open(pickle_path, 'rb') as f:
					last_username = pickle.load(f) # Now you can use `last_username` to log in
					# Use the new service function to get the user
					last_User = get_user_by_username(last_username)
					if last_User:
						self.saveLoginAs(last_User, last_username)
			else:
				# If no previous user found or the previosly logged in user logged out, direct them to the login page
				self.app.openPage("userLoginPage")
		except (OSError, IOError, pickle.UnpicklingError) as e:
			print(f"Error reading '{LAST_USER_PICKLE_FILE}': {e}")
			# Handle error or fallback
		except Exception as e:
			print(f"Unexpected error checking for previous user: {e}")
			# Handle unexpected exceptions

class ThemeManager:
	def __init__(self, app):
		self.app = app
		self.isDarkTheme = True
		
	def applyTheme(self):
		'''Applies color changes to the application'''
		if (self.isDarkTheme):
			ctk.set_appearance_mode("Dark")
		else:
			ctk.set_appearance_mode("Light")

	def toggleTheme(self):
		'''Toggles theme of the application and reloads the page to show the changes '''
		self.isDarkTheme = not (self.isDarkTheme)
		self.applyTheme()

class App(ctk.CTk):
	width = 1280
	height=800
	def __init__(self):
		# Initialize window and resize it based on the user's viewport width and height
		super().__init__()
		self.title("BookSmart.Ai")
		# Use config for icon path
		self.iconbitmap(os.path.join(PROJECT_ROOT, IMAGES_SUBDIRECTORY, ICON_FILE))
		self.width = self.winfo_screenwidth()
		self.geometry(f"{self.width}x{self.winfo_screenheight()}")
		# AI model class instance that's going to be used throughout the application
		# Use config for image_path
		self.image_path = os.path.join(PROJECT_ROOT, IMAGES_SUBDIRECTORY)
		self.storyGPT = StoryGPT()

		'''
		- currentPage: Tkinter frame class representing the current page the user is on
		- loggedInUser: User object that represents the user that's currently logged into the application
		- currentStory: Current story object that the user has selected and is editing with. 
			Useful for rendering the saved messages for a selected story.
		- isSavedStory: Boolean indicating whether the story the user is on is already saved into the database or not
		- isRemixedStory: Boolean indicating whether the stor ythe user is writing is a remix
		- unsavedStoryMessages: Array of message objects that represent the messages that the 
			user and ai have written that haven't been saved into a story yet
		- storyGenObj: Generator object that will yield the AI's response message to the user's query
		
		- remixStoryObj: Story object that the user is planning to make a remix on.
			It's useful to store this in Main, as the user may want to toggle the theme, which'll reload 
			the page. So we need that same story they wanted to remix when reloading
		'''
		self.themeManager = ThemeManager(self)
		self.userSessionManager = UserSessionManager(self)
		self.loadedPages = {}
		self.currentPage = None
		self.loggedInUser = None  
		self.currentStory = None
		self.isSavedStory = False
		self.isRemixedStory = False
		self.unsavedStoryMessages = []
		self.storyGenObj = None
		self.remixStoryObj = None
		#Initialize current AI mode Balanced at startup
		self.currentMode='Balanced'
		self.currentModeKey=0
		self.msgboxes=[]
		'''
		- Map of colors for the theme. Value in left tuple 
			is light theme color, while value in right tuple 
			is dark theme color
		'''
		# Use theme from config
		self.theme = THEME_COLORS
		# self.isDarkTheme is removed from App class as ThemeManager handles its own theme state.
	
		# self.engine and self.session are no longer initialized here
		# as UserSessionManager now uses get_user_by_username,
		# and no other App methods directly use the session.
		# If other components need DB access, they should call get_session()
		# or use a relevant service function.
		self.engine = db_engine # Retained for now if any page relies on app.engine
		                         # TODO: Audit and remove if app.engine is not used by pages

		# Apply theme of application
		self.themeManager.applyTheme()

		self.sidebar = Sidebar(self)

		self.userSessionManager.checkForPrevUser()
	
	def enableSidebar(self):
		self.sidebar.pack(side="left", fill="y")
	
	def disableSidebar(self):
		self.sidebar.pack_forget()

	'''
	- Returns a class of a page (a tkinter frame) for the application 
	1. module: Python module/file as an object.
	2. pageClass: A class for a tkinter frame
	'''
	def getPage(self, pageName):
		try:
			# import the module using the path.
			module = importlib.import_module(f"pages.{pageName}")
			# get the page class from the module
			pageClass = getattr(module, pageName)
			return pageClass
		except (ImportError, AttributeError) as e:
			print(e)
			return None

	def getPageLazy(self, pageName):
		if pageName not in self.loadedPages:
			pageClass = self.getPage(pageName)
			if pageClass:
				self.loadedPages[pageName] = pageClass
		return self.loadedPages.get(pageName, None)
	
	'''
	- Loads and opens a page with pageName in the tkinter application
	1. pageName: The name of the class for the page that's being opened
	'''  
	def openPage(self, pageName, *args):
		pageClass = self.getPageLazy(pageName) # pageClass is now the constructor for the page
		if not pageClass:
			return
		
		# If there is a currentPage already, destroy it, then reassign it to the new page class
		# We pageClass to create the tkinter frame, and pass in self (App class), and any potential arguments
		if self.currentPage:
			self.currentPage.destroy()
		
		# Create an instance of the page, passing 'self' (the App instance)
		# The page's __init__ method will receive 'self' as 'master' or 'app_instance'
		self.currentPage = pageClass(self, *args) 
  
		# Pack the new page on the screen
		self.currentPage.pack(fill="both", expand=True)
		
# Make it so application can only be run from this file; 'python Main.py'
if __name__ == "__main__":
	app = App()
	app.mainloop()