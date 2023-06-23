#__________________________VERSION DE PYTHON: 3__________________________________
import tkinter as tk   #libreria grafica
from tkinter import filedialog   
import tkinter.simpledialog as sd   
import time as t                    #libreria de tiempo
import datetime as dt               #libreria de fecha
import locale                       
from tkinter import messagebox    
from tkinter import ttk
import numpy as np                 #libreria para arrays      Nota: hay que instalarla    pip install numpy
from PIL import ImageTk, Image    #libreria para imagenes     Nota: hay que instalarla    pip install pillow
import os

#_____________________________INICIALIZACION DE VARIABLES______________________________

locale.setlocale(locale.LC_TIME, 'es_ES')   #cambia el idioma local (para la fecha)
ventana = tk.Tk()                           #crea una ventana
cont = 0                                    #contador que almacena la cantidad de lineas de la caja de texto ocupadas

icono = tk.PhotoImage(file="icono/CHMaquina.png")  # Carga la imagen
ventana.iconphoto(True, icono)                    #coloca la imagen de icono
ventana.title("CHMaquina")                     #le coloca un titulo a la ventana
ventana.geometry("300x200")                 # Define las dimensiones de la ventana 
acumulador=0                                #acumulador del programa
programas = 0                               #cuenta la cantidad de programas
contenido=""                                #variable temporal que almacena el contenido de los archivos
valor_kernel = 39                           #valor por defecto del kernel
cont_velocidad = 0                          #contador que guardara los valores de velocidad dados por el usuario
paso = tk.BooleanVar()                      # Variable booleana  de tkinter
parar= tk.BooleanVar()                      # Variable booleana  de tkinter
principal={}                                #diccionario donde se almacena informacion de los programas
my_array = np.empty(80, dtype='U90')        #declaracion del array en numpy con espacio por defecto
my_array[0]=0                               # inicializacion del acumulador en el array



"""
Rellena el array con sistema operativo 39
veces  que  es el valor por defecto del Kernel
"""
for i in range(1,40):
    my_array[i] = "Sistema Operativo"
    
    
  
#Creacion de la tabla para mostrar el mapa de memoria
table = ttk.Treeview(ventana, columns=('col1', 'col2'), show='headings')
scrollbar2 = ttk.Scrollbar(ventana, orient='vertical', command=table.yview)  #creacion del scroll para la tabla para navegar por ella
table.configure(yscrollcommand=scrollbar2.set) 
    
    
#________________________ FUNCIONES HELPERS_______________________

"""
Al cambiar el valor de la memoria
se llama esta funcion la cual llama 
el array principal de los programas y le asigna
el espacio dado por el usuario
"""
def memoria_funcion()->None:
    global my_array
    valor = int(memoria.get())  
    my_array.resize(valor, refcheck=False)  # le asigna el valor dado por el usuario a el espacio del array
    
    
""" 
Al cambiar el valor del kernel
se llama esta funcion la cual a travez 
de un for rellena el array la cantidad de veces que el 
usuario puso, con el string Sistema Operativo
"""
def kernel_funcion()-> None:
    global my_array  
    global valor_kernel
    valor = int(kernel.get())  
    valor_kernel = valor
    for i in range(1,valor +1):
        my_array[i] = "Sistema Operativo"
 
 
"""
Al cambiar el valor de la velocidad
se llama esta funcion la cual asigna el
valor pasado por el usuario a cont_velocidad
"""   
def velocidad_funcion(val : str) -> None:
    global cont_velocidad   # variable global de velocidad 
    cont_velocidad = val
   
   
"""
recibe un array el cual recorre con un for
y va contando en cada iteracion excluyendo a las
posiciones del array que contengan ''
retorna un entero
"""   
def lenght(array)-> int:
    count = 0
    for i in array:
        if i != '':
            count += 1
    return count


"""
string : recibe un valor en string de una variable del programa
tipo: recibe un char del tipo de variable que se trata
retorna: True o False si el valor si o no corresponde al tipo de
variable
"""
def tipo_valor(string : str, tipo : chr) -> bool:
    if ("I" in tipo) or ("R" in tipo):
        try:
            entero = int(string)
            return True
        except:
            return False
    elif "C" in tipo:
        return True
    elif "L" in tipo:
        if string == "1" or string == "0":
            return True
        else:
            return False
    else:
        return False



"""
key: es un string que seria el nombre de la variable
num_pro: es un entero el cual es el ID del programa
retorna: un booleano el cual indica si key se encuentra
en el diccionario variables
"""
def cargar_variable(key : str, num_pro :  int)-> bool:
    if key in principal[num_pro]["variables"]:
        return  True
    else:
        return False
    
    

"""
key: es un string que seria el nombre de la etiqueta
num_pro: es un entero el cual es el ID del programa
retorna: un booleano el cual indica si key se encuentra
en el diccionario etiquetas
"""   
def cargar_etiqueta(key: str,num_pro : int)-> bool:
    if key in principal[num_pro]["etiquetas"]:
        return  True
    else:
        return False
  
  
  
"""
No recibe ningun parametro
Cambia el valor de parar por el
contrario del que tenia
"""  
def parar_funcion()->None:
    global parar
    parar.set(not parar.get())



"""
No recibe ningun parametro
Cambia el valor de paso por el
contrario del que tenia
""" 
def paso_a_paso()->None:
    global paso
    paso.set(not paso.get())




