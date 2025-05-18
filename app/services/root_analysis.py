def analyze_student(student):
    causes = []
    if student['attendance'] < 75:
        causes.append("Low Attendance")
    if student['math_marks'] < 40:
        causes.append("Weak in Math")
    if student['science_marks'] < 40:
        causes.append("Weak in Science")
    if student['behavior'].lower() == 'distracted':
        causes.append("Needs Behavioral Support")
    return causes