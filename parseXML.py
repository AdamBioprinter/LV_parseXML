import xml.etree.ElementTree as ET
from itertools import zip_longest
import numpy as np
import sys
import scipy.io as sio
import os

# must supply the file name for parsing
# myFile = sys.argv[1]
def parseXML(myFile):
  # myFile = 'TomTec Data/phtn0268_main_saxmid_70%_3bts.xml'

  tree = ET.parse(myFile)
  root = tree.getroot()

  # Excel Hierarchy:
  # Worsheet --> Table --> Row --> Cell --> Data

  DataWS = []
  EndoXWS = []
  EndoYWS = []
  for child in root:
    # Save information in the Data Worksheet to a python list
    # Much easier to deal with when pulling information
    if 'Worksheet' in child.tag and 'Data' in  child.attrib.values():

      # iterate through all rows, the [0] indexing is to step into table
      for i, row in enumerate(child[0]):
        if i > 0:
          DataWS.append(RowLis)
          RowLis = []
        else:
          RowLis = []
        for j, cell in enumerate(row):
          RowLis.append(cell[0].text)

    if 'Worksheet' in child.tag and 'EndoX' in child.attrib.values():

      # iterate through all rows, the [0] indexing is to step into table
      for i, row in enumerate(child[0]):
        if i > 0:
          EndoXWS.append(RowLis)
          RowLis = []
        else:
          RowLis = []
        for j, cell in enumerate(row):
          RowLis.append(cell[0].text)
    
    if 'Worksheet' in child.tag and 'EndoY' in child.attrib.values():

      # iterate through all rows, the [0] indexing is to step into table
      for i, row in enumerate(child[0]):
        if i > 0:
          EndoYWS.append(RowLis)
          RowLis = []
        else:
          RowLis = []
        for j, cell in enumerate(row):
          RowLis.append(cell[0].text)

  # Transposing WS for easier access to row index
  DataWS2 = list(map(list, zip_longest(*DataWS)))
  EndoXWS2 = list(map(list, zip_longest(*EndoXWS)))
  EndoYWS2 = list(map(list, zip_longest(*EndoYWS)))

  # -------------------------------------------------------------
  # Extraction info from Data Worksheet
  Date = DataWS[0][0]
  # find index of patient ID
  PID = DataWS2[1][DataWS2[0].index('PatientID:')]
  Bpm = DataWS2[1][DataWS2[0].index('Bpm')]
  EsFr = DataWS2[2][DataWS2[0].index('es')]
  EsT = DataWS2[4][DataWS2[0].index('es')]
  EdFr = DataWS2[2][DataWS2[0].index('ed')]
  EdT = DataWS2[4][DataWS2[0].index('ed')]

  PixDim, i = [(y[1], i) for i, y in enumerate(DataWS) if 'PixelDimension' in y][0]
  PixUnits = DataWS[i][2]

  RWind = [i for i, L in enumerate(DataWS) if 'RWaves' in L][0]
  Rwaves = np.array([x for x in DataWS[RWind+1] if x is not None], dtype='float32')
  FrTind = [i for i, L in enumerate(DataWS) if 'FrameTime(ms)' in L][0]
  FrT = np.array([x for x in DataWS[FrTind+1] if x is not None], dtype='float32')
  NumFr = len(FrT)
  TProgind = [i for i, L in enumerate(DataWS) if 'TimeProgression(ms)' in L][0]
  TP = np.array([x for x in DataWS[TProgind+1] if x is not None], dtype='float32')

  # clean the lists --> remove None, and convert strings to floats

  EDA = DataWS2[1][DataWS2[0].index('EDA')]
  EDAUnit = DataWS2[2][DataWS2[0].index('EDA')]

  print('Date: ', Date)
  print('PID: ', PID)
  print('Bpm: ',Bpm)
  print('EsFr: ',EsFr)
  print('EsT: ', EsT)
  print('PixDim: ',PixDim)
  print('PixUnits: ', PixUnits)
  print('RWaves: ',Rwaves)
  # print('TP: ',TP)
  # print('FrT: ',FrT)

  # ----------------------------------------------------------------------------------------
  # Extract info from EndoX worksheet
  # remove the text
  EndXL = [y for y in EndoXWS if not 'EndoX pixel coord' in y]
  EndXMat = np.array(EndXL[1:], dtype='float32')
  print('EndXMat: ',EndXMat)

  # ----------------------------------------------------------------------------------------
  EndYL = [y for y in EndoYWS if not 'EndoY pixel coord' in y]
  EndYMat = np.array(EndYL[1:], dtype='float32')
  print('EndYMat: ',EndYMat)

  # --------------------------------------------------------------------
  # save .mat file
  PID = PID.replace("\"","")
  sio.savemat(os.path.basename(myFile).replace('.xml','.mat'), \
      {'EndoX':EndXMat, 'EndoY':EndYMat, 'RWaves':Rwaves, 'TProg':TP, 'FrT':FrT, \
      'EDA':float(EDA), 'EDA_Unit':str(EDAUnit), 'Pix_Unit':PixUnits, 'PixDim':float(PixDim), \
      'EsT':EsT, 'EsFr':int(EsFr), 'EdFr':int(EdFr), 'EdT':EdT, \
      'Bpm':float(Bpm), 'Date':Date, 'PID':PID})
