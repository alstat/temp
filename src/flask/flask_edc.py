"""
Flask interface for handling computations
"""
from flask import Flask
from flask import jsonify
from flask import request
import json

# method handling cover sheet computation
from interface import *

# Host and Port Variables
# 127.0.0.1 - Local network connection
app = Flask(__name__)

HOST = "127.0.0.1"
PORT = "5000"

"""
Handles computation for Hole and Casing Summary
"""
@app.route("/compute_hole_casing", methods = ["POST"])
def flask_compute_hole_casing():
    print "Request for Hole and Casing"

    data = json.loads(request.get_data().decode())
    out = compute_hole_casing(data)
    # print out
    # print jsonify(out).text
    response = jsonify(out)
    # response = json.dumps(out)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

"""
Handles computation for Analysis of the EDC Permutation
"""
@app.route("/compute_afe_costs/<type_>", methods = ["POST"])
def flask_compute_afe_costs(type_):
    print "Request for Run Analysis received"

    data = json.loads(request.get_data().decode())
    out = compute_afe_costs(data, {}, type_)
    response = jsonify(out)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

"""
Handles computation the increments of casing depth
"""
@app.route("/compute_baseline_depth", methods = ["POST"])
def flask_compute_casing_depth():
    print "Receive Request for Computing Casing Depth"

    data = json.loads(request.get_data().decode())
    out = compute_analysis_depth_baseline(data)

    response = jsonify(out)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

"""
Handles computation of baseline ROP
"""
@app.route("/compute_baseline_rop", methods = ["POST"])
def flask_compute_baseline_rop():
    print "Request for Baseline ROP received"

    data = json.loads(request.get_data().decode())
    out = compute_analysis_rop_baseline(data)
    response = jsonify(out)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

"""
Handles computation of target rop etc
"""
@app.route("/compute_target_rop_etc", methods = ["POST"])
def flask_compute_target_rop_etc():
    print "Receive Request for Target ROP"

    data = json.loads(request.get_data().decode())
    out = compute_target_rop_etc(data, {})

    response = jsonify(out)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


"""
Handles computation of baseline Days
"""
@app.route("/compute_baseline_days", methods = ["POST"])
def flask_compute_baseline_days():
    print "Request for Baseline Days received"

    data = json.loads(request.get_data().decode())
    out = compute_analysis_rop_baseline(data, None, "days")
    response = jsonify(out)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

"""
Handles computation for Cover Sheet fields

@inputs - Main Inputs, Hole/Casing Summary, Other Inputs, Driling Schedule
@outs - Values for Cover Sheet in json format
"""
@app.route("/compute_cover_sheet", methods=["POST"])
def flask_compute_cover_sheet():
    print("Received cover sheet computation request")

    data = json.loads(request.get_data().decode())
    out = compute_cover_sheet(data, {})
    response = jsonify(out)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


"""
Handles computation for permutation

@inputs - Main Inputs, Hole/Casing Summary, Other Inputs, Driling Schedule
@outs - Values for Cover Sheet in json format 
"""
@app.route("/compute_permutation", methods = ["POST"])
def flask_compute_permutation():
    """
    Computes Permutation
    """
    print("Received permutation computation request")

    data = json.loads(request.get_data().decode())
    out = compute_permutation(data, {})
    response = jsonify(out)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

@app.route("/get_permutations", methods = ["POST"])
def flask_compute_permutation_count():
    """
    Computes Permutation Count
    """
    print("Received permutation count request")

    data = json.loads(request.get_data().decode())
    out = compute_permutation_count(data, {})
    response = jsonify(out)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

@app.route("/compute_cost_details", methods = ["POST"])
def flask_compute_cost_details():
    """
    Computes the Cost Details
    """
    print "received cost details request"

    data = json.loads(request.get_data().decode())
    out = compute_cost_details(data, {})
    response = jsonify(out)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

@app.route("/export_cover_sheet", methods = ["POST"])
def flask_export_cover_sheet():
    """
    Export Cover Sheet
    """
    print "recieved exportation of cover sheet request"

    data = json.loads(request.get_data().decode())
    out = export_cover_sheet(data)

    print "this is the path" + data

@app.route("/compute_baseline_costs/<type_>", methods = ["POST"])
def flask_compute_baseline_costs(type_):
    """
    Computes Baseline Costs of all Items/Tables
    """
    print("received computation of baseline costs")

    data = json.loads(request.get_data().decode())
    out = compute_baseline_costs(data, type_, {})
    response = jsonify(out)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response
        
if __name__ == "__main__":
    # Set up Flask Application with host and port variables
    app.run(HOST, PORT)
