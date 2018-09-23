import os
import sys
import subprocess

def getPdfFiles(path):
    files = {}
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if filename.endswith('.pdf'):
                files[filename] = os.path.join(dirpath, filename)

    return files

def checkIfPdfIsSearchable(filename):
    filename = filename.replace(" ","\\ ").replace("(", "\(").replace(")", "\)")
    command = "pdffonts {0}"
    command = command.format(filename)
    result = subprocess.check_output(command, shell=True)
    return len(result.splitlines())>2

def convertPdfToMultipageTiff(filename):
    command = "gs -o {0}.tiff -sDEVICE=tiff24nc -r300x300 {1}"
    tiffFile = os.path.splitext(filename)[0]
    command = command.format(tiffFile.replace(" ","\\ ").replace("(", "\(").replace(")", "\)"),filename.replace(" ","\\ ").replace("(", "\(").replace(")", "\)"))
    subprocess.check_output(command, shell=True)
    return tiffFile

def convertMultipageTiffToSearchablePdf(filename):
    command = "tesseract {0}.tiff {0} -l nld pdf"
    command = command.format(filename.replace(" ","\\ ").replace("(", "\(").replace(")", "\)"))
    subprocess.check_output(command, shell=True)

def removeTiffFile(filename):
    os.remove(filename + ".tiff")

files = getPdfFiles(sys.argv[1])

for filename in files:
    file = files[filename]
    if (checkIfPdfIsSearchable(file) == False):
        tiffFile = convertPdfToMultipageTiff(file)
        convertMultipageTiffToSearchablePdf(tiffFile)
        removeTiffFile(tiffFile)
        print (filename)