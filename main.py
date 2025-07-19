import sqlite3

# Підключення до бази даних
data_base = sqlite3.connect('university.db')

cursor = data_base.cursor()

# Створення таблиць

cursor.execute('''
CREATE TABLE IF NOT EXISTS students(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name VARCHAR(100),
               age INTEGER,
               major VARCHAR(100)
               )''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS courses (
               course_id INTEGER PRIMARY KEY AUTOINCREMENT,
               course_name VARCHAR(100),
               instructor VARCHAR(100)
               )''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS student_courses (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               student_id INTEGER,
               course_id INTEGER,
               FOREIGN KEY (student_id) REFERENCES students(id),
               FOREIGN KEY (course_id) REFERENCES courses(course_id)
               )''')

while True:
    print("\n1. Додати нового студента")
    print("2. Додати новий курс")
    print("3. Показати список студентів")
    print("4. Показати список курсів")
    print("5. Зареєструвати студента на курс")
    print("6. Показати студентів на конкретному курсі")
    print("7. Вийти")
    choice = input("Оберіть опцію (1-7): ")

    # Додавання нового студента
    if choice == "1":
        name = input("Введіть ім'я студента: ").lower().strip() 
        age = int(input("Введіть вік студента: "))
        major = input("Введіть спеціальність студента: ")
        cursor.execute('INSERT INTO students (name, age, major) VALUES (?, ?, ?)', (name, age, major))
        data_base.commit()
        print("Студент доданий успішно.")

    # Додавання нового курсу
    elif choice == "2":
        course_name = input("Введіть назву курсу: ").lower().strip()
        instructor = input("Введіть ім'я викладача: ").lower().strip()
        cursor.execute('INSERT INTO courses (course_name, instructor) VALUES (?, ?)', (course_name, instructor))
        data_base.commit()
        print("Курс доданий успішно.")

    # Показати список студентів
    elif choice == "3":
        cursor.execute('SELECT * FROM students')
        students = cursor.fetchall()
        if students:
            print("Список студентів:")
            for student in students:
                print(f"ID: {student[0]}, Ім'я: {student[1]}, Вік: {student[2]}, Спеціальність: {student[3]}")
        else:
            print("Немає зареєстрованих студентів.")

    # Показати список курсів
    elif choice == "4":
        cursor.execute('SELECT * FROM courses')
        courses = cursor.fetchall()
        if courses:
            print("Список курсів:")
            for course in courses:
                print(f"ID: {course[0]}, Назва курсу: {course[1]}, Викладач: {course[2]}")
        else:
            print("Немає зареєстрованих курсів.")

    # Зареєструвати студента на курс
    elif choice == "5":
        student_id = int(input("Введіть ID студента: "))
        course_id = int(input("Введіть ID курсу: "))
        cursor.execute('INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)', (student_id, course_id))
        data_base.commit()
        print("Студент успішно зареєстрований на курс.")

    # Показати студентів на конкретному курсі
    elif choice == "6":
        course_id = int(input("Введіть ID курсу: "))
        cursor.execute('''
        SELECT students.id, students.name FROM students
        JOIN student_courses ON students.id = student_courses.student_id
        WHERE student_courses.course_id = ?''', (course_id,))
        enrolled_students = cursor.fetchall()
        if enrolled_students:
            print(f"Студенти на курсі з ID {course_id}:")
            for student in enrolled_students:
                print(f"ID: {student[0]}, Ім'я: {student[1]}")
        else:
            print("Немає студентів, зареєстрованих на цей курс.")

    # Вийти з програми
    elif choice == "7":
        break
    else:
        print("Некоректний вибір. Будь ласка, введіть число від 1 до 7.")