"""
No recibe ningun parametro
con un for rellena la tabla de muestre memoria
"""
def muestre_memoria()->None:
    global my_array  
    table.delete(*table.get_children())
    # Configurar las columnas
    table.heading('col1', text='Direc')
    table.heading('col2', text='Contenido')
    table.column('col1', width=50)
    table.column('col2', width=150)
    cont = 0
    for i in my_array:
        table.insert('', index='end', values=(f'{str(cont).zfill(4)}', i))
        cont+=1
    table.update()

    table.place(x=1130, y=50, height=500)
    scrollbar2.place(x=1332, y=50, height=500)




"""
string: string
retorna: un string con __ en la cantidad 
indicada para conservar el orden
"""
def estilo_(string : str) -> str:
    tamaño = len(string)
    resultado = ""
    for i in range(1, (19-tamaño)+1):
        resultado += "_"
    return resultado



#__________________________IMAGENES_______________________


#Muestra en la ventana principal la imagen del computador
imagen = Image.open("icono/Compuatdor.png")
imagen = imagen.resize((300, 200), Image.LANCZOS) # le da tamaño a la imagen
imagen_tk = ImageTk.PhotoImage(imagen)
label_imagen = tk.Label(ventana, image=imagen_tk)
label_imagen.place(y="0", x="550")



#Muestra en la ventana principal la imagen de la torre
imagen_Torre = Image.open("icono/Torre.png")
imagen_Torre = imagen_Torre.rotate(360) #rota la imagen 360°
imagen_Torre= imagen_Torre.resize((370, 100), Image.LANCZOS)
imagen_Torre_tk = ImageTk.PhotoImage(imagen_Torre)
label_imagen_Torre = tk.Label(ventana, image=imagen_Torre_tk)
label_imagen_Torre.place(y="260", x="520")



#Muestra en la ventana principal la imagen de la impresora
imagen_Impresora = Image.open("icono/Impresora.png")
imagen_Impresora = imagen_Impresora.rotate(360)
imagen_Impresora= imagen_Impresora.resize((300, 230), Image.LANCZOS)
imagen_Impresora_tk = ImageTk.PhotoImage(imagen_Impresora)
label_imagen_Impresora = tk.Label(ventana, image=imagen_Impresora_tk)
label_imagen_Impresora.place(y="360", x="540")



#Muestra en la ventana principal la imagen en blanco de la torre
imagen_blanco = Image.open("icono/Blanco.png")
imagen_blanco = imagen_blanco.resize((111, 87), Image.LANCZOS)
imagen_blanco_tk = ImageTk.PhotoImage(imagen_blanco)
label_imagen_blanco = tk.Label(ventana, image=imagen_blanco_tk)
label_imagen_blanco.place(y="275", x="525")



#Muestra el cuadro de texto de la pantalla 
cuadro_texto = tk.Text(ventana,background="#1E1E1E", foreground="white")
cuadro_texto.place(width=275, height=137, y="10", x="564")
scrollbar_computador = tk.Scrollbar(ventana)
scrollbar_computador.config(command=cuadro_texto.yview)
scrollbar_computador.place(height="136",width=7,y="10", x="840")



#Muestra el cuadro de texto de la impresora
cuadro_texto_impresora = tk.Text(ventana)
cuadro_texto_impresora.place(width=140, height=135, y="530", x="610")
scrollbar_impresora = tk.Scrollbar(ventana)
scrollbar_impresora.config(command=cuadro_texto_impresora.yview)
scrollbar_impresora.place(height="135",width=7,y="530", x="750")



#Muestra un escrito con la palabra del acumulador
acumulador_label = tk.Label(ventana, text= "Acumulador", font=("Arial", 11,"bold"), background="white")
acumulador_label.place(y="280", x="655")
#Muestra una caja de texto 
texto_acumulador = tk.Text(ventana, height=8, width=30)
texto_acumulador.place(y="280", x="745", height=24, width=130)



#Muestra un escrito con la palabra PC
pc = tk.Label(ventana, text= "PC", font=("Arial", 11), background="white")
pc.place(y="330", x="655")
#Muestra una caja de texto 
texto_pc = tk.Text(ventana, height=8, width=30)
texto_pc.place(y="330", x="680", height=23, width=193)



#Muestra una caja de texto
memoria_texto = tk.Label(ventana, text= "Memoria", font=("Arial", 11,"bold"), background="white", fg="#0404B4")
memoria_texto.place(y="305", x="525")


#Muestra una caja de texto
modo_texto = tk.Label(ventana, text= "Modo Kernel", font=("Arial", 13,"bold"), fg="#088A08")
modo_texto.place(y="220", x="650")


#Muestra una caja de texto
kernel_texto = tk.Label(ventana, text= "Kernel", font=("Arial", 11,"bold"), background="white", fg="#088A08")
kernel_texto.place(y="330", x="525")


#Muestra una caja de texto
texto = tk.Text(ventana, background="gray")
texto_variables = tk.Text(ventana, background="gray")
texto_etiquetas = tk.Text(ventana, background="gray")
texto_programas = tk.Text(ventana, background="gray")
scrollbar = tk.Scrollbar(ventana)
#Muestra un caja scroll para la caja de texto
scrollbar.config(command=texto.yview)



#____________________FOOTER___________________


