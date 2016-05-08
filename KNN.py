import math
import time 
import sys
def case1(file_path):
	file  = open(file_path, "r")
	boo = 0
	for line in file:
		aux = line	
		aux1 = line.split(',')
		aux1[len(aux1)-1]=aux1[len(aux1)-1].rstrip() #para tirar o \n da string classe
		if(boo==0): #so entra aqui uma vez no arquivo todo
			number_att = len(aux1)-1
			boo=1
		temp_entity = entity_training()
		temp_entity.attributes = []
		for b in range (number_att) :
			temp_entity.attributes.append(float(aux1[b]))
		temp_entity.classification = (aux1[b+1])
		temp_entity.distance = 0
		all_classes.append(aux1[b+1])
		training.append(temp_entity)
	file.close
	
def find_normalicacao(training,total_att):
	for l in range(total_att):
		temp =aque()
		temp.max = -sys.maxsize
		temp.min = sys.maxsize
		normalizacao.append(temp)
	for i in range(len(training)):
		temp1 = training[i].attributes
		for j in range(len(temp1)):
			temp2 = normalizacao[j]
			#print("atributo ", j , "valor de entrada ",temp1[j], " o que eu tenho max" , temp2.max," min " ,temp2.min)
			if(temp1[j]>temp2.max):
				temp2.max = temp1[j]
			if(temp1[j]<temp2.min):
				temp2.min = temp1[j]
			
class aque:
	max = 0 #vai ter o menor valor possivel
	min = 0 #vai ter o maior valor possivel

def euclidian (array,target,normalizacao): 
	aux = 0
	total = [0 for l in range (len(array))]
	#print('target: ',target.att1, ' ', target.att2, ' ', target.att3, ' ', target.att4, ' ', target.att5)
	i=0
	for i in range (len(array)):
		#print('array: ', array[i].att1, ' ', array[i].att2, ' ', array[i].att3, ' ', array[i].att4, ' ', array[i].att5)
		diff = 0
		for j in range(len(target.attributes)):
			temp = normalizacao[j]
			r = (temp.max-temp.min)
			if(r==0):
				r=1
			#print("max ",temp.max ," min " , temp.min, "range ",r)
			diff = diff + math.pow(((target.attributes[j]-array[i].attributes[j])/r),2)
		#diff = math.pow((target.att1 - array[i].att1),2) + math.pow((target.att2 - array[i].att2),2) + math.pow((target.att3 - array[i].att3),2) + math.pow((target.att4 - array[i].att4),2)+ math.pow((target.att5 - array[i].att5),2)
		#print('diff ',diff)
		#aux =  math.pow(diff,2) 
		raiz = math.sqrt(diff)
		#print(i,"Distancia :",diff)
		array[i].distance = diff

	return array 


def calc_classification(k,training_example):
	classe1 =0
	classe2 =0
	classes = {}
	for i in range (k) :
		if(training_example[i].classification in classes.keys()):
			classes[training_example[i].classification] = classes[training_example[i].classification]+1
		else : 
			classes[training_example[i].classification] =1
	
	classification = maxi(classes,max(classes.values()))
	#print("classificacao ",classification)
	return classification

def maxi(classes,x):
	#print("classes ",x)
	for key in classes.keys():
		if(classes[key]==x):
			return key 
	return 1

def calc_classification_weighted (k,training_example):

	classes = {}
	for i in range (k) :
		if(training_example[i].classification in classes.keys()):
			if(training_example[i].distance==0):
				return training_example[i].classification
			else:
				classes[training_example[i].classification] = classes[training_example[i].classification]+(1/training_example[i].distance)
		else : 
			classes[training_example[i].classification] =1
	classification = maxi(classes,max(classes.values()))
	#print("classificacao ",classification)
	return classification



class entity_training :
	attributes =[]
	classification = 0
	distance = 0

class entity_test :
	attributes=[]
	classification_from_Knn = []
	classification_real = 0
	distance = 0

