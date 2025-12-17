"""
Flask REST API for Sri Lankan NIC Validation
--------------------------------------------
This module provides a RESTful API endpoint to validate NIC numbers
using the DFA implementation.

Endpoints:
----------
POST /validate-nic
    Request body: { "nic": "981234567V" }
    Response: { "result": "ACCEPT", "final_state": "q10", "input": "981234567V" }

GET /health
    Health check endpoint
    Response: { "status": "healthy" }
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dfa import NICDFA

app = Flask(__name__)
CORS(app)
nic_dfa = NICDFA()


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        JSON response with status
    """
    return jsonify({
        "status": "healthy",
        "message": "NIC DFA Validator API is running"
    }), 200


@app.route('/validate-nic', methods=['POST'])
def validate_nic():
    """
    Validate a Sri Lankan NIC number using the DFA.
    
    Request Body (JSON):
        {
            "nic": "981234567V"
        }
    
    Response (JSON):
        {
            "result": "ACCEPT",
            "final_state": "q10",
            "input": "981234567V",
            "format": "Old NIC (9 digits + V/X)"
        }
    
    Returns:
        JSON response with validation result
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            "error": "Invalid request",
            "message": "Request body must be JSON"
        }), 400
    
    if 'nic' not in data:
        return jsonify({
            "error": "Missing field",
            "message": "Request must include 'nic' field"
        }), 400
    
    nic_number = data['nic']
    
    if not isinstance(nic_number, str):
        return jsonify({
            "error": "Invalid data type",
            "message": "'nic' field must be a string"
        }), 400
    
    result, final_state = nic_dfa.validate(nic_number)
    
    nic_format = None
    if result == "ACCEPT":
        if final_state == nic_dfa.OLD_NIC_ACCEPT:
            nic_format = "Old NIC (9 digits + V/X)"
        elif final_state == nic_dfa.NEW_NIC_ACCEPT:
            nic_format = "New NIC (12 digits)"
    
    response = {
        "result": result,
        "final_state": final_state,
        "input": nic_number
    }
    
    if nic_format:
        response["format"] = nic_format
    
    return jsonify(response), 200


@app.route('/validate-nic-trace', methods=['POST'])
def validate_nic_with_trace():
    """
    Validate a NIC number and return detailed trace information.
    
    This endpoint is useful for educational purposes to see
    the step-by-step state transitions of the DFA.
    
    Request Body (JSON):
        {
            "nic": "981234567V"
        }
    
    Response (JSON):
        {
            "result": "ACCEPT",
            "final_state": "q10",
            "input": "981234567V",
            "trace": [
                {"step": 0, "input": "", "state": "q0"},
                {"step": 1, "input": "9", "state": "q1"},
                ...
            ]
        }
    
    Returns:
        JSON response with validation result and trace
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            "error": "Invalid request",
            "message": "Request body must be JSON"
        }), 400
    
    if 'nic' not in data:
        return jsonify({
            "error": "Missing field",
            "message": "Request must include 'nic' field"
        }), 400
    
    nic_number = data['nic']
    
    if not isinstance(nic_number, str):
        return jsonify({
            "error": "Invalid data type",
            "message": "'nic' field must be a string"
        }), 400
    
    result_data = nic_dfa.validate_with_trace(nic_number)
    
    result_data["input"] = nic_number
    
    return jsonify(result_data), 200


@app.route('/dfa-info', methods=['GET'])
def get_dfa_info():
    """
    Get information about the DFA structure.
    
    Returns:
        JSON response with DFA specification
    """
    return jsonify({
        "automaton_type": "Deterministic Finite Automaton (DFA)",
        "purpose": "Validate Sri Lankan NIC number format",
        "alphabet": ["0-9", "V", "X"],
        "states": {
            "q0": "Start state",
            "q1-q9": "Processing digits 1-9",
            "q10": "Accept state (Old NIC: 9 digits + V/X)",
            "q11": "Processing 10th digit",
            "q12": "Processing 11th digit",
            "q13": "Accept state (New NIC: 12 digits)",
            "q_reject": "Reject state"
        },
        "start_state": "q0",
        "accepting_states": ["q10", "q13"],
        "valid_formats": [
            "Old NIC: 9 digits followed by V or X (e.g., 981234567V)",
            "New NIC: 12 digits (e.g., 199812345678)"
        ]
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "error": "Not found",
        "message": "The requested endpoint does not exist"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500


if __name__ == '__main__':
    print("=" * 70)
    print("Starting NIC DFA Validator API Server")
    print("=" * 70)
    print("\nAvailable Endpoints:")
    print("  POST   /validate-nic        - Validate NIC number")
    print("  POST   /validate-nic-trace  - Validate with state trace")
    print("  GET    /dfa-info            - Get DFA information")
    print("  GET    /health              - Health check")
    print("\n" + "=" * 70)
    print()
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
