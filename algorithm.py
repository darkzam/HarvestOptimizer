import pulp
import pandas as pd
import time

class InputObject:
	
	benefit = 0
	bestSolution = []
	optTimes = []
	solution = ''
	cantidadParcelas = 0
	tiempoParcelas = []
	sumaTiempos = 0
	utilidadesParcelas = []
	runningTime = 0

	def __init__(self, cantidadParcelas = 0, tiempoParcelas = [], sumaTiempos = 0, utilidadesParcelas = []):
		self.cantidadParcelas = cantidadParcelas
		self.tiempoParcelas = tiempoParcelas
		self.sumaTiempos = sumaTiempos
		self.utilidadesParcelas = utilidadesParcelas

	def harvest(self):

		bigM = 43204232

		my_lp_problem = pulp.LpProblem("Planificacion de cosechas de hortalizas", pulp.LpMaximize)

		#Variables de decision
		indicesParcelas = []
		for i in range(0, self.cantidadParcelas) :
		    indicesParcelas.append(i)

		indicesTiempos = []
		for i in range(0, self.sumaTiempos) :
		    indicesTiempos.append(i)

		#Variables de decision
		varT = pulp.LpVariable.dicts('T',(indicesParcelas, indicesTiempos), cat='Binary')
		varTc = pulp.LpVariable.dicts('Tc',(indicesParcelas), lowBound=0, upBound=self.sumaTiempos-1,cat='Integer')
		#variables auxiliares
		varY = pulp.LpVariable.dicts('Y', (tiempo for tiempo in range(0,(self.cantidadParcelas-1)*self.cantidadParcelas)),cat='Binary')

		#Funcion objetivo
		my_lp_problem += pulp.lpSum([self.utilidadesParcelas[parcela][tiempo] * varT[parcela][tiempo]
		    for parcela in indicesParcelas for tiempo in indicesTiempos]), "Z"


		#Restriccion: Se cosecha una y solo una vez en cada parcela
		for i in range(0, self.cantidadParcelas):
		    my_lp_problem += pulp.lpSum([varT[i][tiempos] for tiempos in indicesTiempos]) == 1

		#Restriccion: No se puede cosechar en mas de una parcelas al mismo tiempo
		for i in range(0, self.sumaTiempos):
		    my_lp_problem += pulp.lpSum([varT[parcela][i] for parcela in indicesParcelas]) <= 1


		#Restriccion: Asociacion de la variable de decision Tc con T
		for i in range(0, self.cantidadParcelas):
		    my_lp_problem+= pulp.lpSum([tiempos * varT[i][tiempos]] for tiempos in range(0,self.sumaTiempos)) == varTc[i]

		#Restriccion: Asociacion de variables auxiliares para aplicar el OR (Y1 + Y2 == 1)
		count1 = 0
		valor=0
		for i in range (0,(self.cantidadParcelas-1)):
		    for j in range(1, self.cantidadParcelas):
		        valor+= self.cantidadParcelas-1
		        if count1%self.cantidadParcelas == 0 and count1!=0:
		            valor = count1 + self.cantidadParcelas-1
		        if count1%(self.cantidadParcelas-1) == 0 and count1 != 0:
		            #print count1, ((count1/(cantidadParcelas-1))-1)
		            valor = ((count1/(self.cantidadParcelas-1))-1)
		        else:
		            #print(count1, valor)
		            my_lp_problem += (varY[count1] + varY[valor]) == 1
		        count1+=1


		#Restriccion: Cuando termina una parcela, en el tiempo + 1 debe iniciar la siguiente
		count = 0
		for i in range(0, self.cantidadParcelas):
		    for j in range(0,self.cantidadParcelas):
		        if i!=j:
		            my_lp_problem += ((varTc[i] + self.tiempoParcelas[i])) <= varTc[j] + bigM * (1 - varY[count])
		            #print(count , ": " , i, j)
		            count+=1

		#Restriccion: El ultimo momento en el que puede iniciar una parcela es en: ultimo timepo - duracion de cosecha
		#no se le resta uno ya que nuestro primer tiempo es 0
		for i in range(0,self.cantidadParcelas):
		   # my_lp_problem += varTc[i] + self.tiempoParcelas[i] <= self.sumaTiempos
		    my_lp_problem += varTc[i] <= (self.sumaTiempos - self.tiempoParcelas[i])

		time1 = int(round(time.time() * 1000))
		my_lp_problem.solve()
		time2 = int(round(time.time() * 1000))
		self.runningTime = time2 - time1

		pulp.LpStatus[my_lp_problem.status]


		#print("por aca paso1")
		self.optTimes = []
		contador2 = 1

		for variable in my_lp_problem.variables():
		    print("{} = {}".format(variable.name,variable.varValue))
		    if variable.name.find("Tc")!= -1:
		    	self.bestSolution.append(variable)
		    	self.optTimes.append(int(variable.varValue)+1)
		    	self.solution = self.solution + "[Parcela " + str(contador2)+": " + str(int(variable.varValue)+1)+"] "
		    	contador2 += 1

		print(pulp.value(my_lp_problem.objective))

		self.benefit = pulp.value(my_lp_problem.objective)
		#print(my_lp_problem)

	def readFile(self, path):

		self.utilidadesParcelas = []
		self.tiempoParcelas = []

		archivo = open(path, 'r')
		contador = 0
		for linea in archivo.readlines():
			if contador == 0 :
				self.cantidadParcelas = int(linea)
			if contador == 1 :
				for tiempo in linea.strip().split(" "):
					self.tiempoParcelas.append(int(tiempo))
			if contador == 2 :
				self.sumaTiempos = int(linea)
			if contador > 2 :
				utilidadParcela = []
				for utilidad in linea.strip().split(" "):
					utilidadParcela.append(int(utilidad))
				self.utilidadesParcelas.append(utilidadParcela)
			contador = contador + 1
		archivo.close()

	def writeFile(self):

		open("solution.txt", 'w').close()
		archivo = open("solution.txt", 'w')
		archivo.write(str(int(self.benefit))+"\n")
		archivo.write(' '.join(str(e)for e in self.optTimes)+"\n")
		archivo.close()
