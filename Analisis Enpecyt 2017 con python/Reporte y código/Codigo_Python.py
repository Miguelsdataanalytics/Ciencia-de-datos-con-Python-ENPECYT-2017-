"""
Created on Sat Oct 31 00:05:00 2020

@author: JOSE_
@e-mail: actmiguelalpha@gmail.com
"""
#%%
'''Organización de la información
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#debes cambiar la ruta en donde haz descargado los archivos en tu ordenador
ruta="C:/Users/JOSE_/Downloads/Carpetas/Cursos/Ciencia-de-datos-con-Python-master/enpecyt/conjunto de datos/"
cuestio1 = pd.read_csv(ruta + "tr_cbasico1.csv")
cuestio2 = pd.read_csv(ruta + "tr_cbasico2.csv")
socio1 = pd.read_csv(ruta + "tr_csocio1.csv")
socio2 = pd.read_csv(ruta + "tr_csocio2.csv")
socio3 = pd.read_csv(ruta + "tr_csocio3.csv")
ciudades = pd.read_csv(ruta + "ciudades.csv",names=['CD_A','Enti'] ,header=None, usecols=[0,1])
socio = pd.concat([socio1,socio2,socio3],axis = 0,keys = ["socio1","socio2","socio3"])

'''
#Construimos una vatiable indetificadora la cual contiene 
#CD_A:  Ciudad Representativa
#PER:   Periodo de levantamiento     
#ENT:   Entidad 
#CON:   Número de control
#V_SEL: Vivienda seleccionada
#N_HOG: Número de hogar
#N_REN: Número de renglon
'''
socio['ID'] = (socio['CD_A'].astype(str) + '_' +
               socio['PER'].astype(str) + '_' + 
               socio['ENT'].astype(str) + '_' +
               socio['CON'].astype(str)+'_'+
               socio['V_SEL'].astype(str)+'_'+
               socio['N_HOG'].astype(str)+'_'+
               socio['N_REN'].astype(str))

cuestio2 = cuestio2.drop(columns=list(cuestio2.columns[0:7]))
del(cuestio2['FAC'])
cuestio = cuestio1.join(cuestio2.set_index(["ID"]),on = ["ID"],how = "inner")
socio_aux=socio[['SEX', 'EDA','FAC18', 'ID']]
cuestio = cuestio.join(socio_aux.set_index(["ID"]),on = ["ID"],how = "inner")
cuestio = cuestio.join(ciudades.set_index(["CD_A"]),on = ["CD_A"],how = "inner")
cuestio['S3P1'].fillna(0, inplace=True)
#%%
'''Resultado 1.
1. Muestra cuántas personas mayores de 18 años viven en vivienda propia
en cada una de las 32 ciudades que conforman esa encuesta. Mediante
una gráfica de barras, representa cada uno de esos valores.
'''
estados=pd.DataFrame(cuestio.groupby('Enti')['FAC18'].sum())
estados_1=estados.reset_index()
estados_1.sort_values(by=['FAC18'],inplace=True,ascending=False)
estados_1['FAC18']=estados_1['FAC18']/1000
x = sorted(list(ciudades['Enti']))
y = list(estados['FAC18']/1000)
#uilizamos la lista de estados en la pregunta9 por eso la guardo
edo9=x
max(estados['FAC18'])

#Gráfica
plt.bar(range(32),y,edgecolor='black')
plt.xticks(range(32), x, rotation=90)
plt.title('Personas mayores de 18 años que viven en vivienda propia \n en cada una de las 32 ciudades',fontsize=10,loc='center')
plt.xlabel('Ciudades',fontsize=7)
plt.ylabel('Número de personas\n dividido entre 1000',fontsize=7)
plt.show()
#%%
'''Resultado 2.
2. Engloba los estudios de cada registro de la siguiente manera:
    1.Sin estudios para quienes no tienen ningún tipo de estudios; 
    2.Educación Básica para quienes tienen estudios desde kinder a secundaria; 
    3.media superior para quienes tienen estudios de bachillerato;
    4.posgrado para quienes tienen especialidad, maestría o doctorado,
    5 superior para todos los demás.
    Presenta un gráfico de pastel donde se represente el porcentaje total de cada clasicación
    respecto del nivel nacional (ojo: toma en cuenta que te debes basar
    en los factores de expansión: FAC18).
'''

part=cuestio[['FAC18','Enti','S3P1']]
part_s=pd.DataFrame(part.groupby(['S3P1'])['FAC18'].sum())
part_s.reset_index(inplace=True)
conditions = [
       (part_s['S3P1']==0),
       (part_s['S3P1'] <= 3) & (part_s['S3P1'] > 0),
       (part_s['S3P1'] == 4),
       (part_s['S3P1'] > 4) & (part_s['S3P1'] < 8 ),
       (part_s['S3P1'] >= 8) & (part_s['S3P1'] <= 10 )]       
choices = ['Sin estudios','Básica', 'Media superior', 'Superior','posgrado']
part_s['estudios'] = np.select(conditions, choices, default='NO DEFINIDO')
part_s=pd.DataFrame(part_s.groupby('estudios')['FAC18'].sum())
part_s.reset_index(inplace=True)
total=sum(part_s['FAC18'])
part_s['porcen']=(part_s['FAC18']/total)*100

##graficar
a=list(part_s['porcen'])
b=tuple(part_s['estudios'])
desfase = (0.1, 0 , 0, 0,0)

fig, ax = plt.subplots()
ax.set_title("Clasicación de nivel educativo\n a nivel nacional",fontsize=10,fontweight='bold')
ax.pie(a,labeldistance=1, pctdistance=0.7,autopct='%1.1f%%', shadow=False, startangle=90,explode=desfase,textprops=dict(color="w"))
ax.axis('equal')  
ax.legend( labels=b, loc='center left', bbox_to_anchor=(0.8, 0, 0.5, 1))
#%%
'''Resultado 3.
3.Para cada una de las 32 ciudades, realiza el mismo gráco de pastel
respecto de la población de la ciudad. Sin embargo, presenta las 32
gráficas en un solo cuadro de 4 x 8 (es decir, 8 las de gráficas con
cuatro gráficas cada una).
'''
part_ci=pd.DataFrame(part.groupby(['S3P1','Enti'])['FAC18'].sum())
part_ci.reset_index(inplace=True)
conditions = [
       (part_ci['S3P1']==0),
       (part_ci['S3P1'] <= 3) & (part_ci['S3P1'] > 0),
       (part_ci['S3P1'] == 4),
       (part_ci['S3P1'] > 4) & (part_ci['S3P1'] < 8 ),
       (part_ci['S3P1'] >= 8) & (part_ci['S3P1'] <= 10 )]       
choices = ['Sin estudios','Básica', 'Media superior', 'Superior','posgrado']
part_ci['estudios'] = np.select(conditions, choices, default='NO DEFINIDO')
part_ci=pd.DataFrame(part_ci.groupby(['Enti','estudios'])['FAC18'].sum())
part_ci_1=part_ci
part_ci_1.reset_index(inplace=True)
part_ci.reset_index(inplace=True)
lis_ciu=list(ciudades['Enti'])
fig, ax = plt.subplots(8,4,figsize = (25,25))  
ax = ax.flatten()
i=0
for ciu in lis_ciu:    
    ciudad=part_ci[part_ci["Enti"] == ciu][["Enti","FAC18","estudios"]]
    ciudad.reset_index(inplace=True)
    total=sum(ciudad['FAC18'])
    ciudad['porcen']=(ciudad['FAC18']/total)*100
    ciudad=ciudad[['estudios','porcen']]
    a=list(ciudad['porcen'])
    b=tuple(ciudad['estudios'])
    ax[i].pie(a,pctdistance=0.73,autopct='%1.2f%%', shadow=False, startangle=90, textprops=dict(color="w"))
    ax[i].set_title(ciu,fontsize=15)
    ax[i].legend(labels=b,title='Nivel academico', loc='center left', bbox_to_anchor=(0.8, 0, 0.5, 1),fontsize='large')
    ax[i].axis('equal') 
    i+=1


#%%
'''Resukltado 4.
Presenta lo mismo que en los dos puntos anteriores pero clasificando ahora
por dos niveles de estudio: sin estudios de nivel superior y con estudios de nivel superior.'''

part_s_2=pd.DataFrame(part.groupby(['S3P1'])['FAC18'].sum())
part_s_2.reset_index(inplace=True)
conditions = [
    (part_s_2['S3P1'] >= 0) & (part_s_2['S3P1'] <= 4),
    (part_s_2['S3P1'] > 4) & (part_s_2['S3P1'] <= 10 )]       
choices = ['Sin estudios\n de nivel superior','Con estudios\n de nivel superior']
part_s_2['estudios'] = np.select(conditions, choices, default='nada')
part_s_2=pd.DataFrame(part_s_2.groupby('estudios')['FAC18'].sum())
part_s_2.reset_index(inplace=True)
total=sum(part_s_2['FAC18'])
part_s_2['porcen']=(part_s_2['FAC18']/total)*100

##graficar
a=list(part_s_2['porcen'])
b=tuple(part_s_2['estudios'])
fig, ax = plt.subplots()
ax.pie(a,labeldistance=1, pctdistance=0.7,autopct='%1.1f%%', shadow=True, startangle=90,explode=(0,.1),textprops=dict(color="w"))
ax.set_title("Nivel de estudios",fontsize=15)
ax.legend( labels=b, loc='center left', bbox_to_anchor=(0.8, 0, 0.5, 1))
ax.axis('equal')
part_ci_2=pd.DataFrame(part.groupby(['S3P1','Enti'])['FAC18'].sum())
part_ci_2.reset_index(inplace=True)
conditions = [
    (part_ci_2['S3P1'] >= 0) & (part_ci_2['S3P1'] <= 4),
    (part_ci_2['S3P1'] > 4) & (part_ci_2['S3P1'] <= 10 )]       
choices = ['Sin estudios\n de nivel superior','Con estudios\n de nivel superior']
part_ci_2['estudios'] = np.select(conditions, choices, default='nada')
part_ci_2=pd.DataFrame(part_ci_2.groupby(['Enti','estudios'])['FAC18'].sum())
part_ci_2.reset_index(inplace=True)
part_ci_21=part_ci_2
part_ci_21.reset_index(inplace=True)
lis_ciu=list(ciudades['Enti'])

#graficar
fig, ax = plt.subplots(8,4,figsize = (30,25))  
ax = ax.flatten()
i=0
for ciu in lis_ciu:    
    ciudad=part_ci_2[part_ci_2["Enti"] == ciu][["Enti","FAC18","estudios"]]
    ciudad.reset_index(inplace=True)
    total=sum(ciudad['FAC18'])
    ciudad['porcen']=(ciudad['FAC18']/total)*100
    ciudad=ciudad[['estudios','porcen']]
    a=list(ciudad['porcen'])
    b=tuple(ciudad['estudios'])
    ax[i].pie(a,pctdistance=0.65,autopct='%1.2f%%', shadow=False, startangle=90, textprops=dict(color="w"))
    ax[i].set_title(ciu, fontweight='bold',fontsize=30)
    ax[i].legend(labels=b,title='Nivel academico', loc='center left', bbox_to_anchor=(0.8, 0, 0.5, 1),fontsize='large')
    ax[i].axis('equal')
    i+=1
#%%
'''Resultado 5.
5.Del punto anterior, realiza un gráfico de puntos representando las 32
ciudades, donde las coordenadas en horizontal será el total de gente
con estudios superiores y en el eje vertical el total de gente sin estudios
superiores.'''

part_ci_2_5_1=part_ci_2[part_ci_2['estudios']=='Con estudios\n de nivel superior'][['FAC18','Enti']]
part_ci_2_5_1.columns=['CEDNS','Enti']
part_ci_2_5_2=part_ci_2[part_ci_2['estudios']=='Sin estudios\n de nivel superior'][['FAC18','Enti']]
part_ci_2_5_2.columns=['SEDNS','Enti']
part_ci_2_5=part_ci_2_5_1.join(part_ci_2_5_2.set_index(["Enti"]),on = ["Enti"],how = "inner")
#Graficar
x =part_ci_2_5["CEDNS"]/1000
y =part_ci_2_5["SEDNS"]/1000
fig, axes = plt.subplots(figsize = (10,6))
corr = round(np.corrcoef(x,y)[0][1],2)
axes.scatter(x,y,s=150, marker = "*",color = "black",alpha=0.5,label=f"Correlación = {corr}")
axes.spines["top"].set_visible(False)
axes.set_title("Población con educacion de nivel superior\n vs sin educacion de nivel superior",fontsize = 15,loc='center')
axes.set_xlabel("con educacion de nivel superior\ncifras en miles",fontsize=10)
axes.set_ylabel("sin educacion de nivel superior\ncifras en miles",fontsize=10)
axes.legend(fancybox=True,prop={"size":14},loc="best")
'''

