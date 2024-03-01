from flask import Flask, render_template, request, url_for, redirect, flash
from htmlmin import minify
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замініть це на реальний ключ

# Функція для виконання SQL-запитів
def execute_query(query, data=None, fetchall=True):
    try:
        connection = mysql.connector.connect(
            host='crmstroy.mysql.tools',
            user='crmstroy_nazar',
            password='+9)Y2Dfpe4',
            database='crmstroy_nazar'
        )
        if connection.is_connected():
            cursor = connection.cursor()

            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)

            if fetchall:
                result = cursor.fetchall()
            else:
                result = None

            connection.commit()
            cursor.close()
            connection.close()
            return result
        else:
            print("Не вдалося підключитися до бази даних")
            return ''
        
    except Exception as e:
        print(f"Помилка підключення до бази даних: {e}")
        return ''

# Головна сторінка
@app.route('/', methods=['GET'])
def index():
    try:
        html_content = render_template('index.html')
        minified_html = minify(html_content, remove_comments=True, remove_empty_space=True)
        return minified_html
    except Exception as e:
        print(e)


##############      Все шо стосується предметів         #################################################################################################################
        
# Реалізація пошуку предметів та фільтрів
@app.route('/subject', methods=['GET'])
def subject():
    try:
        # Формуємо частину SQL-запиту для фільтрації результатів
        search_predmet = request.args.get('search_predmet', '')
        if search_predmet:
            PredmetSQL = f"AND UPPER(name) LIKE UPPER('%{search_predmet}%') "
        else:
            PredmetSQL = ''
        
        query = f""" 
        SELECT 
            * 
        FROM 
            `subjects` 
        WHERE 
            id != ''
            {PredmetSQL}
        ORDER BY 
            `id` ASC 
        """
        result = execute_query(query)

        html_content = render_template('subject.html', subjects=result, search_predmet=search_predmet)
        minified_html = minify(html_content, remove_comments=True, remove_empty_space=True)
        return minified_html
    except Exception as e:
        print(e)

        
# Предмети - внутрішня сторінка
@app.route('/subject/<id>', methods=['GET'])
def subject_view(id):
    try:
        
        query = f""" 
        SELECT 
            * 
        FROM 
            `subjects` 
        WHERE 
            id = '{id}'
        LIMIT 
            1
        """
        result = execute_query(query)
        
        html_content = render_template('subject.html', result=result)
        minified_html = minify(html_content, remove_comments=True, remove_empty_space=True)
        return minified_html
    except Exception as e:
        print(e) 

#Редагування предмета
@app.route('/subject/<id>/edit', methods=['POST'])
def subject_edit(id):
    try:
        name_subject = request.form.get('name_subject', '') 

        query = f""" UPDATE `subjects` SET `name` = '{name_subject}' WHERE `subjects`.`id` = {id} """
        result = execute_query(query)

        return redirect(url_for('subject_view', id=id))
        
    except Exception as e:
        print(e)


##########      1 крок додавання предмета      ##########

# Додавання предмета (сторінка)
@app.route('/subject/add1', methods=['GET'])
def subject_add1():
    try:
        html_content = render_template('subject/add1.html')
        minified_html = minify(html_content, remove_comments=True, remove_empty_space=True)
        return minified_html
    except Exception as e:
        print(e)

# Додавання предмета (функціонал)
@app.route('/addsubjecttolist', methods=['POST'])
def addsubjecttolist():
    try:
        if request.method == 'POST':
            # Отримати дані про нового студента з форми
            name = request.form.get('name')

            # Виконати запит для додавання студента до бази даних
            query = f""" 
            INSERT INTO `subjects` (`name`)
            VALUES ('{name}')
            """
            execute_query(query)

            # Перенаправити користувача на сторінку зі списком студентів або іншу відповідну сторінку
            return redirect(url_for('table'))
        
    except Exception as e:
        print(e)

##########      /1 крок додавання предмета      ##########

