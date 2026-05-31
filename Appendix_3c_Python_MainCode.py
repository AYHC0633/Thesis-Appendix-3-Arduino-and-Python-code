import os
os.environ["BLINKA_FT232H"] = "1"
import sys
#import Adafruit_GPIO.FT232H 
#from pyftdi.ftdi import Ftdi
#Ftdi().open_from_url('ftdi:///?')

sys.path.append('../Python/CASSIELibrary')
sys.path.append('../Python')

import raspberryPiFileReadModule as rPFRM

import time
import tensorflow as tf

from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib as plt
from PIL import ImageTk,Image
import threading
import pandas as pd

#---- Excel table Database loading 
d = rPFRM.fileloadingmoduleforhelicoidV3()
did = rPFRM.fileloadingmoduleforhelicoidNamesearchV3()
a = rPFRM.fileloadingmodule()

aa = rPFRM.fileloadingmoduleV2()

df = rPFRM.fileloading()

#---- DNN h5 model loading 
h5model = rPFRM.DNNh5loadForGUI()

def bytes(integer):
    return divmod(integer, 0x100)

def ArrayI2Csetting(Amp,AngleDir,calEnable):
    global helicoidflag 
    global DNNhelicoidflag
    global Excelloadflag
    if calEnable ==1:
        CalibratePhase= rPFRM.EVRcalibratedElementV4(AngleDir)
        # print("check", CalibratePhase) 
    else:
        CalibratePhase=np.mod(list(AngleDir),360)

    for x in range(len(CalibratePhase)):   
        
        i2c = board.I2C()
        # data=rPFRM.calibratedElementV3(data)
        position =rPFRM.Searching(np.round(float(CalibratePhase[x]),1),df)
        # print("position", position)

        try:
            if len(Amp)>2:
                Amplitudeindex=rPFRM.fileloadingmoduleV2namesearchV2(Amp[x])
                b= aa[Amplitudeindex]
                data = b[int(position),1:]# loading the setting of that Element
            else:
                b= aa[0]
                data = b[int(position),1:] # a[int(position),1:]# loading the setting of that Element
        except:
            b= aa[0]
            data = b[int(position),1:]#a[int(position),1:] loading the setting of that Element

        #-------------swapping DAC value because the MSB sending order 
        ##------swapping I DAC value because the MSB sending order
        # swap = data[-4] 
        # data[-4] =data[-5]
        # data[-5] =swap

        # ##------swapping Q DAC value because the MSB ssending order
        # swap = data[-2] 
        # data[-2]  = data[-1]
        # data[-1] = swap 
        
        data=data.astype('int64')
        ##---formating data and sent data to unitcell 
        
        newlist =  data.tolist()
        
        newlist.insert(0,x) # dont use c= newlist.insert() , it will return the function itself and became none
        newlist.append(10)
        print("Data sent",newlist)
        i2c.writeto(0x0a,newlist)
        if helicoidflag == 1:
            Phase2shiftlab.config(text = "Setting Element " + str(x) +" in phase "+str(round(CalibratePhase[x],2)) + "....")
        elif DNNhelicoidflag == 1 or Excelloadflag == 1:
            Phase3shiftlab.config(text = "Setting Element " + str(x) +" in phase "+str(round(CalibratePhase[x],2)) + "....")
        else:
            break
        time.sleep(0.2)

def singleElementI2Csetting(Amp,AngleDir,unitcell):
        position =rPFRM.Searching(AngleDir,df)
        try:
            b= aa[Amp]
            data = b[int(position),1:]# loading the setting of that Element
            print('Amplitude Data loaded!')
        except:
            b= aa[0]
            data = b[int(position),1:]# loading the setting of that Element
            print('No Amplitude data! Set All to 1!')
        #-------------swapping DAC value because the MSB sending order 
        ##------swapping I DAC value because the MSB sending order
        # swap = data[-4] 
        # data[-4] =data[-5]
        # data[-5] =swap

        # ##------swapping Q DAC value because the MSB ssending order
        # swap = data[-2] 
        # data[-2]  = data[-1]
        # data[-1] = swap 
        
        data=data.astype('int64')
        
        ##---formating data and sent data to unitcell 
        newlist =  data.tolist()
        newlist.insert(0,unitcell) # dont use c= newlist.insert() , it will return the function itself and became none
        if IQSingleflag == 1:
            newlist.append(int(r.get()))
            # newlist[int(r.get())] =  int(ElemIQ01.get())
            newlist[1] =  int(ElemIQ01.get())
        else:
            newlist.append(10)

        print("Data sent",newlist)

        # device = I2CDevice(i2c, 0x70)
        i2c.writeto(0x0a,newlist)
        if sweepsingleFlag == 1:
            Phase1shiftlab.config(text = "phase set "+str(round(AngleDir,2)) + "....")
        if linearkeyFlag ==1:
            ManualCodestatus.config(text = "phase set "+str(round(AngleDir,2)) + " on "+str(unitcell) +" ....")
        time.sleep(0.1)

