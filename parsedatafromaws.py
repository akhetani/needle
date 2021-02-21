#!/usr/bin/python
import os
from os import name, walk
import sys, getopt

def main(argv):
    input_accesskey =""
    input_secret =""
    input_bucketname = ""
    input_evidencefolder =""
    input_casename =""
    try:
      opts, args = getopt.getopt(argv,"ha:s:b:e:c:",["accesskey=","secret=","bucketname=","evidencefolder=","casename="])
    except getopt.GetoptError:
      print("Try extractartefacts.py -h")
      sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "help"):
            print("Help file is underdevelopment")
        elif opt in ("-a", "--accesskey"):
            input_accesskey = arg
        elif opt in ("-s", "--secretkey"):
            input_secret=arg
        elif opt in ("-b", "--bucketname"):
            input_bucketname = arg
        elif opt in ("-e", "--evidencefolder"):
            input_evidencefolder = arg
        elif opt in ("-c", "--casename"):
            input_casename = arg
    aws_extractevidencefiles(input_accesskey,input_secret,input_bucketname,input_evidencefolder, input_casename)

def aws_extractevidencefiles(accesskey, secret, bucketname, evidencefolder, casename):
    print("Access Key : " + accesskey)
    print("Secret : " + secret)
    print("Bucket Name : " + bucketname)
    print("evidencefolder : " + evidencefolder)
    print("casename :" + casename)

    working_directory="/home/ubuntu/" + casename
    os.system("mkdir " + working_directory)
    output_directory= working_directory + "/output"
    os.system("mkdir " + output_directory)
    s3_mountpoint = working_directory + "/s3-drive/"
    try:
        os.system("echo " + accesskey + ':' + secret + ' > ' + "~/.passwd-s3fs")
        os.system("chmod 600 ~/.passwd-s3fs")
        os.system("mkdir " + s3_mountpoint)
        os.system("s3fs " + bucketname + " " + s3_mountpoint)
    except :
        print("That did not go as planned. S3bucket is not mounted.")
        sys.exit()
    
    fullpathtoevidence = s3_mountpoint
    os.system("sudo apt install p7zip-full p7zip-rar")
    if evidencefolder !="" :
        fullpathtoevidence= fullpathtoevidence + evidencefolder +'/' 
        print(fullpathtoevidence)
    for (dirpath, dirnames, filenames) in os.walk(fullpathtoevidence):
        print(filenames)
        for file in filenames:
            print(file)
            if file.endswith(('.vmdk','.E01')):
                temp_output_directory = output_directory + "/" + (file.split('.')[0])
                os.system("mkdir " + "'" + temp_output_directory + "'")
                print("Extracting files from :" + file)
                evidence_file = fullpathtoevidence + file
                print("temp output dircetory :" + temp_output_directory)
                os.system("cd "+ dirpath)
                os.system("7z " + "l " + "\"" + evidence_file + "\"")
                os.system("7z " + "x " + "'" + evidence_file + "'" + " -o/" + "'" + temp_output_directory + "' " + "[SYSTEM]/*" )
if __name__ == "__main__":
    main(sys.argv[1:])
    