##########      2 крок додавання предмета      ##########

# Додавання таблиці зв'язків
@app.route('/table', methods=['GET'])
def table():
    try:

        # період
        query = f""" 
        SELECT 
            *,
            YEAR(`start`) AS start_years,
            YEAR(`end`) AS end_years
        FROM 
            `period`
        ORDER BY 
            `start` DESC
        """
        periods = execute_query(query)

        # семестр
        query = f""" 
        SELECT 
            *
        FROM 
            `semestr`
        ORDER BY 
            `id` ASC
        """
        semesters = execute_query(query)

        # курс
        query = f""" 
        SELECT 
            *
        FROM 
            `course`
        ORDER BY 
            `id` ASC
        """
        courses = execute_query(query)

        # групи
        query = f""" 
        SELECT 
            *
        FROM 
            `groups`
        ORDER BY 
            `id` ASC
        """
        groups = execute_query(query)

        # предмети
        query = f""" 
        SELECT 
            *
        FROM 
            `subjects`
        ORDER BY 
            `id` ASC
        """
        subjects = execute_query(query)

        html_content = render_template('table.html', periods=periods, semesters=semesters, courses=courses, groups=groups, subjects=subjects)
        minified_html = minify(html_content, remove_comments=True, remove_empty_space=True)
        return minified_html
    except Exception as e:
        print(e)

# Редагування таблиці
@app.route('/table/add', methods=['POST'])
def add_to_table():
    try:
        # Отримання даних з форми
        id_period = request.form.get('id_period')
        id_semester = request.form.get('id_semester')
        id_course = request.form.get('id_course')
        id_group = request.form.get('id_group')
        id_subjects = request.form.get('id_subjects')

        # Збереження даних в таблицю groups_subjects
        query = """
        INSERT INTO groups_subjects (id_period, id_semestr, id_course, id_group, id_subjects)
        VALUES (%s, %s, %s, %s, %s)
        """
        data = (id_period, id_semester, id_course, id_group, id_subjects)

        execute_query(query, data)

        flash("Дані збережено!", 'success')
        return redirect(url_for('table',  # Додано параметри для передачі значень фільтрів
                                id_period=id_period,
                                id_semester=id_semester,
                                id_course=id_course,
                                id_group=id_group,
                                id_subjects=id_subjects))

    except Exception as e:
        flash(f"Помилка збереження даних: {e}", 'error')
        return redirect(url_for('table'))
    
##########      /2 крок додавання предмета      ##########

##############      Все шо стосується груп         #################################################################################################################

# Групи
@app.route('/groups', methods=['GET'])
def groups():
    try:
        # Отримуємо параметр search_group з параметрів запиту (GET)
        search_group = request.args.get('search_group', '')
        
        # Формуємо частину SQL-запиту для фільтрації результатів
        if search_group:
            groupsSQL = f"AND UPPER(name) LIKE UPPER('%{search_group}%') "
        else:
            groupsSQL = ''
            
        # Формуємо частину SQL-запиту для фільтру період
        id_period = request.args.get('id_period', '')
        if id_period:
            id_periodSQL = f"AND id_period = '{id_period}' "
        else:
            id_periodSQL = ''

        # Формуємо частину SQL-запиту для фільтру семестр
        id_semester = request.args.get('id_semester', '')
        if id_semester:
            id_semesterSQL = f"AND id_semestr = '{id_semester}' "
        else:
            id_semesterSQL = ''

        # Формуємо SQL-запит з урахуванням фільтрації та сортування
        query = f""" 
        SELECT 
            * 
        FROM 
            `groups` 
        WHERE   
            id != ''
            {groupsSQL} {id_periodSQL} {id_semesterSQL}
        ORDER BY 
            `id` ASC 
        """
        # Викликаємо функцію execute_query для виконання SQL-запиту
        result = execute_query(query)

        # період
        query = f""" 
        SELECT 
            *,
            YEAR(`start`) AS start_years,
            YEAR(`end`) AS end_years
        FROM 
            `period`
        ORDER BY 
            `start` DESC
        """
        periods = execute_query(query)

        # семестр
        query = f""" 
        SELECT 
            *
        FROM 
            `semestr`
        ORDER BY 
            `id` ASC
        """
        semesters = execute_query(query)

        # Передаємо результат в шаблон "groups.html" разом із значенням search_group
        html_content = render_template('groups.html', groups=result, search_group=search_group, periods=periods, semesters=semesters)
        minified_html = minify(html_content, remove_comments=True, remove_empty_space=True)
        return minified_html
    except Exception as e:
        print(e)