for label, x, y in zip(labels, x, y):
       plt.annotate(
           label,
           xy=(x, y), xytext=(-10, 10),
           textcoords='offset points', ha='right', va='bottom',
           bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.2),
           arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))

plt.show()
'''
#con etiquetas sin Mexico
max(part_ci_2_5['CEDNS'])
max(part_ci_2_5['SEDNS'])
part_ci_2_5_sm=part_ci_2_5[part_ci_2_5['Enti'] != 'Mexico'][['CEDNS','SEDNS','Enti']]
part_ci_2_5_sm.reset_index()

#Graficar
x = part_ci_2_5_sm["CEDNS"]/1000
y = part_ci_2_5_sm["SEDNS"]/1000
fig, axes = plt.subplots(figsize = (10,6))
corr = round(np.corrcoef(x,y)[0][1],2)
axes.scatter(x,y,s=150, marker = "*",color = "green",alpha=0.5,label=f"Correlación = {corr}")
axes.spines["top"].set_visible(False)
axes.set_title("Población con educacion de nivel superior\n vs sin educacion de nivel superior",fontsize = 15,loc='center')
axes.set_xlabel("con educacion de nivel superior\ncifras en miles",fontsize=10)
axes.set_ylabel("sin educacion de nivel superior\ncifras en miles",fontsize=10)
axes.legend(fancybox=True,prop={"size":14},loc="best")
labels=part_ci_2_5_sm["Enti"]
'''
#Labels identificador
for label, x, y in zip(labels, x, y):
       plt.annotate(
           label,
           xy=(x, y), xytext=(-10, 10),
           textcoords='offset points', ha='right', va='bottom',
           bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.2),
           arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'))

plt.show()
'''
#%%
'''Resultado 6.
6.Construye una nueva columna en cuestio que explique explícitamente
el signicado de cada clave de carrera.     
'''
conditions = [
    (cuestio['S3P1'] == 5),
    (cuestio['S3P1'] == 6),
    (cuestio['S3P1'] == 7),
    (cuestio['S3P1'] == 8),
    (cuestio['S3P1'] == 9),
    (cuestio['S3P1'] == 10 )]       
choices = ['Normal','Carrera Tec\\Comer','Lic \\ ing','Especilidad','Maestría','Doctorado']
cuestio['estudios_en'] = np.select(conditions, choices, default='*estudios <= bachillerato')
cuestio['S3P2']=cuestio['S3P2'].replace('N122',122)
cuestio['S3P2']=cuestio['S3P2'].replace('N121',121)
cuestio['S3P2']=cuestio['S3P2'].replace('N120',120)
cuestio['S3P2']=cuestio['S3P2'].astype(float)
cuestio['S3P2_ES']=cuestio['S3P2_ES'].astype(str)
cuestio = cuestio.sort_values('S3P2')

def frase_inv(frase):
    frase_l=frase.lower()
    frase_aux=(frase_l.split())
    frase_aux=(frase_aux[::-1])
    frase_aux[0]=frase_aux[0].capitalize()
    frase_aux=' '.join(frase_aux[:])
    return frase_aux

cuestio['result'] = (cuestio['S3P2_ES'].map(lambda x: frase_inv(x).replace(' ','.'))) + '.'
cuestio['result']=cuestio['result'].map(lambda x: x[ 0 : x.find('.') ]).str.upper()
cuestio.sort_values('S3P2',inplace=True)
cuestio['S3P2_ES'] = cuestio['S3P2_ES'].map(lambda x: x.replace(' ','.'))
cuestio['grado']=cuestio['S3P2_ES'].map(lambda x: x[ 0 : x.find('.') ])
cuestio.sort_values('S3P2',inplace=True)
cuestio['carrera'] = (cuestio['estudios_en'] + ' :   '+cuestio['grado'] +" "+ cuestio['result'].map(lambda x: frase_inv(x))).str.upper()
nuevaa_var=cuestio[['S3P2','carrera']]
#%%
'''Resultado 7.
Crea una nueva columna donde clasifiques cada una de las claves de
carrera por área: salud, ciencias, ingenierías, humanidades, administración,
artes, enseñanza y deportes (y otras que te puedas encontrar).

Clasificasiones

1 ADMINISTRACION
2 DANZA Y DEPORTES
3 CIENCIAS EXACTAS Y FM
4 COMERCIO
5 CONTABILIDAD
6 DISEÑO
7 EDUCACION
8 CIENCIAS SOCIALES Y HUMANIDADES
9 IDIOMAS
10 INGENIERIAS
11 SALUD 
12 SECRETARIADO
13 TECNOLOGIA
14 TURISMO
 
