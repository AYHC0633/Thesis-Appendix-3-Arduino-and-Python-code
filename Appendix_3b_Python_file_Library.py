# Write your code here :-)
#import smbus2 # I2C module
import sys

import matplotlib
import numpy as np
import pandas as pd
import time
from operator import add
import tensorflow as tf
from scipy.signal import savgol_filter

def fileloading(): # loading a excel only for speeding up program
    df = pd.read_excel('SteeringBeamTableWithP1AccuracyV2.xlsx')
    return df

def Searching(degree,df): # LTC5589 +DAC configuration
    # df = pd.read_excel('SteeringBeamTable.xlsx')#file path: /home/pi/Documents
    aa = df.loc[np.round(df["Degree"],1)  == np.round(degree,1)]
    aa = aa.index[0]
    return int(aa)

def fileloadingmodule(): # LTC5589 +DAC configuration
    # df = pd.read_excel('SteeringBeamTable.xlsx')#file path: /home/pi/Documents
    df = pd.read_excel('SteeringBeamTableWithP1AccuracyV2.xlsx')
    array1 = [[0 for x in range(len(df.columns))] for x in range(len(df.index))]
    for degree in range(len(df.index)):
        for x in range(len(df.columns)):
            array1[degree][x] = df.iloc[degree,x]
    #vhex = np.vectorize(hex)
    #array = vhex(array)
    #print(df)

    for x in range (7):#Trimp the array because of code limit
        array1 = np.delete(array1,1,axis=1)

    return np.array(array1)

def fileloadingmoduleV2():# amp1 =0, amp0.95=1 ...
    xl = pd.ExcelFile('SteeringBeamTableWithP1AccuracyV5.xlsx')

    phaselist = [0 for x in range(len(xl.sheet_names))]
    for x in range(len(xl.sheet_names)): 
        aa = np.array(xl.parse(xl.sheet_names[x]))   
        for xx in range (7):#Trimp the array because of code limit
            aa = np.delete(aa,1,axis=1)
        phaselist[x] = aa
        # print(xl.sheet_names[x])
    # print(phaselist[2])
    # print(xl.sheet_names.index('Amp1'))
    return phaselist

def fileloadingmoduleV2namesearchV2(Ampvalue):
    xl = pd.ExcelFile('SteeringBeamTableWithP1AccuracyV5.xlsx')#Range from 1 to 0
    value= round(Ampvalue* 2,1) / 2
    # print(value)
    if value<=0.2:
       value = 0.2
    aa = xl.sheet_names.index('Amp'+str(value))
    return int(aa)

def fileloadingmoduleNameSearch(degree): # LTC5589 +DAC configuration
    # df = pd.read_excel('SteeringBeamTable.xlsx')#file path: /home/pi/Documents
    df = pd.read_excel('SteeringBeamTableWithP1Accuracy.xlsx')
    aa = df.loc[np.round(df["Degree"],1)  == np.round(degree,1)]
    aa = aa.index[0]
    return int(aa)

def NanoControlFile():# 8x8 helical array configuration 
    df = pd.read_excel('PhaseShiftFileforCassieInAzumith.xlsx')#file path: /home/pi/Documents
    #df.head()
    array2 = [[0 for x in range(363)] for x in range(64)]
    for Element in range(64):
        for degree in range(363):
            array2[Element][degree] = df.iloc[Element,degree]
       
    return np.array(array2) #it will return the phase of that element

def fileloadingmoduleforlineararray():# 8x1 helical array configuration 
    df = pd.read_excel('ArrayFactorShiftFileforCassieInAzumith_8x1.xlsx')#file path: /home/pi/Documents
    #df.head()
    array1 = [[0 for x in range(362)] for x in range(8)]
    for angle in range(362):
        for x in range(8):
            array1[x][angle] = df.iloc[x,angle]
    #vhex = np.vectorize(hex)
    #array = vhex(array)
    #print(df)
    return np.array(array1)

