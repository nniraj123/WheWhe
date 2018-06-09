#!/usr/bin/env python
# -*- coding: utf-8 -*-
#https://jolthgs.wordpress.com/2012/02/12/desarrollo-web-con-python-y-web-py-parte-3/
import web
from web import form
print("Importado web.py. Version:",web.__version__)
import numpy as np
import pandas as pd


urls = (
  '/', 'index'
)

plantilla = web.template.render('./templates/')

app = web.application(urls, globals())

myform = form.Form(
  form.Textbox('departureCity', form.notnull, description="Departure city", class_="textEntry",\
  value="3 letters ICAO code", id="cajatext", post="  City where you want to start your travel. It should has an airport", size="15"),
  
  form.Textbox('firstPossibleDepartureDate', form.notnull, description="First possible departure date", class_="textEntry",\
  value="DD/MM/YYYY", id="cajatext", post="  First  day on which you can start your trip ", size="15"),
  
  form.Textbox('lasttPossibleDepartureDate', form.notnull, description="Last possible departure date", class_="textEntry",\
  value="DD/MM/YYYY", id="cajatext", post="  Last day on which you can start your trip: The more flexible you are, the better suggestions we can give you", size="15"),

  form.Textbox('duration', form.notnull, description="Duration", class_="textEntry",\
  value="number of days", id="cajatext", post="  How many days will your trip last?", size="15"),

  form.Textbox('numberOfResults', form.notnull, description="Number of results", class_="textEntry",\
  value="number of results", id="cajatext", post="  How many suggestions do you want to obtain?", size="15"),
  
#  form.Textbox("nombre"),
#  form.Textbox("id1",
#    form.notnull,
#    form.regexp('\d+', 'Debe ser un dígito'),
#    form.Validator('Debe ser más de 5', lambda x:int(x)>5)),
#  form.Textbox("id2",
#    form.notnull,
#    form.regexp('\d+', 'Debe ser un dígito'),
#    form.Validator('Debe ser más de 5', lambda x:int(x)>5)),
#  form.Textarea('observacion'),
#  form.Checkbox('reenviar'),
#  form.Dropdown('prioridad', ['baja', 'media', 'alta'])
  
  )


def Respuesta(ciudadSalida,firstPossibleDepartureDate,lasttPossibleDepartureDate,duration,numberOfResults):
    #return ("Gran exito! Nombre: %s, ID: %s" % (nombreIntroducido, (valor1+valor2)))

    #https://stackoverflow.com/questions/19622407/2d-numpy-array-to-html-table?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
        
    num = np.array([[ "0.33093259",  0.33093259,  0.2076353,   0.06130814,],
                    [ 0.20392888,  0.42653105,  0.33325891,  0.10473969,],
                    [ 0.17038247,  0.19081956,  0.10119709,  0.09032416,],
                    [-0.10606583, -0.13680513, -0.13129103, -0.03684349,],
                    [ 0.20319428,  0.28340985,  0.20994867,  0.11728491,],
                    [ 0.04396872,  0.23703525,  0.09359683,  0.11486036,],
                    [ 0.27801304, -0.05769304, -0.06202813,  0.04722761,],])
    
    num[:,0]=ciudadSalida
    
    days = ['Departure city', 'Departure date', '20 days', '60 days']
    
    prices = ['AAPL', 'ADBE', 'AMD', 'AMZN', 'CRM', 'EXPE', 'FB']
    
    df = pd.DataFrame(num, index=prices, columns=days)
    
    html = df.to_html()
    
    return html

class index:
  #Metodo de llegada
  def GET(self):
    form = myform()
    return plantilla.formulario_2(form)

# Método POST
  def POST(self):
     form = myform()
     if not form.validates():
       return plantilla.formulario_2(form)
     else:
       return Respuesta(form['departureCity'].value,form['firstPossibleDepartureDate'].value,form['lasttPossibleDepartureDate'].value,form['duration'].value,form['numberOfResults'].value)

if __name__ == "__main__":
    app.run()