'''
#ADMINISTRACION
grupo1='ADMON|ADIMINISTRACION|ADIMISTRACION|ADMINISTARACION|ADMINISTARCION|ADMINISTRACCION|ADMINISTRACIÃ“N|ADMINISTRACIO|ADMINISTRACION|ADMINISTRACON|ADMINISTRADOR|ADMINISTRAION|ADMINISTRATIVO|ADMINISTRCION|ADMINSTRACION|ADMISTRACION|MERCADOTECNIA|GERONTOLOGIA'
cuestio['G01']=cuestio.S3P2_ES.str.contains(grupo1,case=False).astype(str).replace('True','ADMINIS').replace('False','_')
#DANZA Y DEPORTES
grupo2='ARTES|BELLEZA|DANZA|EDUCACIOON.FISICA|LENGUISTICA|LETRAS|CANTO|DEPORTE|DANSA'
cuestio['G02']=cuestio.S3P2_ES.str.contains(grupo2,case=False).astype(str).replace('True','DANZYDEP').replace('False','_')
#CIENCIAS EXACTAS Y FM
grupo3='QUIMICA|ARQUITECTO|ACTUARIO|CIENCIA|CIENC|CIEN|ACTUARIA|AGRONOMIA|ARQUITECTURA|ARQUITECTYRA|BIOENERGETICA|INVESTIGACION|MATEMATICAS|ENERGIA|ESTADISTICAS|GEOGRAFIA|QUIMICAS|MECANICA|MECATRONICA|QUIMICO|QUIMICO|AERONAUTICA'
cuestio['G03']=cuestio.S3P2_ES.str.contains(grupo3,case=False).astype(str).replace('True','CIENEXACTASYFM').replace('False','_')
#COMERCIO
grupo4='COMERCIAL|COMERCIALES|COMERCIO|COPMERCIO'
cuestio['G04']=cuestio.S3P2_ES.str.contains(grupo4,case=False).astype(str).replace('True','COMERC').replace('False','_')
#CONTABILIDAD
grupo5='AUDITORIA|CONTABLE|CONTADOR|CONTABILIDAD|CONTADURIA|FINANZAS|EVALUACION.DE.PROYECTOS|NCONTABILIDAD'
cuestio['G05']=cuestio.S3P2_ES.str.contains(grupo5,case=False).astype(str).replace('True','CONTAB').replace('False','_')
#DISEÑO
grupo6='DISEÃ‘O|DISEÑO|DISEÑ'
cuestio['G06']=cuestio.S3P2_ES.str.contains(grupo6,case=False).astype(str).replace('True','DISEÑO').replace('False','_')
#EDUCACION
grupo7='PEDADOGIA|MAESTRA|PROFESOR|PRIMARIA|EDUCATIVO|EDUCACION|EDUCACION|EDUCATIVA|DOCENTE|PREESCOLAR|SECUNDARIA|EDUACION|EDUCAION|ESPAÃ‘OL|PEDAGOGÃA|SECUNDARIA|PSICOPEDAGOGIA|NORMAL|PUERICULTURA'
cuestio['G07']=cuestio.S3P2_ES.str.contains(grupo7,case=False).astype(str).replace('True','EDUCAC').replace('False','_')
#CIENCIAS SOCIALES Y HUMANIDADES
grupo8='OLISTICA|MAESTRIA.EN.NEGOCIOS|NEGOCIOS.INTERNACIONALES|NBEGOCIOS.INTERNACIONALES|GESTION.EM|OLISMO|ABOGADA|ABOGADO|RELACIONES|SEGURIDAD|COMUNICACION|JURIDICO|CRIMINOLOGIA|DERECHO|DESARROLLO.DE.NEGOCIOS|DESARROLLO.E.INNOVACION.EMPRESARIAL|SOCIALES.Y.HUMANIDADES|ESTUDIOS.REGIONALES|PRIMEROS.AUXILIO|ECONOMIA|GASTRONOMICOS|URBANA|FILOSOFIA|GASTRONOMIA|PEDAGOGIA|MERCADOTECNIA|TRABAJO.SOCIAL|HISTORIA|BIBLIOTECOLOGIA|JURIDICO.PENAL|COMUNICACIONES|INTERVENCION.EN.PAREJA|VENTAS|PUBLICIDAD|MANTENIMIENTO.INDUSTRIAL|ALIMENTOS.Y.BEBIDAS|PSICOTERAPIA|RECURSOS.HUMANOS|RELACIONES|SACERDOTE|SUPERVISOR|TRABAJADORA.SOCIAL|NAVAL|SEGURIDAD|ALIMENTOS|HOTELERIA'
cuestio['G08']=cuestio.S3P2_ES.str.contains(grupo8,case=False).astype(str).replace('True','CIENSOYHUMA').replace('False','_')
#IDIOMAS
grupo9='IDIOMAS|LENGUA|LENGUAS|INGLES|EXTRANJERAS'
cuestio['G09']=cuestio.S3P2_ES.str.contains(grupo9,case=False).astype(str).replace('True','IDIOMAS').replace('False','_')
#INGENIERIAS
grupo10='ELECTRONICA.Y.COMUNICASIONES|ELETROMECANICA|INFORMATICA|INFORMATICA.ADMINISTRATIVA|ING..EN.GESTION.EMPRESARIAL|ING..INDISTRIAL|PILOTO.AVIADOR|SISTEMAS.DE.INFORMACION|SISTEMAS.DIGITALES.Y.ROBOTICA|TECNICO.EN.AVIACION|IJNGENERIA.|IMNGENIERO.|INEGENIERIA.|ING.|INGENERIA.|INGENIERI.|INGENIERIA.|INGENIERIRIA.|INGENIERO.|INGENIOERIA|INGERIA|INGIENERIA'
cuestio['G10']=cuestio.S3P2_ES.str.contains(grupo10,case=False).astype(str).replace('True','INGENI').replace('False','_')
#SALUD
grupo11='NUTRICCION|CIRUJANO|ENFERMERIA|BIOLOGIA|BIOLOGIA.MARINA|BIOMEDICINA|BIOTECNOLOGIA|ODONTOLOGIA|DENTISTA|EMFERMERA|NUTRICION|REHABLITACION|OBSTETRICIA|PSICOLOGIA|DENTALES|ESTOMATOLOGIA|FISIOTERAPIA|HISTOPATOLOGIA|PFISIOTERAPIA|FICIOTERAPIA|REAVILITACION|TERAPIA.GESTAL|SALUD.PUBLICA|FISIO.TERAPIA|MEDICINA|MEDICO|ODONTOLOGÃ|TERAPIA.FISICA|CICOTERAPIA.INFANTIL|OPTOMETRIA|CLINICA|RADIOLOGIA|DOCTOR|DOCTORA|DOCT|EMFERMERIA|GINECOLOGIA|GINECOLOGÃA|ENFERMERA|ENFEMERIA|ENEFERMERIA|MEDICAS|MOLECULAR|REHABILITACION|SICOLOGIA|SICOTERAPIA|ODONTOLOGÃA|PARTERO|PEDAGOGICA|PEDIATRICA|PREHOSPITALARIAS'
cuestio['G11']=cuestio.S3P2_ES.str.contains(grupo11,case=False).astype(str).replace('True','SALUD').replace('False','_')
#SECRETARIADO
grupo12='SECRETARIA|SECRETARIADO|SECRETARA|SECRETAIRA|SECRETARIA,'
cuestio['G12']=cuestio.S3P2_ES.str.contains(grupo12,case=False).astype(str).replace('True','SECRET').replace('False','_')
#TECNOLOGIA
grupo13='COMPUTACIÃ“N.Y.CONTABILIDAD|ELECTRONICA|PROGRAMADOR|INFORMATICA.ADMINISTRATIVA|PROGRAMAD|COMPUTACI|ENINFRMATICA|SISTEMAS.COMPUTACIONALES|SISTEMAS.|NFORMATICA.ADMINISTRATIVA|COMPUTADORAS|RÃA.EN.COMPUTACIÃ“N|SISTEMA.COMPUTACIONALES|SISTEMAS.COMPUTACIONALES.ADMINISTRATIVOS|TAQUIMACANOGRAFIA|TAQUIMECANOGRAFA|INFORMATICA|INFORMAT'
cuestio['G13']=cuestio.S3P2_ES.str.contains(grupo13,case=False).astype(str).replace('True','TECNOL').replace('False','_')
#TURISMO
grupo14='TURISTICO|TURISMO|TURISTICA|GESTION.Y.DESARROLLO.TURISTICO|TURISMO|TURISMO.ALTERNATIVO|TURISMO.Y.HOTELERIA'
cuestio['G14']=cuestio.S3P2_ES.str.contains(grupo14,case=False).astype(str).replace('True','TURISMO').replace('False','_')
cuestio['ID_CLAS']=cuestio['G01'] + cuestio['G02'] + cuestio['G03'] + cuestio['G04'] + cuestio['G05'] + cuestio['G06'] + cuestio['G07'] + cuestio['G08'] + cuestio['G09'] + cuestio['G10'] + cuestio['G11'] + cuestio['G12'] + cuestio['G13'] + cuestio['G14']
#%%
'''Resultado 8.
Crea un gráfico de barras donde en el eje X aparezcan las clasicaciones
del punto anterior pero separadas por sexo (los dos sexos en la misma
tabla y que se diferencíen por color). 

