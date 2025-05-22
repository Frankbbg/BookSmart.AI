import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DATABASE_FILENAME = "PyProject.db"
DATABASE_SUBDIRECTORY = "assets"
DATABASE_PATH = os.path.join(PROJECT_ROOT, DATABASE_SUBDIRECTORY, DATABASE_FILENAME) # Full path

ICON_FILENAME = "BookSmartLogo.ico" # Just the filename
IMAGES_SUBDIRECTORY = os.path.join("assets", "images") # Relative to project root

LAST_USER_PICKLE_FILE = "last_user.pkl" # Just the filename, assumed in PROJECT_ROOT

# Theme colors, directly copied and adapted from Main.py
THEME_COLORS = {
    "main_clr": ("#E9EDEF", "#030712"),
    "sub_clr": ("#9ca3af", "#0f172a"),
    "label_clr": ("#000000", "#FFFFFF"),
    "btn_clr": ("#4267B2", "#9ca3af"),
    "btn_text_clr": "#FFFFFF",
    "hover_clr": ("#34d399", "#4267B2"),
    "entry_clr": ("#FFFFFF", "#374151"),
    "entry_text_clr": ("#000000", "#FFFFFF"),
}

# For convenience, you might also want to define full paths here if used often
FULL_IMAGES_PATH = os.path.join(PROJECT_ROOT, IMAGES_SUBDIRECTORY)
FULL_ICON_PATH = os.path.join(FULL_IMAGES_PATH, ICON_FILENAME)
# However, the task asks for Main.py to construct some of these, so I will stick to that.
# FULL_LAST_USER_PICKLE_PATH = os.path.join(PROJECT_ROOT, LAST_USER_PICKLE_FILE)
# Let Main.py handle os.path.join(PROJECT_ROOT, LAST_USER_PICKLE_FILE) for now.
# This way, if LAST_USER_PICKLE_FILE needs to move, only config.py changes.
# No, the task implies Main.py will use PROJECT_ROOT and LAST_USER_PICKLE_FILE.
# So, LAST_USER_PICKLE_FILE should just be the filename.
# The icon path in Main.py is specified as os.path.join(PROJECT_ROOT, IMAGES_SUBDIRECTORY, ICON_FILE)
# So ICON_FILE in config should be ICON_FILENAME.

# Renaming ICON_FILE to ICON_FILENAME to avoid confusion as it's just a name.
# Main.py will construct os.path.join(PROJECT_ROOT, IMAGES_SUBDIRECTORY, ICON_FILENAME)
# The task description for Main.py:
# Icon path: os.path.join(PROJECT_ROOT, IMAGES_SUBDIRECTORY, ICON_FILE)
# This means ICON_FILE in config.py should indeed be just the filename.
# So, ICON_FILENAME is correct.
# IMAGES_SUBDIRECTORY is also correct as specified.
# LAST_USER_PICKLE_FILE is also correct as just the filename.
# DATABASE_PATH is a convenience, but Database.py is asked to construct it.
# I'll provide both DATABASE_PATH and its components for flexibility,
# but ensure Database.py uses the components as requested.
# Let's refine DATABASE_PATH to be constructed as required by Database.py,
# and the individual components.
# The task says: "Define variables in config.py for: ... DATABASE_SUBDIRECTORY ... (or a full DATABASE_PATH)"
# And then for Database.py: "Construct db_path using these imported config values: os.path.join(PROJECT_ROOT, DATABASE_SUBDIRECTORY, DATABASE_FILENAME)"
# So, Database.py does the join.
# So, config.py should provide PROJECT_ROOT, DATABASE_SUBDIRECTORY, DATABASE_FILENAME.
# The DATABASE_PATH I defined above in config.py is fine as an *additional* variable, but not the one Database.py will primarily use.

# Final check on variables for config.py:
# - DATABASE_FILENAME = "PyProject.db" (Correct)
# - DATABASE_SUBDIRECTORY = "assets" (Correct)
# - ICON_FILE = "BookSmartLogo.ico" (Correct, will use this name: ICON_FILE)
# - IMAGES_SUBDIRECTORY = "assets/images" (Correct)
# - LAST_USER_PICKLE_FILE = "last_user.pkl" (Correct)
# - THEME_COLORS (Correct)
# - PROJECT_ROOT (Correct)

# Re-writing with only the specifically requested variable names for clarity and adherence to task.
# I will use ICON_FILE as the variable name for the icon's filename.
# I will remove the pre-constructed DATABASE_PATH from config.py as Database.py needs to construct it.
# I will also remove FULL_IMAGES_PATH and FULL_ICON_PATH as Main.py is specified to construct them.
# This keeps config.py as a list of basic components as much as possible.
# The task for Main.py says:
# Icon path: os.path.join(PROJECT_ROOT, IMAGES_SUBDIRECTORY, ICON_FILE)
# self.image_path: os.path.join(PROJECT_ROOT, IMAGES_SUBDIRECTORY)
# This means config.py should provide PROJECT_ROOT, IMAGES_SUBDIRECTORY, and ICON_FILE (as filename).
# This looks consistent.
