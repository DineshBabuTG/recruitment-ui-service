"""The candidate service access.

This module manages saving the candidates and reading them back.
"""
import logging
import datetime
import json
import os
import requests

logger = logging.getLogger('customeruiservice')

apphostname = os.environ['apphostname']
print("App hostname is " + apphostname)
logger.info("App hostname is " + apphostname)

customerServiceBaseurl = "http://"+ apphostname + ":8001"
addCustomerAPIURL = customerServiceBaseurl + "/customerservice/addcustomer"
getAllCustomersAPIURL = customerServiceBaseurl + "/customerservice/getallcustomers"

headers = {'Content-Type': 'application/json'}

def get_all_customers():
    """Returns all the existing customers.
    """
    logger.info("In Get All Customer method")
    customers = requests.get(getAllCustomersAPIURL, headers=headers)
    responseData = json.loads(customers.content)
    logger.info("GET Customers: " + str(customers.content))
    return responseData

def save_customer(name, address):
    logger.info("In Save Customer method")
    timestamp = datetime.datetime.now().isoformat().replace(":","")

    logger.info("name " + name + " address " + address)
    logger.info("Going to trigger Add Customer API from web app")
    customerPayload = dict({'name': name, 'address': address})
    data = json.dumps(customerPayload)
    logger.info("Request payload is: " + data)

    response = requests.post(addCustomerAPIURL, data, headers=headers)
