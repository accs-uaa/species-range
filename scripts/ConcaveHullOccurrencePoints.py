# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Convex Hull from Occurrence Points
# Author: Timm Nawrocki, Alaska Center for Conservation Science
# Created on: 2016-11-05
# Usage: Must be executed as an ArcPy Script.
# Description: This tool estimates a concave hull from occurrence points. The output is buffered by a user determined distance to represent a species range.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy, os, numpy
from arcpy.sa import *

# Set overwrite option
arcpy.env.overwriteOutput = True

# Define input point occurrence dataset
Input_Points = arcpy.GetParameterAsText(0)

# Define input clip dataset
Clip_Dataset = arcpy.GetParameterAsText(1)

# Define location of a workspace folder
Workspace = arcpy.GetParameterAsText(2)

# Define location of output concave hull
Concave_Hull = arcpy.GetParameterAsText(3)

# Define minimum search distance
Min_Search_Distance = arcpy.GetParameterAsText(4)

# Define buffer distance
Buffer_Distance = arcpy.GetParameterAsText(5)

# Define modification factor (the value that multiplies the 90th percentile to form the Max for the aggregate step)
Mod = arcpy.GetParameterAsText(6)
Mod_Float = float(Mod)

# Define intermediate files for user selected workspace
Search_Raster = os.path.join(Workspace, "Search_Raster.tif")
Search_Points = os.path.join(Workspace, "Search_Points.shp")
Aggregate_Polygon = os.path.join(Workspace, "Aggregate.shp")
Buffer_Polygon = os.path.join(Workspace, "Aggregate_Buffer.shp")
Dissolve_Polygon = os.path.join(Workspace, "Aggregate_Dissolve.shp")
Smooth_Polygon = os.path.join(Workspace, "Aggregate_Smooth.shp")
Agg_Table = os.path.join(Workspace, "Aggregate_Tbl.dbf")
Agg_Table_CPG = os.path.join(Workspace, "Aggregate_Tbl.cpg")
Agg_Table_XML = os.path.join(Workspace, "Aggregate_Tbl.dbf.xml")
Log = os.path.join(Workspace, "log")

# Set coordinate system
arcpy.env.outputCoordinateSystem = Input_Points

# Determine type of input feature
file_extension = os.path.splitext(Input_Points)[1]

# Select search points based on minimum search distance
arcpy.AddMessage("Determining search points based on minimum search distance...")
arcpy.RepairGeometry_management(Input_Points, "DELETE_NULL")
if file_extension == ".shp":
    valField = "FID"
    assignmentType = "MAXIMUM"
    priorityField = ""
    arcpy.PointToRaster_conversion(Input_Points, valField, Search_Raster, assignmentType, priorityField, Min_Search_Distance)
else:
    valField = "OBJECTID"
    assignmentType = "MAXIMUM"
    priorityField = ""
    arcpy.PointToRaster_conversion(Input_Points, valField, Search_Raster, assignmentType, priorityField, Min_Search_Distance)
reclassField = "VALUE"
remap = RemapRange([[0,1000000,1]])
Search_Reclassify = Reclassify(Search_Raster, reclassField, remap, "NODATA")
Search_Extract = ExtractByMask(Search_Reclassify, Input_Points)
outputField = "VALUE"
arcpy.RasterToPoint_conversion(Search_Extract, Search_Points, outputField)

# Conduct near point analysis and calculate maximum near distance
arcpy.AddMessage("Determining maximum point distances...")
arcpy.Near_analysis(Search_Points, Search_Points, "", "NO_LOCATION", "NO_ANGLE", "PLANAR")
arr = arcpy.da.FeatureClassToNumPyArray(Search_Points, ('NEAR_DIST'))['NEAR_DIST']
Max = (numpy.percentile(arr, 90) * Mod_Float)

# Aggregate input points based on maximum near distance
arcpy.AddMessage("Creating concave polygon based on maximum point distances (step 1 of 3)...")
arcpy.AggregatePoints_cartography(Input_Points, Aggregate_Polygon, Max)

# Buffer aggregate polygon based on buffer distance
arcpy.AddMessage("Creating concave polygon based on maximum point distances (step 2 of 3)...")
sideType = "FULL"
endType = "ROUND"
dissolveType = "NONE"
dissolveField = ""
Method = "PLANAR"
arcpy.Buffer_analysis(Aggregate_Polygon, Buffer_Polygon, Buffer_Distance, sideType, endType, dissolveType, dissolveField, Method)

# Dissolve buffered polygon
arcpy.AddMessage("Creating concave polygon based on maximum point distances (step 3 of 3)...")
arcpy.Dissolve_management(Buffer_Polygon, Dissolve_Polygon, "", "", "MULTI_PART", "DISSOLVE_LINES")

# Smooth polygon using Bezier Interpolation and export without clipping
if Clip_Dataset == "":
    arcpy.AddMessage("No clip dataset was specified, exporting concave hull polygon...")
    arcpy.SmoothPolygon_cartography(Dissolve_Polygon, Concave_Hull, "BEZIER_INTERPOLATION", "0 Meters", "FIXED_ENDPOINT", "NO_CHECK")
# Smooth polygon using Bezier Interpolation and clip the output
elif Clip_Dataset != "":
    arcpy.SmoothPolygon_cartography(Dissolve_Polygon, Smooth_Polygon, "BEZIER_INTERPOLATION", "0 Meters", "FIXED_ENDPOINT", "NO_CHECK")
    xy_tolerance = ""
    arcpy.AddMessage("Clipping concave hull polygon to the clip dataset...")
    arcpy.Clip_analysis(Smooth_Polygon, Clip_Dataset, Concave_Hull, xy_tolerance)
else:
    arcpy.AddError("An invalid clip dataset was entered.")

# Delete intermediate data
arcpy.Delete_management(Search_Raster)
arcpy.Delete_management(Search_Points)
arcpy.Delete_management(Aggregate_Polygon)
arcpy.Delete_management(Buffer_Polygon)
arcpy.Delete_management(Dissolve_Polygon)
if os.path.exists(Smooth_Polygon) == True:
    arcpy.Delete_management(Smooth_Polygon)
if os.path.exists(Agg_Table) == True:
    os.remove(Agg_Table)
if os.path.exists(Agg_Table_CPG) == True:
    os.remove(Agg_Table_CPG)
if os.path.exists(Agg_Table_XML) == True:
    os.remove(Agg_Table_XML)
if os.path.exists(Log) == True:
    os.remove(Log)