#!/usr/bin/python
import argparse
import os
import boto3
import botocore


def main():
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('-accessKey', required=True, help='Bucket Access Key Required')
    parser.add_argument('-secret', required=True, help='Bucket Secret Key Required')
    parser.add_argument('-bucketName', required=True, help='Bucket Name Key Required')
    parser.add_argument('-evidenceFolderPath', required=True, help='Path of Evidence Folder Required')
    parser.add_argument('-caseName', required=False, help='Case Name Required')
    parser.add_argument('-localFolder', required=False, help='Path of Local Folder to store data - else defaults to working dir')
    args = parser.parse_args()
    downloadDirectoryFroms3(args.accessKey, args.secret,args.bucketName, args.evidenceFolderPath,args.localFolder,args.caseName)

def downloadDirectoryFroms3(access_key, secret,  bucketName, evidenceFolderPath, localFolder, caseName):
    s3_resource = boto3.resource('s3',aws_access_key_id=access_key, aws_secret_access_key=secret)
    bucket = s3_resource.Bucket(bucketName) 
    for obj in bucket.objects.filter(Prefix = evidenceFolderPath):
        target = obj.key if localFolder is None \
            else os.path.join(localFolder, os.path.relpath(obj.key, evidenceFolderPath))
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        bucket.download_file(obj.key, target)
        print(target)

"""
def aws_extractevidencefiles(accesskey, secret, bucketname, evidencefolder, casename):
    print(f"Access Key: {accesskey}")
    print(f"Secret {secret}")
    print(f"Bucket Name {bucketname}")
    print(f"evidencefolder {evidencefolder}")
    print(f"casename {casename}")

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
                os.system("7z " + "x " + "'" + evidence_file + "'" + " -o/" + "'" + temp_output_directory + "' " + "[SYSTEM]/* \
                            \"Windows/System32/winevt/*\" \
                            \"Users/*\" \
                            \"Windows/System32/config\" \
                            \"*/History/*\" \
                            \"*/prefetch/*\" \
                            \"*.etl\"")
                os.system("7z a '" + temp_output_directory + ".zip'" + " '" + temp_output_directory+"/'" )
                os.system("cp '" +  temp_output_directory + "'.zip " + "'" + s3_mountpoint + "'")
    os.system("umount " + s3_mountpoint)
    """

if __name__ == '__main__':
    main()
    