# Crear el marco del footer
footer_frame = tk.Frame(ventana, bg="#E8E7E7")
footer_defecto = tk.Label(footer_frame, text=f'No hay programa actualmente cargado')
footer_defecto.pack()


def correr_archivo():
    global principal
    global acumulador
    global cont_velocidad
    global valor_kernel
    global programas
    global paso
    global parar
    inicio=0
    final=0
    modo_texto.config(text="Modo Usuario") #cambia el escrito de Modo Kernel
    if lenght(my_array) == 1 + valor_kernel:  # evalua si no se ha cargado ningun programa
        messagebox.showinfo("Error!","No se cargo ningun programa")
    else:
        respuesta = True     #varaible booleana que cambia cuando el usuario no quiere seguir con la ejecucion
        for i in range(0, programas ): # recorre de 0 a la cantidad de programas que hayan
            inicio = principal[i]["inicio"]
            final = principal[i]["final_total"]
            cuadro_texto.insert(tk.END,f'\n{principal[i]["direccion"]}\n') #pone en el cuadro de texto del computador
                                                                        #la direccion de este
            nombre_archivo = tk.Label(ventana, text= f'{principal[i]["nombre"]}.ch', font=("Arial", 9,"bold"), fg="white", bg="#1D09F3")
            nombre_archivo.place(y="306", x="660")
            if i > 0: #no va aparecer el anuncio hasta que pase al segundo programa
                respuesta = messagebox.askokcancel("Programa", "Desea seguir cargando el siguiente programa?")
            if principal[i]["contador_errores"] == 0 and respuesta:
                
                while inicio <= final:  #correr de cierta posicion en el array  inicio fin diccionario
                    k = my_array[inicio]
                    print(k)
                    print(acumulador)
                    if "//" in k:
                        pass
                    else:
                        t.sleep(float(cont_velocidad))  #duerme el programa con el valor de velocidad pasado por el usuario
                        texto_acumulador.delete('1.0', tk.END) #elimina el texto del acumulador
                        texto_acumulador.insert(tk.END, str(acumulador)) #agrega el texto del acumulador
                        texto_pc.delete('1.0', tk.END)  #elimina el texto del PC
                        texto_pc.insert(tk.END, f'{inicio}>{k}') #agrega el texto de las instrucciones al PC
                        if parar.get():      
                            while parar.get(): # ciclo con sleep que se detiene cuando parar sea false
                                t.sleep(1)
                                ventana.update()   #actualiza la ventana
                        elif paso.get():  #mensaje que se muestra cuando paso es true
                            paso.set((messagebox.askokcancel("Programa", "Desea seguir en el modo paso a paso?")))
                                    
                            
                        elif "cargue" in k:
                            lista = k.split()  # divide por espacios a k que es una cadena y se obtiene un array
                            if cargar_variable(lista[1], i): #si la varaible existe en el diccionario
                                try:
                                    acumulador =int(my_array[principal[i]["variables"][lista[1]]["posicion"]])
                                    #le da el valor de la variable al acumulador
                                except:
                                    acumulador =my_array[principal[i]["variables"][lista[1]]["posicion"]]
                            else:
                                principal[i]["contador_errores"] +=1
                                principal[i]["string_errores"] += f"La variable que intenta cargar no existe no invente error linea {inicio} \n"

                        
                        elif "lea" in k:
                            lista = k.split()
                            if cargar_variable(lista[1], i):
                                valor = sd.askstring("Variable", f"Ingrese el valor de {lista[1]} :")
                                my_array[principal[i]["variables"][lista[1]]["posicion"]] = valor
                                #le asigna el valor ingresado por el usuario a la posicion de la variable asignada
                            else:
                                principal[i]["contador_errores"] +=1
                                principal[i]["string_errores"]  += f"La variable que intenta cargar no existe no invente error linea {inicio} \n"
                
                    
            
                        elif "almacene" in k:
                            lista = k.split()
                            if cargar_variable(lista[1], i):
                                my_array[principal[i]["variables"][lista[1]]["posicion"]] = acumulador
                                #le da el valor del acumulador a la varaible
                            else:
                                principal[i]["contador_errores"] +=1
                                principal[i]["string_errores"]  += f"La variable que intenta cargar no existe no invente error linea {inicio} \n"
                
        
                        elif "sume" in k:
                            lista = k.split()
                            tipo = principal[i]["variables"][lista[1]]["tipo"] # carga el tipo de la varaible
                            if  tipo == "I" or tipo == "R": #solo se aceptan este tipo de variables
                                if cargar_variable(lista[1], i):
                                    numero = int(my_array[principal[i]["variables"][lista[1]]["posicion"]])
                                    acumulador += numero
                                else:
                                    principal[i]["contador_errores"] +=1
                                    principal[i]["string_errores"]  += f"La variable que intenta cargar no existe no invente error linea {inicio} \n"
                            else:
                                principal[i]["string_errores"]  += f"El tipo de variable no corresponde con la operacion ¡Error! en la linea {inicio} \n"
            
                        elif "reste" in k:
                            lista = k.split()
                            tipo = principal[i]["variables"][lista[1]]["tipo"]
                            if  tipo == "I" or tipo == "R":
                                if cargar_variable(lista[1], i):
                                    numero = int(my_array[principal[i]["variables"][lista[1]]["posicion"]])
                                    acumulador -= numero
                                else:
                                    principal[i]["contador_errores"] +=1
                                    principal[i]["string_errores"] += f"La variable que intenta cargar no existe no invente error linea {inicio} \n"
                            else:
                                principal[i]["string_errores"]  += f"El tipo de variable no corresponde con la operacion ¡Error! en la linea {inicio} \n"
            
            
                        elif "multiplique" in k:
                            lista = k.split()
                            tipo = principal[i]["variables"][lista[1]]["tipo"]
                            if  tipo == "I" or tipo == "R":
                                if cargar_variable(lista[1], i):
                                    numero = int(my_array[principal[i]["variables"][lista[1]]["posicion"]])
                                    acumulador *= numero
                                else: 
                                    principal[i]["contador_errores"] +=1
                                    principal[i]["string_errores"]  += f"La variable que intenta cargar no existe no invente error linea {inicio} \n"
                            else:
                                principal[i]["string_errores"]  += f"El tipo de variable no corresponde con la operacion ¡Error! en la linea {inicio} \n"
            
            
                        elif "divida" in k:
                            lista = k.split()
                            tipo = principal[i]["variables"][lista[1]]["tipo"]
                            if  tipo == "I" or tipo == "R":
                                if cargar_variable(lista[1], i):
                                    numero = int(my_array[principal[i]["variables"][lista[1]]["posicion"]])
                                    if numero != 0:
                                        acumulador = acumulador/numero
                                    else:
                                        principal[i]["contador_errores"] +=1
                                        principal[i]["string_errores"]  += f"\n Indefinida linea {inicio} \n"
                                else: 
                                    principal[i]["contador_errores"] +=1
                                    principal[i]["string_errores"]  += f"La variable que intenta cargar no existe no invente error linea {inicio} \n"
                            else:
                                principal[i]["string_errores"]  += f"El tipo de variable no corresponde con la operacion ¡Error! en la linea {inicio} \n"
            
                      
                        elif "dividaentera" in k:
                            """
                            Divicion entera de el valor del acumulador por el valor indicado por la 
                            variable señalada por el operando.
                            El divisor deberá ser una cantidad diferente de cero.
                            """
                            lista = k.split()
                            tipo = principal[i]["variables"][lista[1]]["tipo"]
                            if  tipo == "I" or tipo == "R":
                                if cargar_variable(lista[1], i):
                                    numero = int(my_array[principal[i]["variables"][lista[1]]["posicion"]])
                                    if numero != 0:
                                        acumulador = acumulador//numero
                                    else:
                                        principal[i]["contador_errores"] +=1
                                        principal[i]["string_errores"]  += f"\n Indefinida linea {inicio} \n"
                                else: 
                                    principal[i]["contador_errores"] +=1
                                    principal[i]["string_errores"]  += f"La variable que intenta cargar no existe no invente error linea {inicio} \n"
                            else:
                                principal[i]["string_errores"]  += f"El tipo de variable no corresponde con la operacion ¡Error! en la linea {inicio} \n"
            
            
                        elif "potencia" in k:
                            lista = k.split()
                            tipo = principal[i]["variables"][lista[1]]["tipo"]
                            if  tipo == "I" or tipo == "R":
                                if cargar_variable(lista[1], i):
                                    numero = int(my_array[principal[i]["variables"][lista[1]]["posicion"]])
                                    acumulador = acumulador ** numero
                                else: 
                                    principal[i]["contador_errores"] +=1
                                    principal[i]["string_errores"]  += f"La variable que intenta cargar no existe no invente error linea {inicio} \n"
                            else:
                                principal[i]["string_errores"]  += f"El tipo de variable no corresponde con la operacion ¡Error! en la linea {inicio} \n"
            
            
                        elif "modulo" in k:
                            lista = k.split()
                            tipo = principal[i]["variables"][lista[1]]["tipo"]
                            if  tipo == "I" or tipo == "R":
                                if cargar_variable(lista[1], i):
                                    numero = int(my_array[principal[i]["variables"][lista[1]]["posicion"]])
                                    acumulador = acumulador % numero
                                else: 
                                    principal[i]["contador_errores"] +=1
                                    principal[i]["string_errores"]  += f"La variable que intenta cargar no existe no invente error linea {inicio} \n"
                            else:
                                principal[i]["string_errores"]  += f"El tipo de variable no corresponde con la operacion ¡Error! en la linea {inicio} \n"
            

                        
                        
                        elif "concatene" in k:
                            lista = k.split()
                            tipo = principal[i]["variables"][lista[1]]["tipo"]
                            if  tipo == "C":
                                if cargar_variable(lista[1], i):
                                    cadena = str(my_array[principal[i]["variables"][lista[1]]["posicion"]])
                                    acumulador = str(acumulador) + cadena
                                else: 
                                    principal[i]["contador_errores"] +=1
                                    principal[i]["string_errores"]  += f"La variable que intenta cargar no existe no invente error linea {inicio} \n"
                            else:
                                principal[i]["string_errores"]  += f"El tipo de variable no corresponde con la operacion ¡Error! en la linea {inicio} \n"
            
            
                        elif "elimine" in k:
                            lista = k.split()
                            tipo = principal[i]["variables"][lista[1]]["tipo"]
                            if  tipo == "C":
                                if cargar_variable(lista[1], i):
                                    cadena = str(my_array[principal[i]["variables"][lista[1]]["posicion"]])
                                    try:
                                        acumulador = str(acumulador).replace(cadena, "")
                                    except:
                                        principal[i]["contador_errores"] +=1
                                        principal[i]["string_errores"]  += f"La palabra que intenta eliminar no existe en la cadena {inicio} \n"
                                    
                                else: 
                                    principal[i]["contador_errores"] +=1
                                    principal[i]["string_errores"]  += f"La variable que intenta cargar no existe no invente error linea {inicio} \n"
                            else:
                                principal[i]["string_errores"]  += f"El tipo de variable no corresponde con la operacion ¡Error! en la linea {inicio} \n"
            
            
                        elif "extraiga" in k:
                            lista = k.split()
                            try:
                                cantidad_caracteres = int(lista[1])
                                acumulador = str(acumulador)[:cantidad_caracteres]
                            except:
                                principal[i]["contador_errores"] +=1
                                principal[i]["string_errores"]  += f"El valor de la cantidad de caracteres no es de tipo entero {inicio} \n"
                                    
                                
            
                        elif "Y" in k:
                            lista = k.split()
                            tipo = principal[i]["variables"][lista[1]]["tipo"]    
                            tipo_2 = principal[i]["variables"][lista[2]]["tipo"]
                            tipo_3 = principal[i]["variables"][lista[3]]["tipo"]
                            if  tipo == "L" and tipo_2 == "L" and tipo_3 == "L":# las 3 varaibles deben tener tipo L
                                if (cargar_variable(lista[1], i)) and (cargar_variable(lista[2], i)) and (cargar_variable(lista[3], i)):
                                    numero_1 = bool(int(my_array[principal[i]["variables"][lista[1]]["posicion"]]))
                                    numero_2 = bool(int(my_array[principal[i]["variables"][lista[2]]["posicion"]]))
                                    resultado = int(numero_1 and numero_2)
                                    my_array[principal[i]["variables"][lista[3]]["posicion"]] = resultado
                                else: 
                                    principal[i]["contador_errores"] +=1
                                    principal[i]["string_errores"]  += f"La variable que intenta cargar no existe no invente error linea {inicio} \n"
                            else:
                                principal[i]["string_errores"]  += f"El tipo de variable no corresponde con la operacion ¡Error! en la linea {inicio} \n"
            
            
            
                        elif "O" in k:
                            lista = k.split()
                            if "NO" in lista[0]:
                                tipo_2 = principal[i]["variables"][lista[2]]["tipo"]
                                tipo = principal[i]["variables"][lista[1]]["tipo"]
                                if  tipo == "L" and tipo_2=="L":
                                    try:
                                        if (cargar_variable(lista[1], i)) and (cargar_variable(lista[2], i)):
                                            numero_1 = bool(int(my_array[principal[i]["variables"][lista[1]]["posicion"]]))
                                            resultado = int(not numero_1)
                                            my_array[principal[i]["variables"][lista[2]]["posicion"]] = resultado
                                        else: 
                                            principal[i]["contador_errores"] +=1
                                            principal[i]["string_errores"]  += f"La variable que intenta cargar no existe no invente error linea {inicio} \n"
                                    except:
                                        principal[i]["contador_errores"] +=1
                                        principal[i]["string_errores"]  += f"El orden de las variables no es el adecuado {inicio} \n"
                                else:
                                    principal[i]["string_errores"]  += f"El tipo de variable no corresponde con la operacion ¡Error! en la linea {inicio} \n"
                            else:
                                
                                tipo = principal[i]["variables"][lista[1]]["tipo"]
                                tipo_2 = principal[i]["variables"][lista[2]]["tipo"]
                                tipo_3 = principal[i]["variables"][lista[3]]["tipo"]
                                if  tipo == "L" and tipo_2 == "L" and tipo_3 == "L":
                                    if (cargar_variable(lista[1], i)) and (cargar_variable(lista[2], i)) and (cargar_variable(lista[3], i)):
                                        numero_1 = bool(int(my_array[principal[i]["variables"][lista[1]]["posicion"]]))
                                        numero_2 = bool(int(my_array[principal[i]["variables"][lista[2]]["posicion"]]))
                                        resultado = int(numero_1 or numero_2)
                                        my_array[principal[i]["variables"][lista[3]]["posicion"]] = resultado
                                    else: 
                                        principal[i]["contador_errores"] +=1
                                        principal[i]["string_errores"]  += f"La variable que intenta cargar no existe no invente error linea {inicio} \n"
                                else:
                                    principal[i]["string_errores"]  += f"El tipo de variable no corresponde con la operacion ¡Error! en la linea {inicio} \n"
                                
    
            
            
                        elif "muestre" in k:
                            if principal[i]["contador_errores"] == 0:
                                lista = k.split()
                                if lista[1] == "acumulador":
                                    cuadro_texto.insert(tk.END,f'{acumulador}')
                                else:
                                    if cargar_variable(lista[1], i):
                                        mostrar = my_array[principal[i]["variables"][lista[1]]["posicion"]]
                                        cuadro_texto.insert(tk.END,f'{principal[i]["string_errores"]} \n {mostrar}\n ')
                            
                                    else:
                                        principal[i]["contador_errores"] +=1
                                        principal[i]["string_errores"]  += f"La variable que intenta cargar no existe no invente error linea {inicio} \n"
                                        cuadro_texto.insert(tk.END,f'{ principal[i]["string_errores"]}\n')
                            else:
                                principal[i]["contador_errores"] +=1
                                principal[i]["string_errores"]  += "Lo siento no puedo mostrar nada tiene errores\n"
                                cuadro_texto.insert(tk.END,f'{ principal[i]["string_errores"]}\n')
                                
            
                        elif "imprima" in k:
                            if principal[i]["contador_errores"] == 0:
                                lista = k.split()
                                if lista[1] == "acumulador":
                                    cuadro_texto_impresora.insert(tk.END,f'{acumulador}')
                                    #muestra el valor del acumulador en la caja de texto de la impresora
                                else:
                                    if cargar_variable(lista[1], i):
                                        mostrar = my_array[principal[i]["variables"][lista[1]]["posicion"]]
                                        cuadro_texto_impresora.insert(tk.END,f'{mostrar}\n ')
                            
            
                        elif "retorne" in k:
                            #muestra en la caja de texto del monitor la cantidad de errores
                            #y tambien muestra que termino la ejecucion
                            cuadro_texto.insert(tk.END, f'Cantidad de errores:{principal[i]["contador_errores"]}\n')
                            cuadro_texto.insert(tk.END,"Ha terminado la ejecucion del programa")
            
                        elif "vaya" in k:
                            lista = k.split()
                        
                            if "si" in k:
                                if acumulador > 0:
                                    if cargar_etiqueta(lista[1], i): # revisa si la etiqueta se encuentra en el diccionario
                                        inicio =  int(principal[i]["etiquetas"][lista[1]]) -1
                                    else:
                                        principal[i]["contador_errores"] +=1
                                        principal[i]["string_errores"]  += f"La variable que intenta cargar no existe no invente error linea {inicio}"
                                elif acumulador < 0:
                                    if cargar_etiqueta(lista[2], i):
                                        inicio =  int(principal[i]["etiquetas"][lista[2]]) -1
                                    else:
                                        principal[i]["contador_errores"] +=1
                                        principal[i]["string_errores"]  += f"La variable que intenta cargar no existe no invente error linea {inicio}"
                                elif acumulador == 0:
                                    pass
                            else:
                                if cargar_etiqueta(lista[1], i):
                                    inicio =  int(principal[i]["etiquetas"][lista[1]]) -1
                                else:
                                    principal[i]["contador_errores"] +=1
                                    principal[i]["string_errores"]  += f"La variable que intenta cargar no existe no invente error linea {inicio}"
                        
                    inicio += 1
                    my_array[0] = acumulador
                    ventana.update()
            else:
                principal[i]["string_errores"]  += f"Lo siento pero no puedo cargar nada ya que hay un problema en declaracion de variables\n" 
                cuadro_texto.insert(tk.END,f'{principal[i]["string_errores"]}')   
                cuadro_texto.insert(tk.END,f'Ha terminado la ejecucion del programa')     
            
            acumulador = 0
            respuesta = messagebox.askokcancel("Programa", "Desea seguir cargando el siguiente programa?") if i > 1 else False
           #operador ternario cuando i > 0 se muestra el mensaje
            



