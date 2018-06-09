
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
runTime = StringVar()

def readfile(path):

		inputObject = InputObject()
		inputObject.readFile(path)
		tileAmount.set(inputObject.cantidadParcelas)
		tileTimes.set(' '.join(str(e)for e in inputObject.tiempoParcelas))
		totalTime.set(inputObject.sumaTiempos)
		tileUtilities.set(' '.join(str(e)for e in inputObject.utilidadesParcelas))
		#print(fileName.get())

def run():
		#print("run algorithm")
		#print(cantidadParcelas)
		inputObject = InputObject()
		inputObject.readFile(pathFile.get())
		inputObject.harvest()
		benefit.set(int(inputObject.benefit))
		optimum.set(inputObject.solution)
		runTime.set(str(inputObject.runningTime) + " ms")
		inputObject.writeFile()
	

def browseFile(event):
		print(tileUtilities.get())
		root.fileName = askopenfilename(filetypes=(("Tile Texts", ".txt"),("All files","*.*")))	
		fileName.set("File Path: "+ root.fileName)
		pathFile.set(root.fileName)
		readfile(root.fileName)

topFrame = Frame(root, bg="#006600")
topFrame.pack()

bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

label1 = Label(topFrame,fg="#1aff1a",text="Welcome to Harvest Optimizer",bg="#006600", font="Arial 14 bold")
label1.pack()

label2 = Label(topFrame,fg="#1aff1a",text="Please Select a farm file before beginning",bg="#006600")
label2.config(font=("Arial", 12))
label2.pack()

bt1 = Button(topFrame, text="Select Input File", width=20, bg="blue")
bt1.config(font=("Arial",10))
bt1.bind("<ButtonRelease-1>",browseFile)
bt1.pack()

labelFile = Label(topFrame, textvariable = fileName )
labelFile.config(font=("Arial", 14))
labelFile.pack()

label3 = Label(bottomFrame,text="Data input")
label3.config(font=("Arial", 14))
label3.pack()

label4 = Label(bottomFrame,text="Tile Amount:")
label4.config(font=("Arial", 14))
label4.pack()
tileAmountLabel = Label(bottomFrame,textvariable= tileAmount)
tileAmountLabel.config(font=("Arial", 12),fg="red")
tileAmountLabel.pack()

label5 = Label(bottomFrame,text="Tile Times:")
label5.config(font=("Arial", 14))
label5.pack()
tileTimesLabel = Label(bottomFrame,textvariable= tileTimes)
tileTimesLabel.config(font=("Arial", 12),fg="red")
tileTimesLabel.pack()

label6 = Label(bottomFrame,text="Total time:")
label6.config(font=("Arial", 14))
label6.pack()
totalTimeLabel = Label(bottomFrame,textvariable= totalTime)
totalTimeLabel.config(font=("Arial", 12),fg="red")
totalTimeLabel.pack()

label7 = Label(bottomFrame,text="Tile Utility:")
label7.config(font=("Arial", 14))
label7.pack()
tileUtilitiesLabel = Label(bottomFrame,textvariable= tileUtilities, justify=LEFT)
tileUtilitiesLabel.config(font=("Arial", 12),fg="red")
tileUtilitiesLabel .pack()

bt2 = Button(bottomFrame, text="Run", width=20, bg="gray", command=run)
#bt2.bind("<ButtonRelease-1>",run)
bt2.pack()

label8 = Label(bottomFrame,text="Maximum Benefit")
label8.config(font=("Arial", 14))
label8.pack()

labelBenefit = Label(bottomFrame,textvariable= benefit)
labelBenefit.config(font=("Arial", 12),fg="blue")
labelBenefit.pack()

label9 = Label(bottomFrame,text="Optimal Harvesting")
label9.config(font=("Arial", 14))
label9.pack()

labelOptimum = Label(bottomFrame,textvariable= optimum)
labelOptimum.config(font=("Arial", 12),fg="blue")
labelOptimum.pack()

label10 = Label(bottomFrame,text="Running Time")
label10.config(font=("Arial", 14))
label10.pack()

labelRunTime = Label(bottomFrame,textvariable= runTime)
labelRunTime.config(font=("Arial", 12),fg="blue")
labelRunTime.pack()

root.title("HarvestOptimizer")
root.mainloop()

