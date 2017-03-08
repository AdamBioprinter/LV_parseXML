import xml.etree.ElementTree as ET
from itertools import zip_longest
import numpy as np
import sys
import scipy.io as sio
import parseXML
import os

# obtain directory supplied by user that contains all xml files desired to parse
myDir = sys.argv[1]

# obtain list of all xml files in folder's direct child (no subdirectories within)
dirs = os.listdir(myDir)
FilList = []
for files in dirs:
  filesL = files.lower()
  if filesL.endswith('.xml'):
    FilList.append(os.path.join(myDir, files))

for file in FilList:
  parseXML.parseXML(file)
