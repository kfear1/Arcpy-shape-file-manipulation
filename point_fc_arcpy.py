"""Using arcpy to create and manipulate point feature classes"""

#importing libraries

import arcpy

#setting workspace
arcpy.env.workspace= "C:\\Users\\kfear\\Python"

#allowing overwriting of exisiting files
arcpy.env.overwriteOutput=True

#import and read files
myLocationFile= open("locations.txt","r")
allLocations=myLocationFile.readlines() [1:]

#Goal 1: create point feature class from locations text file

#Constructing new shape file in current folder- setting projection as NAD 1983 State Plane Coordinate System: North Carolina

arcpy.CreateFeatureclass_management(arcpy.env.workspace, "locations.shp", "Point",spatial_reference=arcpy.SpatialReference(2264))

#Adding location ID column to new shape file
arcpy.AddField_management("locations.shp", "LocID", "TEXT", "","",10)

#creating insert cursor to add values to locations shape file
loc_ins_cursor=arcpy.da.InsertCursor("locations.shp", ["LocID","SHAPE@XY"])

#loop through each line of text file and add each line to cursor

for aLine in allLocations:
    aListArgs=aLine.split(",")
    locID= aListArgs[0]
    x,y= float(aListArgs[1]), float(aListArgs[2])

    # add the x and y values to the cursor
    loc_ins_cursor.insertRow([locID, (x,y)])

#delete cursor, close file
del loc_ins_cursor
myLocationFile.close()

#print completion message to user
print("Point file has been created successfully")

#Goal 2: calculate the mean center for locations.shp and create a new shapefile with all the locations as well as the mean center

# Creation of search cursor to search through locations.shp file
loc_search_Cursor=arcpy.da.SearchCursor("locations.shp",["LocID","SHAPE@XY"])

#Create new shape file - projection = NAD 1983 State Plane Coordinate System: North Carolina
arcpy.CreateFeatureclass_management(arcpy.env.workspace,"loc_mean_c.shp","Point",spatial_reference=arcpy.SpatialReference(2264))

#Create 1st column in loc_mean_c.shp
arcpy.AddField_management("loc_mean_c.shp","LocID","TEXT","","",10)

#Create cursor to insert rows into loc_mean_c.shp
loc_mean_ins_cursor=arcpy.da.InsertCursor("loc_mean_c.shp",["LocID","SHAPE@XY"])

#initialize variables to sum the x, y and count of each point as we loop through

totalX =0
totalY= 0
count=0

#loop through each row in the Cursor of locations.shp and pull out the location ID, the x and y value, and update the total X total Y and count values
#there is no need for type conversions- moving from one shapefile to another

for aRow in loc_search_Cursor:
    locationID= aRow[0]
    x,y=aRow[1][0], aRow[1][1]
    totalX += x
    totalY +=y
    count+=1

    #insert the location ID, and the x,y of each point into the loc_mean_c.shp
    loc_mean_ins_cursor.insertRow([locationID, (x,y)])

#calculate mean center point
avgX= totalX/count
avgY=totalY/count

#Add mean center point to loc_mean_ins_cursor

loc_mean_ins_cursor.insertRow(["MC",(avgX,avgY)])

#Delete all cursors
del loc_search_Cursor, loc_mean_ins_cursor

#Print completion message to user
print("Point file 'loc_mean_c.shp' has been created successfully")