# Редагування групи
@app.route('/groups/<id>/edit', methods=['POST'])
def group_edit(id):
    try:
        name_group = request.form.get('name_group') 

        query = f""" UPDATE `groups` SET `name` = '{name_group}' WHERE `groups`.`id` = {id} """
        result = execute_query(query)

        groups_query = f""" 
        SELECT 
            *
        FROM 
            `groups`
        ORDER BY 
            `id` ASC
        """
        groups = execute_query(groups_query)

        # return redirect(url_for('groups', id=id))
        html_content = render_template('groups.html', groups=groups)
        minified_html = minify(html_content, remove_comments=True, remove_empty_space=True)
        return minified_html
    except Exception as e:
        print(e)

# Додавання групи (сторінка)
@app.route('/groups/add1', methods=['GET'])
def groups_add1():
    try:
        html_content = render_template('groups/add1.html')
        minified_html = minify(html_content, remove_comments=True, remove_empty_space=True)
        return minified_html
    except Exception as e:
        print(e)

# Додавання групи (функціонал)
@app.route('/addgrouptolist', methods=['POST'])
def addgrouptolist():
    try:
        if request.method == 'POST':
            # Отримати дані про нової групи з форми
            name = request.form.get('name')

            # Виконати запит для додавання групи до бази даних
            query = f""" 
            INSERT INTO `groups` (`name`)
            VALUES ('{name}')
            """
            execute_query(query)

            # Перенаправити користувача на сторінку зі списком груп або іншу відповідну сторінку
            return redirect(url_for('groups/add1'))
        
    except Exception as e:
        print(e)

##############      Все шо стосується студентів         #################################################################################################################
        
#Студенти
@app.route('/students', methods=['GET'])
def students():
    try:
        # Отримуємо параметр search_student з параметрів запиту (GET)
        search_student = request.args.get('search_student', '')
        
        # Формуємо частину SQL-запиту для фільтрації результатів
        if search_student:
            studentSQL = f"AND UPPER(pid) LIKE UPPER('%{search_student}%') "
        else:
            studentSQL = ''
            
        # Формуємо частину SQL-запиту для фільтру період
        id_period = request.args.get('id_period', '')
        if id_period:
            id_periodSQL = f"AND id_period = '{id_period}' "
        else:
            id_periodSQL = ''

        # Формуємо частину SQL-запиту для фільтру семестр
        id_semester = request.args.get('id_semester', '')
        if id_semester:
            id_semesterSQL = f"AND id_semestr = '{id_semester}' "
        else:
            id_semesterSQL = ''

        # Формуємо частину SQL-запиту для фільтру груп
        id_group = request.args.get('id_group', '')
        if id_group:
            id_groupSQL = f"AND id_group = '{id_group}' "
        else:
            id_groupSQL = ''

        # Формуємо частину SQL-запиту для фільтру курсів
        id_course = request.args.get('id_course', '')
        if id_course:
            id_courseSQL = f"AND id_course = '{id_course}' "
        else:
            id_courseSQL = ''

        # Формуємо SQL-запит з урахуванням фільтрації та сортування
        query = f""" 
        SELECT 
            * 
        FROM 
            `students` 
        WHERE   
            id != ''
            {studentSQL} {id_periodSQL} {id_semesterSQL} {id_groupSQL} {id_courseSQL}
        ORDER BY 
            `id` ASC 
        """
        # Викликаємо функцію execute_query для виконання SQL-запиту
        result = execute_query(query)

        # період
        query = f""" 
        SELECT 
            *,
            YEAR(`start`) AS start_years,
            YEAR(`end`) AS end_years
        FROM 
            `period`
        ORDER BY 
            `start` DESC
        """
        periods = execute_query(query)

        # семестр
        query = f""" 
        SELECT 
            *
        FROM 
            `semestr`
        ORDER BY 
            `id` ASC
        """
        semesters = execute_query(query)

        # курс
        query = f""" 
        SELECT 
            *
        FROM 
            `course`
        ORDER BY 
            `id` ASC
        """
        courses = execute_query(query)

        # групи
        query = f""" 
        SELECT 
            *
        FROM 
            `groups`
        ORDER BY 
            `id` ASC
        """
        groups = execute_query(query)

        # студенти
        query = f""" 
        SELECT 
            *
        FROM 
            `students`
        ORDER BY 
            `id` ASC
        """
        students = execute_query(query)


        # Передаємо результат в шаблон "students.html" разом із значенням search_student
        html_content = render_template('students.html', students=result, search_student=search_student, periods=periods, semesters=semesters, groups=groups, courses=courses)
        minified_html = minify(html_content, remove_comments=True, remove_empty_space=True)
        return minified_html
    except Exception as e:
        print(e)

