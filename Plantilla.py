# !/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk 
import tkinter.ttk as ttk
from tkinter import messagebox as mssg
import sqlite3
import ctypes #Para las dimennsiones de la Pantalla donde se ejecuta
from os import path #Para la ruta de la base de datos
from datetime import date

class Inventario:
  def __init__(self, master=None):
    crear_base_datos() #Crea la base de datos con sus tablas
    # Para entrega
    # self.path =  r'X:/Users/ferna/Documents/UNal/Alumnos/2023_S2/ProyInventario'
    # self.db_name = self.path + r'\Inventario.db'
    # Para pruebas
    self.path = str(path.dirname(__file__))
    self.db_name = r"" + self.path + r'\Inventario.db'
    # Dimensione de la pantalla
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    self.alto_p = user32.GetSystemMetrics(1)
    ancho = 830 
    alto = self.cambiar_alto(840)
    self.actualiza = False
    self.elimina = False
    # Crea ventana principal
    self.win = tk.Tk() 
    self.win.geometry(f"{ancho}x{alto}")
    self.win.iconbitmap("f2.ico")
    self.win.resizable(False, False)
    self.win.title("Manejo de Proveedores") 

    #Centra la pantalla
    self.centra(self.win,ancho,alto)

    # Contenedor de widgets   
    self.win = tk.LabelFrame(master)
    self.win.configure(background="#e0e0e0",font="{Arial} 12 {bold}",
    height=alto,labelanchor="n",width=ancho)
    self.tabs = ttk.Notebook(self.win)
    self.tabs.configure(height=self.cambiar_alto(800), width=799)

    #Frame de datos
    self.frm1 = ttk.Frame(self.tabs)
    self.frm1.configure(height=self.cambiar_alto(200), width=200)

    #Etiqueta IdNit del Proveedor
    self.lblIdNit = ttk.Label(self.frm1)
    self.lblIdNit.configure(text='Id/Nit', width=6)
    self.lblIdNit.place(anchor="nw", x=10, y=self.cambiar_alto(40))

    #Captura IdNit del Proveedor
    self.idNit = ttk.Entry(self.frm1)
    self.idNit.configure(takefocus=True)
    self.idNit.place(anchor="nw", x=50, y=self.cambiar_alto(40))
    #binds para validaciones de espacio, Backspace y largo
    self.idNit.bind("<BackSpace>", lambda _: self.idNit.delete(len(self.idNit.get())) )
    self.idNit.bind("<space>", self.espacio)
    self.idNit.bind("<KeyPress>", self.validaIdNit)
    self.idNit.focus()

    #Etiqueta razón social del Proveedor
    self.lblRazonSocial = ttk.Label(self.frm1)
    self.lblRazonSocial.configure(text='Razon social', width=12)
    self.lblRazonSocial.place(anchor="nw", x=210, y=self.cambiar_alto(40))

    #Captura razón social del Proveedor
    self.razonSocial = ttk.Entry(self.frm1)
    self.razonSocial.configure(width=36)
    self.razonSocial.place(anchor="nw", x=290, y=self.cambiar_alto(40))
    #binds para validaciones Backspace y largo
    self.razonSocial.bind("<BackSpace>", lambda _: self.razonSocial.delete(len(self.razonSocial.get())) )
    self.razonSocial.bind("<KeyPress>", self.validaRazon)

    #Etiqueta ciudad del Proveedor
    self.lblCiudad = ttk.Label(self.frm1)
    self.lblCiudad.configure(text='Ciudad', width=7)
    self.lblCiudad.place(anchor="nw", x=540, y=self.cambiar_alto(40))

    #Captura ciudad del Proveedor
    self.ciudad = ttk.Entry(self.frm1)
    self.ciudad.configure(width=30)
    self.ciudad.place(anchor="nw", x=590, y=self.cambiar_alto(40))
    #binds para validaciones Backspace y largo
    self.ciudad.bind("<BackSpace>", lambda _: self.ciudad.delete(len(self.ciudad.get())))
    self.ciudad.bind("<KeyPress>", self.validaCiudad)

    #Separador
    self.separador1 = ttk.Separator(self.frm1)
    self.separador1.configure(orient="horizontal")
    self.separador1.place(anchor="nw", width=800, x=0, y=self.cambiar_alto(79))

    #Etiqueta Código del Producto
    self.lblCodigo = ttk.Label(self.frm1)
    self.lblCodigo.configure(text='Código', width=7)
    self.lblCodigo.place(anchor="nw", x=10, y=self.cambiar_alto(120))

    #Captura el código del Producto
    self.codigo = ttk.Entry(self.frm1)
    self.codigo.configure(width=15)
    self.codigo.place(anchor="nw", x=60, y=self.cambiar_alto(120))
    #binds para validaciones de espacio, Backspace y largo
    self.codigo.bind("<space>", self.espacio)
    self.codigo.bind("<BackSpace>", lambda _: self.codigo.delete(len(self.codigo.get())))
    self.codigo.bind("<KeyPress>", self.validaCodigo)

    #Etiqueta descripción del Producto
    self.lblDescripcion = ttk.Label(self.frm1)
    self.lblDescripcion.configure(text='Descripción', width=11)
    self.lblDescripcion.place(anchor="nw", x=220, y=self.cambiar_alto(120))

    #Captura la descripción del Producto
    self.descripcion = ttk.Entry(self.frm1)
    self.descripcion.configure(width=36)
    self.descripcion.place(anchor="nw", x=290, y=self.cambiar_alto(120))
    #binds para validaciones Backspace y largo
    self.descripcion.bind("<BackSpace>", lambda _: self.descripcion.delete(len(self.descripcion.get())))
    self.descripcion.bind("<KeyPress>", self.validaDescrip)

    #Etiqueta unidad o medida del Producto
    self.lblUnd = ttk.Label(self.frm1)
    self.lblUnd.configure(text='Unidad', width=7)
    self.lblUnd.place(anchor="nw", x=540, y=self.cambiar_alto(120))

    #Captura la unidad o medida del Producto
    self.unidad = ttk.Entry(self.frm1)
    self.unidad.configure(width=10)
    self.unidad.place(anchor="nw", x=590, y=self.cambiar_alto(120))
    #binds para validaciones Backspace y largo
    self.unidad.bind("<BackSpace>", lambda _: self.unidad.delete(len(self.unidad.get())))
    self.unidad.bind("<KeyPress>", self.validaUnidad)

    #Etiqueta cantidad del Producto
    self.lblCantidad = ttk.Label(self.frm1)
    self.lblCantidad.configure(text='Cantidad', width=8)
    self.lblCantidad.place(anchor="nw", x=10, y=self.cambiar_alto(170))

    #Captura la cantidad del Producto
    self.cantidad = ttk.Entry(self.frm1)
    self.cantidad.configure(width=12)
    self.cantidad.place(anchor="nw", x=70, y=self.cambiar_alto(170))
    #validacion de cantidad
    self.cantidad.bind("<KeyRelease>", self.validaCtdad)

    #Etiqueta precio del Producto
    self.lblPrecio = ttk.Label(self.frm1)
    self.lblPrecio.configure(text='Precio $', width=8)
    self.lblPrecio.place(anchor="nw", x=170, y=self.cambiar_alto(170))

    #Captura el precio del Producto
    self.precio = ttk.Entry(self.frm1)
    self.precio.configure(width=15)
    self.precio.place(anchor="nw", x=220, y=self.cambiar_alto(170))
    #Validacion de precio
    self.precio.bind("<KeyRelease>", self.validaPrecio)

    #Etiqueta fecha de compra del Producto
    self.lblFecha = ttk.Label(self.frm1)
    self.lblFecha.configure(text='Fecha', width=6)
    self.lblFecha.place(anchor="nw", x=350, y=self.cambiar_alto(170))

    #Captura la fecha de compra del Producto
    self.fecha = ttk.Entry(self.frm1)
    self.fecha.configure(width=14,foreground='grey')
    self.fecha.place(anchor="nw", x=390, y=self.cambiar_alto(170))
    #Validacion de fecha
    self.fecha.bind("<KeyPress>", self.valida_Fecha)
    self.fecha.bind("<BackSpace>", lambda _:self.fecha.delete(tk.END))  # Permite borrar

    #Mostrar formato
    self.fecha.insert(0, 'DD/MM/AAAA')
    self.fecha.bind("<FocusIn>", self.formato)
    self.fecha.bind("<FocusOut>", self.formato)

    #Separador
    self.separador2 = ttk.Separator(self.frm1)
    self.separador2.configure(orient="horizontal")
    self.separador2.place(anchor="nw", width=800, x=0, y=self.cambiar_alto(220))

    #tablaTreeView
    self.style=ttk.Style()
    self.style.configure("estilo.Treeview", highlightthickness=0, bd=0, background="#e0e0e0", font=('Calibri Light',10))
    self.style.configure("estilo.Treeview.Heading", background='Azure', font=('Calibri Light', 10,'bold')) 
    self.style.layout("estilo.Treeview", [('estilo.Treeview.treearea', {'sticky': 'nswe'})])
    
    #Árbol para mosrtar los datos de la B.D.
    self.treeProductos = ttk.Treeview(self.frm1, style="estilo.Treeview")
    
    self.treeProductos.configure(selectmode="extended")

    #Bind del treeview para insertar seleccion a los campos

    self.treeProductos.bind("<<TreeviewSelect>>", self.click) 

    # Etiquetas de las columnas para el TreeView

    self.treeProductos["columns"]=("Codigo","Descripcion","Und","Cantidad","Precio","Fecha")

    #Quitar resizable de las columnas treeview
    def prevent_resize(event):
      if self.treeProductos.identify_region(event.x, event.y) == "separator":
        return "break"
      
    self.treeProductos.bind('<Button-1>', prevent_resize)
    self.treeProductos.bind('<Motion>', prevent_resize)

    # Características de las columnas del árbol

    self.treeProductos.column ("#0",          anchor="w",stretch=True,width=42)
    self.treeProductos.column ("Codigo",      anchor="w",stretch=True,width=3)
    self.treeProductos.column ("Descripcion", anchor="w",stretch=True,width=150)
    self.treeProductos.column ("Und",         anchor="w",stretch=True,width=3)
    self.treeProductos.column ("Cantidad",    anchor="w",stretch=True,width=3)
    self.treeProductos.column ("Precio",      anchor="w",stretch=True,width=8)
    self.treeProductos.column ("Fecha",       anchor="w",stretch=True,width=3)

    # Etiquetas de columnas con los nombres que se mostrarán por cada columna

    self.treeProductos.heading("#0",          anchor="center", text='ID / Nit')
    self.treeProductos.heading("Codigo",      anchor="center", text='Código')
    self.treeProductos.heading("Descripcion", anchor="center", text='Descripción')
    self.treeProductos.heading("Und",         anchor="center", text='Unidad')
    self.treeProductos.heading("Cantidad",    anchor="center", text='Cantidad')
    self.treeProductos.heading("Precio",      anchor="center", text='Precio')
    self.treeProductos.heading("Fecha",       anchor="center", text='Fecha')

    #Carga los datos en treeProductos

    self.treeProductos.place(anchor="nw", height=self.cambiar_alto(560), width=790, x=2, y=self.cambiar_alto(230))

    #Scrollbar en el eje Y de treeProductos

    self.scrollbary=ttk.Scrollbar(self.treeProductos, orient='vertical', command=self.treeProductos.yview)
    self.treeProductos.configure(yscroll=self.scrollbary.set)
    self.scrollbary.place(x=778, y=self.cambiar_alto(25), height=self.cambiar_alto(478))

    # Título de la pestaña Ingreso de Datos

    self.frm1.pack(side="top")
    self.tabs.add(self.frm1, compound="center", text='Ingreso de datos')
    self.tabs.pack(side="top")

    #Frame 2 para contener los botones

    self.frm2 = ttk.Frame(self.win)
    self.frm2.configure(height=self.cambiar_alto(100), width=800)

    #Botón para Buscar un Proveedor

    self.btnBuscar = ttk.Button(self.frm2)
    self.btnBuscar.configure(text='Buscar', command=self.buscar)
    self.btnBuscar.place(anchor="nw", width=70, x=200, y=10)

    #Botón para Guardar los datos
    self.btnGrabar = ttk.Button(self.frm2)
    self.btnGrabar.configure(text='Grabar',command=self.adiciona_Registro)
    self.btnGrabar.place(anchor="nw", width=70, x=275, y=10)

    #Botón para Editar los datos
    self.btnEditar = ttk.Button(self.frm2)
    self.btnEditar.configure(text='Editar',command = self.edita)
    self.btnEditar.place(anchor="nw", width=70, x=350, y=10)

    #Botón para Elimnar datos
    self.btnEliminar = ttk.Button(self.frm2)
    self.btnEliminar.configure(text='Eliminar',command=self.eliminaRegistro)
    self.btnEliminar.place(anchor="nw", width=70, x=425, y=10)

    #Botón para cancelar una operación
    self.btnCancelar = ttk.Button(self.frm2)
    self.btnCancelar.configure(text='Cancelar', width=80,command = self.cancelar)
    self.btnCancelar.place(anchor="nw", width=70, x=500, y=10)

    #Ubicación del Frame 2
    self.frm2.place(anchor="nw", height=60, relwidth=1, y=self.cambiar_alto(755))
    self.win.pack(anchor="center", side="top")

    # widget Principal del sistema
    self.mainwindow = self.win



    self.ventana= tk.Toplevel()
    self.ventana.withdraw()
    ancho=410
    alto=155
    self.ventana.resizable(False,False)
    self.ventana.overrideredirect(True)#Quita los controles superiores
    self.ventana.title("Manejo de Proveedores")
    self.selection=tk.IntVar()
    op1=tk.Radiobutton(self.ventana,text='''Eliminar el producto de todos los proveedores ''', variable=self.selection, value=1,font=('Calibri Light',11),padx=10)
    op1.pack(anchor='nw',pady=5)
    op2=tk.Radiobutton(self.ventana,text='''Eliminar el producto del proveedor seleccionado ''', variable=self.selection, value=2,font=('Calibri Light',11),padx=10)
    op2.pack(anchor='nw')
    op3=tk.Radiobutton(self.ventana,text='''Eliminar el proveedor seleccionado con todos sus productos''', variable=self.selection, value=3,font=('Calibri Light',11),padx=10)
    op3.pack(anchor='nw',pady=5)
    aceptar = ttk.Button(self.ventana,text='Aceptar',width=10,command=self.acepta)
    aceptar.pack(anchor='s',pady=5)
  def acepta(self):
      query = f'''DELETE from Proveedores Where IdNitProv = {self.idNit.get()}'''
      query_0=f'''DELETE from Productos Where IdNit = '{self.idNit.get()}' '''
      query_1=f'''DELETE from Productos Where Codigo = '{self.codigo.get()}' '''
      query_2=f'''DELETE from Productos Where Codigo = '{self.codigo.get()}' and IdNit = '{self.idNit.get()}' '''
      if self.selection.get() == 1:
        self.ventana.withdraw()
        self.run_Query(query_1)
        self.cancelar()
        self.limpiaCampos()
        self.limpia_treeView()
        mssg.showinfo('Eliminado','Producto eliminado exitosamente')
      elif self.selection.get()==2:
         self.ventana.withdraw()
         self.run_Query(query_2)
         self.cancelar()
         self.limpiaCampos()
         self.limpia_treeView()
         mssg.showinfo('Eliminado','Producto eliminado exitosamente del proveedor')
      elif self.selection.get()==3:
         self.ventana.withdraw()
         self.run_Query(query)
         self.run_Query(query_0)
         self.cancelar()
         self.limpiaCampos()
         self.limpia_treeView()
         mssg.showinfo('Eliminado','Proveedor eliminado exitosamente con sus productos')

  def cambiar_alto(self, altura):
     nuevo_alto = int((altura / 1080) * self.alto_p)
     return nuevo_alto

  #Fución de manejo de eventos del sistema
  def run(self):
      item_Pv = self.run_Query(''' Select IdNitProv from Proveedores''').fetchall()
      item_Pd = self.run_Query(''' Select Codigo from Productos''').fetchall()
      nulo = True
      for i in item_Pv:
         if i[0] == None:
            mssg.showwarning('Cuidado!','Valor nulo en llave primaria, esto puede generar errores en el funcionamiento del programa.')
            nulo = False
      if nulo == True:
        for j in item_Pd:
          if j[0] == None:
              mssg.showwarning('Cuidado!','Valor nulo en llave primaria, esto puede generar errores en el funcionamiento del programa.')    
      self.mainwindow.mainloop()
  ''' ......... Métodos utilitarios del sistema .............'''
  #Rutina de centrado de pantalla
  def centra(self,win,ancho,alto): 
      """ centra las ventanas en la pantalla """ 
      x = win.winfo_screenwidth() // 2 - ancho // 2 
      y = win.winfo_screenheight() // 3 - alto // 3
      win.geometry(f'{ancho}x{alto}+{x}+{y}') 
      win.deiconify() # Se usa para restaurar la ventana

 # Validaciones del sistema
  def espacio(self,event):
     if event:
        mssg.showerror('Atención!!','.. ¡No se admiten espacios! ..')
        return "break"
  def validaIdNit(self, event):
    ''' Valida que la longitud no sea mayor a 15 caracteres'''
    
    if event:
      if len(self.idNit.get()) > 14:
         mssg.showerror('Atención!!','.. ¡Máximo 15 caracteres! ..')
         return "break"
  def validaCodigo(self, event):
    ''' Valida que la longitud no sea mayor a 15 caracteres'''
    if event:
        if len(self.codigo.get()) > 14:
            mssg.showerror('Atención!!','.. ¡Máximo 15 caracteres! ..')
            return'break'
  def validaRazon (self,event):
     if event:
        if len(self.razonSocial.get()) > 49:
            mssg.showerror('Atención!!','.. ¡Máximo 50 caracteres! ..')
            return 'break'
    
  def validaCiudad (self,event):
     if event:
        if len(self.ciudad.get()) > 14:
            mssg.showerror('Atención!!','.. ¡Máximo 15 caracteres! ..')
            return 'break' #Para cancelar la incersion a nivel de clase ya que el comportamiento es hecho por la clase
  def validaDescrip (self,event):
     if event:
        if len(self.descripcion.get()) > 49:
            mssg.showerror('Atención!!','.. ¡Máximo 50 caracteres! ..')
            return 'break'
  def validaUnidad (self,event):
     if event:
        if len(self.unidad.get()) > 9:
            mssg.showerror('Atención!!','.. ¡Máximo 10 caracteres! ..')
            return 'break'
  def validaCtdad(self,event):
     if event: 
        try:
            float(self.cantidad.get())
        except:
           if self.cantidad.get() != '':
            mssg.showerror('Atención!!','.. ¡Solo caracteres numericos! ..')
            cont = 0
            for i in self.cantidad.get():
              try:
                  int(i)
                  cont +=1
              except ValueError:
               self.cantidad.delete(cont)
        if len(self.cantidad.get()) > 12:
            mssg.showerror('Atención!!','.. ¡Máximo 12 caracteres! ..')
            self.cantidad.delete(12,'end')
  def validaPrecio(self,event):
     if event: 
        try:
            float(self.precio.get())
        except:
           if self.precio.get() != '':
            mssg.showerror('Atención!!','.. ¡Solo caracteres numericos! ..')
            cont = 0
            for i in self.precio.get():
              try:
                  int(i)
                  cont +=1
              except ValueError:
               self.precio.delete(cont)
        if len(self.precio.get()) > 15:
            mssg.showerror('Atención!!','.. ¡Máximo 15 caracteres! ..')
            self.precio.delete(15,'end')
  def valida_Fecha(self, event):
    if event.char.isdigit():
        letras = 0
        for letra in self.fecha.get():
              letras += 1

        if letras == 2:
            self.fecha.insert(2,"/")
        elif letras == 5:
            self.fecha.insert(5,"/")
        elif letras == 10:
            return "break"
    else:
      return "break"
  def valida_Fecha_Final (self):
      today = date.today()
      try:
        nDia, nMes, nAño = (int (i) for i in str(self.fecha.get()).split('/'))
        if (nDia in range(1, 32) and nMes in range (1,13) and nAño >= 2000): #revisa que el mes los dias y los años existan
          if nAño % 4 !=0 or nAño % 400 !=0 and nAño % 100 == 0:
              #Bisiesto = False
              if ( nDia >= 29 and nMes == 2) or ((nMes == 4 or nMes == 6 or nMes == 9 or nMes == 11) and nDia == 31):
                mssg.showerror('Atención!!','.. ¡La fecha ingreasada no existe! ..')
                return False
              else:
                    fecha_Ingresada = date(nAño, nMes, nDia)
                    if fecha_Ingresada > today: # comprueba que la fecha no sea mayor que hoy
                        mssg.showerror('Atención!!','.. ¡La fecha ingreasada no puede ser mayor que la actual! ..')
                        return False
                    else:
                      if nDia < 10 and nMes < 10:
                          return True,(f"0{nDia}/0{nMes}/{nAño}")
                      elif nDia < 10 and nMes >=10:
                        return True,(f"0{nDia}/{nMes}/{nAño}")
                      elif nDia >= 10 and nMes <10: 
                        return True,(f"{nDia}/0{nMes}/{nAño}")
                      else:
                        return True,(f"{nDia}/{nMes}/{nAño}")
          else:
              #Bisiesto = True
              if (nDia > 29 and nMes == 2) or ((nMes == 4 or nMes == 6 or nMes == 9 or nMes == 11) and nDia == 31):
                mssg.showerror('Atención!!','.. ¡La fecha ingreasada no existe! ..')
                return False
              else:
                    fecha_Ingresada = date(nAño, nMes, nDia)
                    if fecha_Ingresada > today: # comprueba que la fecha no sea mayor que hoy
                        mssg.showerror('Atención!!','.. ¡La fecha ingreasada no existe! ..')
                        
                        return False
                    else:
                      if nDia < 10 and nMes < 10:
                          return True,(f"0{nDia}/0{nMes}/{nAño}")
                      elif nDia < 10 and nMes >=10:
                        return True,(f"0{nDia}/{nMes}/{nAño}")
                      elif nDia >= 10 and nMes <10: 
                        return True,(f"{nDia}/0{nMes}/{nAño}")
                      else:
                        return True,(f"{nDia}/{nMes}/{nAño}")
        else:
          mssg.showerror('Atención!!','.. ¡La fecha ingreasada no existe o es inferior al 2000! ..')  
          return False
      except ValueError:
         mssg.showerror('Atención!!','.. ¡Ingrese una Fecha valida! ..')
         return False
  
  #Revisa que se haga doble click

  def click (self,event):
       if event :
          self.treeProductos.bind('<Double-1>', self.insert)
  
  #Inserta informacion en los campos

  def insert (self,event):
    region = self.treeProductos.identify_region(event.x,event.y)
    if region == "cell":
      if event:
        self.limpiaCampos()
        try:
          self.codigo.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][0])
          self.fecha.delete(0,'end')
          self.fecha.config(foreground='black')
          self.idNit.insert(0,self.treeProductos.item(self.treeProductos.selection())['text'])
          self.descripcion.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][1])
          self.unidad.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][2])
          self.cantidad.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][3])
          self.precio.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][4])
          self.fecha.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][5])
          query=('SELECT * FROM Proveedores WHERE idNitProv LIKE ?')
          parametros=(self.idNit.get())
          db_rows = self.run_Query(query,(parametros,))
          row=[]
          for row in db_rows:
            self.razonSocial.delete(0,'end')
            self.razonSocial.insert(0, row[1])
            self.ciudad.delete(0,'end')
            self.ciudad.insert(0, row[2])
        except:
          pass
  def limpiaCampos(self):
      ''' Limpia todos los campos de captura'''
      
      self.idNit.delete(0,'end')
      self.razonSocial.delete(0,'end')
      self.ciudad.delete(0,'end')
      self.idNit.delete(0,'end')
      self.codigo.delete(0,'end')
      self.descripcion.delete(0,'end')
      self.unidad.delete(0,'end')
      self.cantidad.delete(0,'end')
      self.precio.delete(0,'end')
      self.fecha.delete(0,'end')
      self.fecha.insert(0,'DD/MM/AAAA')
      self.fecha.config(foreground='grey')
      
  #Rutina para cargar los datos en el árbol  

  def carga_Datos(self):
    self.idNit.insert(0,self.treeProductos.item(self.treeProductos.selection())['text'])
    self.idNit.configure(state = 'readonly')
    self.razonSocial.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][0])
    self.unidad.insert(0,self.treeProductos.item(self.treeProductos.selection())['values'][3])

  # Operaciones con la base de datos

  def run_Query(self, query, parametros = ()):
    ''' Función para ejecutar los Querys a la base de datos '''
    with sqlite3.connect(self.db_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parametros)
        conn.commit()
    return result
  def run_Query_M(self, query, param):
     with sqlite3.connect(self.db_name) as conn:
        cursor = conn.cursor()
        result = cursor.executemany(query, param)
        conn.commit()
     return result
  
  def limpia_treeView(self):
    ''' Carga los datos y Limpia la Tabla tablaTreeView '''
    tabla_TreeView = self.treeProductos.get_children()
    for linea in tabla_TreeView:
        self.treeProductos.delete(linea) # Límpia la filas del TreeView

  def lee_treeProductos(self):
    self.limpia_treeView
    
    # Seleccionando los datos de la BD
    query = '''SELECT * from Proveedores INNER JOIN Productos WHERE idNitProv = idNit ORDER BY idNitProv'''
    db_rows = self.run_Query(query) # db_rows contine la vista del query
      
    # Insertando los datos de la BD en treeProductos de la pantalla
    row=[]
    for row in db_rows:
      self.treeProductos.insert('',0, text = row[0], values = [row[4],row[5],row[6],row[7],row[8],row[9]])

    ''' Al final del for row queda con la última tupla
        y se usan para cargar las variables de captura
    '''
    if row:
      self.idNit.insert(0,row[0])
      self.razonSocial.insert(0,row[1])
      self.ciudad.insert(0,row[2])
      self.codigo.insert(0,row[4])
      self.descripcion.insert(0,row[5])
      self.unidad.insert(0,row[6])
      self.cantidad.insert(0,row[7])
      self.precio.insert(0,row[8])
      self.fecha.insert(0,row[9])  
    self.limpiaCampos()

