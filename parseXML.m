% 3/4/2016
% XML parser for TomTec Output files 
% Adam Rauff

% choose xml file to parse
myFile = '/Users/adamrauff/Desktop/LV Project/XML Parser/TomTec Data/phtn0268_main_saxmid_ra_3bts.xml';

% read xml file to obtain the DOM - Document Object Method
xDoc = xmlread(myFile);

% find all elements in the "Data worksheet"
WorkSheets = xDoc.getElementsByTagName('Worksheet');