G01 ADMINISTRACION
G02 DANZA Y DEPORTES
G03 CIENCIAS EXACTAS Y FM
G04 COMERCIO
G05 CONTABILIDAD
G06 DISEÑO
G07 EDUCACION
G08 CIENCIAS SOCIALES Y HUMANIDADES
G09 IDIOMAS
G10 INGENIERIAS
G11 SALUD 
G12 SECRETARIADO
G13 TECNOLOGIA
G14 TURISMO

'''
part_8=cuestio[cuestio['S3P1'] >= 5][['FAC18',
                                      'Enti',
                                      'S3P1',
                                      'S3P2',
                                      'S3P2_ES',
                                      'estudios_en',
                                      'grado',
                                      'SEX',
                                      'G01',
                                      'G02',
                                      'G03',
                                      'G04',
                                      'G05',
                                      'G06',
                                      'G07',
                                      'G08',
                                      'G09',
                                      'G10',
                                      'G11',
                                      'G12',
                                      'G13',
                                      'G14',
                                      'ID_CLAS']]

sexos = pd.DataFrame(part_8.groupby(['G01','SEX'])['FAC18'].sum())
sexos.reset_index(inplace=True)
sexos=sexos[sexos["G01"] == 'ADMINIS'][['G01','SEX','FAC18']]
sexos.index = sexos['SEX']
sexos['FAC18'] = sexos['FAC18']/1000
sexos=sexos.T
sexos.reset_index(inplace=True)
sexos=sexos[sexos["index"] == 'FAC18']
sexos["index"]='ADMINISTRACION'

def tabla_area(IDG,Area,Nomtab,Area_R):
    global sexos
    Nomtab =pd.DataFrame(part_8.groupby([IDG,'SEX'])['FAC18'].sum())
    Nomtab.reset_index(inplace = True)
    Nomtab=Nomtab[Nomtab[IDG] == Area][[IDG,'SEX','FAC18']]
    Nomtab.columns =['G01','SEX','FAC18']
    Nomtab.index = Nomtab['SEX']
    Nomtab['FAC18']=Nomtab['FAC18']/1000
    Nomtab=Nomtab.T
    Nomtab.reset_index(inplace=True)
    Nomtab=Nomtab[Nomtab["index"] == 'FAC18']
    Nomtab["index"]=Area_R    
    sexos= pd.concat([sexos,Nomtab],axis=0)
    return Nomtab, sexos

tabla_area('G02','DANZYDEP','SEXO2','DANZA Y DEPORTE')
tabla_area('G03','CIENEXACTASYFM','SEXO3','CIENCIAS EXACTAS Y FISICO MATEMATICAS')
tabla_area('G04','COMERC','SEXO04','COMERCIO')
tabla_area('G05','CONTAB','SEXO05','CONTABILIDAD')
tabla_area('G06','DISEÑO','SEXO06','DISEÑO')
tabla_area('G07','EDUCAC','SEXO07','EDUCACIÓN')
tabla_area('G08','CIENSOYHUMA','SEXO08','CIENCCIAS SOCIALES Y HUAMIDADES')
tabla_area('G09','IDIOMAS','SEXO09','IDIOMAS')
tabla_area('G10','INGENI','SEXO10','INGENIERIAS')
tabla_area('G11','SALUD','SEXO11','SALUD')
tabla_area('G12','SECRET','SEXO12','SECRETARIADO')
tabla_area('G13','TECNOL','SEXO13','TECNOLOGIA')
tabla_area('G14','TURISMO','SEXO14','TURISMO')
sexos.columns =['Área','Hombre','Mujer']
sexos.index = sexos['Área']
sexos.plot(kind = 'bar',title='Gráfico de las áreas de estudio\nseparada por sexo a nivel nacional\n',ylabel='Número de personas en miles')

sexos_aux=sexos
sexos_aux.fillna(0,inplace=True)
sexos_aux['Total_sex']=sexos_aux['Hombre'] + sexos_aux['Mujer']
sexos_aux['Hombre_']=(round((sexos_aux['Hombre']/sexos_aux['Total_sex'])*100,2))
sexos_aux['Hombre']=sexos_aux['Hombre_'].astype(str) + "%"
sexos_aux['Mujer_']=(round((sexos_aux['Mujer']/sexos_aux['Total_sex'])*100,2))
sexos_aux['Mujer']=sexos_aux['Mujer_'].astype(str) + "%"
sexos_aux['Diferencia_']=abs(round(sexos_aux['Hombre_']-sexos_aux['Mujer_'],2))
sexos_aux['Diferencia']=sexos_aux['Diferencia_'].astype(str) + "%"
sexos_aux=sexos_aux[['Área','Hombre','Mujer','Diferencia']]
#%%
'''Resultado 9.
 Realiza el mismo gráfico que en el punto anterior pero para cada unade las 32 ciudades.