# Función para cargar el archivo
def cargar_archivo():
    global cont
    global principal
    global programas
    global footer_frame
    archivo = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Archivo de CHMaquina", "*.ch"), ("Todos los archivos", "*.*")])
    # funciona para seleccionar el tipo de archivo
    #obtiene direccion
    nombre = os.path.splitext(os.path.basename(archivo))[0]
    inicio = lenght(my_array)
    num_lineas = 0     #cantidad de lineas del programa sin variables 
    excedente_variables = 0
    if archivo:
        with open(archivo, "r") as f:
            contenido = f.readlines()  #almacena las lineas del archivo
            
        num_lineas = len(contenido)
        for i in contenido:           #busca cuantas variables se declaran ya que son espacios que ocupan
                if "nueva" in i:
                    excedente_variables +=1

    if (len(my_array) - (num_lineas + excedente_variables + lenght(my_array))) > 0:   #para saber si la memoria puede almacenar el programa
        for i in contenido:
            if "\n" in i:
                i= i.split("\n")[0]
            my_array[lenght(my_array)] =i
    else:
        messagebox.showinfo("Error!","No se puede cargar el programa la memoria esta llena")
        return 0 
    footer_defecto.destroy()   #elimina el escrito que tiene el footer al comenzar
    
    #________________________________LLAVES DEL DICCIONARIO____________________________
    
    principal[programas] = {}   #diccionario que tiene como llave programas que es el ID del programa
    principal[programas]["nombre"] = nombre   #crea la llave nombre para el diccionario programas
    principal[programas]["string_errores"] = ""  #crea una llave
    principal[programas]["contador_errores"] = 0 #crea una llave
    principal[programas]["direccion"] = archivo  #crea una llave y le da la direccion del archivo
    principal[programas]["inicio"] = inicio     # crea una llave inicio y le pasa el numero de donde comienza el programa
    variables = {}      #un diccionario llamado variable
    etiquetas = {}      #un diccionario llamado etiquetas
    final = lenght(my_array) -1      #obtiene el final del programa sin variables
    principal[programas]["final_total"] = final  
    
    #_______________________CAJAS DE TEXTO PARA CARGAR EL PROGRAMA____________________
    
    texto.configure(width=50,background="#1E1E1E",yscrollcommand=scrollbar.set, height=80)
    texto_variables.configure(width=50,background="#1E1E1E", height=80, foreground="white")
    texto_etiquetas.configure(width=50,background="#1E1E1E", height=80, foreground="white")
    texto_programas.configure(width=50,background="#1E1E1E", height=80, foreground="white")

    for k in range(principal[programas]["inicio"], lenght(my_array) + 1): # recorre el programa de inicio al final
        i = my_array[k]
        if "//" in i:
            pass
        else:
            if "nueva" in i:   #obtiene las variables si encuentra "nueva"
                lista = i.split()
                if not(lista[1] in variables):  #si la variable no se encuentra ya creada
                    if len(lista) >= 4:
                        valor = i.split(f"{lista[2]} ")[1]
                        if  tipo_valor(valor,lista[2]) :     #si el valor corresponde con el tipo
                            variables[lista[1]] = {}       #crea un diccionario de cada variable    
                            variables[lista[1]]["posicion"] = lenght(my_array)
                            variables[lista[1]]["tipo"] = lista[2]
                            my_array[lenght(my_array)] = i.split(f"{lista[2]} ")[1]
                        else:
                            principal[programas]["contador_errores"] +=1
                            principal[programas]["string_errores"] += f"El valor no corresponde al tipo de variable error en la linea {k} \n"
                    elif len(lista) == 3:
                        if lista[2] == "I" or lista[2] == "R" or lista[2] == "L":  # si entra un tipo de variable  correcto
                            variables[lista[1]] = {}           
                            variables[lista[1]]["posicion"] = lenght(my_array)
                            variables[lista[1]]["tipo"] = lista[2]
                            if lista[2] == "C":
                                my_array[lenght(my_array)] = " "
                            else:
                                my_array[lenght(my_array)] = 0
                        else:
                            principal[programas]["contador_errores"] +=1
                            principal[programas]["string_errores"] += f"El tipo de variable no existe Error linea {k} \n"
                else:
                    principal[programas]["contador_errores"] +=1
                    principal[programas]["string_errores"] += f"Esa variable ya existe Error linea {k} \n"
           
           
            elif "etiqueta" in i:
                lista = i.split()
                if not(lista[1] in etiquetas): #si la variable no se encuentra ya creada
                    linea_etiqueta = principal[programas]["inicio"] + int(lista[-1]) -1
                    #Evalua si la etiqueta esta en el rango correspondiente entre el incio y el final 
                    if linea_etiqueta <= final:
                        etiquetas[lista[1]] = principal[programas]["inicio"] + int(lista[-1]) -1
                    else:
                        principal[programas]["contador_errores"] +=1
                        principal[programas]["string_errores"] += f"No se puede cargar etiqueta {k} \n"
                else:
                    principal[programas]["contador_errores"] +=1
                    principal[programas]["string_errores"] += f"Esa etiqueta ya existe Error linea {k} \n"
                

    
    
    for i in range(principal[programas]["inicio"],final +1):  #Muestra el archivo en la caja de texto
        elemento = my_array[i]
        texto.insert(tk.END, f"{str(i).zfill(4)}  {str(elemento)}\n")
        texto.tag_add(elemento, f"{cont + 1}.5", f"{cont + 1}.99")
        texto.tag_config(elemento, foreground="white")
        texto.tag_add(f"{str(i).zfill(4)}", f"{cont + 1}.0", f"{cont + 1}.4")
        texto.tag_config(f"{str(i).zfill(4)}", foreground="gray")
        cont +=1
        
    if programas == 0:
        texto_variables.insert(tk.END,"Pos        Variables\n")  #muestra las varibales  
        texto_variables.tag_add("Pos        Variables\n", f"1.0", f"1.99")
        texto_variables.tag_config("Pos        Variables\n", foreground="#C586C0")
        
        texto_etiquetas.insert(tk.END,"Pos        Etiquetas\n")  #muestra las etiquetas
        texto_etiquetas.tag_add("Pos        Etiquetas\n", f"1.0", f"1.99")
        texto_etiquetas.tag_config("Pos        Etiquetas\n", foreground="#007acc")
        
        texto_programas.insert(tk.END," ID       Programa           #ins     RB     RLC     RLP\n") #muestra la informacion del programa
        texto_programas.tag_add(" ID       Programa           #ins     RB     RLC     RLP\n", f"1.0", f"1.99")
        texto_programas.tag_config(" ID       Programa           #ins     RB     RLC     RLP\n", foreground="green")
    cant_variables= 0 #cuenta la cantidad de variables
    cant_etiquetas=0  #cuenta la cantidad de etiquetas
    for llave in variables.keys():
        texto_variables.insert(tk.END,f'{str(variables[llave]["posicion"]).zfill(4)}       {str(programas).zfill(4)}{llave}\n')
        #mustra las variables
        cant_variables +=1
    for llave in etiquetas.keys():
        texto_etiquetas.insert(tk.END,f'{str(etiquetas[llave]).zfill(4)}       {str(programas).zfill(4)}{llave}\n')
        #mustra las etiquetas
        cant_etiquetas +=1
   

    principal[programas]["final"] = lenght(my_array)-1 #añade al diccionario el total de instrucciones que posee
    principal[programas]["etiquetas"] = etiquetas      #añade un diccionario de etiquetas 
    principal[programas]["variables"] = variables       #añade un diccionario de variables
    
    
    #mustra la informacion del programa
    texto_programas.insert(tk.END,f'{str(programas).zfill(4)}      {str(principal[programas]["nombre"])}.ch{estilo_(str(principal[programas]["nombre"])+".ch")}{int(principal[programas]["final"])-int(principal[programas]["inicio"]) + 1}       {principal[programas]["inicio"]}      {final}     {principal[programas]["final"]}\n')

    #________________________INFORMACION DEL FOOTER______________________
    fecha_actual = dt.datetime.now().strftime('%A, %d de %B de %Y') #fecha actual con formato
    footer_final = tk.Label(footer_frame, text=f'El chprograma ha compilado con {principal[programas]["contador_errores"]} errores     {fecha_actual}')
    footer_final.place(x = 950)
    footer_completo = tk.Label(footer_frame, text=f'{str(programas).zfill(4)} {str(principal[programas]["direccion"])}   {int(principal[programas]["final"])-int(principal[programas]["inicio"]) + 1} Instrucciones   {cant_variables} Variables   {cant_etiquetas} Etiquetas')
    footer_completo.place(x=0)


    texto.place(x=0, y=50, width=285, height=470) #muestra el texto
    texto_variables.place(x=300, y=50, width=220, height=300) #muestra el texto
    texto_etiquetas.place(x=300, y=350, width=220, height=170)  #muestra el texto
    texto_programas.place(x=0, y=521, width=520, height=120) #muestra el texto
    scrollbar.place(x=285, y=50, width=15, height=470) #muestra el texto
    programas+=1  #aumenta en 1 el ID de los programas
    

