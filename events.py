
from tkFileDialog import *

def browseFile():
		root.fileName = askopenfilename(filetypes=(("Tile Texts", ".txt"),("All files","*.*")))	