'''
def grafica_sexo(ciudad):
    part_8=cuestio[(cuestio['S3P1'] >= 5) & (cuestio['Enti'] >= ciudad)][['FAC18',
                                      'Enti',
                                      'S3P1',
                                      'S3P2',
                                      'S3P2_ES',
                                      'estudios_en',
                                      'grado',
                                      'SEX',
                                      'G01',
                                      'G02',
                                      'G03',
                                      'G04',
                                      'G05',
                                      'G06',
                                      'G07',
                                      'G08',
                                      'G09',
                                      'G10',
                                      'G11',
                                      'G12',
                                      'G13',
                                      'G14',
                                      'ID_CLAS']]               
    global sexos
    sexos = pd.DataFrame(part_8.groupby(['G01','SEX'])['FAC18'].sum())
    sexos.reset_index(inplace=True)
    sexos=sexos[sexos["G01"] == 'ADMINIS'][['G01','SEX','FAC18']]
    sexos.index = sexos['SEX']
    sexos['FAC18'] = sexos['FAC18']/1000
    sexos=sexos.T
    sexos.reset_index(inplace=True)
    sexos=sexos[sexos["index"] == 'FAC18']
    sexos["index"]='ADMINISTRACION'
    
    def tabla_area(IDG,Area,Nomtab,Area_R):
        global sexos
        Nomtab =pd.DataFrame(part_8.groupby([IDG,'SEX'])['FAC18'].sum())
        Nomtab.reset_index(inplace = True)
        Nomtab=Nomtab[Nomtab[IDG] == Area][[IDG,'SEX','FAC18']]
        Nomtab.columns =['G01','SEX','FAC18']
        Nomtab.index = Nomtab['SEX']
        Nomtab['FAC18']=Nomtab['FAC18']/1000
        Nomtab=Nomtab.T
        Nomtab.reset_index(inplace=True)
        Nomtab=Nomtab[Nomtab["index"] == 'FAC18']
        Nomtab["index"]=Area_R
        sexos= pd.concat([sexos,Nomtab],axis=0)
        return Nomtab, sexos
            
    tabla_area('G02','DANZYDEP','SEXO2','DANZA Y DEPORTE')
    tabla_area('G03','CIENEXACTASYFM','SEXO3','CIENCIAS EXACTAS Y FISICO MATEMATICAS')
    tabla_area('G04','COMERC','SEXO04','COMERCIO')
    tabla_area('G05','CONTAB','SEXO05','CONTABILIDAD')
    tabla_area('G06','DISEÑO','SEXO06','DISEÑO')
    tabla_area('G07','EDUCAC','SEXO07','EDUCACIÓN')
    tabla_area('G08','CIENSOYHUMA','SEXO08','CIENCCIAS SOCIALES Y HUAMIDADES')
    tabla_area('G09','IDIOMAS','SEXO09','IDIOMAS')
    tabla_area('G10','INGENI','SEXO10','INGENIERIAS')
    tabla_area('G11','SALUD','SEXO11','SALUD')
    tabla_area('G12','SECRET','SEXO12','SECRETARIADO')
    tabla_area('G13','TECNOL','SEXO13','TECNOLOGIA')
    tabla_area('G14','TURISMO','SEXO14','TURISMO')
    sexos.columns =['Area','Hombre','Mujer']
    sexos.index = sexos['Area']
    sexos.plot(kind = 'bar')    
    plt.ylabel('Número de personas en miles')
    plt.title('Gráfico de las áreas de estudio separada por sexo de {} \n'.format(ciudad),fontsize=10,fontweight='bold',loc='center')

lista_edos=list(edo9)
for i,ide in enumerate(lista_edos):
    grafica_sexo(ide)
#%%
'''Resultado 10.
10. Para cada pregunta de la familia S4P18 (son las preguntas sobre conocimientos 
científicos), realiza un gráfico de pastel donde representes
el porcentaje de quiénes tuvieron mas de la mitad de las respuestas
correctas vs quienes no.
'''
part_10=cuestio[['FAC18',
                'Enti',
                'S3P1',
                'S4P18_1',
                'S4P18_2',
                'S4P18_3',
                'S4P18_4',
                'S4P18_5',
                'S4P18_6',
                'S4P18_7',
                'S4P18_8',
                'S4P18_9',
                'S4P18_10',
                'S4P18_11',
                'S4P18_12',
                'S4P18_13',
                'S4P18_14',
                'S4P18_15',
                'S4P18_16',
                'S4P18_17',
                'S4P18_18',
                'S4P18_19',
                'S4P18_20']]

'''
1.El centro de la tierra es muy
caliente
R=1 CIERTO
'''
#La correcta es la 1
part_10['S4P18_1']=part_10['S4P18_1'].apply(lambda x: 1 if x == 1 else 0)
'''
2.Toda la radioactividad está
hecha por el hombre
R=2 FALSO
'''
#La correcta es el 2
part_10['S4P18_2']=part_10['S4P18_2'].apply(lambda x: 1 if x == 2 else 0)
'''
3.Todo el oxígeno que respiramos
proviene de las plantas
R= 2 FALSO
'''
#La correcta es el 2
part_10['S4P18_3']=part_10['S4P18_3'].apply(lambda x: 1 if x == 2 else 0)
'''
4.El gen del padre es el que decide
si el bebé es niño o niña
R=1 cierto
'''
#La correcta es el 1
part_10['S4P18_4']=part_10['S4P18_4'].apply(lambda x: 1 if x == 1 else 0)
'''
5.El rayo láser trabaja por el
enfoque de ondas sonoras
R=2 falso
'''
#La correcta es el 2
part_10['S4P18_5']=part_10['S4P18_5'].apply(lambda x: 1 if x == 2 else 0)
'''
6.Los electrones son más pequeños
que los átomos
R=1 cierto
'''
#La correcta es el 1
part_10['S4P18_6']=part_10['S4P18_6'].apply(lambda x: 1 if x == 1 else 0)
'''
7.Los antibióticos sirven para
tratar enfermedades causadas
tanto por virus como por
bacterias
R=2 falso
'''
#La correcta es el 2
part_10['S4P18_7']=part_10['S4P18_7'].apply(lambda x: 1 if x == 2 else 0)
'''
8.El universo inició con una gran
explosión
R=1 cierto
'''
#La correcta es el 1
part_10['S4P18_8']=part_10['S4P18_8'].apply(lambda x: 1 if x == 1 else 0)
'''
9.Alemania ganó la 2a Guerra
Mundial
R=2 falso 
'''
#La correcta es el 2
part_10['S4P18_9']=part_10['S4P18_9'].apply(lambda x: 1 if x == 2 else 0)

'''
10.Los seres humanos de hoy
se desarrollaron a partir de la
evolución de otras especies
animales
R=1 cierto
'''
#La correcta es el 1
part_10['S4P18_10']=part_10['S4P18_10'].apply(lambda x: 1 if x == 1 else 0)
'''
11.Fumar puede causar cáncer
pulmonar 
R=1 cierto
'''
#La correcta es el 1
part_10['S4P18_11']=part_10['S4P18_11'].apply(lambda x: 1 if x == 1 else 0)

'''
12.Los primeros humanos vivieron
en la misma época que los
dinosaurios 
R=2 falso
'''
#La correcta es el 2
part_10['S4P18_12']=part_10['S4P18_12'].apply(lambda x: 1 if x == 2 else 0)
'''
13.Existe el premio Nobel de
matemáticas
R=2 falso
'''
#La correcta es el 2
part_10['S4P18_13']=part_10['S4P18_13'].apply(lambda x: 1 if x == 2 else 0)
'''
14.Mario Molina, premio Nobel de
Química, es mexicano
R=1 cierto 
'''
#La correcta es el 1
part_10['S4P18_14']=part_10['S4P18_14'].apply(lambda x: 1 if x == 1 else 0)
'''
15.México limita al sur con el
Salvador
R=2 falso
'''
#La correcta es el 2
part_10['S4P18_15']=part_10['S4P18_15'].apply(lambda x: 1 if x == 2 else 0)
'''
16.En México hay plantas nucleares
R=1 cierto
'''
#La correcta es el 1
part_10['S4P18_16']=part_10['S4P18_16'].apply(lambda x: 1 if x == 1 else 0)
'''
17.La tierra da la vuelta al sol en
un mes
R=2 falso
'''
#La correcta es el 2
part_10['S4P18_17']=part_10['S4P18_17'].apply(lambda x: 1 if x == 2 else 0)
'''
18.El sonido viaja más rápido que
la luz
R=2 falso
'''
#La correcta es el 2
part_10['S4P18_18']=part_10['S4P18_18'].apply(lambda x: 1 if x == 2 else 0)
'''
19.Al menos cinco mexicanos han
ganado el premio Nobel
R=2 falso
'''
#La correcta es el 1
part_10['S4P18_19']=part_10['S4P18_19'].apply(lambda x: 1 if x == 2 else 0)
'''
20.el hombre ya ha llegado a la
luna
R=1 cierto
'''
#La correcta es el 1
part_10['S4P18_20']=part_10['S4P18_20'].apply(lambda x: 1 if x == 1 else 0)

part_10_copy=part_10
part_10['SUMRESP']=part_10.iloc[:,3:].sum(axis=1)
part_10_1=part_10
part_10_1['SUMRESP_ID']= part_10_1.apply(lambda x: True if x['SUMRESP'] > 10 else False , axis=1)
total=sum(part_10_1['FAC18'])
part_10_2=pd.DataFrame(part_10_1.groupby('SUMRESP_ID')['FAC18'].sum())
part_10_2.reset_index(inplace=True)
part_10_2['porcen']=(part_10_2['FAC18']/total)*100

##graficar
a=list(part_10_2['porcen'])
b=['Menos del 50% correctas','Más del 50% correctas']
fig, ax = plt.subplots()
ax.pie(a,labeldistance=1, pctdistance=0.7,autopct='%1.1f%%', shadow=False, startangle=90,explode=(0,0.1),textprops=dict(color="w"))
ax.set_title('Población que obtuvo más del 50% de respuestas correctas\n sobre cultura cientifica vs quienes no', fontweight='bold')
ax.legend( labels=b, loc='center', bbox_to_anchor=(0.5, -0.1, 0, 0))
ax.axis('equal')
#%%  
'''Resultado 11.
Lo mismo que en el anterior, pero primero clasificando por cada uno de
los niveles escolares que construiste anteriormente (sin estudios, educación básica, etc...)
'''
part_11=part_10
conditions = [
       ( part_11['S3P1'] == 0 ) & ( part_11['SUMRESP'] > 10 ),
       ( part_11['S3P1'] == 0 ) & ( part_11['SUMRESP'] <= 10),
       ( part_11['S3P1'] <= 3 ) & ( part_11['S3P1'] > 0 ) & ( part_11['SUMRESP'] > 10 ),
       ( part_11['S3P1'] <= 3 ) & ( part_11['S3P1'] > 0 ) & ( part_11['SUMRESP'] <= 10), 
       ( part_11['S3P1'] == 4 ) & ( part_11['SUMRESP'] > 10 ),
       ( part_11['S3P1'] == 4 ) & ( part_11['SUMRESP'] <= 10) ,
       ( part_11['S3P1'] > 4 ) & (part_11['S3P1'] < 8) & ( part_11['SUMRESP'] > 10 ),
       ( part_11['S3P1'] > 4 ) & (part_11['S3P1'] < 8) & ( part_11['SUMRESP'] <= 10) ,
       ( part_11['S3P1'] >= 8) & (part_11['S3P1'] <= 10)& ( part_11['SUMRESP'] > 10 ),
       ( part_11['S3P1'] >= 8) & (part_11['S3P1'] <= 10)& ( part_11['SUMRESP'] <= 10) ]     
choices = ['Sin estudios con más del 50% correctas',
           'Sin estudios con menos del 50% correctas',
           'Básica con más del 50% correctas',
           'Básica con menos del 50% correctas', 
           'Media superior con más del 50% correctas',
           'Media superior con menos del 50% correctas',
           'Superior con más del 50% correctas',
           'Superior con menos del 50% correctas',
           'Posgrado con más del 50% correctas',
           'Posgrado con menos del 50% correctas']
part_11['estudios'] = np.select(conditions, choices, default='NO DEFINIDO')
part_123 = part_11[( part_11['estudios'] == 'Sin estudios con más del 50% correctas' )]
part_1234 = part_11[( part_11['estudios'] =='Sin menos con del 50% correctas' )]
part_11_1 = pd.concat([part_123,part_1234],axis = 0,keys = ["part_123","part1234"])

def grupo_estudios(class1,class2,niveled):
    part_select = part_11[(part_11['estudios']  == class1)]
    part_select_ = part_11[(part_11['estudios']  == class2)]  
    part_11_1 = pd.concat([part_select,part_select_],axis = 0,keys = ["part_select","part_select_"])
    total=sum(part_11_1['FAC18'])
    part_11_2=pd.DataFrame(part_11_1.groupby('estudios')['FAC18'].sum())
    part_11_2.reset_index(inplace=True)
    part_11_2['porcen']=(part_11_2['FAC18']/total)*100
    
    ##graficar
    a=list(part_11_2['porcen'])
    b=tuple(part_11_2['estudios'])
    fig, ax = plt.subplots()
    ax.pie(a, labels=b,pctdistance=0.5, autopct='%1.1f%%', shadow=False, startangle=90,textprops=dict(color="w"),explode=(0,0.1))
    ax.set_title('Población '+ niveled +' que obtuvo más del 50% de respuestas correctas\n sobre cultura cientifica vs quienes no.', fontweight='bold',loc='center')
    ax.legend( labels=b, loc='center', bbox_to_anchor=(.5, -.1, 0., 0))
    ax.axis('equal')   
    return part_select

grupo_estudios('Sin estudios con más del 50% correctas','Sin estudios con menos del 50% correctas','Sin estudios')
grupo_estudios('Básica con más del 50% correctas','Básica con menos del 50% correctas','de nivel básico')
grupo_estudios('Media superior con más del 50% correctas','Media superior con menos del 50% correctas','de nivel medio superior')
grupo_estudios('Superior con más del 50% correctas','Superior con menos del 50% correctas','de nivel superior')
grupo_estudios('Posgrado con más del 50% correctas','Posgrado con menos del 50% correctas','de nivel posgrado')
#%%
''' Resultado 12.
12.En el cuestionario, busca las preguntas que tienen que ver con pseudociencias.
Establece gráficas de pastel análogas a los dos puntos anteriores
pero utilizando las pseudociencias en lugar del total de respuestas

