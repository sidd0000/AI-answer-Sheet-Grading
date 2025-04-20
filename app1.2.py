# app.py
from flask import Flask, request, jsonify, render_template, send_file
import os
import json
import uuid
import shutil
import datetime
from werkzeug.utils import secure_filename

# Import your modules
import text_extraction
import marking_scheme_generation
import answer_extraction
import evaluation
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SESSION_FOLDER'] = 'sessions'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['SESSION_FOLDER'], exist_ok=True)

# Dictionary to store active sessions
sessions = {}

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/create-session', methods=['POST'])
def create_session():
    """Create a new evaluation session"""
    session_id = str(uuid.uuid4())
    session_dir = os.path.join(app.config['SESSION_FOLDER'], session_id)
    os.makedirs(session_dir, exist_ok=True)
    
    sessions[session_id] = {
        'id': session_id,
        'created_at': datetime.datetime.now().isoformat(),
        'question_paper': None,
        'marking_scheme': None,
        'students': []
    }
    
    return jsonify({
        'status': 'success',
        'session_id': session_id
    })

@app.route('/api/upload-question-paper', methods=['POST'])
def upload_question_paper():
    """Upload and process a question paper"""
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'}), 400
    
    file = request.files['file']
    session_id = request.form.get('session_id')
    
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400
    
    if not session_id or session_id not in sessions:
        return jsonify({'status': 'error', 'message': 'Invalid session ID'}), 400
    
    if file:
        session_dir = os.path.join(app.config['SESSION_FOLDER'], session_id)
        filename = secure_filename(file.filename)
        file_path = os.path.join(session_dir, 'question_paper.pdf')
        
        # Delete previous question paper if exists
        if os.path.exists(file_path):
            os.remove(file_path)
        
        file.save(file_path)
        
        try:
            # Extract text from question paper
            question_paper_text = text_extraction.extract_text_from_pdf_file(file_path)
            
            # Generate marking scheme
            marking_scheme = marking_scheme_generation.extract_marking_scheme(question_paper_text)
            
            # Save marking scheme
            marking_scheme_path = os.path.join(session_dir, 'marking_scheme.json')
            with open(marking_scheme_path, 'w') as f:
                f.write(marking_scheme)
            
            # Update session data
            sessions[session_id]['question_paper'] = file_path
            sessions[session_id]['marking_scheme'] = marking_scheme
            
            return jsonify({
                'status': 'success',
                'message': 'Question paper uploaded and processed successfully',
                'marking_scheme': marking_scheme
            })
        
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Error processing question paper: {str(e)}'
            }), 500

@app.route('/api/upload-student-submission', methods=['POST'])
def upload_student_submission():
    """Upload and process a student's submission"""
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'}), 400
    
    file = request.files['file']
    session_id = request.form.get('session_id')
    student_name = request.form.get('student_name')
    student_id = request.form.get('student_id')
    
    if file.filename == '' or not student_name or not student_id:
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
    
    if not session_id or session_id not in sessions:
        return jsonify({'status': 'error', 'message': 'Invalid session ID'}), 400
    
    if 'marking_scheme' not in sessions[session_id] or not sessions[session_id]['marking_scheme']:
        return jsonify({'status': 'error', 'message': 'Please upload question paper first'}), 400
    
    if file:
        session_dir = os.path.join(app.config['SESSION_FOLDER'], session_id)
        student_dir = os.path.join(session_dir, f'student_{student_id}')
        
        # Delete previous student directory if it exists
        if os.path.exists(student_dir):
            shutil.rmtree(student_dir)
        
        os.makedirs(student_dir, exist_ok=True)
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(student_dir, 'submission.pdf')
        file.save(file_path)
        
        # try:
        #     # Extract text from student submission
        #     student_text = text_extraction.extract_text_from_pdf_file(file_path)
            
        #     # Extract student answers
        #     answer_script = answer_extraction.extract_student_scipts(student_text)
            
        #     # Save answers
        #     answers_path = os.path.join(student_dir, 'answers.json')
        #     with open(answers_path, 'w') as f:
        #         f.write(answer_script)
            
        #     # Evaluate answers
        #     marking_scheme = sessions[session_id]['marking_scheme']
        #     result = evaluation.grade_all_answers(marking_scheme, answer_script)
            
        #     # Save evaluation results
        #     result_path = os.path.join(student_dir, 'result.json')
        #     with open(result_path, 'w') as f:
        #         json.dump(result, f)
            
        #     # Update session data - replace student if exists
        #     student_info = {
        #         'student_id': student_id,
        #         'student_name': student_name,
        #         'submission_path': file_path,
        #         'answers_path': answers_path,
        #         'result_path': result_path,
        #         'result': result
        #     }
        try:
            # [E101] Extract text from student submission
            student_text = text_extraction.extract_text_from_pdf_file(file_path)

    # [E102] Extract student answers
            answer_script = answer_extraction.extract_student_scipts(student_text)

    # [E103] Save extracted answers to file with UTF-8 encoding
            answers_path = os.path.join(student_dir, 'answers.json')
            with open(answers_path, 'w', encoding='utf-8') as f:
                f.write(answer_script)

    # [E104] Evaluate answers using marking scheme
            marking_scheme = sessions[session_id]['marking_scheme']
            result = evaluation.grade_all_answers(marking_scheme, answer_script)

    # [E105] Save evaluation results with UTF-8 encoding
            # result_path = os.path.join(student_dir, 'result.json')
            # with open(result_path, 'w', encoding='utf-8') as f:
            #     json.dump(result, f, ensure_ascii=False, indent=2)

            result_path = os.path.join(student_dir, 'result.json')
            with open(result_path, 'w', encoding='utf-8') as f:
               f.write(result)

    # [E106] Update session data - replace student if exists
            student_info = {
        'student_id': student_id,
        'student_name': student_name,
        'submission_path': file_path,
        'answers_path': answers_path,
        'result_path': result_path,
        'result': result
        }

            
            # Remove existing student entry if any
            sessions[session_id]['students'] = [s for s in sessions[session_id]['students'] 
                                               if s['student_id'] != student_id]
            # Add new student entry
            sessions[session_id]['students'].append(student_info)
            
            return jsonify({
                'status': 'success',
                'message': 'Student submission processed successfully',
                'result': result
            })
        
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Error processing student submission: {str(e)}'
            }), 500


      