##--------------------------first file version for 8x8 helicoid array
def fileloadingmoduleforhelicoidNamesearch():
    # df = pd.read_excel('PhaseShiftFileforCassieInAzumith.xlsx')#file path: /home/pi/Documents
    # df = pd.read_excel('8x8PhaseShiftFileforCassieInAzumithclockwise.xlsx')
    df = pd.read_excel('8x8PhaseShiftFileforCassieInAzumithclockwiseP1accuracy.xlsx')
    indexarray = [0 for x in range(len(df.columns))]
    for col in range(len(df.columns)):
        indexarray[col] = df.columns[col]
    return indexarray

def fileloadingmoduleforhelicoid():
    # df = pd.read_excel('PhaseShiftFileforCassieInAzumith.xlsx')#file path: /home/pi/Documents
    # df = pd.read_excel('8x8PhaseShiftFileforCassieInAzumithclockwise.xlsx')
    df = pd.read_excel('8x8PhaseShiftFileforCassieInAzumithclockwiseP1accuracy.xlsx')
    
    #df.head()
    array1 = [[0 for x in range(len(df.columns))] for x in range(len(df.index))]
    # for col in df.columns:
    #     print(col)
    for angle in range(len(df.columns)):
        for x in range(len(df.index)):
            array1[x][angle] = df.iloc[x,angle]
    #vhex = np.vectorize(hex)
    #array = vhex(array)
    #print(df)
    return np.array(array1)

##--------------------------Second file version for 8x8 helicoid array
def fileloadingmoduleforhelicoidNamesearchV2():
    df = pd.read_excel('8x8PhaseShiftFileforCassieInAzumithZeroP1accuracy.xlsx')#file path: /home/pi/Documents
    indexarray = [0 for x in range(len(df.columns))]
    for col in range(len(df.columns)):
        indexarray[col] = df.columns[col]
    return indexarray

def fileloadingmoduleforhelicoidV2():
    df = pd.read_excel('8x8PhaseShiftFileforCassieInAzumithZeroP1accuracy.xlsx')#file path: /home/pi/Documents
    #df.head()
    array1 = [[0 for x in range(df.shape[1]-3)] for x in range(df.shape[0])]
    # for col in df.columns:
    # print(col)
    for angle in range(df.shape[1]-3):
        for x in range(df.shape[0]):
            array1[x][angle] = df.iloc[x,angle]
    #vhex = np.vectorize(hex)
    #array = vhex(array)
    #print(df)
    return np.array(array1)

##-------------------------third file version for 8x8 helical array 
def fileloadingmoduleforhelicoidNamesearchV3():
    df = pd.read_excel('8x8PSfCAzClk0p1V2.xlsx')#file path: /home/pi/Documents
    indexarray = [0 for x in range(len(df.columns))]
    for col in range(len(df.columns)):
        indexarray[col] = df.columns[col]
    return indexarray

def fileloadingmoduleforhelicoidV3():
    df = pd.read_excel('8x8PSfCAzClk0p1V2.xlsx')#file path: /home/pi/Documents
    #df.head()
    array1 = [[0 for x in range(df.shape[1]-3)] for x in range(df.shape[0])]
    # for col in df.columns:
    # print(col)
    for angle in range(df.shape[1]-3):
        for x in range(df.shape[0]):
            array1[x][angle] = df.iloc[x,angle]
    #vhex = np.vectorize(hex)
    #array = vhex(array)
    #print(df)
    return np.array(array1)