# Редагування студента
@app.route('/students/<id>/edit', methods=['POST'])
def student_edit(id):
    try:
        pid_student = request.form.get('pid_student') 

        query = f""" UPDATE `students` SET `pid` = '{pid_student}' WHERE `students`.`id` = {id} """
        result = execute_query(query)

        students_query = f""" 
        SELECT 
            *
        FROM 
            `students`
        ORDER BY 
            `id` ASC
        """
        students = execute_query(students_query)

        # return redirect(url_for('students_view', id=id))
        html_content = render_template('students.html', students=students)
        minified_html = minify(html_content, remove_comments=True, remove_empty_space=True)
        return minified_html
    except Exception as e:
        print(e)

# Студенти - внутрішня сторінка
@app.route('/students/<id>', methods=['GET'])
def students_view(id):
    try:
        # Формуємо частину SQL-запиту для фільтру період
        id_period = request.args.get('id_period', '')
        if id_period:
            id_periodSQL = f"AND id_period = '{id_period}' "
        else:
            id_periodSQL = ''

        # Формуємо частину SQL-запиту для фільтру семестр
        id_semester = request.args.get('id_semester', '')
        if id_semester:
            id_semesterSQL = f"AND id_semestr = '{id_semester}' "
        else:
            id_semesterSQL = ''

        # Формуємо частину SQL-запиту для фільтру курсів
        id_course = request.args.get('id_course', '')
        if id_course:
            id_courseSQL = f"AND id_course = '{id_course}' "
        else:
            id_courseSQL = ''

        query = f""" 
        SELECT 
            * 
        FROM 
            `students` 
        WHERE 
            id = '{id}'
        LIMIT 
            1
        """
        result = execute_query(query)


        
         # період
        query = f""" 
        SELECT 
            *,
            YEAR(`start`) AS start_years,
            YEAR(`end`) AS end_years
        FROM 
            `period`
        ORDER BY 
            `start` DESC
        """
        periods = execute_query(query)

        # семестр
        query = f""" 
        SELECT 
            *
        FROM 
            `semestr`
        ORDER BY 
            `id` ASC
        """
        semesters = execute_query(query)

        # курс
        query = f""" 
        SELECT 
            *
        FROM 
            `course`
        ORDER BY 
            `id` ASC
        """
        courses = execute_query(query)

        # Отримайте дані з бази даних
        query = f"""
        SELECT 
            a.id_subjects,
            a.ocenka,
            b.name
        FROM 
            ocenki a
            inner join subjects b on b.id = a.id_subjects
        WHERE 
            a.id_student = '{id}'
            {id_periodSQL} {id_semesterSQL} {id_courseSQL}
        ORDER BY 
            a.id ASC
        """
        ocenki = execute_query(query)
         
        html_content = render_template('students/index.html', id=id, result=result, ocenki=ocenki, periods=periods, semesters=semesters, courses=courses, 
                                       id_semester = id_semester)
        minified_html = minify(html_content, remove_comments=True, remove_empty_space=True)
        return minified_html
    except Exception as e:
        print(e) 