def imprime_array(array):
	print('--------------------------------------------------')
	for i in range(len(array)):
		print('array na posicao ',i , 'e a classe igual a ',array[i].classification, " distancia para x eh ",array[i].distance)
		#print('array na posicao ',i , 'e a classe igual a ',array[i].classification,"atributos ",array[i].attributes, " distancia para x eh ",array[i].distance)
		


def imprime_array_test(array):
	print('--------------------------------------------------')
	print(" Tamanho  do teste eh ",len(array))
	for i in range(len(array)):
		for j in range(len(values_k)):		
			print('array na posicao ',i , ' a classe real eh : ',array[i].classification_real , 'e a classe calculada eh  ',array[i].classification_from_Knn[j], ' para o k igual a ', values_k[j])

def imprime_test_bytest(array,j,i):
	print('array na posicao ',i , ' a classe real eh : ',array[i].classification_real , 'e a classe calculada eh  ',array[i].classification_from_Knn[j], ' para o k igual a ', values_k[j])

def vdmg(training,target,number_classes,m) : 
	total = 0
	numb_att = len (target.attributes)
	for j in range (len(training)) :
		total = 0
		#print("calculando distancia par ao treinamento ", j )
		for i in range (numb_att):
			#print(" calculando vdm para o atributo ",i)
			a=target
			ai = a.attributes[i]
			b = training[j]
			bi = b.attributes[i]
			total = total + vdm(i,ai,bi,training,number_classes)
		#print("treinamento ",j, 'diatancia foi de' , math.sqrt(total))
		training[j].distance = math.sqrt(total)
	return training


def vdm(i,ai,bi,training,number_classes):
	q = 2
	total = 0
	for x in range (number_classes):
		c = all_classes[x]
		retorno = probabilities(ai,bi,c,i,training,number_classes)
		total = total + math.pow(retorno,q)
	return total


def probabilities(ai,bi,c,i,training,number_classes):
	count_Niac =0
	count_Nibc = 0
	Nai = 0
	Nbi = 0
	for j in range(len(training)) :
		if(training[j].attributes[i]==ai and training[j].classification==c):
			count_Niac = count_Niac+1
		elif(training[j].attributes[i]==bi and training[j].classification==c):
			count_Nibc = count_Nibc+1
	dic = all_attributes[i]
	#print("dicionario " , dic, "a : " , a, "b " ,b)
	if(ai not in dic.keys()) : 
		Nai = 0 
	elif(bi not in dic.keys()):
		Nbi = 0 
	else :
		Nai = dic.get(ai)
		Nbi = dic.get(bi)
	if(Nai ==0 and Nbi==0):
		return 0
	elif(Nai ==0) :
		return abs( 0-(count_Nibc/Nbi))
	elif(Nbi==0):
		return abs((count_Niac/Nai)-(0))
	else :
		return abs((count_Niac/Nai)-(count_Nibc/Nbi))


def sets (all_classes,training):
	classes = set(all_classes) #vou ter um set com todas as classes,sem repeticao
	classes = list(classes)
	#print("list all classes :",classes)
	array_classes = [[] for l in range(len(classes))] #cada posicao vai ter todas as entidades dessa classe
	for i in range(len(training)): #para todas as entidades
		for j in range (len(classes)): #separe elas por classe
			if(training[i].classification == classes[j]): 
				array_classes[j].append(training[i])
	#for k in range (len(classes)) :
	training = separation_training_test(array_classes,classes)
	return training
def separation_training_test(array_classes,classes) :

	for j in range(len(array_classes)):
		aux_entity = array_classes[j]
		size = len(array_classes[j])
		#print(" para a classe  ",classes[j], ": ")
		size_test = int(size*0.3)
		#print("tamanho do teste ", size_test)
		size_training = int(size*0.7)
		#print("tamanho do treinamento ",size_training)
		size_to_remove = ( size -size_training-size_test) #remover os denescessarios
		for i in range (size_test):
			aux = entity_test()
			aux.attributes = aux_entity[i].attributes
			aux.classification_real = aux_entity[i].classification
			aux.distance = 0
			aux.classification_from_Knn = [0 for l in range (len(values_k))]
			test.append(aux)
			aux_entity.remove(aux_entity[i])
		for j in range(size_to_remove):
			aux_entity.remove(aux_entity[j]) #removendo o que nao vou usar , o que sobrar eh do treinamento
	list_aux =[]
	for k in range(len(array_classes)):
		x = array_classes[k]
		for l in range(len(x)):
			list_aux.append(x[l])
	
	training = list_aux
	return list_aux