@app.route('/api/delete-student', methods=['DELETE'])
def delete_student():
    """Delete a student's submission from a session"""
    session_id = request.args.get('session_id')
    student_id = request.args.get('student_id')
    
    if not session_id or session_id not in sessions:
        return jsonify({'status': 'error', 'message': 'Invalid session ID'}), 400
    
    if not student_id:
        return jsonify({'status': 'error', 'message': 'Student ID required'}), 400
    
    # Remove from session data
    sessions[session_id]['students'] = [s for s in sessions[session_id]['students'] 
                                       if s['student_id'] != student_id]
    
    # Delete student directory
    student_dir = os.path.join(app.config['SESSION_FOLDER'], session_id, f'student_{student_id}')
    if os.path.exists(student_dir):
        shutil.rmtree(student_dir)
    
    return jsonify({
        'status': 'success',
        'message': f'Student {student_id} removed successfully'
    })

@app.route('/api/delete-all-students', methods=['DELETE'])
def delete_all_students():
    """Delete all student submissions from a session"""
    session_id = request.args.get('session_id')
    
    if not session_id or session_id not in sessions:
        return jsonify({'status': 'error', 'message': 'Invalid session ID'}), 400
    
    # Clear students array
    sessions[session_id]['students'] = []
    
    # Delete all student directories
    session_dir = os.path.join(app.config['SESSION_FOLDER'], session_id)
    for dir_name in os.listdir(session_dir):
        if dir_name.startswith('student_'):
            student_dir = os.path.join(session_dir, dir_name)
            shutil.rmtree(student_dir)
    
    return jsonify({
        'status': 'success',
        'message': 'All students removed successfully'
    })

@app.route('/api/reset-session', methods=['POST'])
def reset_session():
    """Reset a session (delete question paper and all students)"""
    session_id = request.form.get('session_id')
    
    if not session_id or session_id not in sessions:
        return jsonify({'status': 'error', 'message': 'Invalid session ID'}), 400
    
    session_dir = os.path.join(app.config['SESSION_FOLDER'], session_id)
    
    # Option 1: Delete and recreate directory
    if os.path.exists(session_dir):
        shutil.rmtree(session_dir)
    os.makedirs(session_dir, exist_ok=True)
    
    # Reset session data but keep the same ID
    sessions[session_id] = {
        'id': session_id,
        'created_at': datetime.datetime.now().isoformat(),
        'question_paper': None,
        'marking_scheme': None,
        'students': []
    }
    
    return jsonify({
        'status': 'success',
        'message': 'Session reset successfully'
    })

@app.route('/api/delete-session', methods=['DELETE'])
def delete_session():
    """Delete a session completely"""
    session_id = request.args.get('session_id')
    
    if not session_id or session_id not in sessions:
        return jsonify({'status': 'error', 'message': 'Invalid session ID'}), 400
    
    # Delete session directory
    session_dir = os.path.join(app.config['SESSION_FOLDER'], session_id)
    if os.path.exists(session_dir):
        shutil.rmtree(session_dir)
    
    # Remove from sessions dictionary
    del sessions[session_id]
    
    return jsonify({
        'status': 'success',
        'message': 'Session deleted successfully'
    })

@app.route('/api/get-session-results', methods=['GET'])
def get_session_results():
    """Get all results for a session"""
    session_id = request.args.get('session_id')
    
    if not session_id or session_id not in sessions:
        return jsonify({'status': 'error', 'message': 'Invalid session ID'}), 400
    
    session_data = sessions[session_id]
    
    return jsonify({
        'status': 'success',
        'session_id': session_id,
        'has_question_paper': session_data['question_paper'] is not None,
        'students': [
            {
                'student_id': student['student_id'],
                'student_name': student['student_name'],
                'result': student['result']
            }
            for student in session_data['students']
        ]
    })

@app.route('/api/download-results', methods=['GET'])
def download_results():
    """Generate and download a CSV of all results for a session"""
    import csv
    from io import StringIO
    
    session_id = request.args.get('session_id')
    
    if not session_id or session_id not in sessions:
        return jsonify({'status': 'error', 'message': 'Invalid session ID'}), 400
    
    session_data = sessions[session_id]
    
    # Create CSV in memory
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Student ID', 'Student Name', 'Total Score', 'Question Details'])
    
    # Write student data
    for student in session_data['students']:
        result = student['result']
        writer.writerow([
            student['student_id'],
            student['student_name'],
            result.get('total_score', 'N/A'),
            json.dumps(result.get('question_scores', {}))
        ])
    
    # Prepare response
    output.seek(0)
    return send_file(
        StringIO(output.getvalue()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'results_{session_id}.csv'
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)