##########      students/add1      ##########

# Додавання студента (сторінка)
@app.route('/students/add1', methods=['GET'])
def students_add1():
    try:
        html_content = render_template('students/add1.html')
        minified_html = minify(html_content, remove_comments=True, remove_empty_space=True)
        return minified_html
    except Exception as e:
        print(e)

# Додавання студента (функціонал)
@app.route('/addstudenttolist', methods=['POST'])
def addstudenttolist():
    try:
        if request.method == 'POST':
            # Отримати дані про нового студента з форми
            pid = request.form.get('pid')

            # Виконати запит для додавання студента до бази даних
            query = f""" 
            INSERT INTO `students` (`pid`)
            VALUES ('{pid}')
            """
            execute_query(query)

            # Перенаправити користувача на сторінку зі списком студентів або іншу відповідну сторінку
            return redirect(url_for('addstudent'))
        
    except Exception as e:
        print(e)

##########      /students/add1      ##########
        

##########      students/addstudent      ##########

# Додавання зв'язків студентів
@app.route('/addstudent', methods=['GET'])
def addstudent():
    try:

        # період
        query = f""" 
        SELECT 
            *,
            YEAR(`start`) AS start_years,
            YEAR(`end`) AS end_years
        FROM 
            `period`
        ORDER BY 
            `start` DESC
        """
        periods = execute_query(query)

        # семестр
        query = f""" 
        SELECT 
            *
        FROM 
            `semestr`
        ORDER BY 
            `id` ASC
        """
        semesters = execute_query(query)

        # курс
        query = f""" 
        SELECT 
            *
        FROM 
            `course`
        ORDER BY 
            `id` ASC
        """
        courses = execute_query(query)

        # групи
        query = f""" 
        SELECT 
            *
        FROM 
            `groups`
        ORDER BY 
            `id` ASC
        """
        groups = execute_query(query)

        # студенти
        query = f""" 
        SELECT 
            *
        FROM 
            `students`
        ORDER BY 
            `id` ASC
        """
        students = execute_query(query)

        html_content = render_template('students/addstudent.html', periods=periods, semesters=semesters, courses=courses, groups=groups, students=students)
        minified_html = minify(html_content, remove_comments=True, remove_empty_space=True)
        return minified_html
    except Exception as e:
        print(e)

# Редагування зв'язків студентів
@app.route('/student/add', methods=['POST'])
def add_to_student():
    try:
        # Отримання даних з форми
        id_period = request.form.get('id_period')
        id_semestr = request.form.get('id_semestr')
        id_course = request.form.get('id_course')
        id_group = request.form.get('id_group')
        pid = request.form.get('pid')
        print(id_period, pid)

        # Збереження даних в таблицю students
        query = f"""
            UPDATE `students` SET `id_period` = '{id_period}', `id_semestr` = '{id_semestr}', `id_course` = '{id_course}', `id_group` = '{id_group}' WHERE `id` = '{pid}'
        """
        execute_query(query)

        flash("Дані збережено!", 'success')
        return redirect(url_for('addstudent',  # Додано параметри для передачі значень фільтрів
                                id_period=id_period,
                                id_semestr=id_semestr,
                                id_course=id_course,
                                id_group=id_group,
                                pid=pid))

    except Exception as e:
        flash(f"Помилка збереження даних: {e}", 'error')
        return redirect(url_for('addstudent'))


##########      /students/addstudent      ##########
    
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='9999')