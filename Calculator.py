from tkinter import *
from tkinter import ttk


_heightBtn = 50
_widthBtn =68



class CalcDisplay(ttk.Frame):
    _value='0'
    _espositivo = True
    def __init__(self, parent,  **kwargs):
        
        ttk.Frame.__init__(self, parent, height=50, width=272)

        self.pack_propagate(0) #los componentes hijos controlan su tamaño si se pone "0", pero con  "True" o "1" pasan a tener el control standar anulando el estilo. 

        s = ttk.Style()
        s.theme_use('alt')
        s.configure("my.TLabel", font="Helvetica 32")

        self.lblDisplay = ttk.Label(self, text=self._value, style="my.TLabel", anchor=E, foreground="white", background="black")
        self.lblDisplay.pack(fill=BOTH, expand=True)   #rellenar y expandir

        #Tambien se puede utilizar s.theme_use() y dentro del paréntesis poner uno de los siguientes 'aqua, clam, alt, default, classic'

    def addDigit(self, digito):    #añade digito
        if  self._value[0] != '-' and len(self._value) >= 10 or len(self._value) >= 11:  # quiere decir: si distinto de '-' y >= 10   o   igual a '-' y >= 11 
            return
        '''
        if len(self._value) == 11 or self._value[0] == '-' and len(self._value) == 10:
            return'''
      
        #O también:
        
        '''
        if self.value[0]:
            longmax = 11
        else:
            longmax = 10
        if len(self._value) >= longmax:
            return
        '''    

        if self._value == '0':    #el if es para que empiece en cero pero se olvide de el al meter un digito nuevo.
            self._value= digito
        else:
            self._value += digito
        
        self.pintar()

    def pintar(self):               #pinta
        self.lblDisplay.configure(text=self._value)


    def reset(self):
        self._value = '0'
        self._espositivo = True
        self.pintar()


    def signo(self):
        if self._value == '0':
            return
        if self._espositivo:
            self._value = '-'+self._value
        else:
            self._value = self._value[1:]
        self.pintar()
        self._espositivo = not self._espositivo




class CalcButton(ttk.Frame):
    def __init__(self, parent, **kwargs):
        '''
        if 'bw' in kwargs:
            bw = kwargs['bw']
        else:
            bw = 1
        '''
        # lo del arriba es equivalente a:       
        bw= kwargs['bw'] if 'bw' in kwargs else 1   

        ttk.Frame.__init__(self, parent, height=_heightBtn, width=_widthBtn * bw)  #kwargs['bw'] y depueés la doy valores bw= 1,2,3,.. lo que sea)
        #bw es por lo que se multiplica el ancho del botón
        self.pack_propagate(0)

        self.button = ttk.Button(self, text=kwargs["text"], command=kwargs["command"])
        self.button.pack(fill=BOTH, expand=True)


class Calculator(ttk.Frame):
    _op1 = None
    _op2 = None
    _operador = None
    swBorrado = True

    def __init__(self, parent, **kwargs):
        ttk.Frame.__init__(self, parent, height=kwargs["height"], width=kwargs["width"])
        self.display = CalcDisplay(self)
        #self.display.place(x=0, y=0)
        self.display.grid(column=0, row=0, columnspan=4)

        CalcButton(self, text="0", command=lambda: self.addDigit('0'), bw=2).grid(column=0, row=5, columnspan=2)  #bw es por lo que se multiplica el ancho del botón
        #btn.place(x=0, y=5*_heightBtn)

        CalcButton(self, text="1", command=lambda: self.addDigit('1')).grid(column=0, row=4)
        CalcButton(self, text="2", command=lambda: self.addDigit('2')).grid(column=1, row=4)
        CalcButton(self, text="3", command=lambda: self.addDigit('3')).grid(column=2, row=4)
        CalcButton(self, text="4", command=lambda: self.addDigit('4')).grid(column=0, row=3)
        CalcButton(self, text="5", command=lambda: self.addDigit('5')).grid(column=1, row=3)
        CalcButton(self, text="6", command=lambda: self.addDigit('6')).grid(column=2, row=3)
        CalcButton(self, text="7", command=lambda: self.addDigit('7')).grid(column=0, row=2)
        CalcButton(self, text="8", command=lambda: self.addDigit('8')).grid(column=1, row=2)
        CalcButton(self, text="9", command=lambda: self.addDigit('9')).grid(column=2, row=2)
        
        CalcButton(self, text="C", command=self.reset).grid(column=0, row=1) #no pone display, solo con reset es suficiente.
        CalcButton(self, text="+/-", command=self.display.signo).grid(column=1, row=1)
        CalcButton(self, text="%", command=lambda: self.display.addDigit('%')).grid(column=2, row=1)
        CalcButton(self, text="/", command=lambda: self.opera('/')).grid(column=3, row=1)

        CalcButton(self, text="X", command=lambda: self.opera('X')).grid(column=3, row=2) #Aquí pasa igual, no pone display, ya va dentro de la función
        CalcButton(self, text="-", command=lambda: self.opera('-')).grid(column=3, row=3)
        CalcButton(self, text="+", command=lambda: self.opera('+')).grid(column=3, row=4)
        CalcButton(self, text="=", command=lambda: self.opera('=')).grid(column=3, row=5)
        CalcButton(self, text=".", command=lambda: self.display.addDigit(',')).grid(column=2, row=5)

    def addDigit(self, digito):
        if self.swBorrado:
            self.display.reset()
            self.swBorrado = False

        self.display.addDigit(digito)



    def reset(self):                #los 3 siguientes resetean la calculadora, la parte de lista del programa
            self._op1 = None
            self._op2 = None
            self._operador = None
            self.display.reset()   #este resetea solo la pantalla  ;)


    def opera(self, operador):
        if self._op1 is None:
            self._op1 = float(self.display._value)   #aquí introduce ._value en op1
            self._operador = operador

        else:
            if self._op2 == None:
                self._op2 = float(self.display._value)   #aquí introduce ._value en op2

            if self._operador == '+':
                resultado = self._op1 + self._op2
            elif self._operador == '-':
                resultado = self._op1 - self._op2
            elif self._operador == 'X':
                resultado = self._op1 * self._op2
            elif self._operador == '/':
                resultado = self._op1 / self._op2    
            else:
                print('Operador incorrecto')

            self._op1 = resultado     #mete el resultado en OP1!!!
            if operador != '=':
                self._operador = operador   #guardo el operador que será '=' en _operador
                self._op2 = None            #dejo _op2 en None

            resultado = str(resultado)
            self.display._value = resultado
            self.display.pintar()

        self.swBorrado = True  #así, al meterle el siguiente número, pasa por addDigit y te hace el display.reset()

class MainApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Calculator")
        self.geometry("{}x{}".format(_widthBtn*4, _heightBtn*6))   #en el geometry() se puede poner la ubicación, ej: geometry() "200x300+0+10" donde x= 0, y=10

        self.calculator = Calculator(self, height=_heightBtn*6, width=_widthBtn*4)
        self.calculator.place(x=0, y=0)

    def start(self):
        self.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.start()