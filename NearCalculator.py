#-------------------------------------------------------------------------------
# Name:        exploratoryregressionsetup
# Purpose:
#
# Author:      Andrew Harvey
#
# Created:     04/09/2017
# Copyright:   (c) PK 2017
# Licence:     For educational or non-profit use only
#-------------------------------------------------------------------------------

import arcpy, os
def main():
    pass

if __name__ == '__main__':
    main()

#Feature class that holds the locations and values of the dependent variables to be used in the future regression analysis
inputfc = arcpy.GetParameterAsText(0)

#Location of the feature datasets that will hold indepdendent variables
#Distance variables only used for distance analysis
distancevariables = r"C:\Masters\Thesis\FinalProject\Design\Data\Thesis.gdb\NearDistanceVariables"

#nearFieldValues used only for field values with the field name "Iterate" and renames the field to the name of the
#Feature class so be descriptive in your feature class names
nearFieldValues = r"C:\Masters\Thesis\FinalProject\Design\Data\Thesis.gdb\NearFieldValues"
##indyFC = "C:\Masters\Thesis\FinalProject\Design\Data\Thesis.gdb\AC_Independent\Nicollet7th"
##inputfc = "C:\Masters\Thesis\FinalProject\Design\Data\Thesis.gdb\AD_StartAll\MemberType_1"

###Performs functions related to those fields in the database that require distance analysis (IE how close is the closest bike lane)
def nearanalysis(inputFC, inputAnalysis):
    arcpy.AddField_management(inputfc,  fc,"DOUBLE")
    arcpy.Near_analysis(inputFC, inputAnalysis)
    arcpy.CalculateField_management(inputfc, fc, "!NEAR_DIST!", "PYTHON", "")


#Performs functions related to those variables where the field value is the important variable (IE the speed limit of the closest road)
def nearvalue(inputFC, inputAnalysis):
    arcpy.Near_analysis(inputFC, inputAnalysis)
    arcpy.JoinField_management(inputFC, "NEAR_FID",inputAnalysis, "OBJECTID", "Iterate")
    arcpy.AddField_management(inputfc,  fc,"DOUBLE")
    arcpy.CalculateField_management(inputfc, fc, "!Iterate!", "PYTHON", "")
    arcpy.DeleteField_management(inputfc, "Iterate")


###Iterates through the feature classes and conducts the approrpriate analysis for the independent variable
###first step iteration second step is to run through the appropriate function from above
arcpy.env.workspace = distancevariables
for fc in arcpy.ListFeatureClasses():
    arcpy.AddMessage("Appending distance data from " + fc)
    nearanalysis(inputfc, distancevariables + '\\'+ fc)

arcpy.env.workspace = nearFieldValues
for fc in arcpy.ListFeatureClasses():
    arcpy.AddMessage("Appending field value data from " + fc)
    nearvalue(inputfc, nearFieldValues + "\\" + fc)
    arcpy.AddMessage(nearFieldValues + fc)