#Funcion para editar registros

  def edita(self):
    ''' Edita una tupla del TreeView'''
    if self.idNit.get() != '' or self.codigo.get() != '':
       item_Pv = self.run_Query(''' Select IdNitProv from Proveedores''').fetchall()
       item_Pd = self.run_Query(''' Select Codigo,IdNit from Productos''').fetchall()
       if self.codigo.get() == '':
          for item in item_Pv:
             if item[0] == self.idNit.get():
                mssg.showinfo('Info','Para guardar los cambios presione grabar, para salir del modo editar presione cancelar')
                item_Pv = True
                self.actualiza= True
                self.idNit.config(state="disabled")
                self.codigo.config(state="disabled")
                self.descripcion.config(state="disabled")
                self.unidad.config(state="disabled")
                self.cantidad.config(state="disabled")
                self.precio.config(state="disabled")
                self.fecha.delete(0, tk.END)
                self.fecha.config(state="disabled")
                self.btnEliminar.configure(state="disabled")
                self.btnBuscar.configure(state="disabled")
                self.btnGrabar.configure(command=self.guardarCambios)
          if item_Pv != True:
            mssg.showerror('Advertencia','Solo se pueden editar proveedores existentes')
       elif self.idNit.get()=='':
          mssg.showerror('Advertencia','Ingrese un id para poder editar')
       else:
          for item in item_Pv:
             if item[0] == self.idNit.get():
                item_Pv = True
                for item in item_Pd:
                  if item[0] == self.codigo.get() and item[1]== self.idNit.get() :
                      mssg.showinfo('Info','Para guardar los cambios presione grabar, para salir del modo editar presione cancelar')
                      item_Pd = True
                      self.actualiza= True
                      self.idNit.config(state="disabled")
                      self.codigo.config(state="disabled")
                      self.btnEliminar.configure(state="disabled")
                      self.btnBuscar.configure(state="disabled")
                      self.btnGrabar.configure(command=self.guardarCambios)
                if item_Pd != True:
                  mssg.showerror('Advertencia','Solo se pueden editar productos existentes') 
          if item_Pv != True:
           mssg.showerror('Advertencia','Solo se pueden editar proveedores existentes')
    else:
        mssg.showwarning ('Advertencia','Inserte un id o código o seleccione un producto del tree para editarlo')
  