def CustomcodI2Csetting():
    newlist = [0 for x in range(0,9)]
    newlist[0] = int(Elemnum.get())
    newlist[1] = int(FU1.get())
    # newlist[2] = int(FU2.get())
    # newlist[3] = int(FU3.get())
    # newlist[4] = int(FU4.get())
    # newlist[5] = int(FU5.get())
    # newlist[6] = int(FU6.get())
    # newlist[7] = int(FU7.get())
    # newlist[8] = int(FU8.get())
    # newlist[9] = 49 # Q
    # newlist[12] = 56 #I
    newlist[2] = 49 # Q
    newlist[5] = 56 #I
    if cr.get() == 1:
         Qup,Qdown = bytes(Qslicer.get())      
         Iup,Idown = bytes(Islicer.get())   
    else:
        Qup,Qdown = bytes(int(QEntry.get()))
        Iup,Idown = bytes(int(IEntry.get()))
        Qslicer.set(QEntry.get())
        Islicer.set(IEntry.get())

    newlist[3] = Qup 
    newlist[4] = Qdown 
    newlist[6] = Iup
    newlist[7] = Idown 
    status =int(mr.get())
    newlist[8] = status
    print("Data sent",newlist)

        # device = I2CDevice(i2c, 0x70)
    i2c.writeto(0x0a,newlist)

