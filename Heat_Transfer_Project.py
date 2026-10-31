import tkinter 
from tkinter import *
import math
import pandas as pd
import sys
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
            Nuss = MixedConvection_Laminar(Gz,Gr,Pr,ub,uw)
        elif (-2000 - (8000.0 / (10 ** 7 - 10 ** 4)) * (Product - 10 ** 4) + Rey < 0):
            Nuss = MixedConvection_Turbulent(Rey,Pr,Gr,d,l)
        else:
            Nuss = ForcedConvection_Turbulent(Rey,Pr,uf,uw,d,l)
    else:
        if (Rey > 10 ** 3):
            Nuss = ForcedConvection_Turbulent(Rey,Pr,uf,uw,d,l)
        elif (-10 - (990.0 / 9990.0) * (Product - 10) + Rey < 0):
            Nuss = MixedConvection_Laminar(Gz,Gr,Pr,ub,uw)
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

def MixedConvection_Laminar(Gz,Gr,Pr,ub,uw):
    A = (ub / uw) ** 0.14
    B = Gz * (Gr ** (1.0 / 3.0))
    C = Gz + 0.012 * (B ** (4.0 / 3.0))
    Nuss = 1.75 * (A) * (C ** (1.0 / 3.0))
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




#Window for Air
def Air_Window():

    window2 = tkinter.Tk()
    window2.title("\t\tEnter Values for Air in SI Units")
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
    l4 = Label(window2, text="Bulk Temperature in Celsius ", bg="powder blue", fg="black", font="none 20 bold")
    l4.grid(row=4, column=0, stick=W)
    Temp_B = Entry(window2, width=20, bg="white")
    Temp_B.grid(row=4, column=1, stick=W)

    #Velocity(window2, 5)
    l5 = Label(window2, text="Velocity ", bg="powder blue", fg="black", font="none 20 bold")
    l5.grid(row=5, column=0, stick=W)
    Velo = Entry(window2, width=20, bg="white")
    Velo.grid(row=5, column=1, stick=W)

    h=0.0
    def Air():
        d = float(Dia.get())
        l = float(Len.get())
        Tw = float(Temp_W.get()) + 273.0
        Tb = float(Temp_B.get()) + 273.0
        Tf = ((Tw + Tb) / 2.0)
        v = float(Velo.get())

        data = pd.read_csv("Air.csv")
        Temperature = data.iloc[:, 0].values
        Prandtl = data.iloc[:, 4].values
        Density = data.iloc[:, 1].values
        Viscosity = data.iloc[:, 2].values
        Conductivity = data.iloc[:, 3].values
        dens=interpolate.interp1d(Temperature,Density)
        visco = interpolate.interp1d(Temperature, Viscosity)
        condu = interpolate.interp1d(Temperature, Conductivity)
        Pran= interpolate.interp1d(Temperature, Prandtl)

        pf = dens(Tf)
        uw = visco(Tw)
        uf = visco(Tf)
        ub = visco(Tb)
        Kf = condu(Tf)
        Pr = Pran(Tf)

        beta = 1.0 / (Tf)
        f = ((pf ** 2) * 9.8 * beta * (Tw - Tb) * d ** 3)
        Gr = f / (uf ** 2)
        Ref = (pf * v * d) / uf
        r = d / l
        pro = Gr * Pr * r
        Gz = Ref * Pr * r
        Nu = float(check_Value(Ref, pro, Gr, Gz, uf, uw, d, l, Pr, ub))
        global h
        h = (Kf * Nu) / d
        T = Text(window2, height=10, width=30)
        T.grid(row=13, column=0, stick=W)
        T.insert(END, "Value of Convective Heat Transfer Coefficient h - " + str(h)+"\n"+str(s)+"\n"+"Grasoff - "+str(Gr)+"\nRenolds - "+str(Ref)+"\nGraetz - "+str(Gz)+"\nNusselt - "+str(Nu))

    button_SUBMIT=Button(window2,text="Submit",command=Air)
    button_SUBMIT.grid(row=14,column=0,stick=W)

    def exi_Air():
        window2.destroy()

    button_EXI=Button(window2,text="Exit",command=exi_Air)
    button_EXI.grid(row=14,column=1,stick=W)

    window2.mainloop()