##------------------------- DNN model
def DNNphaseOut(theta,phi):#linear array
    import sys
    import tensorflow as tf
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import tensorboard
    from datetime import datetime
    from packaging import version
    from tensorflow import keras

    # print(tf.__version__)
    # print(tf.config.list_physical_devices())
    # #print(tf.sysconfig.get_build_info()['cuda_version'])
    RTD = 180/np.pi
    # #print(tf.sysconfig.get_build_info()['cudnn_version'])
    #interpreter = tf.lite.Interpreter(model_path="TestHelicoidModel_V1Mk4_MC_SupersmallSizemodel.tflite")
    interpreter = tf.lite.Interpreter(model_path="TestlinearArrayV1Mk1_SupersmallSizemodel.tflite")
    interpreter.allocate_tensors()

    #2 ---------------Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    #3---------------------------Test model on random input data
    
    input_data = tf.constant([phi/359,(theta-81)/(96-81)], shape=[1,2], dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    #4-----------------------The function `get_tensor()` returns a copy of the tensor data, Use `tensor()` in order to get a pointer to the tensor
    # output_data =np.mod(interpreter.get_tensor(output_details[0]['index'])*RTD,360)#<---remember what is the output answer
    output_data =np.mod(interpreter.get_tensor(output_details[0]['index']),360)

    output_data = output_data.astype('int64')
    output_data = output_data.reshape(-1)
    # print(output_data)
    return output_data

def DNNphaseOutHelicoid(theta,phi):#Helical array
    import sys
    import tensorflow as tf
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import tensorboard
    from datetime import datetime
    from packaging import version
    from tensorflow import keras

    # print(tf.__version__)
    # print(tf.config.list_physical_devices())
    # #print(tf.sysconfig.get_build_info()['cuda_version'])
    RTD = 180/np.pi
    # #print(tf.sysconfig.get_build_info()['cudnn_version'])
    # interpreters = tf.lite.Interpreter(model_path="TestHelicoidModel_V1Mk4_MC_SupersmallSizemodel.tflite")
    interpreters = tf.lite.Interpreter(model_path="Test8x8HelicoidModel_V1Mk6_MC_clockwise.tflite")
    
    interpreters.allocate_tensors()

    #2 ---------------Get input and output tensors.
    input_detailss = interpreters.get_input_details()
    output_detailss = interpreters.get_output_details()

    #3---------------------------Test model on random input data
  
    input_dataa = tf.constant([[phi/359,(theta-80)/(100-80)]], shape=(1,2,1), dtype=np.float32)
  
    interpreters.set_tensor(input_detailss[0]['index'],input_dataa)
    interpreters.invoke()

    #4-----------------------The function `get_tensor()` returns a copy of the tensor data, Use `tensor()` in order to get a pointer to the tensor
    output_data =np.mod(interpreters.get_tensor(output_detailss[0]['index'])*RTD,360)#<---remember what is the output answer
    # output_data =np.mod(interpreters.get_tensor(output_detailss[0]['index']),360)
    
    # output_data = output_data.astype('int64')
    # output_data = np.round(output_data,1)
    output_data = output_data.reshape(-1)
    print(output_data)
    return output_data

def DNNsetuponGUI():#forGUI only
    import sys
    import tensorflow as tf
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import tensorboard
    from datetime import datetime
    from packaging import version
    from tensorflow import keras

    # print(tf.__version__)
    # print(tf.config.list_physical_devices())
    # #print(tf.sysconfig.get_build_info()['cuda_version'])
    RTD = 180/np.pi
    # #print(tf.sysconfig.get_build_info()['cudnn_version'])
    # interpreters = tf.lite.Interpreter(model_path="TestHelicoidModel_V1Mk4_MC_SupersmallSizemodel.tflite")
    interpreters = tf.lite.Interpreter(model_path="Test8x8HelicoidModel_V1Mk6_MC_clockwise.tflite")
    
    interpreters.allocate_tensors()
    return interpreters

def DNNoutForGUI(theta,phi,interpreters):#forGUI only
    RTD = 180/np.pi
    #2 ---------------Get input and output tensors.
    input_detailss = interpreters.get_input_details()
    output_detailss = interpreters.get_output_details()

    #3---------------------------Test model on random input data
  
    input_dataa = tf.constant([[phi/359,(theta-80)/(100-80)]], shape=(1,2,1), dtype=np.float32)
  
    interpreters.set_tensor(input_detailss[0]['index'],input_dataa)
    interpreters.invoke()

    #4-----------------------The function `get_tensor()` returns a copy of the tensor data, Use `tensor()` in order to get a pointer to the tensor
    output_data =np.mod(interpreters.get_tensor(output_detailss[0]['index'])*RTD,360)#<---remember what is the output answer
    # output_data =np.mod(interpreters.get_tensor(output_detailss[0]['index']),360)
    
    # output_data = output_data.astype('int64')
    # output_data = np.round(output_data,1)
    output_data = output_data.reshape(-1)
    print(output_data)
    return output_data

def DNNh5loadForGUI():
    def custom_loss(y_true, y_pred):
        # Calculate loss
        DTR = tf.constant((np.pi/180.))
        #loss = (tf.reduce_sum(((tf.math.cos(y_pred*DTR)-tf.math.cos(y_true*DTR))**2))/8) +(tf.reduce_sum(((tf.math.sin(y_pred*DTR)-tf.math.sin(y_true*DTR))**2))/8)
        #loss =  ((((tf.math.cos(y_pred)-tf.math.cos(y_true)))**2) +(((tf.math.sin(y_pred)-tf.math.sin(y_true)))**2))*tf.math.cos(y_true-y_pred)**2#<-- this is in radian
        loss = (((tf.math.cos(y_pred)-tf.math.cos(y_true)))**2) +(((tf.math.sin(y_pred)-tf.math.sin(y_true)))**2)
        #loss = tf.math.cos((y_true-y_pred)**2)
        return  tf.reduce_mean(loss) # tf.keras.losses.mae #loss
    model = tf.keras.models.load_model("TestHelicoidModel_V1Mk4_MC_SupersmallSizemodel.h5", custom_objects={'custom_loss': custom_loss})
    model.load_weights("TestHelicoidModel_V1Mk4_MC_SupersmallSizemodel.h5")
    return model

##-------------------------cable calibration-----------

def calibratedElement(ArrayPhase,Layer):
    # UnitcellPhaseMapCAl = [180,175,185,200,178,170,178,178,178,178]#phase Zeroing (unitcell number listing: [1 2 3 4 9 6 7 10])

    # cableoffset = [0,4,-2,0,2,10,-1,0]

    # totalphaseshift = list(map(add,UnitcellPhaseMapCAl,cableoffset))

    # finalphase = np.mod(list(map(add,ArrayPhase,totalphaseshift)),360)

    NewUnitcellPhaseMapCAlV2 = [200,178,170,178,200,185,175,180
                              ,200,200,188,205,205,190,178,178
                              ,205,195,195,195,208,195,210,170
                              ,210,205,215,201,210,195,200,189
                              ,195,200,155,182,204,205,198,190
                              ,197,184,198,220,210,200,185,205
                              ,190,190,207,203,206,201,188,188
                              ,198,213,208,215,203,207,210,197]
    # oldUnitcellPhaseMapCAlV2 = [180,175,185,200,178,170,178,200
    #                          ,178,178,190,205,205,188,200,202
    #                          ,170,210,195,208,195,195,195,205
    #                          ,189,200,195,210,201,215,205,210
    #                          ,190,198,205,204,182,155,200,195
    #                          ,205,185,200,210,220,198,184,197
    #                          ,188,188,201,206,203,207,190,190
    #                          ,197,210,207,203,215,208,213,198]
                             
    newcableoffsetV2 = [100,99,110,102,100,98,104,100
                        ,100,92,92,92,90,86,92,86
                        ,90,69,93,68,86,90,90,85
                        ,70,88,93,90,91,92,90,69
                        ,90,90,89,88,90,92,92,90
                        ,91,88,88,93,92,84,73,94
                        ,91,87,68,43,93,-4,63,-10
                        ,93,93,89,91,91,93,89,90]
    # oldcableoffsetV2 = [100,104,98,100,102,110,99,100
    #                 ,86,92,86,90,92,92,92,100
    #                 ,85,90,90,86,68,93,69,90
    #                 ,69,90,92,91,90,93,88,70
    #                 ,90,92,92,90,88,89,90,90
    #                 ,94,73,84,92,93,88,88,91
    #                 ,-10,63,-4,93,43,68,87,91
    #                 ,90,89,93,91,91,89,93,93]

   
    
    splitter14 = [35,38,40,39
                  ,33,35,35,34
                    ,33,35,36,34
                    ,31,33,33,33
                    ,31,33,35,33
                    ,35,35,33,30
                    ,33.4,35,36,34
                    ,34,35,34,27
                    ,32,35,37,37
                    ,38,37,39,34
                    ,32,34,33,35
                    ,34,35,36,32
                    ,36,37,36,37
                    ,33,34,26,23
                    ,31,34,32,25
                    ,20,22,33,32]  # normalise with phase 34
    splitter14 = [x - 34 for x in splitter14]# setting offset 

    splitter116 = ([-47 for x in range(4)]
                   +[-48 for x in range(4)]
                   +[-47 for x in range(4)]
                   +[-47 for x in range(4)]
                   +[-42 for x in range(4)]
                   +[16 for x in range(4)]
                   +[-47 for x in range(4)]
                   +[-46 for x in range(4)]
                   +[-45 for x in range(4)]
                   +[-42 for x in range(4)]
                   +[-45 for x in range(4)]
                   +[-44 for x in range(4)]
                   +[-51 for x in range(4)]
                   +[-55 for x in range(4)]
                   +[-46 for x in range(4)]
                   +[-42 for x in range(4)])
    splitter116 = [x + 48 for x in splitter116]# setting offset 

    totalphaseshiftV2 = list(map(add,NewUnitcellPhaseMapCAlV2,newcableoffsetV2))
    totalphaseshift14V2=list(map(add,totalphaseshiftV2,splitter14))
    totalphaseshift14116V2=list(map(add,totalphaseshift14V2,splitter116))
    # finalphaseV2 = np.mod(list(map(add,ArrayPhase,totalphaseshiftV2)),360)
    totalphaseshift14116V2 =totalphaseshift14116V2[(8*(Layer)):(8*(Layer)+8)]
    finalphase =np.mod(list(map(add,totalphaseshift14116V2,ArrayPhase)),360)

    return finalphase

def calibratedElementV2(ArrayPhase):
    

    NewUnitcellPhaseMapCAlV2 = [200,178,170,178,200,185,175,180
                              ,200,200,188,205,205,190,178,178
                              ,205,195,195,195,208,195,210,170
                              ,210,205,215,201,210,195,200,189
                              ,195,200,155,182,204,205,198,190
                              ,197,184,198,220,210,200,185,205
                              ,190,190,207,203,206,201,188,188
                              ,198,213,208,215,203,207,210,197]
    # oldUnitcellPhaseMapCAlV2 = [180,175,185,200,178,170,178,200
    #                          ,178,178,190,205,205,188,200,202
    #                          ,170,210,195,208,195,195,195,205
    #                          ,189,200,195,210,201,215,205,210
    #                          ,190,198,205,204,182,155,200,195
    #                          ,205,185,200,210,220,198,184,197
    #                          ,188,188,201,206,203,207,190,190
    #                          ,197,210,207,203,215,208,213,198]
                             
    newcableoffsetV2 = [100,99,110,102,100,98,104,100
                        ,100,92,92,92,90,86,92,86
                        ,90,69,93,68,86,90,90,85
                        ,70,88,93,90,91,92,90,69
                        ,90,90,89,88,90,92,92,90
                        ,91,88,88,93,92,84,73,94
                        ,91,87,68,43,93,-4,63,-10
                        ,93,93,89,91,91,93,89,90]
    # oldcableoffsetV2 = [100,104,98,100,102,110,99,100
    #                 ,86,92,86,90,92,92,92,100
    #                 ,85,90,90,86,68,93,69,90
    #                 ,69,90,92,91,90,93,88,70
    #                 ,90,92,92,90,88,89,90,90
    #                 ,94,73,84,92,93,88,88,91
    #                 ,-10,63,-4,93,43,68,87,91
    #                 ,90,89,93,91,91,89,93,93]

   
    
    splitter14 = [35,38,40,39
                  ,33,35,35,34
                    ,33,35,36,34
                    ,31,33,33,33
                    ,31,33,35,33
                    ,35,35,33,30
                    ,33.4,35,36,34
                    ,34,35,34,27
                    ,32,35,37,37
                    ,38,37,39,34
                    ,32,34,33,35
                    ,34,35,36,32
                    ,36,37,36,37
                    ,33,34,26,23
                    ,31,34,32,25
                    ,20,22,33,32]  # normalise with phase 34
    splitter14 = [x - 34 for x in splitter14]# setting offset 

    splitter116 = ([-47 for x in range(4)]
                   +[-48 for x in range(4)]
                   +[-47 for x in range(4)]
                   +[-47 for x in range(4)]
                   +[-42 for x in range(4)]
                   +[16 for x in range(4)]
                   +[-47 for x in range(4)]
                   +[-46 for x in range(4)]
                   +[-45 for x in range(4)]
                   +[-42 for x in range(4)]
                   +[-45 for x in range(4)]
                   +[-44 for x in range(4)]
                   +[-51 for x in range(4)]
                   +[-55 for x in range(4)]
                   +[-46 for x in range(4)]
                   +[-42 for x in range(4)])
    splitter116 = [x + 48 for x in splitter116]# setting offset 

    totalphaseshiftV2 = list(map(add,NewUnitcellPhaseMapCAlV2,newcableoffsetV2))
    totalphaseshift14V2=list(map(add,totalphaseshiftV2,splitter14))
    totalphaseshift14116V2=list(map(add,totalphaseshift14V2,splitter116))
    # finalphaseV2 = np.mod(list(map(add,ArrayPhase,totalphaseshiftV2)),360)
    finalphaseV2 =np.mod(list(map(add,totalphaseshift14116V2,ArrayPhase)),360)
    return finalphaseV2

def calibratedElementV3(ArrayPhase):
    NewUnitcellPhaseMapCAlV2 = [15,297,88,8,353,359,355,7
                              ,15,297,88,8,353,359,355,7
                              ,15,297,88,8,353,359,355,7
                              ,15,297,88,8,353,359,355,7
                              ,15,297,88,8,353,359,355,7
                              ,15,297,88,8,353,359,355,7
                              ,15,297,88,8,353,359,355,7
                              ,15,297,88,8,353,359,355,7]
    finalphaseV3 =np.mod(list(map(add,NewUnitcellPhaseMapCAlV2,ArrayPhase)),360)
    print(finalphaseV3)
    return finalphaseV3

##-------------------------EVR calibration-----------
def EVRcalibratedElementV4(ArrayPhase):
    try:
        print("Phase Input:" +str(ArrayPhase))
        df = pd.read_excel("LoadingResultonCalibratedResult90V2.xlsx")
        offsetdata = np.array(df['Offset'])
        finalphaseV4 =np.mod(list(map(lambda x, y: 360-x - y,offsetdata,ArrayPhase)),360)
        print("After calibrated phase" + str(finalphaseV4))
        print("Active phase loading successful!")
        return finalphaseV4
    except:
        calibratedElementV3(ArrayPhase)   
        print("Active phase loading fail!")

def EVRcalibratedElementV0(ArrayPhase):
    try:
        finalphaseV0 =np.mod(list(ArrayPhase),360)
        print(finalphaseV0)
        print("Plane phase loading successful!")
        return finalphaseV0
    except:
        calibratedElementV3(ArrayPhase)   
        print("Active phase loading fail!")
    

##---------------------data processing

def bytes(integer):
    return divmod(integer, 0x100)

def CurveSmmothing(y,pylomu):
    window = int(round(len(y)/5,0))
   
    yhat = savgol_filter(y, window,pylomu)#savgol_filter(y, 51, 3) # window size 51, polynomial order 3
    return list(yhat)