12.1. Para cada pregunta de la familia pseudociencias , realiza un gráfico de pastel donde representes
el porcentaje de quiénes tuvieron mas de la mitad de las respuestas
correctas vs quienes no.

12.2 Lo mismo que en el anterior, pero primero clasificando por cada uno de los
niveles escolares que construiste anteriormente (sin estudios, educación básica, etc...)
'''

part_12=cuestio[['FAC18',
                'Enti',
                'S3P1',
                'S4P31',
                'S4P33']]

part_12_33=part_12[['FAC18','S4P33']]
conditions=[
    (part_12_33['S4P33']== 1),
    (part_12_33['S4P33']== 2),
    (part_12_33['S4P33']== 3),
    (part_12_33['S4P33']== 4),
    (part_12_33['S4P33']== 5)]
choices=['a) Todo ser vivo, ha evolucionado\n mediante un proceso de selección natural',
         'b) Todas las especies de seres vivos\n fueron creadas por un ser supremo (Dios)',
         'c) Ambas afirmaciones son válidas',
         'd) Ninguna de esas afirmaciones son válidas',
         'e) No sabe']

part_12_33['pseudo']=np.select(conditions,choices,default='ninguna de las anteriores')
part_12_33=pd.DataFrame(part_12_33.groupby('pseudo')['FAC18'].sum())
part_12_33.reset_index(inplace=True)
total=sum(part_12_33['FAC18'])
part_12_33['porcent'] = (part_12_33['FAC18']/total)*100

##graficar
a=list(part_12_33['porcent'])
b=tuple(part_12_33['pseudo'])
fig, ax = plt.subplots()
ax.pie(a,pctdistance=1.2, autopct='%1.1f%%', shadow=False, startangle=150, explode=(0.05,0.05,0.05,0.05,0.05),textprops=dict(size=12))
ax.set_title("Percepción de población a nivel nacional acerca de \nlas ciencias modernas y de las pseudociencias",fontweight='bold', fontsize='large',loc = 'center')
ax.legend( labels=b, loc='center', bbox_to_anchor=(0.5, -0.3, 0, 0),fontsize=8)
ax.axis('equal')

part_12_33_1=part_12[['FAC18','S4P33','S3P1']]
conditions = [
       (part_12_33_1['S3P1']==0),
       (part_12_33_1['S3P1'] <= 3) & (part_12_33_1['S3P1'] > 0),
       (part_12_33_1['S3P1'] == 4),
       (part_12_33_1['S3P1'] > 4) & (part_12_33_1['S3P1'] < 8 ),
       (part_12_33_1['S3P1'] >= 8) & (part_12_33_1['S3P1'] <= 10 )]       
choices = ['Sin estudios','Básica', 'Media superior', 'Superior','posgrado']
part_12_33_1['estudios'] = np.select(conditions, choices, default='NO DEFINIDO')
conditions=[
    (part_12_33_1['S4P33']== 1),
    (part_12_33_1['S4P33']== 2),
    (part_12_33_1['S4P33']== 3),
    (part_12_33_1['S4P33']== 4),
    (part_12_33_1['S4P33']== 5)]
choices=['a)',
         'b)',
         'c)',
         'd)',
         'e)']
part_12_33_1['pseudo']=np.select(conditions,choices,default='ninguna de las anteriores')
part_12_33_1['id_pseudo']=part_12_33_1['estudios']+' '+part_12_33_1['pseudo'] 
part_12_33_1=pd.DataFrame(part_12_33_1.groupby('id_pseudo')['FAC18'].sum())
part_12_33_1.reset_index(inplace=True)

part_12_33_12=part_12_33_1[(part_12_33_1['id_pseudo']== 'Sin estudios a)') | (part_12_33_1['id_pseudo'] == 'Sin estudios b)')
                           |(part_12_33_1['id_pseudo']== 'Sin estudios c)')| (part_12_33_1['id_pseudo']== 'Sin estudios d)')
                           |(part_12_33_1['id_pseudo']== 'Sin estudios e)')]
conditions=[
    (part_12_33_12['id_pseudo'] == 'Sin estudios a)'),
    (part_12_33_12['id_pseudo'] == 'Sin estudios b)'),
    (part_12_33_12['id_pseudo'] == 'Sin estudios c)'),
    (part_12_33_12['id_pseudo'] == 'Sin estudios d)'),
    (part_12_33_12['id_pseudo'] == 'Sin estudios e)')]
choices=['a) Todo ser vivo, ha evolucionado\n mediante un proceso de selección natural',
         'b) Todas las especies de seres vivos\n fueron creadas por un ser supremo (Dios)',
         'c) Ambas afirmaciones son válidas',
         'd) Ninguna de esas afirmaciones son válidas',
         'e) No sabe']
part_12_33_12['id_pseudo']=np.select(conditions,choices,default='ninguna de las anteriores')
total=sum(part_12_33_12['FAC18'])
part_12_33_12['porcent'] = (part_12_33_12['FAC18']/total)*100

##graficar
a=list(part_12_33_12['porcent'])
b=tuple(part_12_33_12['id_pseudo'])
fig, ax = plt.subplots()
ax.pie(a,pctdistance=1.2, autopct='%1.1f%%', shadow=False, startangle=150,  explode=(0.05,0.05,0.05,0.05,0.05),textprops=dict(size=12))
ax.set_title("Percepción de población sin estudios acerca de\n las ciencias modernas y de las pseudociencias\n", fontweight='bold')
ax.legend( labels=b, loc='center', bbox_to_anchor=(0.5, -0.3, 0, 0),fontsize=8)
ax.axis('equal')

part_12_33_11=part_12_33_1[(part_12_33_1['id_pseudo']== 'Básica a)') | (part_12_33_1['id_pseudo'] == 'Básica b)')
                           |(part_12_33_1['id_pseudo']== 'Básica c)')| (part_12_33_1['id_pseudo']== 'Básica d)')
                           |(part_12_33_1['id_pseudo']== 'Básica e)')]
conditions=[
    (part_12_33_11['id_pseudo']== 'Básica a)'),
    (part_12_33_11['id_pseudo'] == 'Básica b)'),
    (part_12_33_11['id_pseudo']== 'Básica c)'),
    (part_12_33_11['id_pseudo']== 'Básica d)'),
    (part_12_33_11['id_pseudo']== 'Básica e)')]
choices=['a) Todo ser vivo, ha evolucionado\n mediante un proceso de selección natural',
         'b) Todas las especies de seres vivos\n fueron creadas por un ser supremo (Dios)',
         'c) Ambas afirmaciones son válidas',
         'd) Ninguna de esas afirmaciones son válidas',
         'e) No sabe']
part_12_33_11['id_pseudo']=np.select(conditions,choices,default='ninguna de las anteriores')
total=sum(part_12_33_11['FAC18'])
part_12_33_11['porcent'] = (part_12_33_11['FAC18']/total)*100

##graficar
a=list(part_12_33_11['porcent'])
b=tuple(part_12_33_11['id_pseudo'])
fig, ax = plt.subplots()
ax.pie(a,pctdistance=1.2, autopct='%1.1f%%', shadow=False, startangle=150,  explode=(0.05,0.05,0.05,0.05,0.05),textprops=dict(size=12))
ax.set_title("Percepción de población con estudios de nivel basico acerca\n de las ciencias modernas y de las pseudociencias\n", fontweight='bold')
ax.legend( labels=b, loc='center', bbox_to_anchor=(0.5, -0.3, 0, 0),fontsize=8)
ax.axis('equal')

part_12_33_13=part_12_33_1[(part_12_33_1['id_pseudo']== 'Media superior a)') | (part_12_33_1['id_pseudo'] == 'Media superior b)')
                           |(part_12_33_1['id_pseudo']== 'Media superior c)')| (part_12_33_1['id_pseudo']== 'Media superior d)')
                           |(part_12_33_1['id_pseudo']== 'Media superior e)')]
conditions=[
    (part_12_33_13['id_pseudo']== 'Media superior a)'),
    (part_12_33_13['id_pseudo']== 'Media superior b)'),
    (part_12_33_13['id_pseudo']== 'Media superior c)'),
    (part_12_33_13['id_pseudo']== 'Media superior d)'),
    (part_12_33_13['id_pseudo']== 'Media superior e)')]
choices=['a) Todo ser vivo, ha evolucionado\n mediante un proceso de selección natural',
         'b) Todas las especies de seres vivos\n fueron creadas por un ser supremo (Dios)',
         'c) Ambas afirmaciones son válidas',
         'd) Ninguna de esas afirmaciones son válidas',
         'e) No sabe']
part_12_33_13['id_pseudo']=np.select(conditions,choices,default='ninguna de las anteriores')
total=sum(part_12_33_13['FAC18'])
part_12_33_13['porcent'] = (part_12_33_13['FAC18']/total)*100

##graficar
a=list(part_12_33_13['porcent'])
b=tuple(part_12_33_13['id_pseudo'])
fig, ax = plt.subplots()
ax.pie(a,pctdistance=1.2, autopct='%1.1f%%', shadow=False, startangle=155,  explode=(0.05,0.05,0.05,0.05,0.05),textprops=dict(size=12))
ax.set_title("Percepción de población con estudios de nivel medio superior\n acerca de las ciencias modernas y de las pseudociencias\n", fontweight='bold')
ax.legend( labels=b, loc='center', bbox_to_anchor=(0.5, -0.3, 0, 0),fontsize=8)
ax.axis('equal')

part_12_33_14=part_12_33_1[(part_12_33_1['id_pseudo']== 'Superior a)') | (part_12_33_1['id_pseudo'] == 'Superior b)')
                           |(part_12_33_1['id_pseudo']== 'Superior c)')| (part_12_33_1['id_pseudo']== 'Superior d)')
                           |(part_12_33_1['id_pseudo']== 'Superior e)')]
conditions=[
    (part_12_33_14['id_pseudo']== 'Superior a)'),
    (part_12_33_14['id_pseudo']== 'Superior b)'),
    (part_12_33_14['id_pseudo']== 'Superior c)'),
    (part_12_33_14['id_pseudo']== 'Superior d)'),
    (part_12_33_14['id_pseudo']== 'Superior e)')]
choices=['a) Todo ser vivo, ha evolucionado\n mediante un proceso de selección natural',
         'b) Todas las especies de seres vivos\n fueron creadas por un ser supremo (Dios)',
         'c) Ambas afirmaciones son válidas',
         'd) Ninguna de esas afirmaciones son válidas',
         'e) No sabe']
part_12_33_14['id_pseudo']=np.select(conditions,choices,default='ninguna de las anteriores')
total=sum(part_12_33_14['FAC18'])
part_12_33_14['porcent'] = (part_12_33_14['FAC18']/total)*100

##graficar
a=list(part_12_33_14['porcent'])
b=tuple(part_12_33_14['id_pseudo'])
fig, ax = plt.subplots()
ax.pie(a,pctdistance=1.2, autopct='%1.1f%%', shadow=False, startangle=155,  explode=(0.05,0.05,0.05,0.05,0.05),textprops=dict(size=12))
ax.set_title("Percepción de población con estudios de nivel superior\n acerca de las ciencias modernas y de las pseudociencias\n", fontweight='bold')
ax.legend( labels=b, loc='center', bbox_to_anchor=(0.5, -0.3, 0, 0),fontsize=8)
ax.axis('equal')

part_12_33_15=part_12_33_1[(part_12_33_1['id_pseudo']== 'posgrado a)') | (part_12_33_1['id_pseudo'] == 'posgrado b)')
                           |(part_12_33_1['id_pseudo']== 'posgrado c)')| (part_12_33_1['id_pseudo']== 'posgrado d)')
                           |(part_12_33_1['id_pseudo']== 'posgrado e)')]
conditions=[
    (part_12_33_15['id_pseudo'] == 'posgrado a)'),
    (part_12_33_15['id_pseudo'] == 'posgrado b)'),
    (part_12_33_15['id_pseudo'] == 'posgrado c)'),
    (part_12_33_15['id_pseudo'] == 'posgrado d)'),
    (part_12_33_15['id_pseudo'] == 'posgrado e)')]
choices=['a) Todo ser vivo, ha evolucionado\n mediante un proceso de selección natural',
         'b) Todas las especies de seres vivos\n fueron creadas por un ser supremo (Dios)',
         'c) Ambas afirmaciones son válidas',
         'd) Ninguna de esas afirmaciones son válidas',
         'e) No sabe']
part_12_33_15['id_pseudo']=np.select(conditions,choices,default='ninguna de las anteriores')
total=sum(part_12_33_15['FAC18'])
part_12_33_15['porcent'] = (part_12_33_15['FAC18']/total)*100

##graficar
a=list(part_12_33_15['porcent'])
b=tuple(part_12_33_15['id_pseudo'])
fig, ax = plt.subplots()
ax.pie(a,pctdistance=1.2, autopct='%1.1f%%', shadow=False, startangle=155,  explode=(0.05,0.05,0.05,0.05),textprops=dict(size=12))
ax.set_title("Percepción de población con estudios de nivel posgrado\n acerca de las ciencias modernas y de las pseudociencias\n", fontweight='bold')
ax.legend( labels=b, loc='center', bbox_to_anchor=(0.5, -0.3, 0, 0),fontsize=8)
ax.axis('equal')

part_12_31=part_12[['FAC18','S4P31']]
conditions=[
    (part_12_31['S4P31']== 1),
    (part_12_31['S4P31']== 2),
    (part_12_31['S4P31']== 3),
    (part_12_31['S4P31']== 4),
    (part_12_31['S4P31']== 5),
    (part_12_31['S4P31']== 6)]
choices=['Confía más en la ciencia',
         'Confía más en la fe o religión',
         'Confía de igual manera en ambas',
         'Confía en su intuición',
         'No confía en ninguna',
         'No sabe']
part_12_31['FEVSCIEN']=np.select(conditions,choices,default='ninguna de las anteriores')
part_12_31=pd.DataFrame(part_12_31.groupby('FEVSCIEN')['FAC18'].sum())
part_12_31.reset_index(inplace=True)
total=sum(part_12_31['FAC18'])
part_12_31['porcent'] = (part_12_31['FAC18']/total)*100

##graficar
a=list(part_12_31['porcent'])
b=tuple(part_12_31['FEVSCIEN'])
fig, ax = plt.subplots()
ax.pie(a,pctdistance=1.2, autopct='%1.1f%%', shadow=False, startangle=125,  explode=(0.05,0.05,0.05,0.05,0.22,0.05),textprops=dict(size=12))
ax.set_title("Percepción sobre fe y ciencia de la población a nivel nacional \n", fontweight='bold')
ax.legend( labels=b, loc='center', bbox_to_anchor=(0.5, -0.3, 0, 0),fontsize=8)
ax.axis('equal')


part_12_31_1=part_12[['FAC18','S3P1','S4P31']]
part_12_31_11=part_12_31_1[part_12_31_1['S3P1'] == 0]                            
conditions=[
    (part_12_31_11['S4P31']== 1),
    (part_12_31_11['S4P31']== 2),
    (part_12_31_11['S4P31']== 3),
    (part_12_31_11['S4P31']== 4),
    (part_12_31_11['S4P31']== 5),
    (part_12_31_11['S4P31']== 6)]
choices=['Confía más en la ciencia',
         'Confía más en la fe o religión',
         'Confía de igual manera en ambas',
         'Confía en su intuición',
         'No confía en ninguna',
         'No sabe']
part_12_31_11['FEVSCIEN']=np.select(conditions,choices,default='ninguna de las anteriores')
part_12_31_11=pd.DataFrame(part_12_31_11.groupby('FEVSCIEN')['FAC18'].sum())
part_12_31_11.reset_index(inplace=True)
total=sum(part_12_31_11['FAC18'])
part_12_31_11['porcent'] = (part_12_31_11['FAC18']/total)*100

##graficar
a=list(part_12_31_11['porcent'])
b=tuple(part_12_31_11['FEVSCIEN']) 
fig, ax = plt.subplots()
ax.pie(a,pctdistance=1.2, autopct='%1.1f%%', shadow=False, startangle=125,  explode=(0.05,0.05,0.05,0.05,0.22,0.00),textprops=dict(size=12))
ax.set_title("Percepción de sobre fe y ciencia de la población\n que no cuenta con estudios \n", fontweight='bold')
ax.legend( labels=b, loc='center', bbox_to_anchor=(0.5, -0.3, 0, 0),fontsize=8)
ax.axis('equal')

part_12_31_12=part_12_31_1[(part_12_31_1['S3P1'] > 0) & (part_12_31_1['S3P1'] <= 3)]                            
conditions=[
    (part_12_31_12['S4P31']== 1),
    (part_12_31_12['S4P31']== 2),
    (part_12_31_12['S4P31']== 3),
    (part_12_31_12['S4P31']== 4),
    (part_12_31_12['S4P31']== 5),
    (part_12_31_12['S4P31']== 6)]
choices=['Confía más en la ciencia',
         'Confía más en la fe o religión',
         'Confía de igual manera en ambas',
         'Confía en su intuición',
         'No confía en ninguna',
         'No sabe']
part_12_31_12['FEVSCIEN']=np.select(conditions,choices,default='ninguna de las anteriores')
part_12_31_12=pd.DataFrame(part_12_31_12.groupby('FEVSCIEN')['FAC18'].sum())
part_12_31_12.reset_index(inplace=True)
total=sum(part_12_31_12['FAC18'])
part_12_31_12['porcent'] = (part_12_31_12['FAC18']/total)*100

##graficar
a=list(part_12_31_12['porcent'])
b=tuple(part_12_31_12['FEVSCIEN'])
fig, ax = plt.subplots()
ax.pie(a,pctdistance=1.2, autopct='%1.1f%%', shadow=False, startangle=125,  explode=(0.05,0.05,0.05,0.05,0.22,0.00),textprops=dict(size=12))
ax.set_title("Percepción de sobre fe y ciencia de la población\n que cuenta con estudios de nivel básico \n", fontweight='bold')
ax.legend( labels=b, loc='center', bbox_to_anchor=(0.5, -0.3, 0, 0),fontsize=8)
ax.axis('equal')


part_12_31_13=part_12_31_1[(part_12_31_1['S3P1'] == 4) ]                            
conditions=[
    (part_12_31_13['S4P31']== 1),
    (part_12_31_13['S4P31']== 2),
    (part_12_31_13['S4P31']== 3),
    (part_12_31_13['S4P31']== 4),
    (part_12_31_13['S4P31']== 5),
    (part_12_31_13['S4P31']== 6)]
choices=['Confía más en la ciencia',
         'Confía más en la fe o religión',
         'Confía de igual manera en ambas',
         'Confía en su intuición',
         'No confía en ninguna',
         'No sabe']
part_12_31_13['FEVSCIEN']=np.select(conditions,choices,default='ninguna de las anteriores')
part_12_31_13=pd.DataFrame(part_12_31_13.groupby('FEVSCIEN')['FAC18'].sum())
part_12_31_13.reset_index(inplace=True)
total=sum(part_12_31_13['FAC18'])
part_12_31_13['porcent'] = (part_12_31_13['FAC18']/total)*100

##graficar
a=list(part_12_31_13['porcent'])
b=tuple(part_12_31_13['FEVSCIEN']) 
fig, ax = plt.subplots()
ax.pie(a,pctdistance=1.2, autopct='%1.1f%%', shadow=False, startangle=125,  explode=(0.05,0.05,0.05,0.05,0.22,0.00),textprops=dict(size=12))
ax.set_title("Percepción de sobre fe y ciencia de la población\n que cuenta con estudios de nivel medio superior \n", fontweight='bold')
ax.legend( labels=b, loc='center', bbox_to_anchor=(0.5, -0.3, 0, 0),fontsize=8)
ax.axis('equal')

part_12_31_14=part_12_31_1[(part_12_31_1['S3P1'] > 4) & (part_12_31_1['S3P1'] < 8)  ]                            
conditions=[
    (part_12_31_14['S4P31']== 1),
    (part_12_31_14['S4P31']== 2),
    (part_12_31_14['S4P31']== 3),
    (part_12_31_14['S4P31']== 4),
    (part_12_31_14['S4P31']== 5),
    (part_12_31_14['S4P31']== 6)]
choices=['Confía más en la ciencia',
         'Confía más en la fe o religión',
         'Confía de igual manera en ambas',
         'Confía en su intuición',
         'No confía en ninguna',
         'No sabe']
part_12_31_14['FEVSCIEN']=np.select(conditions,choices,default='ninguna de las anteriores')
part_12_31_14=pd.DataFrame(part_12_31_14.groupby('FEVSCIEN')['FAC18'].sum())
part_12_31_14.reset_index(inplace=True)
total=sum(part_12_31_14['FAC18'])
part_12_31_14['porcent'] = (part_12_31_14['FAC18']/total)*100

##graficar
a=list(part_12_31_14['porcent'])
b=tuple(part_12_31_14['FEVSCIEN']) 
fig, ax = plt.subplots()
ax.pie(a,pctdistance=1.2, autopct='%1.1f%%', shadow=False, startangle=125,  explode=(0.05,0.05,0.05,0.05,0.22,0.00),textprops=dict(size=12))
ax.set_title("Percepción de sobre fe y ciencia de la población\n que cuenta con estudios de nivel superior \n", fontweight='bold')
ax.legend( labels=b, loc='center', bbox_to_anchor=(0.5, -0.3, 0, 0),fontsize=8)
ax.axis('equal')

part_12_31_15=part_12_31_1[(part_12_31_1['S3P1'] >= 8) & (part_12_31_1['S3P1'] <= 10)  ]                            
conditions=[
    (part_12_31_15['S4P31']== 1),
    (part_12_31_15['S4P31']== 2),
    (part_12_31_15['S4P31']== 3),
    (part_12_31_15['S4P31']== 4),
    (part_12_31_15['S4P31']== 5),
    (part_12_31_15['S4P31']== 6)]
choices=['Confía más en la ciencia',
         'Confía más en la fe o religión',
         'Confía de igual manera en ambas',
         'Confía en su intuición',
         'No confía en ninguna',
         'No sabe']
part_12_31_15['FEVSCIEN']=np.select(conditions,choices,default='ninguna de las anteriores')
part_12_31_15=pd.DataFrame(part_12_31_15.groupby('FEVSCIEN')['FAC18'].sum())
part_12_31_15.reset_index(inplace=True)
total=sum(part_12_31_15['FAC18'])
part_12_31_15['porcent'] = (part_12_31_15['FAC18']/total)*100

##graficar
a=list(part_12_31_15['porcent'])
b=tuple(part_12_31_15['FEVSCIEN']) 
fig, ax = plt.subplots()
ax.pie(a,pctdistance=1.2, autopct='%1.1f%%', shadow=False, startangle=125,  explode=(0.05,0.05,0.05,0.05,0.27),textprops=dict(size=12))
ax.set_title("Percepción de sobre fe y ciencia de la población\n que cuenta con estudios de nivel posgrado \n", fontweight='bold')
ax.legend( labels=b, loc='center', bbox_to_anchor=(0.5, -0.3, 0, 0),fontsize=8)
ax.axis('equal')
#%%