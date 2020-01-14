import sys
sys.path.append('.')
from examwiz_pkg.examwiz_pkg.gapi_app import grade_book as gb
from examwiz_pkg.examwiz_pkg.gapi_app import mailer as ml
import pandas as pd

def remind_tas(exam_path, exam_name):
    ta_workload = path + '/../ta_exam_workload.csv'


    book = gb.read_grade_book(exam_name)
    if not isinstance(book, pd.DataFrame):
        return book

    submits = set([str(i) for i in pd.read_csv(exam_path + '/student_details.csv').student_id.values])
    graded = set(book['Student ID'].values)

    remain = list(submits - graded)

    to_send = pd.DataFrame([[i] + list(gb.assigned_to(i, ta_workload)) for i in remain]).groupby([1,2])[0].apply(list)
    print(to_send)
    to_send = to_send.reset_index()


    for i in range(to_send.shape[0]):
        name, email, exams = to_send.iloc[0].values
        ml.send_message(ml.create_attached_message(
            sender='charles.cohen@nycdatascience.com',
            to=email,
            subject='Exams Remain to be Graded',
            msg=f"You have {len(exams)} exams\'s to grade. Please grade them promptly.\nUse the following form: {gb.get_link(exam_name)}",
            file_dir=exam_path,
            filenames=[e+'.R' for e in exams]
        ))


if __name__ == '__main__':
    #path = input('Path to exam submissions')
    #name = input('Name of Exam')
    path = 'demo/example_exam/student_submissions'
    name = 'Example Exam'
    remind_tas(path, name)
