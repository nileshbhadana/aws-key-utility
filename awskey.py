#!/usr/local/bin/python3
import boto3
import argparse, os
from devops_commons.logging import get_logger
import logging
import configparser
import shutil

logger = get_logger("AWS Key")
logging.getLogger().setLevel(logging.INFO)


def updateKeys(newAccessKeyId,newSecret):
    config = configparser.RawConfigParser()
    path = os.path.join(os.path.expanduser('~'), '.aws/credentials')
    pathBackup = os.path.join(os.path.expanduser('~'), '.aws/credentials.bkp')
    
    # Making copy of credential file
    shutil.copy2(path,pathBackup)

    config.read(path)
    config.set(args.profile, 'aws_access_key_id',newAccessKeyId)
    config.set(args.profile, 'aws_secret_access_key',newSecret)
    try:
        logger.debug("Updating new generated key in credential file")
        fp=open(path,'w')
        config.write(fp)
        fp.close()
    except Exception as e:
        shutil.copy2(pathBackup,path)
        logger.error("Unexpected Error: {}".format(e.response['Error']['Message']))

def getOldKey():
    keyData = listKeys()
    key1Time,key2Time = keyData[0]['CreateDate'], keyData[1]['CreateDate']
    timeDelta = (key1Time - key2Time).total_seconds()
    if timeDelta < 0:
        return keyData[0]['AccessKeyId']
    else:
        return keyData[1]['AccessKeyId']



def rotateKeys():
    logger.info("Rotating Keys for profile: {profile}".format(profile=args.profile))
    newAccessKeyId,newSecret=generateNewKey()
    updateKeys(newAccessKeyId,newSecret)
    deleteKey(getOldKey())
    logger.info("Key Rotated Successfully")
    logger.info("New Key: {}".format(newAccessKeyId))


def generateNewKey():
    response = client.create_access_key()
    return response['AccessKey'].get('AccessKeyId'), response['AccessKey'].get('SecretAccessKey')

def listKeys():
    response = client.list_access_keys()
    return response['AccessKeyMetadata']

def deleteKey(AccessKeyId):
    try:
        response=client.delete_access_key(AccessKeyId=AccessKeyId)
    except Exception as e:
        logger.error("Unexpected Error: {}".format(e.response['Error']['Message']))

def main():
    if args.delete:
        confirm=input("Confirm to delete {} Key[y/N]:".format(args.delete))
        if confirm[0] == "y" :
            deleteKey(args.delete)
            logger.info("Key Deleted Successfully")
        exit(0)
    elif args.rotate:
        rotateKeys()
    else:
        response = listKeys()
        for key in range(len(response)):
            logger.info("Key: {key} | Status: {status} | Creation Date: {createdate}".format(
                key=response[key]['AccessKeyId'],
                status=response[key]['Status'],
                createdate=response[key]['CreateDate']))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--rotate', dest='rotate', action='store_true', default=False)
    parser.add_argument('--profile', dest='profile', type=str, required=False)
    parser.add_argument('--delete', dest='delete', type=str)
    parser.add_argument('--debug','-v', dest='debug', action='store_true', default=False)
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Creating aws session
    if args.profile:
        logger.debug("Using {} profile".format(args.profile))
        session = boto3.session.Session(profile_name=args.profile)
        client = session.client('iam')
    else:
        logger.debug("Using Default profile")
        client = boto3.client('iam')
    
    main()