##-----------I2C communication--------###
if __name__ == '__main__':
    
    # #-----setting up the I2C protocol 
    try:
        import board
        i2c = board.I2C()
        # i2c = board.STEMMA_I2C()
        while not i2c.try_lock():
            pass
        print("I2C addresses found:",[hex(device_address) for device_address in i2c.scan()])
        i2c.unlock()
        NanoSlave= i2c.scan()
    except:
        print("Not FT232H was Found! but start GUI as usual!")
   #---------------DNN config
    print(tf.__version__)
    print(tf.config.list_physical_devices())
    #-----------GUIvariable---------------
    sinEleFlag = 0
    linearkeyFlag = 0
    helicoidflag = 0
    DNNhelicoidflag = 0
    Excelloadflag =0
    sweepsingleFlag = 0
    IQSingleflag = 0
    ManulaCodeflag = 0

    #£----------GUI position---------------

    ResetButX1 = 120#Resetbutton
    ResetButY1 =500#Resetbutton

    PictureX =40 #picture
    PictureY=40 #picture

    P1LX = 500
    P1LY =80#entry
    ElemlabelX1 = P1LX+50#entryLabel1Element number
    ElemlabelY1 =P1LY+30 #entryLabel1 Element number
    ElemnumX = ElemlabelX1+100 #entry 1 Element number
    ElemnumY = ElemlabelY1#entry 1  Element number  
    ElemlabelX2 = P1LX+250#entryLabel2 phase
    ElemlabelY2 =P1LY+60#entryLabel2 phase
    ElemnumphaX = ElemlabelX2+100#entry 2phase
    ElemnumphaY = ElemlabelY2#entry 2phase
    ElemlabelX3 = P1LX+250#entryLabel3 Sweeping phase
    ElemlabelY3 =P1LY+30 #entryLabel3Sweeping phase
    ElemnumphaX3 = ElemlabelX3+120 #entry 3Sweeping phase
    ElemnumphaY3 = ElemlabelY3#entry 3 Sweeping phase
    ElemnumphaX3end =   ElemnumphaX3 +40 #entry 4 Sweeping phase
    ElemnumphaY3end = ElemnumphaY3#entry 4 Sweeping phase
    ConfirButX0 = P1LX +500#button
    ConfirButY0= ElemnumphaY3#button

    phase1shflabX = P1LX+400#statement
    phase1shflabY = ElemnumphaY#statement
    ConfirButX1 = P1LX +500#button
    ConfirButY1 = ElemnumphaY#button

    #IQSetting
    ElemIQ01LX = 900
    ElemIQ01LY = 170
    ElemIQ01EX = ElemIQ01LX
    ElemIQ01EY = ElemIQ01LY+50
    IQRadiobutX = 550
    IQRadiobuty = 180
    IQConfirButX = ElemIQ01LX + 100
    IQConfirButY = ElemIQ01EY
    

    #Codesetting
    spacing = 60
    FUlabelX = 550
    FUlabelY = 440
    FU1EX = 550
    FU1EY = 500
    FU2EX = FU1EX +spacing
    FU2EY = 500
    FU3EX = FU2EX + spacing
    FU3EY = 500
    FU4EX = FU3EX + spacing
    FU4EY = 500
    FU5EX = FU4EX + spacing
    FU5EY = 500
    FU6EX = FU5EX + spacing
    FU6EY = 500
    FU7EX = FU6EX + spacing
    FU7EY = 500
    FU8EX = FU7EX + spacing
    FU8EY = 500

    FU9EX = FU8EX+ (spacing/2)
    FU9EY = FU8EY 
    FU10EX = FU9EX+(spacing)
    FU10EY = FU9EY 

    singleModeselX = FU6EX
    singleModeselY =FU1EY +20
    
    MCEnterButX = FU10EX+ spacing
    MCEnterButY = FU10EY+ spacing

 
    #8x8Entry
    P2LX = 60 
    P2LY =590
    phase2staX = P2LX+240#entry 
    phase2staY = P2LY+2#entry
    phase2shflabX = P2LX+290
    phase2shflabY = P2LY+2
    ConfirButX2 = P2LX +400
    ConfirButY2 = P2LY +5

    #DNN8x8Entry
    P3LX = 60 
    P3LY =640
    phase3staX = P3LX+280#entry 
    phase3staY = P3LY+2#entry
    phase3shflabX = P3LX+310
    phase3shflabY = P3LY+2
    ConfirButX3 = P3LX +400
    ConfirButY3 = P3LY +5

    #----------GUI start--------------
    root = Tk()
    root.geometry('1200x750')
    root.title('8x8Helical array Steering GUI for FT232H at 0x0a')
    
    #£----scrollBar
    main_frame = Frame(root)
    main_frame.pack(fill=BOTH,expand=1)

    my_canvas =Canvas(main_frame)
    my_canvas.pack(side=LEFT,fill=BOTH,expand=1)
    
    my_scrollbar = ttk.Scrollbar(main_frame,orient=VERTICAL,command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT,fill=Y)

    my_canvas.configure(yscrollcommand=my_scrollbar.set)
    my_canvas.bind('<Configure>',lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    second_frame = Frame(my_canvas)
    my_canvas.create_window((0,0),window=second_frame,anchor="nw")


    #£-----------image 
    imagee1 = Image.open("Maping2.jpg")
    imagee1 = imagee1.resize((450,450))
    imagee = ImageTk.PhotoImage(imagee1)
    myimage =Label(image=imagee)
    # myimage.grid(row=1,column=1)
    myimage.place(x=PictureX,y=PictureY)

    #£-------------function---------
   
    def singlekey():
        global sinEleFlag
        sinEleFlag = 1 - sinEleFlag
        Phase1shiftlab.config(text = "setting...")

    def sweepsinglekey():
        global sweepsingleFlag
        sweepsingleFlag = 1 - sweepsingleFlag
        Phase1shiftlab.config(text = "setting...")

    def linearkey():
        global linearkeyFlag
        linearkeyFlag = 1 - linearkeyFlag
        ManualCodestatus.config(text = "Linear setting...")

    def helicalkey():#
        global helicoidflag 
        helicoidflag = 1 - helicoidflag 
        Phase2shiftlab.config(text = "setting...")

    def h5DNNhelicalkey():#
        global  DNNhelicoidflag
        DNNhelicoidflag = 1 -  DNNhelicoidflag
        Phase3shiftlab.config(text = "setting...")

    def Excelloadkey():#
        global  Excelloadflag
        Excelloadflag = 1 -  Excelloadflag
        Phase3shiftlab.config(text = "setting...")
        
    def IQsinglekey():
        global  IQSingleflag
        IQSingleflag = 1-IQSingleflag
        ElemlabelIQ01.config(text = "setting...")

    def ManulaCodekey():
        global  ManulaCodeflag
        ManulaCodeflag = 1-ManulaCodeflag
        ManualCodestatus.config(text = "setting...")

    def Thread1():
        global sinEleFlag
        global linearkeyFlag
        global helicoidflag 
        global DNNhelicoidflag
        global sweepsingleFlag
        global IQSingleflag
        global ManulaCodeflag 
        global Excelloadflag 
        
        while True:
            if sinEleFlag == 1:
                helicoidflag = 0
                DNNhelicoidflag = 0
                unitcell_sel = Elemnum.get()
                phase2 = Elempha.get()# zero setting
                print('Degree:'+str(phase2))
                print('Element:'+str(unitcell_sel))
                singleElementI2Csetting(0,float(phase2),int(unitcell_sel))
                sinEleFlag = 0
                Phase1shiftlab.config(text = "finished!")
                time.sleep(2)
                Phase1shiftlab.config(text = "Enter the data")
            if linearkeyFlag ==1:
                helicoidflag = 0
                DNNhelicoidflag = 0
                
                Phase=[0 for x in range(len(LAMEntry))]
                CellNo=[0 for x in range(len(LAMEntry))]
                for x in range(len(LAMEntry)):
                    Phase[x]=LAMEntry[x].get()
                    CellNo[x]=CellEntry[x].get()
                    singleElementI2Csetting(0,float(Phase[x]),int(CellNo[x]))

                ManualCodestatus.config(text = "linear code loading finish! ")
                time.sleep(1) 
                ManualCodestatus.config(text = "idle ")
                linearkeyFlag = 0
            if helicoidflag == 1:
                sinEleFlag = 0
                DNNhelicoidflag = 0
                phase = Phase2Value.get() 
               
                phasename ='Degree_'+phase
                print(phasename)
                Phaseloca =did.index(phasename)
                helical_steering_data = d[:,Phaseloca] 
                
                # realphase= np.mod(helical_steering_data,359)  
                     
                ArrayI2Csetting(1,helical_steering_data,1)
                Phase2shiftlab.config(text = "finished!")
                time.sleep(2)
                Phase2shiftlab.config(text = "Enter the data")
                helicoidflag = 0

            if Excelloadflag ==1:
                filename = Phase4Value.get()
                xls = pd.ExcelFile("REV BeamSteeringData/"+filename+".xlsx")
                df = pd.read_excel(xls)#pd.read_excel(filename+".xlsx")
                elementphase  = np.array(df['Phase'])
                TapeChoice=Ar.get()
                if TapeChoice == 1:
                    try:
                        elementAmplitude  = np.array(df['Amplitude'])#
                        ArrayI2Csetting(elementAmplitude,elementphase,0)
                        print("Amplitude loading in...")
                    except:
                        ArrayI2Csetting(1,elementphase,0)
                        print("All element amplitude set to 1 ... ")
                else:
                    ArrayI2Csetting(1,elementphase,0)
                    print("All element amplitude set to 1 ... ")

                Excelloadflag =0

            if DNNhelicoidflag == 1:
                helicoidflag = 0
                sinEleFlag = 0
                phase = Phase3Value.get()
                theta = (90-80)/(100-80)
                phi =  float(phase)/359
                helical_steering_data=h5model.predict([[phi ,theta]])
                realphase= np.mod(helical_steering_data,359) 
                realphase = realphase.reshape(-1)
                print(len(realphase))
                
                ArrayI2Csetting(1,realphase,1)
                Phase3shiftlab.config(text = "finished!")
                time.sleep(2)
                Phase3shiftlab.config(text = "Enter the data")
                DNNhelicoidflag = 0
            if sweepsingleFlag ==1:
                helicoidflag = 0
                sinEleFlag = 0
                DNNhelicoidflag = 0
                unitcell_sel = Elemnum.get()
                phasestart = Elempha3.get()# zero setting
                phasestop =Elempha3end.get()
                for phaSwp in range(int(phasestart),int(phasestop)):
                    print('Degree:'+str(phaSwp))
                    print('Element:'+str(unitcell_sel))
                    
                    singleElementI2Csetting(0,float(phaSwp),int(unitcell_sel))
                    time.sleep(0.2)
                    if sweepsingleFlag == 0:
                        break   
                sinEleFlag = 0
                Phase1shiftlab.config(text = "finished!")
                time.sleep(2)
                Phase1shiftlab.config(text = "Enter the data")
                sweepsingleFlag = 0
            if IQSingleflag == 1:
                helicoidflag = 0
                sinEleFlag = 0
                DNNhelicoidflag = 0
                unitcell_sel = Elemnum.get()
                address =r.get()
                value = ElemIQ01.get()
                print("IQ address to update: 0x0" + str(address))
                print("IQ value sending:0x" + str(value))
                singleElementI2Csetting(0,int(unitcell_sel))
                ElemlabelIQ01.config(text ="Value updated on address 0x0" + str(address)+ " with value " +str(hex(int(value))))
                time.sleep(0.1)
                IQSingleflag = 0
            if ManulaCodeflag == 1:
                CustomcodI2Csetting()
                ManulaCodeflag = 0
                ManualCodestatus.config(text = "Code sent!")
                time.sleep(1)
                ManualCodestatus.config(text = "Enter the data")
            else:
                pass
                
    thread = threading.Thread(target=Thread1,daemon=True).start()

    def hardreset():
        global thread
        # ResetBut1.config(text="Resetting....")
        i2c = board.I2C()
        # i2c = board.STEMMA_I2C()
        while not i2c.try_lock():
            pass
        print("I2C addresses found:",[hex(device_address) for device_address in i2c.scan()])
        i2c.unlock()
        NanoSlave= i2c.scan()
        time.sleep(3)
        # ResetBut1.config(text="Reset")

    #$--------(Layout)Helical array entry--------
    
    
    #$1-------title
    my_label=Label(second_frame,text="8x8 helical array steering GUI ",font=("Helvetica",18))
    my_label.pack(padx=00,pady=10)

    #$1-------hard reset 
    ResetBut1 = Button(second_frame, text="Reset",command =hardreset)
    ResetBut1.place(x=ResetButX1,y=ResetButY1)  

    #$2-------single element entry
    Phase1label=Label(root,text="Enter the element number and phase: ",font=("Helvetica",13))
    Phase1label.place(x=P1LX,y=P1LY)

    Elemlabel=Label(root,text="Element No. :",font=("Helvetica",10))
    Elemlabel.place(x=ElemlabelX1,y=ElemlabelY1)
    Elemnum = Entry (root,width=2)
    Elemnum.place(x=ElemnumX,y=ElemnumY)
    Elemnum.insert(0,"0")
    

    Elemlabel2=Label(root,text="Phase:",font=("Helvetica",10))
    Elemlabel2.place(x=ElemlabelX2,y=ElemlabelY2)
    Elempha = Entry (root,width=4)
    Elempha.place(x=ElemnumphaX,y=ElemnumphaY)
    Elempha.insert(0,"0")

    Phase1shiftlab =Label(root,text=" Nan" ,font=("Helvetica",10))
    Phase1shiftlab.place(x=phase1shflabX,y=phase1shflabY)
    ConfirmBut1 = Button(root, text="enter",command =singlekey)
    ConfirmBut1.place(x=ConfirButX1,y=ConfirButY1)

    #$2.5-------single element Sweeping entry
    Elemlabel3=Label(root,text="Sweeping Phase:",font=("Helvetica",10))
    Elemlabel3.place(x=ElemlabelX3,y=ElemlabelY3)
    Elempha3 = Entry (root,width=3)
    Elempha3.place(x=ElemnumphaX3,y=ElemnumphaY3)
    Elempha3end = Entry (root,width=3)
    Elempha3end.place(x=ElemnumphaX3end,y=ElemnumphaY3end)
    Elempha3.insert(0,"0")
    Elempha3end.insert(0,"0")
    ConfirmBut0 = Button(root, text="Sweep enter",command =sweepsinglekey)
    ConfirmBut0.place(x=ConfirButX0,y=ConfirButY0)

    #$2.5.5-------single element IQ setting entry
    ElemlabelIQ01=Label(root,text="Ender IQ Value:",font=("Helvetica",10))
    ElemlabelIQ01.place(x=ElemIQ01LX,y=ElemIQ01LY)
    ElemIQ01 = Entry (root,width=6)
    ElemIQ01.place(x=ElemIQ01EX,y=ElemIQ01EY)
    ElemIQ01.insert(0,"0")

    r =IntVar()
    
    r.set("1")
    
    IQaddname = ["Gain(0x01):"
                 ,"Offset I-channel(0x02):"
                 ,"Offset Q-channel(0x03):"
                 ,"I/Q Gain Ratio(0x04):"
                 ,"I/Q Phase Balance(0x05):"
                 ,"LO Port Matching Override(0x06):"
                 ,"Temperature Correction Override(0x07):"
                 ,"Operating Mode(0x08):"
                ]
    for i in range(len(IQaddname)):
        Radiobutton(root,text=IQaddname[i],variable =r,value=i+1).place(x=IQRadiobutX,y=IQRadiobuty+i*25)
       
    IQConfirmBut = Button(root, text="IQ enter",command =IQsinglekey)
    IQConfirmBut.place(x=IQConfirButX,y=IQConfirButY)

    #$2.5.6-------Excel Amplitude loading 
    Ar =IntVar()
    
    Ar.set("1")
    
    TapeOrNot = ["Tapping"
                 ,"No Tapping"
                ]
    for i in range(len(TapeOrNot)):
        Radiobutton(root,text=TapeOrNot[i],variable =Ar,value=i+1).place(x=P3LX+300,y=P3LY+20+i*25)

    #$2.5.5.5--------Manual code insert
    IQShortname= ["Gain","Offset I","Offset Q" ,"I/Q Gain","I/Q Phase","LO PMO","Temp","mode","DAC Q","DAC I"]
    IQAddress=["(0x1)","(0x2)","(0x3)","(0x4)","(0x5)","(0x6)","(0x7)","(0x08)","(49)","(56)"]
    for i in range(len(IQShortname)):
        Label(root,text= IQShortname[i],font=("Helvetica",10)).place(x=FUlabelX+ spacing*i,y=FUlabelY) 
        Label(root,text= IQAddress[i],font=("Helvetica",10)).place(x=FUlabelX+ spacing*i,y=FUlabelY+20) 
    FU1= Entry (root,width=5)
    FU1.place(x=FU1EX,y=FU1EY)
    FU1.insert(0,int("0x84",16))
    FU2 = Entry (root,width=5)
    FU2.place(x=FU2EX,y=FU2EY)#
    FU2.insert(0,int("0x80",16))
    FU3 = Entry (root,width=5)
    FU3.place(x=FU3EX,y=FU3EY)
    FU3.insert(0,int("0x80",16))
    FU4 = Entry (root,width=5)
    FU4.place(x=FU4EX,y=FU4EY)
    FU4.insert(0,int("0x80",16))
    FU5 = Entry (root,width=5)
    FU5.place(x=FU5EX,y=FU5EY)
    FU5.insert(0,int("0x10",16))
    FU6 = Entry (root,width=5)
    FU6.place(x=FU6EX,y=FU6EY)
    FU6.insert(0,int("0x50",16))
    FU7 = Entry (root,width=5)
    FU7.place(x=FU7EX,y=FU7EY)
    FU7.insert(0,int("0x06",16))
    FU8 = Entry (root,width=5)
    FU8.place(x=FU8EX,y=FU8EY)
    FU8.insert(0,int("0x00",16))

    CodeConfirmBut = Button(root, text="Man. Enter",command = ManulaCodekey).place(x=MCEnterButX,y=MCEnterButY)
    ManualCodestatus=Label(root,text=" Code Standby ",font=("Helvetica",10))
    ManualCodestatus.place(x=MCEnterButX-300,y=MCEnterButY+80) 

    Qslicer = Scale(root,from_=4369,to=61166)
    Qslicer.place(x=FU9EX,y=FU9EY)
    Qslicer.set("32768")
    QEntry = Entry (root,width=5)
    QEntry.place(x=FU9EX+20,y=FU9EY+120)
    QEntry.insert(0,"32768")

    Islicer = Scale(root,from_=4369,to=61166)
    Islicer.place(x=FU10EX,y=FU10EY)
    Islicer.set("32768")
    IEntry = Entry (root,width=5)
    IEntry.place(x=FU10EX+20,y=FU10EY+120)
    IEntry.insert(0,"32768")

    DACname =["slider","Number input"]
    cr = IntVar()
    cr.set("1")
    for i in range(len(DACname)):
        Radiobutton(root,text=DACname[i],variable =cr,value=i+1).place(x=FU9EX+40,y=FU9EY-120+i*25)

    #$2.5.5.b-------singlemanual code mode select 
    singlemode = ["IQ pack update only"
                  ,"DAC update only"
                  ,"IQ and DAC update"]
    mr = IntVar()
    mr.set("9")
    for i in range(len(singlemode)):
        Radiobutton(root,text= singlemode[i],variable =mr,value=i+len(IQaddname)+1).place(x=singleModeselX,y=singleModeselY+i*25)

    #$2.9-------8x1 manual setting
    CellEntry = [0 for x in range(8)]
    LAMEntry = [0 for x in range(8)]
    Celllable =[0 for x in range(8)]
    Celllabelcontent = ["No1"
                        ,"No2"
                        ,"No3"
                        ,"No4"
                        ,"No5"
                        ,"No6"
                        ,"No7"
                        ,"No8"
                        ,"No9"]
    UCNO=range(32,40)
    for x in range(len(CellEntry)):
        CellEntry[x] = Entry (root,width=5)
        CellEntry[x].place(x=630+60*x,y=680)
        
        CellEntry[x].insert(0,str(UCNO[x]))
        LAMEntry[x] = Entry (root,width=5)
        LAMEntry[x].place(x=630+60*x,y=710)
        Celllable[x] =Label(root,text=Celllabelcontent[x],font=("Helvetica",8))
        Celllable[x].place(x=630+60*x,y=660)
    
    ConfirmBut = Button(root, text="Linearload",command =linearkey)
    ConfirmBut.place(x=670+60*7,y=720)
    Label(root,text="Cell No. :",font=("Helvetica",8)).place(x=570,y=680)
    Label(root,text="phase input:",font=("Helvetica",8)).place(x=550,y=710)

    #$3-------8x8 entry
    Phase2label=Label(root,text="Helicalarray phi steering angle: ",font=("Helvetica",13))
    Phase2label.place(x=P2LX,y=P2LY)
    Phase2Value = Entry (root,width=5)
    Phase2Value.place(x=phase2staX,y=phase2staY)
    Phase2Value.insert(0,"1")
    Phase2shiftlab =Label(root,text=" Nan" ,font=("Helvetica",10))
    Phase2shiftlab.place(x=phase2shflabX,y=phase2shflabY)

    ConfirmBut = Button(root, text="enter",command =helicalkey)
    ConfirmBut.place(x=ConfirButX2,y=ConfirButY2)
   
    #$4-------DNN
    Phase3label=Label(root,text="DNN Helicalarray phi steering angle: ",font=("Helvetica",13))
    Phase3label.place(x=P3LX,y=P3LY)
    Phase3Value = Entry (root,width=5)
    Phase3Value.place(x=phase3staX,y=phase3staY)
    Phase3Value.insert(0,"1")
    Phase3shiftlab =Label(root,text=" Nan" ,font=("Helvetica",10))
    Phase3shiftlab.place(x=phase3shflabX,y=phase3shflabY)

    ConfirmBut3 = Button(root, text="enter",command =h5DNNhelicalkey)
    ConfirmBut3.place(x=ConfirButX3,y=ConfirButY3)

    #$5-------Manualphase load from Excel
    Label(root,text="Manual Excel load phase: ",font=("Helvetica",13)).place(x=P3LX,y=P3LY+50)
    Phase4Value = Entry (root,width=40)
    Label(root,text="/REV BeamSteeringData/",font=("Helvetica",8)).place(x=phase3staX-330,y=phase3staY+75)
    Phase4Value.place(x=phase3staX-190,y=phase3staY+75)
    Phase4Value.insert(0,"CalibratedResult")
   
    ConfirmBut4 = Button(root, text="enter",command =Excelloadkey)
    ConfirmBut4.place(x=ConfirButX3,y=ConfirButY3+50)

   #$End============app start
    root.mainloop()