#Window for Water
def Water_Window():
    window3 = Tk()
    window3.title("\tEnter Values for Water in SI Units")
    window3.configure(background="powder blue")
    window3.option_add('*Font', 'arial 20 bold')

    # Diameter(window2, 1)
    l1 = Label(window3, text="Diameter ", bg="powder blue", fg="black", font="none 20 bold")
    l1.grid(row=0, column=0, stick=W)
    Dia = Entry(window3, width=20, bg="white")
    Dia.grid(row=0, column=1, stick=W)

    # Length(window2, 2)
    l2 = Label(window3, text="Length ", bg="powder blue", fg="black", font="none 20 bold")
    l2.grid(row=1, column=0, stick=W)
    Len = Entry(window3, width=20, bg="white")
    Len.grid(row=1, column=1, stick=W)

    # Temp_Wall(window2, 3)
    l3 = Label(window3, text="Wall Temperature in Celsius ", bg="powder blue", fg="black", font="none 20 bold")
    l3.grid(row=3, column=0, stick=W)
    Temp_W = Entry(window3, width=20, bg="white")
    Temp_W.grid(row=3, column=1, stick=W)

    # Temp_Bulk(window2, 4)
    l4 = Label(window3, text="Bulk Temperature in Celsius ", bg="powder blue", fg="black", font="none 20 bold")
    l4.grid(row=4, column=0, stick=W)
    Temp_B = Entry(window3, width=20, bg="white")
    Temp_B.grid(row=4, column=1, stick=W)

    # Velocity(window2, 5)
    l5 = Label(window3, text="Velocity ", bg="powder blue", fg="black", font="none 20 bold")
    l5.grid(row=5, column=0, stick=W)
    Velo = Entry(window3, width=20, bg="white")
    Velo.grid(row=5, column=1, stick=W)


    h = 0.0

    def Water():
        d = float(Dia.get())
        l = float(Len.get())
        Tw = float(Temp_W.get())
        Tb = float(Temp_B.get())
        Tf = ((Tw + Tb) / 2.0)
        v = float(Velo.get())

        data = pd.read_csv("Water_Property.csv")
        Temperature = data.iloc[:, 0].values
        Prandtl = data.iloc[:, 4].values
        Density = data.iloc[:, 1].values
        Viscosity = data.iloc[:, 2].values
        Conductivity = data.iloc[:, 3].values
        Fun_GrPr=data.iloc[:,5].values
        dens = interpolate.interp1d(Temperature, Density)
        visco = interpolate.interp1d(Temperature, Viscosity)
        condu = interpolate.interp1d(Temperature, Conductivity)
        Pran = interpolate.interp1d(Temperature, Prandtl)
        Fu = interpolate.interp1d(Temperature,Fun_GrPr)

        pf = dens(Tf)
        uw = visco(Tw)
        uf = visco(Tf)
        ub = visco(Tb)
        Kf = condu(Tf)
        Pr = Pran(Tf)
        Funct = Fu(Tf)

        Ref = (pf * v * d) / uf
        GrPr = Funct * (d ** 3) * (Tw - Tb)
        Gr = GrPr / Pr
        pro = GrPr * (d / l)
        Gz = Ref * Pr * (d / l)
        Nu = check_Value(Ref, pro, Gr, Gz, uf, uw, d, l, Pr, ub)
        global h
        h = (Kf * Nu) / d

        T = Text(window3, height=10, width=30)
        T.grid(row=7, column=0, stick=W)
        T.insert(END, "Value of Convective Heat Transfer Coefficient is " + str(h)+"\n"+str(s)+"\n"+"Grasoff - "+str(Gr)+"\nRenolds - "+str(Ref)+"\nGraetz - "+str(Gz)+"\nNusselt - "+str(Nu))




    button_Submit=Button(window3,text="Submit",command=Water)
    button_Submit.grid(row=8,column=0,stick=W)

    def exi_Air():
        window3.destroy()

    button_EXI = Button(window3, text="Exit", command=exi_Air)
    button_EXI.grid(row=8, column=1, stick=W)

    window3.mainloop()


#Re - Reynolds Number  and Product - GrPr(D/L)

#The First window
window1 = tkinter.Tk()
window1.title("Free and Forced Convection")
window1.configure(background="powder blue")
window1.option_add('*Font','arial 20 bold')

#Creating Heading
l1 = Label(window1,text="\t\t      Free and forced convection through horizontal pipe",bg="powder blue",fg="black",font="none 20 bold")
l1.grid(row=0,column=0,stick=W)

#For Air or Liquid
l2=Label(window1,text ="Choose whether Air or Water ",bg="powder blue",fg="black",font="none 20 bold")
l2.grid(row=1,column=0,stick=W)

#For Air
b1=Button(window1,text="AIR",width=10,command=Air_Window)
b1.grid(row=2,column=0,stick=W)

#For Water
b2=Button(window1,text="WATER",width=10,command=Water_Window)
b2.grid(row=3,column=0,stick=W)

def exi():
    window1.destroy()
    try:
        sys.exit()
    except ValueError: # Catch specific errors only
        pass

b4=Button(window1,text="EXIT",width=10,command=exi)
b4.grid(row=4,column=1,stick=W)

window1.mainloop()