#_______________________ENTRADAS DE VALORES__________________________

#Muestra un input para ingresar valores numericos de la memoria
memoria = tk.Spinbox(ventana, from_=3*10 + 50, to=1000*3+ 100, increment=1, command=memoria_funcion) 
memoria.place(y="305", x="600", width= 40 )

#Muestra un input para ingresar valores numericos del kernel
kernel = tk.Spinbox(ventana, from_=10*3 + 9, to=100, increment=1, command=kernel_funcion)
kernel.place(y="332", x="600", width= 40 )


#Muestra un input para ingresar valores numericos de la velocidad
velocidad = tk.Scale(ventana, from_=0.1, to=1.0, orient=tk.HORIZONTAL, background="white" ,command=velocidad_funcion, resolution=0.01)
velocidad.place(y="260", x="524", width= 116)
#Muestra el texto que acompaña al input de velocidad
velocidad_texto = tk.Label(ventana, text= "Velocidad", font=("Arial", 8), background="white", fg="black")
velocidad_texto.place(y="247", x="580")



#______________________________BOTONES______________________________

#Crea la un boton con la palabra archivo y con una imagen
imagen_subir = tk.PhotoImage(file="icono/subir_icono.png")
boton_cargar = tk.Button(ventana, image=imagen_subir, text="Archivo", command=cargar_archivo, compound="left", background="#E8E7E7")
boton_cargar.config(border=0, highlightthickness=0)
boton_cargar.image = imagen_subir
#Muestra el boton
boton_cargar.place(width=80, height=36, x=0, y=0)


