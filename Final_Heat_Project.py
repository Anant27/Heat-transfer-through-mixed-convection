from Tkinter import *
import math
import pandas as pd
from scipy import interpolate
s=""

def check_Value(Rey,Product,Gr,Gz,uf,uw,d,l,Pr,ub):
    if(Rey==0.0):
        Nuss=FreeConvection(Gr,Pr)
    elif (Product > 10 ** 7):
        if (Rey < 850):
            Nuss= FreeConvection(Gr,Pr)
        elif (Rey > 850 and Rey < 10 ** 4):
            Nuss = MixedConvection_Turbulent(Rey,Pr,Gr,d,l)
        else:
            Nuss = ForcedConvection_Turbulent(Rey,Pr,uf,uw,d,l)
    elif (Product > 10 ** 4 and Product < 10 ** 7):
        if (Rey < 850):
            Nuss = MixedConvection_Laminar(Gz,Gr,Pr,uf,uw)
        elif (-2000 - (8000.0 / (10 ** 7 - 10 ** 4)) * (Product - 10 ** 4) + Rey < 0):
            Nuss = MixedConvection_Turbulent(Rey,Pr,Gr,d,l)
        else:
            Nuss = ForcedConvection_Turbulent(Rey,Pr,uf,uw,d,l)
    else:
        if (Rey > 10 ** 3):
            Nuss = ForcedConvection_Turbulent(Rey,Pr,uf,uw,d,l)
        elif (-10 - (990.0 / 9990.0) * (Product - 10) + Rey < 0):
            Nuss = MixedConvection_Laminar(Gz,Gr,Pr,uf,uw)
        else:
            Nuss = ForcedConvection_Laminar(Gz,uf,uw)

    return Nuss

def FreeConvection(Gr,Pr):
    prod=Gr*Pr
    C=0.0
    m=0.0
    if(prod<10**-4):
        C=0.4
        m=0
    elif(prod>10**4 and prod<10**9):
        C=0.53
        m=0.25
    elif(prod>10**9 and prod<10**12):
        C=0.675
        m=0.058
    elif(prod>10**-2 and prod<10**2):
        C=1.02
        m=0.148
    Nuss=C*(Gr*Pr)**m
    global s
    s="FreeConvection"
    return Nuss

def MixedConvection_Laminar(Gz,Gr,Pr,uf,uw):

    A=(uf/uw)**0.14
    B=(Gr*Pr)**(0.75)
    C = Gz + 0.0083 * (B)
    Nuss = 1.75 * (A) * (C ** (1.0/ 3.0))
    global s
    s="MixedConvection_Laminar"
    return Nuss

def MixedConvection_Turbulent(Rey,Pr,Gr,d,l):
    Nuss = 4.69*(Rey**0.27)*(Pr**0.21)*(Gr**0.07)*(d/l)**0.36
    global s
    s="MixedConvection_Turbulent"
    return Nuss

def ForcedConvection_Laminar(Gz,uf,uw):
    Nuss = 1.86*(Gz**(1/3.0))*((uf/uw)**0.14)
    global s
    s="ForcedConvection_Laminar"
    return Nuss

def ForcedConvection_Turbulent(Rey,Pr,uf,uw,d,l):
    Nuss = 0.116*(1+(d/l)**(2/3.0))(Rey**(2/3.0)-125)*(Pr**(1/3.0))*((uf/uw)**0.14)
    global s
    s="ForcedConvection_Turbulent"
    return Nuss

window2 = Tk()
window2.title("\tEnter Values for Air")
window2.configure(background="powder blue")
window2.option_add('*Font', 'arial 20 bold')

    #Diameter(window2, 1)
l1 = Label(window2, text="Diameter ", bg="powder blue", fg="black", font="none 20 bold")
l1.grid(row=0, column=0, stick=W)
Dia = Entry(window2, width=20, bg="white")
Dia.grid(row=0, column=1, stick=W)

    #Length(window2, 2)
l2 = Label(window2, text="Length ", bg="powder blue", fg="black", font="none 20 bold")
l2.grid(row=1, column=0, stick=W)
Len = Entry(window2, width=20, bg="white")
Len.grid(row=1, column=1, stick=W)

    #Temp_Wall(window2, 3)
l3 = Label(window2, text="Wall Temperature in Celsius ", bg="powder blue", fg="black", font="none 20 bold")
l3.grid(row=3, column=0, stick=W)
Temp_W = Entry(window2, width=20, bg="white")
Temp_W.grid(row=3, column=1, stick=W)

    #Temp_Bulk(window2, 4)
l4 = Label(window2, text="Film Temperature in Celsius ", bg="powder blue", fg="black", font="none 20 bold")
l4.grid(row=4, column=0, stick=W)
Temp_B = Entry(window2, width=20, bg="white")
Temp_B.grid(row=4, column=1, stick=W)

    #Velocity(window2, 5)
l5 = Label(window2, text="Velocity ", bg="powder blue", fg="black", font="none 20 bold")
l5.grid(row=5, column=0, stick=W)
Velo = Entry(window2, width=20, bg="white")
Velo.grid(row=5, column=1, stick=W)