#Guarda cambios de editar

  def guardarCambios(self):
    query_Prov= f'''UPDATE Proveedores SET Razon_Social = '{self.razonSocial.get()}', Ciudad = '{self.ciudad.get()}' WHERE idNitProv = {self.idNit.get()} '''
    query_Prod= f'''UPDATE Productos SET Descripcion = '{self.descripcion.get()}', Und = '{self.unidad.get()}', Cantidad = '{self.cantidad.get()}', Precio = '{self.precio.get()}', Fecha = '{self.fecha.get()}' WHERE idNit = {self.idNit.get()} and Codigo = {self.codigo.get()}'''
    if self.codigo.get() != '': #Hay codigo 
      if self.valida_Fecha_Final():#tiene que validar fecha
        self.run_Query(query_Prov)
        self.run_Query(query_Prod)
        mssg.showinfo('Editado','Se han guardado los cambios')
        self.cancelar()

    else:#no hay codigo
      self.run_Query(query_Prov)
      mssg.showinfo('Editado','Se han guardado los cambios')  
      self.cancelar()

#Elimina proveedor, producto o ambos

  def eliminaRegistro(self):
    '''Elimina un Registro en la BD'''
    query = f'''DELETE from Proveedores Where IdNitProv = {self.idNit.get()}'''
    query_0=f'''DELETE from Productos Where IdNit = {self.idNit.get()}'''
    query_1=f'''DELETE from Productos Where Codigo = {self.codigo.get()}'''
    conf = None
    conf_p = None
    if self.idNit.get()!= '' and self.codigo.get() == '':
      items = self.run_Query(''' Select IdNitProv from Proveedores''').fetchall()
      conf = False
      for item in items:
          if item[0] == self.idNit.get():
            valor = mssg.askyesno('Eliminar',f'Desea borrar el proveedor con Id {self.idNit.get()} junto con todos sus productos ?')
            conf = True
            if valor: 
              self.run_Query(query)
              self.run_Query(query_0)
              mssg.showinfo('','Borrado exitosamente')
              self.limpiaCampos()
              self.limpia_treeView()
              break
      if conf == False:
        mssg.showerror('','Id no encontrado')          
    elif self.codigo.get() != '' and self.idNit.get() == '':
      items = self.run_Query(''' Select Codigo from Productos''').fetchall()
      conf=False
      for item in items:
          if item[0] == self.codigo.get():
            valor = mssg.askyesno('Eliminar',f'Desea borrar el producto de código {self.codigo .get()} de todos los proveedores ?')
            conf =True
            if valor:
              self.run_Query(query_1)
              mssg.showinfo('','Producto borrado exitosamente')
              self.limpiaCampos()
              self.buscar_prod()
              break
      if conf == False:
        mssg.showerror('','Codigo no encontrado')  
      
    elif self.codigo.get() != '' and self.idNit.get() != '':
  
      items = self.run_Query('''Select Codigo,IdNit from Productos ''').fetchall()
      items_p = self.run_Query(''' Select IdNitProv from Proveedores''').fetchall()
      for item in items:
          for  i in items_p:
             if i[0] == self.idNit.get():
                conf_p = True
                if item[0] == self.codigo.get() and item[1] == self.idNit.get():
                  conf = True
      if conf and conf_p == True:
        self.centra(self.ventana,410,155)
        self.elimina=True
        self.idNit.config(state="disabled")
        self.razonSocial.config(state="disabled")
        self.ciudad.config(state="disabled")
        self.codigo.config(state="disabled")
        self.descripcion.config(state="disabled")
        self.unidad.config(state="disabled")
        self.cantidad.config(state="disabled")
        self.precio.config(state="disabled")
        self.fecha.delete(0, tk.END)
        self.fecha.config(state="disabled")
        self.btnEditar.configure(state="disabled")
        self.btnBuscar.configure(state="disabled")
        self.btnGrabar.configure(state="disabled")
  
      if conf != True:
        mssg.showerror('','Codigo no encontrado')  
      if conf_p != True:
        mssg.showerror('','Id no encontrado')  
    else:
       mssg.showwarning('','Inserte el Id o código del proveedor o producto a eliminar')

  #Funcion para adicionar registro si es un producto, proveedor o ambos

  def adiciona_Registro(self):
      '''Adiciona un producto a la BD si la validación es True'''
      if self.idNit.get()== '': #Revisa que haya un id, necesario para grabar cualquier cosa
         mssg.showerror('Atención!!','.. ¡No ingresó Id! ..')
      else:
        Existe=False
        items = self.run_Query('''Select IdNitProv from Proveedores''').fetchall()
        for item in items:
          if self.idNit.get() == item[0]:
            Existe = True #Si existe el id
            if self.codigo.get() != '':
              if self.valida_Fecha_Final():
                try:
                    self.agregaProducto(self.valida_Fecha_Final()[1])
                    mssg.showinfo('','Producto creado exitosamente')
                    self.limpiaCampos()
                    self.limpia_treeView()
                    return
                except sqlite3.IntegrityError:
                  mssg.showerror('Atención!!','Código de producto ya existente')
                  self.buscar_prov()
                  self.limpia_treeView()
                  return
              else:
                mssg.showinfo('','No se creo el producto')
                return
            else:
              if (self.descripcion.get() or self.unidad.get() or self.cantidad.get() or self.precio.get()) != '':
                mssg.showerror('Atención!!','No ingresó código de producto')
                self.buscar_prov()
                self.limpia_treeView()
                return
              else:
                mssg.showerror('Atención!!','Proveedor ya existente')
                self.buscar_prov()
                self.limpia_treeView()
                return
        if Existe == False:
          if self.codigo.get() != '': #Si hay contenido en el codigo
              if self.valida_Fecha_Final(): #y la fecha es valida
                try:
                    self.agregaProducto(self.valida_Fecha_Final()[1])
                except sqlite3.IntegrityError: #Codigo ya existente
                    mssg.showerror('Atención!!','Código de producto ya existente')
                    return
                self.agregaProveedor()
                self.limpiaCampos()
                self.limpia_treeView()
                mssg.showinfo('','Proveedor creado exitosamente')
                mssg.showinfo('','Producto creado exitosamente')
                return
              else:
                mssg.showinfo('','No se creo el producto')
                return
          else:#Codigo vacio
              self.agregaProveedor()
              mssg.showinfo('','Proveedor creado exitosamente')
              self.limpia_treeView()
              return
  
  #Caso adiciona Proveedor

  def agregaProveedor(self):
   Registro_Prov=[(self.idNit.get(),self.razonSocial.get(),self.ciudad.get())]
   query="INSERT INTO Proveedores VALUES (?,?,?)"
   self.run_Query_M(query,Registro_Prov)
  
  #Caso adiciona Producto

  def agregaProducto(self,fecha):
    Registro_Prod=[(self.idNit.get(),self.codigo.get(),self.descripcion.get(),self.unidad.get(),self.cantidad.get(),self.precio.get(),fecha)]
    query="INSERT INTO Productos VALUES (?,?,?,?,?,?,?)"
    self.run_Query_M(query,Registro_Prod)
  
  #Formato para la Fecha

  def formato(self,event):
    textoActual = self.fecha.get()
    if textoActual == "DD/MM/AAAA":
        self.fecha.delete(0, tk.END)
        self.fecha.config(foreground= 'black')
    elif textoActual == "":
        self.fecha.insert(0,"DD/MM/AAAA")
        self.fecha.config(foreground = 'grey')

  def buscar_prov(self):
      # Busca los proveedores que comienzen por los caracteres buscados
      query=('SELECT * FROM Proveedores WHERE idNitProv LIKE ?')
      parametros=(self.idNit.get()+"%")
      db_rows = self.run_Query(query,(parametros,))
      cant = 0
      row=[]
      # Limpia las celdas de proveedor y inserta los datos del proveedor
      for row in db_rows:
        cant += 1
        self.razonSocial.delete(0,'end')
        self.razonSocial.insert(0, row[1])
        self.ciudad.delete(0,'end')
        self.ciudad.insert(0, row[2])
      # Busca los productos de los proveedores encontrados
      query=('SELECT * FROM Productos WHERE IdNit LIKE ?')
      db_rows = self.run_Query(query,(parametros,))
      row=[]
      # Inserta en el treeview los productos encontrados de los proveedores
      for row in db_rows:
        self.treeProductos.insert('',0, text = row[0], values = [row[1],row[2],row[3],row[4],row[5],row[6]])
      # Si hay varios proveedores limpia los campos y inserta el idNit buscado inicialmente
      if cant != 1:
        self.limpiaCampos()
        self.idNit.insert(0, parametros[:-1])
        if (list(self.treeProductos.get_children())==[]):
          mssg.showerror('Atención!!','.. ¡Proveedor no encontrado! ..')

  def buscar_prod(self):
      # Busca los productos que comienzen por los caracteres buscados
      query=('SELECT * FROM Productos WHERE codigo LIKE ?')
      # parametros=(self.codigo.get()+"%") # para busqueda inexacta
      parametros = (self.idNit.get())
      db_rows = self.run_Query(query,(parametros,))
      self.limpiaCampos()
      cant_prod = 0
      row=[]
      # Imprime en el treeview los productos encontrados
      for row in db_rows:
        cant_prod += 1
        self.treeProductos.insert('',0, text = row[0], values = [row[1],row[2],row[3],row[4],row[5],row[6]])
      # Si solo hay un proveedor de el/los productos, imprime los datos de este prov
      if cant_prod == 1:
        query=('SELECT * FROM Proveedores WHERE idNitProv LIKE ?')
        parametros=(row[0])
        db_rows = self.run_Query(query,(parametros,))
        row=[]
      # Imprime en los campos los datos del proveedor
        for row in db_rows:
          self.idNit.insert(0, row[0])
          self.razonSocial.delete(0,'end')
          self.razonSocial.insert(0, row[1])
          self.ciudad.delete(0,'end')
          self.ciudad.insert(0, row[2])
      if (list(self.treeProductos.get_children())==[]):
        mssg.showerror('Atención!!','.. ¡Producto no encontrado! ..')

  def buscar_prod_prov(self):
      # Busca los productos que el idNit y el codigo comienzen por los caracteres buscados
      query=('SELECT * FROM Productos WHERE IdNit LIKE ? AND codigo LIKE ?')
      # parametro1=(self.idNit.get()+"%") # para busqueda inexacta
      parametro1 = (self.idNit.get())
      # parametro2=(self.codigo.get()+"%") # para busqueda inexacta
      parametro2 = (self.idNit.get())
      db_rows = self.run_Query(query,(parametro1,parametro2))
      cant_prod = 0
      row = []
      # Imprime en el treeview los productos encontrados
      for row in db_rows:
        cant_prod += 1
        self.treeProductos.insert('',0, text = row[0], values = [row[1],row[2],row[3],row[4],row[5],row[6]])
      if (list(self.treeProductos.get_children())==[]):
        mssg.showerror('Atención!!','.. ¡Producto no encontrado! ..')
      else:
        # Busca los proveedores de los productos encontrados
        query=('SELECT * FROM Proveedores WHERE idNitProv LIKE ?')
        parametros=(row[0])
        db_rows = self.run_Query(query,(parametros,))
        row=[]
        # Imprime en los campos los datos del proveedor
        for row in db_rows:
          self.razonSocial.delete(0,'end')
          self.razonSocial.insert(0, row[1])
          self.ciudad.delete(0,'end')
          self.ciudad.insert(0, row[2])
        # Si hay varios proveedores limpia los campos y inserta los datos buscados inicialmente
        if cant_prod > 1:
          self.limpiaCampos()
          self.idNit.insert(0, parametro1[:-1])
          self.codigo.insert(0, parametro2[:-1])

  def buscar(self):
        self.limpia_treeView()
        # Logica para buscar proveedores y productos
        if self.idNit.get() != "":
          if self.codigo.get() == "":
            # Busca proveedor
            self.buscar_prov()
          else:
            # Busca producto de un proveedor
            self.buscar_prod_prov()
        else:
          if self.codigo.get() != "":
            # Busca producto
            self.buscar_prod()
          else:
            mssg.showerror('Atención!!','.. ¡No busco nada! ..')
            self.limpiaCampos()

  #Cancela las acciones

  def cancelar(self):

    if (self.actualiza == True) or (self.elimina==True):
      if self.actualiza == True:
        mssg.showinfo('Modo editar','Ha salido del modo editar')
      self.actualiza = False
      self.elimina = False
      self.idNit.config(state = 'normal')
      self.razonSocial.config(state = 'normal')
      self.ciudad.config(state = 'normal')
      self.codigo.config(state = 'normal')
      self.descripcion.config(state="normal")
      self.unidad.config(state="normal")
      self.cantidad.config(state="normal")
      self.precio.config(state="normal")
      self.fecha.config(state="normal")
      self.btnBuscar.configure(state="normal")
      self.btnEliminar.configure(state="normal")
      self.btnGrabar.configure(state="normal")
      self.btnEditar.configure(state="normal")
      self.btnGrabar.configure(command=self.adiciona_Registro)
      self.fecha.delete(0,tk.END)
      self.fecha.insert(0,"DD/MM/AAAA")
      self.fecha.config(foreground='grey')
      self.ventana.withdraw()
      
    else:
      self.limpiaCampos()
      self.limpia_treeView()
      self.idNit.focus()
# Crea la base de datos
def crear_base_datos():
  conn = sqlite3.connect('Inventario.db')
  c=conn.cursor()
  c.execute(""" CREATE TABLE IF NOT EXISTS Proveedores (
      idNitProv VARCHAR(15) PRIMARY KEY NOT NULL UNIQUE,
      Razon_Social VARCHAR(50),
      Ciudad VARCHAR(15)
  ); """)

  c.execute(""" CREATE TABLE IF NOT EXISTS Productos(
      IdNit VARCHAR(15) ,
      Codigo VARCHAR(15) NOT NULL,
      Descripcion VARCHAR(50),
      Und VARCHAR(10),
      Cantidad DOUBLE,
      Precio DOUBLE,
      Fecha DATE,
      PRIMARY KEY (IdNit, codigo)
  ) """)
  # c.execute("INSERT INTO Proveedores ")
  conn.close()

if __name__ == "__main__":
    app = Inventario()
    app.run()