#Crea la un boton con la palabra paso a paso y con una imagen
imagen_paso = tk.PhotoImage(file="icono/paso.png")
imagen_paso = imagen_paso.subsample(2, 2)
boton_paso = tk.Button(ventana, image=imagen_paso, text="Paso a paso", command=paso_a_paso, compound="left", background="#E8E7E7")
boton_paso.config(border=0, highlightthickness=0)
boton_paso.image = imagen_paso
#Muestra el boton
boton_paso.place(width=100, height=36, x=280, y=0)


#Crea la un boton con la palabra parar y con una imagen
imagen_parar = tk.PhotoImage(file="icono/icono_parar.png")
boton_parar = tk.Button(ventana, image=imagen_parar, text="Parar", command=parar_funcion, compound="left", background="#E8E7E7")
boton_parar.config(border=0, highlightthickness=0)
boton_parar.image = imagen_parar
#Muestra el boton
boton_parar.place(width=80, height=36, x=380, y=0)


#Crea la un boton con la palabra correr y con una imagen
imagen = tk.PhotoImage(file="icono/run_icono.png")
boton_correr = tk.Button(ventana, image=imagen, text=" Correr", command=correr_archivo, compound="left", background="#E8E7E7")
boton_correr.config(border=0, highlightthickness=0)
boton_correr.image = imagen
#Muestra el boton
boton_correr.place(width=80, height=36, x=80, y=0)


#Crea la un boton con la palabra Mostrar memoria y con una imagen
imagen_tabla = tk.PhotoImage(file="icono/icono_tabla.png")
imagen_tabla = imagen_tabla.subsample(2)
boton_tabla = tk.Button(ventana, image=imagen_tabla, text="Mostrar Memoria", command=muestre_memoria, compound="left", background="#E8E7E7")
boton_tabla.config(border=0, highlightthickness=0)
boton_tabla.image = imagen_tabla
#Muestra el boton
boton_tabla.place(width=120, height=36, x=160, y=0)




#Muestra el footer
footer_frame.pack(side="bottom", fill="x")
# Mostrar la ventana
ventana.mainloop()