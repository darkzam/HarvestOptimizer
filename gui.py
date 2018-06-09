
from Tkinter import *
from tkFileDialog import *
from algorithm import InputObject

root = Tk()

pathFile = StringVar()
fileName = StringVar()
tileAmount = StringVar()
tileTimes = StringVar()
totalTime = StringVar()
tileUtilities = StringVar()

benefit = StringVar()
optimum = StringVar()

def readfile(path):

		inputObject = InputObject()
		inputObject.readFile(path)
		tileAmount.set("")
		tileTimes.set("")
		totalTime.set("")
		tileUtilities.set("")
		tileAmount.set(inputObject.cantidadParcelas)
		tileTimes.set(' '.join(str(e)for e in inputObject.tiempoParcelas))
		totalTime.set(inputObject.sumaTiempos)
		tileUtilities.set(' '.join(str(e)for e in inputObject.utilidadesParcelas))
		#print(cantidadParcelas)

def run():
		#print("run algorithm")
		#print(cantidadParcelas)
		inputObject = InputObject()
		inputObject.readFile(pathFile.get())
		inputObject.harvest()
		benefit.set(inputObject.benefit)
		optimum.set(inputObject.solution)
		inputObject.writeFile()
	

def browseFile(event):
		root.fileName = askopenfilename(filetypes=(("Tile Texts", ".txt"),("All files","*.*")))	
		fileName.set("File Path: "+ root.fileName)
		pathFile.set(root.fileName)
		readfile(root.fileName)

topFrame = Frame(root, width=400, height=200)
topFrame.pack()

bottomFrame = Frame(root, width=400, height=300)
bottomFrame.pack(side=BOTTOM)

label1 = Label(topFrame,text="Welcome to Harvest Optimizer")
label1.pack()

label2 = Label(topFrame,text="Please Select a farm file before beginning")
label2.pack()

bt1 = Button(topFrame, text="Select Input File", fg="blue")
bt1.bind("<ButtonRelease-1>",browseFile)
bt1.pack()

labelFile = Label(topFrame, textvariable = fileName )
labelFile.pack()

label3 = Label(bottomFrame,text="Data input")
label3.pack()

label4 = Label(bottomFrame,text="Tile Amount:")
label4.pack()
tileAmountLabel = Label(bottomFrame,textvariable= tileAmount)
tileAmountLabel.pack()

label5 = Label(bottomFrame,text="Tile Times:")
label5.pack()
tileTimesLabel = Label(bottomFrame,textvariable= tileTimes)
tileTimesLabel.pack()

label6 = Label(bottomFrame,text="Total time:")
label6.pack()
totalTimeLabel = Label(bottomFrame,textvariable= totalTime)
totalTimeLabel.pack()

label7 = Label(bottomFrame,text="Tile Utility:")
label7.pack()
tileUtilitiesLabel = Label(bottomFrame,textvariable= tileUtilities)
tileUtilitiesLabel .pack()

bt2 = Button(bottomFrame, text="Run", fg="red", command=run)
#bt2.bind("<ButtonRelease-1>",run)
bt2.pack()

labelSolution = Label(bottomFrame,text="Solution:")
labelSolution.pack()

label8 = Label(bottomFrame,text="Maximum Benefit")
label8.pack()

labelBenefit = Label(bottomFrame,textvariable= benefit)
labelBenefit.pack()

label9 = Label(bottomFrame,text="Optimal Harvesting")
label9.pack()

labelOptimum = Label(bottomFrame,textvariable= optimum)
labelOptimum.pack()

root.title("HarvestOptimizer")
root.mainloop()

