from flask import Flask, render_template, request
from huggingface_hub import InferenceClient
from werkzeug.utils import secure_filename
from os.path import dirname, abspath, join, isdir, isfile
import json
import requests
from extractPrompt import promptExtractor

app = Flask(__name__)

obj = promptExtractor()
HERE: str = dirname(abspath(__file__))
API_URL = "https://huggingface.co/uralstech/hAI-Spec-Nasa-SpaceApps-Challenge"
prompt: str = "### Instruction:\nPurpose\nThe purpose of this standard is to establish the nondestructive evaluation (NDE) requirements for\nany NASA system or component, flight or ground, where fracture control is a requirement.  This\nstandard defines the primary requirements for NDE in support of NASA-STD-5019, Fracture\nControl Requirements for Spaceflight Hardware.  NDE applied in-process for purposes of process\ncontrol is not addressed in this document.\nIt is the policy of NASA to produce aerospace flight systems with a high degree of reliability and\nsafety.  This is accomplished through good design, manufacturing, test, and operational practices\nincluding the judicious choice of materials, detailed analysis, appropriate factors of safety, rigorous\ntesting and control of hardware, and reliable inspection.  NASA fracture control requirements\nstipulate that all aerospace flight systems be subjected to fracture control procedures to preclude\ncatastrophic failure.  Those procedures frequently rely on NDE to ensure that significant crack-like\nflaws are not present in critical areas.\na.  NDE processes shall meet the requirements in this standard to screen hardware reliably\nfor the presence of crack-like flaws.\nb.  Nothing in this document shall be construed as requiring duplication of effort dictated by\nother contract provisions.\nc.  Conversely, provisions stated herein shall not be interpreted to preclude compliance with\nrequirements invoked by other provisions.\n### Output:\n"
headers = {"Authorization": f"Bearer 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",
        "Content-Type": "application/json",}

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/test')
def query():   
    client = InferenceClient()
    response = client.post(json={"inputs": prompt}, model="uralstech/hAI-Spec-Nasa-SpaceApps-Challenge")
    response.content


# data = query({"inputs": "The answer to the universe is [MASK]."})
 
@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        PDF_PATH: str = join(HERE, f.filename)
        pdf_1= obj.format_pdf(PDF_PATH)
        return render_template('form.html', message=prompt)

if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=True, threaded=True)
