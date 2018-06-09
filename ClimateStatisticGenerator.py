#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generado por Jorge Paz. 
Analiza los archivos descargados por downloader03 de ECMWF y genera ncs con estadisticas. 

"""
##########################################################
## 1: importar todas las librerías #######################
##########################################################
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import netCDF4
#from datetime import datetime, timedelta #for writing dates in nc
#import time #for current time record in .nc
import os
rutaGralCarpeta="D:/ClimateStats/" #en esta carpeta se almacena este script y los archivos generados
os.chdir(rutaGralCarpeta)

rutaTempMax="D:/51 temp max"
rutaTempMin="D:/52 temp min"  
rutaPrecipt="D:/228 precipt"

##########################################################
## 2: Funcion para graficar con escala automatica ########
##########################################################

def GraficarDatosBrutos(array,nombreArray,unidades): #MEJORAR: añadir al parentesis lons,lats
   
    ##Get some parameters for the Stereographic Projection
    lon_0 = lons.mean()
    lat_0 = lats.mean()
    
    m = Basemap(resolution=None,projection='cyl',\
                lat_ts=40,lat_0=lat_0,lon_0=lon_0)
        #ajustar width y height manualmente
        #las opciones de basemap están en 
        #https://matplotlib.org/basemap/api/basemap_api.html
    
        # Because our lon and lat variables are 1D,
        # use meshgrid to create 2D arrays
        # Not necessary if coordinates are already in 2D arrays.
    lon, lat = np.meshgrid(lons, lats)
    xi, yi = m(lon, lat)
       
    ##Plot Data
    cs = m.pcolor(xi,yi,np.squeeze(array),cmap=plt.cm.seismic) # primero ejecutar sin definir vmin y vmax y luego AJUSTAR ESCALA!!!!!
        #remplazar "seismic" por el patron de color que más te guste en https://matplotlib.org/examples/color/colormaps_reference.html
        # vmin y vmax determinan los valores maximos de la escala. ver https://stackoverflow.com/questions/3373256/set-colorbar-range-in-matplotlib
    
    ## Add Grid Lines
    m.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=10)
    m.drawmeridians(np.arange(-180., 181., 10.), labels=[0,0,0,1], fontsize=10)
    
    ## Add Coastlines, States, and Country Boundaries
    #m.drawcoastlines()
    #m.drawstates()
    #m.drawcountries()
    #m.drawrivers()
    m.drawlsmask
    #se puede añadir todo esto: 
    #http://basemaptutorial.readthedocs.io/en/latest/backgrounds.html

    ## Add Colorbar
    cbar = m.colorbar(cs, location='right', pad="10%")
    cbar.set_label(unidades)
    
    ## Add Title to graph
    plt.title(nombreArray)
    
    ## Save and show
    plt.savefig(rutaGralCarpeta+nombreArray+'.png',bbox_inches='tight') #añaidr dpi=fig.dpi es para que se vea igual que se guarda. tomoado de https://stackoverflow.com/questions/7906365/matplotlib-savefig-plots-different-from-show
    plt.show()


###################################################################
## 3: funcion para revisar contenido de archivos .nc ##############
###################################################################

def RevisarNC(nombreFichero,nombreVariable): #seria mas elegante pasarle las lons y lats....como no está montado, definirlas antes de lanzar la funcion

    fh = Dataset(rutaGralCarpeta+nombreFichero, mode='r')
    print('Probando a abrir archivo creado con estas caracteristicas')
    #print(fh.variables)
    lons = fh.variables['longitude'][:]
    lats = fh.variables['latitude'][:]
    var = fh.variables[nombreVariable][:]
    var_units = fh.variables[nombreVariable].units
    fh.close() #con esto cerramos el archivo para no dañarlo
    
    GraficarDatosBrutos(np.nanmean(var,axis=0),nombreFichero,var_units) #MEJORAR: pasar a la funcion tambien lons,lats


###################################################################
## 4: funcion volcado a archivo .nc ###############################
###################################################################
# basado en http://www.ceda.ac.uk/static/media/uploads/ncas-reading-2015/11_create_netcdf_python.pdf

def GuardarEnNC(arrayAGuardar,nombreFichero,descripcion,nombreVariable,unidades,lats,lons,timeserie):      

    #creating a NetCDF file
    print ('Inicio creacion archico nc '+nombreFichero+'.nc')
    dataset = Dataset (nombreFichero, 'w',
                       format='NETCDF4_CLASSIC')
    #print ('Generado fichero'+nombreFichero+' con formato '+dataset.file_format)
    #print ('Caracteristicas iniciales:')
    #print (dataset.dimensions)
    #print ('Debe ser un diccionario vacio')
    
    #Create dimensions
    lat = dataset.createDimension('lat', len(lats))
    #print('creada dimension lat : '+str(dataset.dimensions ['lat']))
    lon = dataset.createDimension('lon', len(lons)) 
    #print('creada dimension len : '+str(dataset.dimensions ['lon']))
    time = dataset.createDimension('time', None)
    #print('creada dimension time: '+str(dataset.dimensions ['time'])+'¿Es ilimitada?:'+str(time.isunlimited())) 
    #print('Resumen dimensiones creadas:')
    #print('Nombre Tamaño Ilimitada')
    #for dimname in dataset.dimensions.keys():
    #    dim = dataset.dimensions[dimname]
    #    print (dimname, len(dim), dim.isunlimited())
        
    #Create coordinate variables for N-dimensions
    times = dataset.createVariable('time', np.float64, ('time',))
    latitudes = dataset.createVariable('latitude', np.float32, ('lat',))
    longitudes = dataset.createVariable('longitude', np.float32, ('lon',))
    
    #create the actual N-d variable
    datos = dataset.createVariable(nombreVariable, np.float32, ('time','lat','lon'))
    #print ('creada variable para almacenar datos vacia:', dataset.variables[nombreVariable])
    
    #print('Resumen variables creadas:')
    #print('Nombre Tipo Dimensiones Tamaño')
    #for varname in dataset.variables.keys():
    #    var = dataset.variables[varname]
    #    print (varname, var.dtype, var.dimensions, var.shape)
        
    #Creation of global Attributes
    dataset.description = descripcion
    import time #importar aqui porque si no se lia con variable time en siguiente linea
    dataset.history = 'Created on' + time.ctime(time.time())
    dataset.source = 'Calculated from C3S CDS Seasonal Forecast'
    
    #Variable Attributes
    latitudes.units = 'degree_north'
    longitudes.units = 'degree_east'
    datos.units = unidades
    times.units = 'hours since 0001-01-01 00:00:00'
    times.calendar = 'gregorian'

    #Repaso del archivo
    #print('Características del archivo creado a falta de escribir datos:')    
    #print('Descripcion: '+dataset.description)
    #print('Historia: '+dataset.history)
    #print('Dimensiones: '+str(dataset.dimensions))
    
    #writing data
    latitudes[:] = lats
    longitudes[:] = lons
    #print ('latitudes =\n', latitudes[:])
    #print ('latitudes =\n', latitudes[:])
    
    #growing data along unlimited dimension
    nPasosTiempo=arrayAGuardar.shape[0]
    #print ('data shape before adding data = ', datos.shape)
    datos[0:int(nPasosTiempo),:,:] = arrayAGuardar
    #print ('data shape before adding data =', datos.shape)
    
    # Fill in times.    <-----------------esta pensado para generar una lista de meses. Innecesario
#    dates = []
#  
#    def add_several_month(dt0,nMeses):# Basado en http://code.activestate.com/recipes/577274-subtract-or-add-a-month-to-a-datetimedate-or-datet/
#        dt3=dt0
#        diaDelMes=dt0.day
#        for i in range (nMeses):
#            dt1 = dt0.replace(day=1)
#            dt2 = dt1 + timedelta(days=32)
#            dt3 = dt2.replace(day=diaDelMes)
#            dt0 = dt3
#        return dt3
#    
#    for n in range(datos.shape[0]):
#        dates.append(add_several_month(datetime(2011, 1, 1),n))
#    times[:] = date2num(dates, units = times.units, calendar = times.calendar)
#    #print ('time values (in units %s): ' % times.units + '\n', times[:])

    times[:] = timeserie


    # Close, and it saved.
    dataset.close()


###################################################################
## 5: leer serie temperaturas #####################################
###################################################################

def generarArraysTemperatura(variable,fechaForecast):

    #matrices a cero para ser rellenadas    
    seriepromedio51numbersBruto=np.zeros((215,721,1440), dtype=float) 
    seriemaximo51numbersBruto = np.zeros((215,721,1440), dtype=float) 
    serieminimo51numbersBruto = np.zeros((215,721,1440), dtype=float)
    serietime=[]
    
    #definicion del nombre de la variable dentro del nc
    if variable=='51':
        codigoVariableEnNc='mx2t24'
        ruta=rutaTempMax
    elif variable=='52':
        codigoVariableEnNc='mn2t24'
        ruta=rutaTempMin
    else:
        print('codigoErroneo!!!!!!!')

    #apertura de un unico archivo para capturar lat, lons, time y var_units
    print("Abriendo un primer archivo para analizar el formato")
    fhPrimerArchivo = netCDF4.Dataset(ruta+'/'+'ecmf'+variable+fechaForecast+'step_'+'24'+'.nc', mode='r')
    print(fhPrimerArchivo)
    print(fhPrimerArchivo.dimensions)
    print(fhPrimerArchivo.variables)
    lons = fhPrimerArchivo.variables['longitude'][:]
    lats = fhPrimerArchivo.variables['latitude'][:]
    #varAllNumbers = fh.variables[codigoVariableEnNc][:] #para 51 'mx2t24', para 52 'mn2t24'
    time = fhPrimerArchivo.variables['time'][:]
    number = fhPrimerArchivo.variables['number'][:]
    var_units = fhPrimerArchivo.variables[codigoVariableEnNc].units
    fhPrimerArchivo.close() #con esto cerramos el archivo para no dañarlo
    print ("Lat, lons, time y var_units netCDF Inicial importandos en arrays numpy")
    print ("Por las lats y lons obtenidas, estas indican el punto central de cada celda")

    #bucle que analiza todo
    for i in range(215):
        print ("--Leyendo step "+str(i*24+24)+" Var: "+codigoVariableEnNc)
        fhTemporal = netCDF4.Dataset(ruta+'/'+'ecmf'+variable+fechaForecast+'step_'+str(i*24+24)+'.nc', mode='r')
        varAllNumbersTemporal = fhTemporal.variables[codigoVariableEnNc]
        print(varAllNumbersTemporal)
        time = fhTemporal.variables['time'][:]
        seriepromedio51numbersBruto[i,:,:]=(np.nanmean(varAllNumbersTemporal, axis=1)) 
        seriemaximo51numbersBruto[i,:,:]=(np.nanmax(varAllNumbersTemporal, axis=1))
        serieminimo51numbersBruto[i,:,:]=(np.nanmin(varAllNumbersTemporal, axis=1))
        serietime.append(time)     
        fhTemporal.close()
    
    #from K to C
    if var_units=="K":
        seriepromedio51numbersBruto=seriepromedio51numbersBruto-273.15
        seriemaximo51numbersBruto=seriemaximo51numbersBruto-273.15
        serieminimo51numbersBruto=serieminimo51numbersBruto-273.15
        var_units="C"

    return(seriepromedio51numbersBruto,seriemaximo51numbersBruto,serieminimo51numbersBruto,serietime,lons,lats)

#Generar indicadores de temp Max----------
arrayTempMaxPromedio,arrayTempMaxMax,arrayTempMaxMin,serietime,lons,lats=generarArraysTemperatura('51','2018-05-01')
superpromedioTempMax=np.nanmean(arrayTempMaxPromedio,axis=0)
GraficarDatosBrutos(superpromedioTempMax ,"arrayTempMaxPromedio","C")

GuardarEnNC(arrayTempMaxPromedio,"TempMaxPromedio.nc","TempMaxPromedio","mx2t24","C",lats,lons,serietime)    
RevisarNC("TempMaxPromedio.nc","mx2t24")
GuardarEnNC(arrayTempMaxMax,"TempMaxMax.nc","TempMaxMax","mx2t24","C",lats,lons,serietime)    
RevisarNC("TempMaxMax.nc","mx2t24")
GuardarEnNC(arrayTempMaxMin,"TempMaxMin.nc","TempMaxMin","mx2t24","C",lats,lons,serietime)    
RevisarNC("TempMaxMin.nc","mx2t24")

#Generar indicadores de temp Min----------
arrayTempMinPromedio,arrayTempMinMax,arrayTempMinMin,serietime,lons,lats=generarArraysTemperatura('52','2018-05-01')
superpromedioTempMin=np.nanmean(arrayTempMinPromedio,axis=0)
GraficarDatosBrutos(superpromedioTempMin ,"TempMinPromedio","C")

GuardarEnNC(arrayTempMinPromedio,"TempMinPromedio.nc","TempMinPromedio","mn2t24","C",lats,lons,serietime)    
RevisarNC("TempMinPromedio.nc","mn2t24")
GuardarEnNC(arrayTempMinMax,"TempMinMax.nc","TempMinMax","mn2t24","C",lats,lons,serietime)    
RevisarNC("TempMinMax.nc","mn2t24")
GuardarEnNC(arrayTempMinMin,"TempMinMin.nc","TempMinMin","mn2t24","C",lats,lons,serietime)    
RevisarNC("TempMinMin.nc","mn2t24")

###################################################################
## 6: leer serie precipitacion ####################################
###################################################################

(variable,fechaForecast)=('228','2018-05-01')
i=0

def generarArraysPrecipitacion(variable,fechaForecast):

    #matrices a cero para ser rellenadas    
    seriepromedio51numbersBruto=np.zeros((215,721,1440), dtype=float) 
    seriemaximo51numbersBruto = np.zeros((215,721,1440), dtype=float) 
    serieminimo51numbersBruto = np.zeros((215,721,1440), dtype=float)
    serietime=[]
    serieProbab51numbersBruto = np.zeros((215,721,1440), dtype=float)
    
    #definicion del nombre de la variable dentro del nc
    if variable=='228':
        codigoVariableEnNc='tp'
        ruta=rutaPrecipt
    else: 
        print('codigoErroneo!!!!!!!')

    #apertura de un unico archivo para capturar lat, lons, time y var_units
    print("Abriendo un primer archivo para analizar el formato")
    fhPrimerArchivo = netCDF4.Dataset(ruta+'/'+'ecmf'+variable+fechaForecast+'step_'+'24'+'.nc', mode='r')
    print(fhPrimerArchivo)
    print(fhPrimerArchivo.dimensions)
    print(fhPrimerArchivo.variables)
    lons = fhPrimerArchivo.variables['longitude'][:]
    lats = fhPrimerArchivo.variables['latitude'][:]
    #varAllNumbers = fh.variables[codigoVariableEnNc][:] #para 51 'mx2t24', para 52 'mn2t24'
    time = fhPrimerArchivo.variables['time'][:]
    number = fhPrimerArchivo.variables['number'][:]
    var_units = fhPrimerArchivo.variables[codigoVariableEnNc].units
    fhPrimerArchivo.close() #con esto cerramos el archivo para no dañarlo
    print ("Lat, lons, time y var_units netCDF Inicial importandos en arrays numpy")
    print ("Por las lats y lons obtenidas, estas indican el punto central de cada celda")

    #bucle que analiza todo
    for i in range(215):
        print ("--Leyendo step "+str(i*24+24)+" Var: "+codigoVariableEnNc)
        fhTemporal = netCDF4.Dataset(ruta+'/'+'ecmf'+variable+fechaForecast+'step_'+str(i*24+24)+'.nc', mode='r')
        varAllNumbersTemporal = fhTemporal.variables[codigoVariableEnNc][:]
        fhTemporal.close()
        print(varAllNumbersTemporal)
        if i==0:
            varAllNumbersCorregida = varAllNumbersTemporal
        else:
            fhRestar = netCDF4.Dataset(ruta+'/'+'ecmf'+variable+fechaForecast+'step_'+str(i*24)+'.nc', mode='r')
            varAllNumbersRestar = fhRestar.variables[codigoVariableEnNc][:]
            varAllNumbersCorregida = varAllNumbersTemporal-varAllNumbersRestar
            fhRestar.close()
        print(varAllNumbersCorregida)
        
        seriepromedio51numbersBruto[i,:,:]=(np.nanmean(varAllNumbersCorregida, axis=1)) 
        seriemaximo51numbersBruto[i,:,:]=(np.nanmax(varAllNumbersCorregida, axis=1))
        serieminimo51numbersBruto[i,:,:]=(np.nanmin(varAllNumbersCorregida, axis=1))
        serietime.append(time)          
        
        varAllNumbersSiNo=varAllNumbersCorregida>0.001
        probLluvia=np.mean(varAllNumbersSiNo,axis=1)
        serieProbab51numbersBruto[i,:,:] = probLluvia
        

    #from m to mm
    if var_units=="m":
        seriepromedio51numbersBruto=seriepromedio51numbersBruto*1000
        seriemaximo51numbersBruto=seriemaximo51numbersBruto*1000
        serieminimo51numbersBruto=serieminimo51numbersBruto*1000
        var_units="mm"

    return(seriepromedio51numbersBruto,seriemaximo51numbersBruto,serieminimo51numbersBruto,serietime,lons,lats,serieProbab51numbersBruto)

#Generar indicadores de precipitacion----------
arrayPrecMaxPromedio,arrayPrecMaxMax,arrayPrecMaxMin,serietime,lons,lats,arrayProbLluvia=generarArraysPrecipitacion('228','2018-05-01')
superpromedioPrecMax=np.nanmean(arrayPrecMaxPromedio,axis=0)
GraficarDatosBrutos(superpromedioPrecMax ,"arrayPrecMaxPromedio","mm")

GuardarEnNC(arrayPrecMaxPromedio,"PrecMaxPromedio.nc","PrecMaxPromedio","tp","mm",lats,lons,serietime)    
RevisarNC("PrecMaxPromedio.nc","tp")
GuardarEnNC(arrayPrecMaxMax,"PrecMaxMax.nc","PrecMaxMax","tp","mm",lats,lons,serietime)    
RevisarNC("PrecMaxMax.nc","tp")
GuardarEnNC(arrayPrecMaxMin,"PrecMaxMin.nc","PrecMaxMin","tp","mm",lats,lons,serietime)    
RevisarNC("PrecMaxMin.nc","tp")

GuardarEnNC(arrayProbLluvia,"ProbLluvia.nc","ProbLluvia","pop","%",lats,lons,serietime)    
RevisarNC("ProbLluvia.nc","pop")