def imprimir_treinamento_byclass(training):
	class1 =0
	class2=0
	class3 =0
	class4=0
	print("Tamanho treinamento ", len(training))
	for i in range(len(training)):
		if(training[i].classification=='unacc'): 
			class1 = class1+1
		elif(training[i].classification=='acc') :
			class2 = class2+1
		elif(training[i].classification=='good') :
			class3= class3+1
		else :
			class4 = class4+1
	print("unacc ",class1," acc ",class2," good ",class3," v-good ",class4)	

if __name__== "__main__":
	file_path = input('Type the path of the file: ')
	func = int(input('Type (1) for k-NN  or (2) for k-NN with weight : '))
	start_time = time.time()
	training = []
	test = [] #test = [0 for l in range (32)]
	normalizacao =[] #vou salvar o maxim e o minimo
	all_classes = []
	values_k = [1,2,3,5,7,9,11,13,15]
	case1(file_path)#ler arquivo......vou salvar o que tem no arquivo em array de classes
	training = sets(all_classes,training)
	find_normalicacao(training,len(training[0].attributes)) #training , total of atts
	number_classes = len(set(all_classes))
	m=0
	for m in range (len(test)): 
		#print(" CALCULANDO DISTANCIA")
		#print("tamanho do treinamento ",len(training))
		#print("tamanho de teste ", len(test))
		training = euclidian(training,test[m],normalizacao) #chama metodo euclidian.......depois de ter a distancia adicionar a cada trainamento o valor da distancia para a query x
		training.sort(key = lambda x:x.distance,reverse = False) # da um sort no array de treinamento -> array.sort(key = lambda x:x.distance,reverse = False) 
		#imprime_array(training)
		k=0
		for k in range (len(values_k)): 
			#print( '----------------------------------')	
			#print('para k igual a ',values_k[k], 'a classificacao foi de ',calc_classification(values_k[k],training))
			if(func==1):
				#print("vou chamar a classificacao para k ",values_k[k])
				aux = calc_classification(values_k[k],training)
			else :
				aux = calc_classification_weighted(values_k[k],training)
			test[m].classification_from_Knn[k] = aux#salvar na classe a classificacao da query x
			#imprime_test_bytest(test,k,m)
			#print('AUX2:  ', 'a classe real eh : ',aux2.classification_real , 'e a classe calculada eh  ', aux2.classification_from_Knn[k], ' para k : ',values_k[k])

		
			#imprime_array_test(test)
		#imprime_array_test(test)
	print("Calcular acuracia")
	j=0
	l=0
	acertos = [0 for l in range (len(values_k))]
	l=0
	erros = [0 for l in range (len(values_k))]
	l=0
	for j in range (len(test)):#chamar o metodo classification para verificar qual a classe que mais aparece nos k primeiros
		#print ('para o teste ',j)
		for l in range(len(values_k)):
			#print('e para k igual a ', values_k[l], ' eu tenho que a classificacao eh ',test[j].classification_from_Knn[l] , 'e o que foi calculado deu ',test[j].classification_real)
			if(test[j].classification_from_Knn[l] == test[j].classification_real):
				acertos[l] = acertos[l]+1
			else:
				erros[l] = erros[l]+1 
			#print('test :', i, ' foi classificado como da classe : ',test[i].classification_from_Knn,' e ele eh da classe ',test[i].classification_real)
	k =0
	for k in range(len(acertos)): 
		print('-------------------------------------')
		print( 'para k igual a: ',values_k[k],' o numero de acertos foi de: ',acertos[k], ' numero de erros foi de: ', erros[k])
	print("Total time %s seconds " % (time.time() - start_time))
	input()
