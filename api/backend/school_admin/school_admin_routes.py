from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

school_admin = Blueprint('school_admin', __name__)

# ------------------------------------------------------------
@school_admin.route('/students', methods=['GET'])
def get_students():
    try:
        cursor = db.get_db().cursor()
        query = '''
            SELECT 
                u.user_id, u.full_name, u.email, u.dob, u.gender,
                gr.course_name, gr.grade, cr.company_name, cr.start_date, cr.end_date
            FROM user u
            LEFT JOIN grade_record gr ON u.user_id = gr.student_id
            LEFT JOIN co_op_record cr ON u.user_id = cr.student_id
            WHERE u.role = 'Student'
        '''
        cursor.execute(query)
        students = cursor.fetchall()
        return make_response(jsonify(students), 200)
    except Exception as e:
        current_app.logger.error(f'Error in get_students: {str(e)}')
        return make_response(jsonify({'error': str(e)}), 500)

# ------------------------------------------------------------
@school_admin.route('/students/<int:user_id>/grades', methods=['GET', 'POST'])
def student_grades(user_id):
    if request.method == 'GET':
        try:
            cursor = db.get_db().cursor()
            query = '''
                SELECT g.grade_id, g.course_name, g.grade, g.recorded_date
                FROM grade_record g
                WHERE g.student_id = %s
            '''
            cursor.execute(query, (user_id,))
            grades = cursor.fetchall()
            return make_response(jsonify(grades), 200)
        except Exception as e:
            current_app.logger.error(f'Error in get_student_grades: {str(e)}')
            return make_response(jsonify({'error': str(e)}), 500)
    elif request.method == 'POST':
        try:
            grade_data = request.json
            cursor = db.get_db().cursor()
            query = '''
                INSERT INTO grade_record (student_id, course_name, grade, recorded_by)
                VALUES (%s, %s, %s, %s)
            '''
            cursor.execute(query, (user_id, grade_data['course_name'], grade_data['grade'], grade_data['recorded_by']))
            db.get_db().commit()
            return make_response(jsonify({'message': 'Grade added successfully'}), 201)
        except Exception as e:
            current_app.logger.error(f'Error in add_student_grade: {str(e)}')
            return make_response(jsonify({'error': str(e)}), 500)

# ------------------------------------------------------------
@school_admin.route('/students/<int:user_id>/grades/<int:grade_id>', methods=['PUT', 'DELETE'])
def update_delete_student_grade(user_id, grade_id):
    if request.method == 'PUT':
        try:
            grade_data = request.json
            cursor = db.get_db().cursor()
            query = '''
                UPDATE grade_record
                SET course_name = %s, grade = %s
                WHERE grade_id = %s AND student_id = %s
            '''
            cursor.execute(query, (grade_data['course_name'], grade_data['grade'], grade_id, user_id))
            db.get_db().commit()
            return make_response(jsonify({'message': 'Grade updated successfully'}), 200)
        except Exception as e:
            current_app.logger.error(f'Error in update_student_grade: {str(e)}')
            return make_response(jsonify({'error': str(e)}), 500)
    elif request.method == 'DELETE':
        try:
            cursor = db.get_db().cursor()
            query = '''
                DELETE FROM grade_record
                WHERE grade_id = %s AND student_id = %s
            '''
            cursor.execute(query, (grade_id, user_id))
            db.get_db().commit()
            return make_response(jsonify({'message': 'Grade deleted successfully'}), 200)
        except Exception as e:
            current_app.logger.error(f'Error in delete_student_grade: {str(e)}')
            return make_response(jsonify({'error': str(e)}), 500)

# ------------------------------------------------------------
@school_admin.route('/students/<int:user_id>/coops', methods=['GET', 'POST'])
def student_coops(user_id):
    if request.method == 'GET':
        try:
            cursor = db.get_db().cursor()
            query = '''
                SELECT cr.co_op_id, cr.company_name, cr.start_date, cr.end_date
                FROM co_op_record cr
                WHERE cr.student_id = %s
            '''
            cursor.execute(query, (user_id,))
            coops = cursor.fetchall()
            return make_response(jsonify(coops), 200)
        except Exception as e:
            current_app.logger.error(f'Error in get_student_coops: {str(e)}')
            return make_response(jsonify({'error': str(e)}), 500)
    elif request.method == 'POST':
        try:
            coop_data = request.json
            cursor = db.get_db().cursor()
            query = '''
                INSERT INTO co_op_record (student_id, company_name, start_date, end_date)
                VALUES (%s, %s, %s, %s)
            '''
            cursor.execute(query, (user_id, coop_data['company_name'], coop_data['start_date'], coop_data['end_date']))
            db.get_db().commit()
            return make_response(jsonify({'message': 'Co-op added successfully'}), 201)
        except Exception as e:
            current_app.logger.error(f'Error in add_student_coop: {str(e)}')
            return make_response(jsonify({'error': str(e)}), 500)

# ------------------------------------------------------------
@school_admin.route('/students/<int:user_id>/coops/<int:coop_id>', methods=['PUT', 'DELETE'])
def update_delete_student_coop(user_id, coop_id):
    if request.method == 'PUT':
        try:
            coop_data = request.json
            cursor = db.get_db().cursor()
            query = '''
                UPDATE co_op_record
                SET company_name = %s, start_date = %s, end_date = %s
                WHERE co_op_id = %s AND student_id = %s
            '''
            cursor.execute(query, (coop_data['company_name'], coop_data['start_date'], coop_data['end_date'], coop_id, user_id))
            db.get_db().commit()
            return make_response(jsonify({'message': 'Co-op updated successfully'}), 200)
        except Exception as e:
            current_app.logger.error(f'Error in update_student_coop: {str(e)}')
            return make_response(jsonify({'error': str(e)}), 500)
    elif request.method == 'DELETE':
        try:
            cursor = db.get_db().cursor()
            query = '''
                DELETE FROM co_op_record
                WHERE co_op_id = %s AND student_id = %s
            '''
            cursor.execute(query, (coop_id, user_id))
            db.get_db().commit()
            return make_response(jsonify({'message': 'Co-op deleted successfully'}), 200)
        except Exception as e:
            current_app.logger.error(f'Error in delete_student_coop: {str(e)}')
            return make_response(jsonify({'error': str(e)}), 500)
