from flask import Flask, render_template
from forms import AddCandidateForm
from forms import AddJobForm
from forms import AddCustomerForm
import logging.config
import candidateuiservice
import jobuiservice
import customeruiservice

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dinasecretkey'
app.config['UPLOAD_FOLDER'] = 'uploaded-files/'
app.config['MAX_CONTENT_PATH'] = 1024 * 1024 * 20

logging.config.fileConfig('logging.conf')
# create logger
logger = logging.getLogger('webapp')

@app.route("/", methods=["GET", "POST"])
def index():
    logger.info("Home Page Loaded Successfully")

    return render_template("base.html")

@app.route("/candidate", methods=["GET", "POST"])
def candidate():
    logger.info("Candidate Page Loaded Successfully")

    return render_template("candidate.html")

@app.route("/job", methods=["GET", "POST"])
def job():
    logger.info("Job Page Loaded Successfully")

    return render_template("job.html")

@app.route("/customer", methods=["GET", "POST"])
def customer():
    logger.info("Customer Page Loaded Successfully")

    return render_template("customer.html")

@app.route("/addcandidate", methods=["GET", "POST"])
def managecandidate():
    form = AddCandidateForm()
    logger.info("Candidate Form Loaded Successfully")
    logger.info(form.validate_on_submit())
    if form.validate_on_submit():
        logger.info("Add Candidate button clicked")
        logger.info("Name is: " + form.name.data)
        #filedata = form.uploadresume.data.read().decode("latin-1")
        #logger.info("Resume Data is: " + filedata)
        fileInput = form.uploadresume.data
        logger.info("Uploaded Resume file name is: " + fileInput.filename)
        uploadedResumefilepath = "uploaded-files/" + fileInput.filename
        fileInput.save(uploadedResumefilepath)
        candidateuiservice.save_candidate(
            name=form.name.data,
            address=form.address.data,
            qualification=form.qualification.data,
            jobskill=form.jobskill.data,
            yearsofexperience=form.yearsofexperience.data,
            uploadedResumefilepath=uploadedResumefilepath)
        return render_template("candidateThankyou.html")
    return render_template("addCandidate.html", form=form)


@app.route("/listcandidates")
def listcandidates():
    allCandidatesList = candidateuiservice.get_all_candidates()

    return render_template("candidateList.html", allCandidatesList=allCandidatesList)

@app.route("/addjob", methods=["GET", "POST"])
def managejob():
    form = AddJobForm()
    logger.info("Job Form Loaded Successfully")
    logger.info(form.validate_on_submit())
    if form.validate_on_submit():
        logger.info("Add Job button clicked")
        logger.info("Client Name is: " + form.clientname.data)
        jobuiservice.save_job(
            clientname=form.clientname.data,
            jobprofile=form.jobprofile.data,
            jobrequirements=form.jobrequirements.data)
        return render_template("jobThankyou.html")
    return render_template("addJob.html", form=form)

@app.route("/listjobs")
def listjobs():
    allJobsList = jobuiservice.get_all_jobs()

    return render_template("jobList.html", allJobsList=allJobsList)

@app.route("/addcustomer", methods=["GET", "POST"])
def managecustomer():
    form = AddCustomerForm()
    logger.info("Customer Form Loaded Successfully")
    logger.info(form.validate_on_submit())
    if form.validate_on_submit():
        logger.info("Add Customer button clicked")
        logger.info("Client Name is: " + form.name.data)
        customeruiservice.save_customer(
            name=form.name.data,
            address=form.address.data)
        return render_template("customerThankyou.html")
    return render_template("addCustomer.html", form=form)


@app.route("/listcustomers")
def listcustomers():
    allCustomersList = customeruiservice.get_all_customers()

    return render_template("customerList.html", allCustomersList=allCustomersList)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
