"""Using arcpy to create and manipulate polyline feature classes"""
#Goals: 1. Create polyline feature class from oneline text file. Oneline.txt has one polyline object. 
#2. Create polyline feature class from Test text file, Test.txt has multiple polyline objects

#importing libraries

import arcpy

#setting workspace
arcpy.env.workspace= "C:\\Users\\kfear\\Python"

#allowing overwriting of exisiting files
arcpy.env.overwriteOutput=True

#Goal 1: Create polyline feature class from Oneline text file. 

#importing and reading files
oneLineFile=open("oneline.txt","r")
allLines=oneLineFile.readlines()

#Creating Oneline.shp in current folder:  setting projection as NAD83 North America
arcpy.CreateFeatureclass_management(arcpy.env.workspace,"Oneline.shp","POLYLINE",spatial_reference=arcpy.SpatialReference(4269))

#Adding first column to Oneline.shp
arcpy.AddField_management("Oneline.shp","LineID","TEXT","","",12)

#Create cursor to add rows to Oneline.shp
polyline_ins_cursor= arcpy.da.InsertCursor("Oneline.shp",["LineID", "SHAPE@"])

#Create point object
pnt=arcpy.Point()

#Create array to store all points
array=arcpy.Array()

#Loop through each line of Oneline.txt and retrieve points
for aLine in allLines:
    aListArgs=aLine.split()
    lineID=aListArgs[0]
    x,y= float(aListArgs[6]), float(aListArgs[5])
    pnt.X= x
    pnt.Y= y
    array.add(pnt)

#Create Polyline from all points stored in array
polyline=arcpy.Polyline(array)

#insert polyline into cursor
polyline_ins_cursor.insertRow([lineID,polyline])

#Delete cursor, close file
del polyline_ins_cursor
oneLineFile.close()

#Print completion message to user
print("Oneline shape file has been created successfully")

#Goal 2:  Create polyline feature class from Test text file. Test.txt has multiple polyline objects

#importing and reading files
testFile=open("test.txt","r")
allLines=testFile.readlines()

#Creating Test_poly.shp
arcpy.CreateFeatureclass_management(arcpy.env.workspace,"Test_poly.shp","POLYLINE",spatial_reference=arcpy.SpatialReference(4269))

#add the first column to Test_poly.shp
arcpy.AddField_management("Test_poly.shp","LineID","TEXT","","",12)

#Create a cursor to add rows to Test_poly.shp
Test_poly_ins_cursor= arcpy.da.InsertCursor("Test_poly.shp",["LineID", "SHAPE@"])

#Create point object
pnt=arcpy.Point()

#Create an array to store all the points
array=arcpy.Array()

#Create variable of the previous line ID
preID=allLines[0].split()[0]

#Loop through each line of the Test.txt file and retrieve points for polyline for as long as location ID remains the same

for aLine in allLines:
    aListArgs=aLine.split()
    lineID=aListArgs[0]
    x,y= float(aListArgs[6]), float(aListArgs[5])
    pnt.X= x
    pnt.Y=y
    
    
    if lineID != preID:
        polyline=arcpy.Polyline(array)
        Test_poly_ins_cursor.insertRow([lineID,polyline])
        preID=lineID
        array.removeAll()
        
    array.add(pnt)

#create the polyline from all the points stored in array

polyline=arcpy.Polyline(array)

#insert this row to the cursor
Test_poly_ins_cursor.insertRow([lineID,polyline])

#Delete cursor, close file
del Test_poly_ins_cursor
testFile.close()

#Print completion message to user
print("Test Polyline shape file has been created successfully")