# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 12:23:16 2022

@author: Propietario
"""
import pandas as pd
import streamlit as st
import pydeck as pdk 
import plotly.express as px
import plotly.graph_objects as go
import base64
import datetime
from PIL import Image 

def get_table_download_link(df):
    csv = df.to_csv(index =False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{ b64}" download="datos.csv">Descargar archivo csv</a>'
    return href

st.set_page_config(layout='wide')
st.markdown("<h1 style ='text-align: center;color:black;'> Empleabilidad en Ontario-Canada🍁💼 </h1>",unsafe_allow_html=True)

pib_def = pd.read_csv('bases/PIB.csv')

empleoclase_def = pd.read_csv('bases/empleo_clase.csv')


poblacion_def = pd.read_csv('bases/Poblacion.csv')

duracion_desem = pd.read_csv('bases/Duracion_desempleo.csv')

rates_education = pd.read_csv('bases/Nivel_educativo.csv')

#---------------------------------------------------------------
c1,c2,c3=st.columns((1,1,1))

img2 = Image.open("img2.png") 
  
c2.image(img2, width=355) 

img = Image.open("img.png") 
  
c1.image(img, width=400) 

img3 = Image.open("img3.png") 
  
c3.image(img3, width=300) 

#---------------------------------------------------------------
# pregunta 4 

st.markdown("<h3 style='text-align: center; color: Black;'> Número de empleados por región y año </h3>", unsafe_allow_html=True)

empleoclase_defa= empleoclase_def.copy()
empleoclase_defc = empleoclase_defa[(empleoclase_defa['geografia']!='Total, Ontario regions') & (empleoclase_defa['clase de trabajador']!='Total employment') & (empleoclase_defa['clase de trabajador']!='  Employees') ]
empleoclase_definal=empleoclase_defc.sort_values('valor', ascending=False)
empleoclase_definal=empleoclase_definal.groupby(['geografia','fecha'])[['valor']].sum().reset_index()


fig = px.bar(empleoclase_definal, x ='fecha', y='valor', color='geografia',
             width=1200, height=450)

 #            title= '<b>Número de empleados por región y año<b>',
  #           color_discrete_sequence=px.colors.qualitative.Dark24)

#Detalles gráfica
fig.update_layout(
    title_x=0.5,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    template = 'simple_white',
    legend_title ='Región o zona Geográfica:',
    xaxis_title = '<b>Año<b>',
    yaxis_title = '<b>Cantidad de empleados<b>')
  
# Enviar gráfica a streamlit
st.plotly_chart(fig)

#-----------------------

#pregunta 1

st.markdown("<h3 style='text-align: center; color: Black;'> Indicador de duración de desempleo por región y año</h3>", unsafe_allow_html=True)

duracion_desem_p1=duracion_desem.copy()

#Eliminando categorías que no son de interes para esta pregunta
duracion_desem_p1=duracion_desem_p1[duracion_desem_p1['duracion']!='total unemployed']
duracion_desem_p1=duracion_desem_p1[duracion_desem_p1['duracion']!='   duration unknown']
duracion_desem_p1=duracion_desem_p1[duracion_desem_p1['duracion']!='average unemployed nc']
duracion_desem_p1=duracion_desem_p1[duracion_desem_p1['duracion']!='average unemployed c99']
duracion_desem_p1=duracion_desem_p1[duracion_desem_p1['geografia']!='total, ontario regions']
duracion_desem_p1['duracion']=duracion_desem_p1['duracion'].replace('   27 weeks or more','      27 - 51 weeks')
duracion_desem_p1=duracion_desem_p1.rename(columns={'mes':'trimestre'})
duracion_desem_p1=duracion_desem_p1[(duracion_desem_p1['rango edad']!='total, 15 years and over')&(duracion_desem_p1['rango edad']!=' 15-64 years')]

#Creando indicador, dependiendo de la categoría de la duranción se dara un valor de criticidad y posteriormente se multiplica dicho valor por la cantidad de personas
def funcion(x):
  if x['duracion'] =='   1 - 4 weeks':
    valor= 1
  elif x['duracion'] =='   5 - 13 weeks':
    valor=2
  elif x['duracion'] =='   14 - 25 weeks':
    valor=3   
  elif x['duracion'] =='   26 weeks ':
    valor=4
  elif x['duracion'] =='      27 - 51 weeks':
    valor=5
  elif x['duracion'] =='      52 weeks':
    valor=6 
  else:
    valor=7
  return valor 

duracion_desem_p1['criticidad'] = duracion_desem_p1.apply(funcion, axis = 1)
duracion_desem_p1['indicador']=duracion_desem_p1['total personas']*duracion_desem_p1['criticidad']
duracion_desem_p1['indicador']=duracion_desem_p1['indicador']/1000

#Dataframe con indicador de duración de desempleo por región y año
duracion_desem_p11 = duracion_desem_p1.groupby(['geografia','fecha'])[['indicador']].sum()
duracion_desem_p11=duracion_desem_p11.reset_index()

#Dataframe con la región con el peor indicador de duración de desempleo por año 
duracion_desem_p111=duracion_desem_p11.copy()
duracion_desem_p111=duracion_desem_p111.sort_values('indicador',ascending=False)
duracion_desem_p111=duracion_desem_p111.drop_duplicates(['fecha'],keep='first')
duracion_desem_p111=duracion_desem_p111.sort_values('fecha', ascending=True)

#Gráfica dataframe con indicador de duración de desempleo por región y año
fig1 = px.bar(duracion_desem_p11, x = 'fecha', y='indicador', color = 'geografia', barmode = 'relative',
             width=1200, height=450)

#Detalles a la gráfica
fig1.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_title = 'Año',
    yaxis_title = 'Indicador criticidad en la duración del desempleo',
    template = 'simple_white',
    title_x = 0.5)

# Enviar gráfica a streamlit
st.plotly_chart(fig1)
#-----------------------------------------------

#pregunta 6 

st.markdown("<h3 style='text-align: center; color: Black;'>Población que permanecio más de 53 semanas desempleada por año y sexo</h3>", unsafe_allow_html=True)

duracion_desem1 = duracion_desem.copy()
duracion_desem6 = duracion_desem1[duracion_desem1['duracion']=='      53 weeks or more'] # categoria que representa la mayor duracion de desempleo 

duracion_desem6 = duracion_desem6.groupby(['fecha'])[['hombres','mujeres']].sum().reset_index() # evolucion del desempleo en hombres y mujeres en base al mayor tiempo de desempleo 

fig = px.bar(duracion_desem6, x ='fecha', y=['hombres', 'mujeres'],
             width=1200, height=450, color_discrete_sequence=px.colors.qualitative.Vivid)

#Detalles gráfica
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_title = '<b>Año<b>',
    yaxis_title = '<b>desempleados por región<b>',
    template = 'simple_white',
    title_x = 0.5)

# Enviar gráfica a streamlit
st.plotly_chart(fig)
#---------------------------------------------------
#pregunta 17

st.markdown("<h3 style ='text-align: center;color:black;'> Desempleabilidad por año con base en los grupos por edad</h3>",unsafe_allow_html=True)

# Ignorar categoria que representa el totalizado de las otras categorias
duracion_desem = duracion_desem[duracion_desem['duracion']!='   27 weeks or more'] 
duracion_desem7 = duracion_desem[(duracion_desem['rango edad']!= 'total, 15 years and over') & (duracion_desem['rango edad']!= ' 15-64 years')] 


# bases con el total de desempleo por año en cada rango de edad 
desem_rango1a = duracion_desem7[duracion_desem7['rango edad']=='  15-19'].groupby(['fecha'])[['total personas']].sum().reset_index()
desem_rango2a = duracion_desem7[duracion_desem7['rango edad']=='  20-24'].groupby(['fecha'])[['total personas']].sum().reset_index()
desem_rango3a = duracion_desem7[duracion_desem7['rango edad']=='  25-44'].groupby(['fecha'])[['total personas']].sum().reset_index()
desem_rango4a = duracion_desem7[duracion_desem7['rango edad']=='  45-54'].groupby(['fecha'])[['total personas']].sum().reset_index()
desem_rango5a = duracion_desem7[duracion_desem7['rango edad']=='  55-64'].groupby(['fecha'])[['total personas']].sum().reset_index()
desem_rango6a = duracion_desem7[duracion_desem7['rango edad']=='  65 years and over'].groupby(['fecha'])[['total personas']].sum().reset_index()

# desempleo por año segun el rango de edad 
desem_rangosa = pd.merge(desem_rango1a, desem_rango2a, how = 'left', on = 'fecha').merge(desem_rango3a, how = 'left', on = 'fecha').merge(desem_rango4a, how = 'left', on = 'fecha').merge(desem_rango5a, how = 'left', on = 'fecha').merge(desem_rango6a, how = 'left', on = 'fecha')
desem_rangosa.columns = ['año','15-19','20-24','25-44','45-54','55-64','65 years and over'] 

# el gráfico anterior en lineas
fig = px.line(desem_rangosa, x = 'año', y =['15-19','20-24','25-44','45-54','55-64','65 years and over'],
             width=1200, height=450,color_discrete_sequence=px.colors.qualitative.Set1)

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_title = 'año',
    yaxis_title = 'desempleados',
    template = 'simple_white',
    title_x = 0.5,
    legend_title_text='',
    legend=dict(orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.8))

#enviar una figura 
st.plotly_chart(fig)
#------------------------------------------------------------------------

st.markdown("<h3 style='text-align: center; color: Black;'>Clase de trabajadores por región</h3>", unsafe_allow_html=True)


empleoclase_def_p3=empleoclase_def
empleoclase_def_p31=empleoclase_def.copy()

#Dataframe con los valores promedio de cada región de Ontario por clase de trabajador
empleoclase_def_p31=empleoclase_def_p31[(empleoclase_def_p31['clase de trabajador']!='Total employment') & (empleoclase_def_p31['clase de trabajador']!='  Employees')&(empleoclase_def_p31['geografia']!='total, ontario regions') & (empleoclase_def_p31['clase de trabajador']!='  Self-employed')]
empleoclase_def_p31=empleoclase_def_p31.reset_index()
empleoclase_def_p31=empleoclase_def_p31.drop(['index'],axis=1)
empleoclase_def_p31 = pd.pivot_table(empleoclase_def_p31, values='valor', index=['clase de trabajador'], columns=['geografia'], aggfunc='mean')

#Dataframe de comuna con más casos por cada criminalidad
columnas = empleoclase_def_p31[['Central region','Eastern region', 'Northern region',	'Western region']]
array1=[]
array2=[]
array3=[]
columnaarray1=['valor promedio']
columnaarray2=['clase trabajador']
columnaarray3=['region']
for i in columnas:
    x=empleoclase_def_p31[i].max()
    y=empleoclase_def_p31[i].idxmax(axis=0)
    array1.append([x])
    array2.append([y])
    array3.append([i])

basevalorp = pd.DataFrame(array1, columns = columnaarray1)
baseclaset = pd.DataFrame(array2, columns = columnaarray2)
baseregion = pd.DataFrame(array3, columns = columnaarray3)
empleoclase_def_p32 = pd.concat([basevalorp, baseclaset, baseregion],axis=1)

#Dataframe para graficos de torta
empleoclase_def_p3graf=empleoclase_def_p31.copy()
empleoclase_def_p3graf=empleoclase_def_p3graf.reset_index()

#-----

#Grafico 1 Central region (%Clase de trabajadores)
fig1 = px.pie(empleoclase_def_p3graf, values = 'Central region', names ='clase de trabajador',
              width=580, height=400,color_discrete_sequence=px.colors.qualitative.G10)

#Detalles a la gráfica
fig1.update_layout(
    template = 'simple_white',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend_title = '<b>Clase<b>',
    title_x = 0.60)



#------

#Grafico 2 Eastern region (%Clase de trabajadores)
fig2 = px.pie(empleoclase_def_p3graf, values = 'Eastern region', names ='clase de trabajador',
             width=580, height=400,color_discrete_sequence=px.colors.qualitative.G10)

#Detalles a la gráfica
fig2.update_layout(
    template = 'simple_white',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend_title = '<b>Clase<b>',
    title_x = 0.60)

#------


#Grafico 3 Northern  region (%Clase de trabajadores)
fig3 = px.pie(empleoclase_def_p3graf, values = 'Northern region', names ='clase de trabajador',
             width=580, height=400,
             color_discrete_sequence=px.colors.qualitative.G10)

#Detalles a la gráfica
fig3.update_layout(
    template = 'simple_white',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend_title = '<b>Clase<b>',
    title_x = 0.60)


#-----


#Grafico 4 Western  region (%Clase de trabajadores)
fig4 = px.pie(empleoclase_def_p3graf, values = 'Western region', names ='clase de trabajador',
             width=580, height=400,
             color_discrete_sequence=px.colors.qualitative.G10)

#Detalles a la gráfica
fig4.update_layout(
    template = 'simple_white',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend_title = '<b>Clase<b>',
    title_x = 0.60)





status = st.radio("Region: ",('Central', 'Eastern','Northern','Western')) 
  
if (status == 'Central'): 
    st.markdown("<h5 style ='text-align: center;color:black;'> Central region (%Clase de trabajadores)</h5>",unsafe_allow_html=True)
    c1,c2,= st.columns((1,1))
    c1.plotly_chart(fig1)
    img = Image.open("Cen.png") 
    c2.image(img, width=550) 
elif(status=='Eastern'):
    st.markdown("<h5 style ='text-align: center;color:black;'> Eastern region (%Clase de trabajadores)</h5>",unsafe_allow_html=True)
    c1,c2,= st.columns((1,1))
    c1.plotly_chart(fig2)
    img = Image.open("Eas.png") 
    c2.image(img, width=650) 
elif(status=='Northern'):
    st.markdown("<h5 style ='text-align: center;color:black;'> Northern region (%Clase de trabajadores)</h5>",unsafe_allow_html=True)
    c1,c2,= st.columns((1,1))
    c1.plotly_chart(fig3)
    img = Image.open("Nor.png") 
    c2.image(img, width=650) 
else: 
    st.markdown("<h5 style ='text-align: center;color:black;'> Western region (%Clase de trabajadores)</h5>",unsafe_allow_html=True)
    c1,c2,= st.columns((1,1))
    c1.plotly_chart(fig4)
    img = Image.open("Wes.png") 
    c2.image(img, width=550) 
#----------------------------------------
#pregunta 8

c3,c4,= st.columns((1,1))

c3.markdown("<h3 style ='text-align: center;color:black;'> Comportamiento del sector público y privado entre los años 2001 al 2015</h3>",unsafe_allow_html=True)


empleoclase_defc = empleoclase_defa[(empleoclase_defa['geografia']!='Total, Ontario regions') & (empleoclase_defa['clase de trabajador']!='Total employment') & (empleoclase_defa['clase de trabajador']!='  Employees') ]
empleo8= empleoclase_defc.copy()

empleo8 = empleo8[(empleo8['clase de trabajador'] =='    Public sector employees') | (empleo8['clase de trabajador'] =='    Private sector employees')]
empleo8 = empleo8.groupby(['fecha','clase de trabajador'])[['valor']].sum().reset_index()

fig = px.line(empleo8, x = 'fecha', y =['valor'],color= 'clase de trabajador',markers = True,
             width=650, height=450,
             color_discrete_sequence=px.colors.qualitative.Set1)

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis_title = 'Año',
    yaxis_title = 'Evolución del empleo por sector',
    legend_title = 'Tipo de sector:',
    template = 'simple_white',
    title_x = 0.5,
    legend_title_text='',
    legend=dict(orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.8))

#enviar una figura 
c3.plotly_chart(fig)

c4.markdown("<h3 style ='text-align: center; color: black;'>Comportamiento del sector formal e informal entre los años 2001 - 2015 </h3>", unsafe_allow_html =True)

conformacion= empleoclase_def.copy()
conformacion1=conformacion[conformacion['clase de trabajador']=='  Employees']
conformacion1=conformacion1[conformacion1['geografia']=='Total, Ontario regions']
conformacion2=conformacion[conformacion['clase de trabajador']=='  Self-employed']
conformacion2=conformacion2[conformacion2['geografia']=='Total, Ontario regions']
conformacion3=pd.merge(conformacion1, conformacion2, how = 'left', on = 'fecha')
conformacion3['total']=conformacion3['valor_x']+conformacion3['valor_y']
conformacion3['porcentaje_x']=conformacion3['valor_x']/conformacion3['total']
conformacion3['porcentaje_y']=conformacion3['valor_y']/conformacion3['total']
conformacion4=conformacion3[['geografia_x','clase de trabajador_x','fecha','valor_x','porcentaje_x']]
conformacion5=conformacion3[['geografia_x','clase de trabajador_y','fecha','valor_y','porcentaje_y']]
conformacion5=conformacion5.rename(columns={'clase de trabajador_y':'clase de trabajador_x','valor_y':'valor_x','porcentaje_y':'porcentaje_x'})
conformacion6=pd.concat([conformacion4,conformacion5], axis=0)
conformacion6=conformacion6.rename(columns={'geografia_x':'geografia','clase de trabajador_x':'clase de trabajador','valor_x':'valor','porcentaje_x':'porcentaje'})


fig = px.line(conformacion6, x = 'fecha', y =['porcentaje'],color= 'clase de trabajador',markers = True,
             width =650, height = 450, color_discrete_sequence=px.colors.qualitative.Set1)

fig.update_layout(
    xaxis_title = 'Año',
    yaxis_title = 'Evolución del empleo por sector',
    legend_title = 'Tipo de sector:',
    template = 'simple_white',
    plot_bgcolor='rgba(0,0,0,0)',
    title_x = 0.5,
    legend=dict(orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.8))

c4.plotly_chart(fig)

#---------------------------------------------------------

#------Sección Nivel académico y PIB
st.markdown("<h3 style ='text-align: center; color: black;'>¿Cuál es la correlación del desempleo por tipo de nivel educativo y el PIB anual?</h3>", unsafe_allow_html =True)

#Dataframe porcentaje de desempleor por Nivel Educativo
rates_education_p2=rates_education[rates_education['nivel_educativo']!='all levels of education']
rates_education_p2=rates_education_p2[rates_education_p2['geografia']=='ontario'].reset_index()
rates_education_p2=rates_education_p2.drop(['index'],axis=1)

#Dataframe PIB
pib_def_p2=pib_def[['fecha','unidad de medida', 'valor']]
pib_def_p2=pib_def_p2.rename(columns={'valor':'monto'})
pib_def_p2=pib_def_p2.reset_index()
pib_def_p2=pib_def_p2.drop(['index'],axis=1)

#Dataframe concatenado
pp2=pd.merge(rates_education_p2, pib_def_p2, how = 'left', on = 'fecha')

#Creación lista 
array1=[]
cor1=pp2[pp2['nivel_educativo']=='less than high school']
cor2=pp2[pp2['nivel_educativo']=='high school']
cor3=pp2[pp2['nivel_educativo']=='college or trade']
cor4=pp2[pp2['nivel_educativo']=='university']
array1.append([cor1['monto'].corr(cor1['valor'])])
array1.append([cor2['monto'].corr(cor2['valor'])])
array1.append([cor3['monto'].corr(cor3['valor'])])
array1.append([cor4['monto'].corr(cor4['valor'])])

#Columna nueva de correlación
def funcion(x):
  if x['nivel_educativo'] =='less than high school':
    valor = array1[0]
  elif  x['nivel_educativo'] =='high school':
    valor = array1[1]
  elif  x['nivel_educativo'] =='college or trade':
    valor = array1[2]
  else:
    valor = array1[3]
  return valor 
pp2['correlacion'] = pp2.apply(funcion, axis = 1)
pp2['correlacion'] =pp2['correlacion'].astype('string')
pp2['correlacion']=pp2['correlacion'].str.replace("[","").str.replace("]","")
pp2['correlacion']=pp2['correlacion'].apply(lambda x: x[0:5])

#Transformación sobre el score para visualizar mayor diferencia entre el tamaño de los puntos
pp2['valor_norm'] = (pp2['valor'] - pp2['valor'].min())/(pp2['valor'].max()- pp2['valor'].min())

#Gráfica
fig = px.scatter(pp2, x = 'valor', y ='monto', color = 'nivel_educativo', width =1200, height = 450,
           hover_name = 'nivel_educativo', size = 'valor_norm', hover_data = ['correlacion'])

#Atributos
fig.update_layout(
    xaxis_title = '<b>Desempleo por nivel educativo<b>',
    yaxis_title = '<b>PIB anual<b>',
    plot_bgcolor='rgba(0,0,0,0)',
    template = 'simple_white',
    title_x = 0.5,)

# Enviar gráfica a streamlit
st.plotly_chart(fig)

if st.checkbox('Obtener el porcentaje mínimo y máximo de desempleo alcanzado por nivel educativo entre 2001 y 2015', False):
    st.markdown("<h3 style ='text-align: center; color: black;'>Porcentaje mínimo y máximo de desempleo alcanzado por nivel educativo entre 2001 y 2015</h3>", unsafe_allow_html =True)
    c1,c2=st.columns((1,1))
    jc=rates_education.copy()
    ja=jc.drop(['fecha'], axis=1).reset_index().drop('index', axis=1)
    jd=ja[ja['nivel_educativo']!='all levels of education']

    jd=jd[jd['geografia']=='canada'].reset_index()
    jd=jd.drop(['index'],axis=1)

    #Máximo
    jn = jd[(jd['nivel_educativo'] == 'less than high school')]
    jn = jn.sort_values('valor',ascending=False)
    jn = jn.head(1)

    jm = jd[(jd['nivel_educativo'] == 'high school')]
    jm = jm.sort_values('valor',ascending=False)
    jm = jm.head(1)
    jk = jd[(jd['nivel_educativo'] == 'college or trade')]
    jk = jk.sort_values('valor',ascending=False)
    jk = jk.head(1)
    jo = jd[(jd['nivel_educativo'] == 'university')]
    jo = jo.sort_values('valor',ascending=False)
    jo = jo.head(1)

    #minimo
    jr = jd[(jd['nivel_educativo'] == 'less than high school')]
    jr = jr.sort_values('valor',ascending=True)
    jr = jr.head(1)

    jt = jd[(jd['nivel_educativo'] == 'high school')]
    jt = jt.sort_values('valor',ascending=True)
    jt = jt.head(1)
    ji = jd[(jd['nivel_educativo'] == 'college or trade')]
    ji = ji.sort_values('valor',ascending=True)
    ji = ji.head(1)
    jl = jd[(jd['nivel_educativo'] == 'university')]
    jl = jl.sort_values('valor',ascending=True)
    jl = jl.head(1)

    uo = pd.concat([jn,jm,jk,jo], axis = 0).reset_index()
    uo=uo.drop(['index'], axis=1)
    nue=pd.concat([jr, jt, ji, jl], axis =0).reset_index()
    final = pd.merge(uo, nue, how = 'left', on = 'nivel_educativo').drop(['index'], axis=1)
    final= final.drop(['geografia_y'], axis=1).rename(columns={'geografia_x':'geografia','valor_x':'valor_max', 'valor_y':'valor_min'})
    final=final.drop(['geografia'], axis=1)
    final[['valor_min','valor_max']]=final[['valor_min','valor_max']].astype('string')
    final[['valor_min','valor_max']] = final[['valor_min','valor_max']].apply(lambda x: x[:]+'%' )
    #final=final.rename(columns={'nivel_educativo':'Nivel Educativo','valor_min':'Valor mínimo','valor_max':'Valor máximo'})


    img2 = Image.open("Educ.png") 
      
    c2.image(img2, width=600) 

    fig = go.Figure(data=[go.Table(
    header =dict(values=list(final.columns),
    fill_color ='orange',
    line_color ='black'),

    cells =dict(values=[final.nivel_educativo, final.valor_max, final.valor_min],
    fill_color ='white',
    line_color ='black'))])
                         
    fig.update_layout(width =500, height = 350)

    c1.write(fig)
    
    c1.markdown(get_table_download_link(final), unsafe_allow_html=True)

#----------------------------
c1,c2=st.columns((2,1))
c1.markdown("<h3 style ='text-align: center; color: black;'>¿Cuál es la correlación de la oferta de empleo y el pib anual?</h3>", unsafe_allow_html =True)

pib_def1 = pib_def.copy()

pib_def1= pib_def1[['fecha','unidad de medida','valor']]

empleo_clase2 = empleoclase_def.copy()
empleo_clase2 = empleo_clase2[empleo_clase2['clase de trabajador']=='Total employment']
empleo_clase2 = empleo_clase2[empleo_clase2['geografia']=='Total, Ontario regions']
empleo_clase2= empleo_clase2[['fecha','valor']]

correlacion =pd.merge(empleo_clase2, pib_def1, how = 'left', on = 'fecha')
correlacion.columns=['fecha','valor','unidad de medida','monto']

#Gráfica
fig = px.scatter(correlacion, x = 'valor', y ='monto', size = 'valor')

#Atributos
fig.update_layout(
    xaxis_title = '<b>Oferta de empleo<b>',
    yaxis_title = '<b>PIB anual<b>',
    template = 'simple_white',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    title_x = 0.5)

c1.plotly_chart(fig)

c2.markdown("<h3 style ='text-align: center; color: black;'>Correlación entre el PIB y el empleo</h3>", unsafe_allow_html =True)
# valor de la correlacion
valor_corr=round(correlacion['monto'].corr(correlacion['valor'])*100,3)

c2.markdown("<h3 style ='text-align: center; color: blue;'>98.808%</h3>", unsafe_allow_html =True)

c2.markdown("<h3 style ='text-align: center; color: blue;'>                                  </h3>", unsafe_allow_html =True)
c2.markdown("<h3 style ='text-align: center; color: blue;'>                                  </h3>", unsafe_allow_html =True)


empleo_clase1= empleoclase_def.copy()
empleo_clase1= empleo_clase1[empleo_clase1['clase de trabajador']=='Total employment']
empleo_clase1= empleo_clase1[empleo_clase1['geografia']=='Total, Ontario regions']
empleo_clase1 = empleo_clase1[(empleo_clase1['fecha']==2001) | (empleoclase_def['fecha']==2015)].reset_index().drop('index', axis=1)

c2.markdown("<h3 style ='text-align: center; color: black;'>Variacion del empleo en el 2015 con respecto al 2001</h3>", unsafe_allow_html =True)

#valor de la variacion del empleo
variacion = round(((empleo_clase1['valor'][1] - empleo_clase1['valor'][0])/empleo_clase1['valor'][1])*100,1)

c2.markdown("<h3 style ='text-align: center; color: blue;'>14.5%</h3>", unsafe_allow_html =True)