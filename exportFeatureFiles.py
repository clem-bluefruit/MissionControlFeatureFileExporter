import csv
import os
import shutil

stringIndent = "  "

def sanitiseString(featureString: str):
    featureString = featureString.replace('\\', '')
    featureString = featureString.replace('/', '')
    #featureString = featureString.replace(',', '')
    featureString = featureString.replace('-', '')
    return featureString.strip()

def IndentScenarioSteps(descriptionString: str):
    returnString = ""
    steps = descriptionString.split('\n')
    for step in steps:
        returnString += stringIndent + step + "\n"
    return returnString


with open('feature_export.csv') as featureFile:
    allFeatures = csv.reader(featureFile, delimiter=',')
    if os.path.isdir("Features"):
        shutil.rmtree("Features")
    os.mkdir("Features")
    os.chdir("Features")
    directoryRoot = os.getcwd()
    for row in allFeatures:
        if "Feature" not in row[0]:
            # Sanitise row data
            featureName = sanitiseString(row[1])
            ruleName = sanitiseString(row[4])

            if (('"' in ruleName) | ("," in ruleName)):
                stripQuotes = ruleName.split('"')
                stripCommas = stripQuotes[0].split(",")
                ruleName = stripCommas[0]
            ruleNameParts = ruleName.split(" ")
            for x in range(len(ruleNameParts)):
                ruleNameParts[x] = ruleNameParts[x].title()
            ruleNameParts[0] = ruleNameParts[0].lower()
            exportedFeatureFileName = "".join(ruleNameParts) + ".feature"

            if ":" in row[1]:
                featureFolders = row[1].split(":")

                featureGroup = featureFolders[0].strip()
                featureChild = featureFolders[1].strip()

                if not os.path.isdir(featureGroup):
                    os.mkdir(featureGroup)
                os.chdir(featureGroup)

                if not os.path.isdir(featureChild):
                    os.mkdir(featureChild)
                os.chdir(featureChild)

                if not os.path.isfile(exportedFeatureFileName):
                    editFile = open(exportedFeatureFileName, 'a+')
                    editFile.write("Feature: " + ruleName + "\n\n\n")

                editFile = open(exportedFeatureFileName, 'a+')
                extraTag = ""
                if row[6] is None:
                    extraTag = "@TBD"
                editFile.write('@feature' + row[0] + " @scenario" + row[5] + extraTag + '\n' + 'Scenario: ' + row[6] + '\n' + IndentScenarioSteps(row[7]) + "\n\n")
                os.chdir(directoryRoot)
    print("Done")