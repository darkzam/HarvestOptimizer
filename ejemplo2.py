import pandas as pd
import pulp

archivo = open('archivo1entrada.txt', 'r')
contador = 0

#Entradas
cantidadParcelas = 0
tiempoParcelas = []
sumaTiempos = 0
utilidadesParcelas = []


for linea in archivo.readlines():
    if contador == 0 :
        cantidadParcelas = int(linea)
    if contador == 1 :
        for tiempo in linea.strip().split(" "):
            tiempoParcelas.append(int(tiempo))
    if contador == 2 :
        sumaTiempos = int(linea)
    if contador > 2 :
        utilidadParcela = []
        for utilidad in linea.strip().split(" "):
            utilidadParcela.append(int(utilidad))
        utilidadesParcelas.append(utilidadParcela)
    contador = contador + 1
archivo.close()

bigM = 43204232

my_lp_problem = pulp.LpProblem("Planificacion de cosechas de hortalizas", pulp.LpMaximize)

#Variables de decision
indicesParcelas = []
for i in range(0, cantidadParcelas) :
    indicesParcelas.append(i)

indicesTiempos = []
for i in range(0, sumaTiempos) :
    indicesTiempos.append(i)

#Variables de decision
varT = pulp.LpVariable.dicts('T',(indicesParcelas, indicesTiempos), cat='Binary')
varTc = pulp.LpVariable.dicts('Tc',(indicesParcelas), lowBound=0, upBound=sumaTiempos-1,cat='Integer')
#variables auxiliares
varY = pulp.LpVariable.dicts('Y', (tiempo for tiempo in range(0,(cantidadParcelas-1)*cantidadParcelas)),cat='Binary')
#print varY
#Funcion objetivo
my_lp_problem += pulp.lpSum([utilidadesParcelas[parcela][tiempo] * varT[parcela][tiempo]
    for parcela in indicesParcelas for tiempo in indicesTiempos]), "Z"


#Restriccion: Se cosecha una y solo una vez en cada parcela
for i in range(0, cantidadParcelas):
    my_lp_problem += pulp.lpSum([varT[i][tiempos] for tiempos in indicesTiempos]) == 1

#Restriccion: No se puede cosechar en mas de una parcelas al mismo tiempo
for i in range(0, sumaTiempos):
    my_lp_problem += pulp.lpSum([varT[parcela][i] for parcela in indicesParcelas]) == 1


#Restriccion: Asociacion de la variable de decision Tc con T


for i in range(0, cantidadParcelas):
    my_lp_problem+= pulp.lpSum([tiempos * varT[i][tiempos]] for tiempos in range(0,sumaTiempos)) == varTc[i]



#Restricciones de variables y
count1 = 0
valor=0
for i in range (0,(cantidadParcelas-1)):
    for j in range(1, cantidadParcelas):
        valor+= cantidadParcelas-1
        if count1%cantidadParcelas == 0 and count1!=0:
            valor = count1 + cantidadParcelas-1

        if count1%(cantidadParcelas-1) == 0 and count1 != 0:
            #print count1, ((count1/(cantidadParcelas-1))-1)
            valor = ((count1/(cantidadParcelas-1))-1)
            #my_lp_problem += (varY[count1] + varY[valor]) == 1
        else:
            print count1, valor
            my_lp_problem += (varY[count1] + varY[valor]) == 1
        count1+=1




#Restriccion: Variables auxiliares
#count = 0
#sum = 0
#for i in range (0,(cantidadParcelas-1)*cantidadParcelas):
#    for j in range (0, cantidadParcelas-1):
#        my_lp_problem += (varY[count] + varY[(cantidadParcelas-1)*(i+j+1)+sum]) == 1
#
#        print count, ((cantidadParcelas-1)*(i+j+1)+ sum), sum, i
#        if (cantidadParcelas == ((count+2)/(i+1))):
#            sum += 1
#        count += 1
#    count += 1


#Restriccion: Cuando termina una parcela, en el tiempo + 1 debe iniciar la siguiente
count = 0
for i in range(0, cantidadParcelas):
    for j in range(0,cantidadParcelas):
        if i!=j:
            my_lp_problem += ((varTc[i] + tiempoParcelas[i])-1) <= varTc[j] + bigM * (1 - varY[count])
            print count , ": " , i, j
            count+=1


    #my_lp_problem += (varTc[i] + tiempoParcelas[i]) <= (varTc[i-1] + bigM * (1 - varY2))
    #print(varTc[i] + tiempoParcelas[i] + 1)

#for i in range(0,cantidadParcelas):
#    my_lp_problem += varTc[i] <= sumaTiempos - tiempoParcelas[i] -1

my_lp_problem+= pulp.lpSum([(varTc[i]+tiempoParcelas[i])-1] for i in range(0,cantidadParcelas))== sumaTiempos




my_lp_problem.solve()
pulp.LpStatus[my_lp_problem.status]

for variable in my_lp_problem.variables():
    print("{} = {}".format(variable.name,variable.varValue))

print (pulp.value(my_lp_problem.objective))

print(my_lp_problem)
print sumaTiempos
