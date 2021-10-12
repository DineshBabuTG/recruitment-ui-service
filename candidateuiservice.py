"""The candidate service access.

This module manages saving the candidates and reading them back.
"""
import logging
import datetime
import json
import requests
import os

logger = logging.getLogger('candidateuiservice')

apphostname = os.environ['apphostname']
print("App hostname is " + apphostname)
logger.info("App hostname is " + apphostname)

candidateServiceBaseurl = "http://" + apphostname + ":8000"
addCandidateAPIURL = candidateServiceBaseurl + "/candidateservice/addcandidate"
getAllCandidatesAPIURL = candidateServiceBaseurl + "/candidateservice/getallcandidates"

headers = {'Content-Type': 'application/json'}
multipartheaders = {'Content-Type': 'multipart/form-data'}

def get_all_candidates():
    """Returns all the existing candidates.
    """
    logger.info("In Get All Candidate method")
    candidates = requests.get(getAllCandidatesAPIURL, headers=headers)
    responseData = json.loads(candidates.content)
    logger.info("GET Candidates: " + str(candidates.content))
    return responseData

def save_candidate(name, address, qualification, jobskill, yearsofexperience, uploadedResumefilepath):
    logger.info("In Save Candidate method")
    timestamp = datetime.datetime.now().isoformat().replace(":","")

    logger.info("name " + name + " address " + address + " qualification " + qualification + " jobskill " + jobskill + " yearsofexperience " + yearsofexperience)
    logger.info("Going to trigger Add Candidate API from web app")
    candidatePayload = dict({'name': name, 'address': address, 'qualification': qualification, 'jobskill': jobskill, 'yearsofexperience': yearsofexperience})
    data = json.dumps(candidatePayload)
    #logger.info("Request payload is: " + data)
    logger.info("Resume file path is " + uploadedResumefilepath)
    #logger.info(open(uploadedResumefilepath).read())
    resumefilename = uploadedResumefilepath.split("/", 1)[1]
    logger.info("Resume file name is " + resumefilename)
    files = [
        ('document', (resumefilename, open(uploadedResumefilepath, 'rb'), 'application/octet')),
        ('data', ('data', data, 'application/json')),
    ]

    #print(candidate_service_api.add_candidate(name=name, address=address, qualification=qualification, jobskill=jobskill, yearsofexperience=yearsofexperience))
    response = requests.post(addCandidateAPIURL, files=files)
    #print("Response is: " + response.content.json)
    #addedcandidate = candidate_service_api.add_candidate(name=name, address=address, qualification=qualification, jobskill=jobskill, yearsofexperience=yearsofexperience)
    #print(addedcandidate)
