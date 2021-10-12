"""The candidate service access.

This module manages saving the candidates and reading them back.
"""
import logging
import datetime
import json
import os
import requests

# create logger
logger = logging.getLogger('jobuiservice')

apphostname = os.environ['apphostname']
print("App hostname is " + apphostname)
logger.info("App hostname is " + apphostname)

jobServiceBaseurl = "http://" + apphostname + ":8002"
addJobAPIURL = jobServiceBaseurl + "/jobservice/addjob"
getAllJobsAPIURL = jobServiceBaseurl + "/jobservice/getalljobs"

headers = {'Content-Type': 'application/json'}

def get_all_jobs():
    """Returns all the existing jobs.
    """
    logger.info("In Get All Job method")
    jobs = requests.get(getAllJobsAPIURL, headers=headers)
    responseData = json.loads(jobs.content)
    logger.info("GET Jobs: " + str(jobs.content))
    return responseData

def save_job(clientname, jobprofile, jobrequirements):
    logger.info("In Save Job method")
    timestamp = datetime.datetime.now().isoformat().replace(":","")

    logger.info("clientname " + clientname + " jobprofile " + jobprofile + " jobrequirements " + jobrequirements)
    logger.info("Going to trigger Add Job API from web app")
    jobPayload = dict({'clientname': clientname, 'jobprofile': jobprofile, 'jobrequirements': jobrequirements})
    data = json.dumps(jobPayload)
    logger.info("Add Job Request payload is: " + data)

    response = requests.post(addJobAPIURL, data, headers=headers)