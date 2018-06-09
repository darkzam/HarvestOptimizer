import pulp
import pandas as pd

class InputObject:
	
	benefit = 0
	bestSolution = []
	optTimes = []
	solution = ''
	cantidadParcelas = 0
	tiempoParcelas = []
	sumaTiempos = 0
	utilidadesParcelas = []

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

		#Restricciones de variables y
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


		for i in range(0,self.cantidadParcelas):
		    my_lp_problem += varTc[i] + self.tiempoParcelas[i] <= self.sumaTiempos


		my_lp_problem.solve()
		pulp.LpStatus[my_lp_problem.status]


		#print("por aca paso1")

		for variable in my_lp_problem.variables():
		    print("{} = {}".format(variable.name,variable.varValue))
		    if variable.name.find("Tc")!= -1:
		    	self.bestSolution.append(variable)
		    	self.optTimes.append(variable.varValue)
		    	self.solution = self.solution + " {} = {}".format(variable.name,variable.varValue)

		print(pulp.value(my_lp_problem.objective))

		self.benefit = pulp.value(my_lp_problem.objective)
		#print(my_lp_problem)

	def readFile(self, path):

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

		archivo = open("solution.txt", 'w')
		archivo.write(str(self.benefit)+"\n")
		archivo.write(' '.join(str(e)for e in self.optTimes))
		archivo.close()
