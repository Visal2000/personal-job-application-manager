from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_connection

jobs_bp = Blueprint('jobs', __name__)

# --- CREATE JOB ---
@jobs_bp.route('/api/jobs', methods=['POST'])
@jwt_required()
def create_job():
    user_id = get_jwt_identity()
    data = request.get_json()
    company = data.get('company')
    role = data.get('role')
    status = data.get('status')
    applied_date = data.get('applied_date')  # YYYY-MM-DD

    if not all([company, role, status, applied_date]):
        return jsonify({'error': 'All fields are required'}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO applications (user_id, company, role, status, applied_date) VALUES (%s, %s, %s, %s, %s)",
            (user_id, company, role, status, applied_date)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Job added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# --- GET ALL JOBS FOR CURRENT USER ---
@jobs_bp.route('/api/jobs', methods=['GET'])
@jwt_required()
def get_jobs():
    user_id = get_jwt_identity()

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM applications WHERE user_id = %s", (user_id,))
        jobs = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(jobs), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# --- UPDATE JOB ---
@jobs_bp.route('/api/jobs/<int:job_id>', methods=['PUT'])
@jwt_required()
def update_job(job_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    company = data.get('company')
    role = data.get('role')
    status = data.get('status')
    applied_date = data.get('applied_date')

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE applications 
            SET company = %s, role = %s, status = %s, applied_date = %s 
            WHERE id = %s AND user_id = %s
        """, (company, role, status, applied_date, job_id, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Job updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# --- DELETE JOB ---
@jobs_bp.route('/api/jobs/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_job(job_id):
    user_id = get_jwt_identity()

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM applications WHERE id = %s AND user_id = %s", (job_id, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Job deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
