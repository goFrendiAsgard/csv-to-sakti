import os, sys, csv

def normalize_score (score, min_score, max_score):
    score = float(score)
    return 100 * (score - min_score) / (max_score - min_score)

def get_nrp (email):
    email_fragment = email.split('@')
    return email_fragment[0]

def student_list_to_js (student_list, default_assignment_score):
    script = []
    for student in student_list:
        nrp = student['nrp']
        score = student['score']
        script.append('$("#nilai_uts_' + nrp + '").val(' + str(int(round(score)))+');')
        script.append('$("#nilai_tugas_' + nrp + '").val(' + str(int(round(default_assignment_score))) + ');')
    return ''.join(script)

def csv_to_js (csv_file_name, min_score, max_score, default_assignment_score):
    csv_file = open(csv_file_name, 'r')
    reader = csv.reader(csv_file, delimiter=',', quotechar='|')
    student_list = []
    for index, row in enumerate(reader):
        if index == 0: # first row is header, ignore it
            continue
        student_list.append({
            'nrp': get_nrp(row[4]), 
            'score': normalize_score(row[9], min_score, max_score)
        })
    return student_list_to_js(student_list, default_assignment_score)

if __name__ == '__main__':
    csv_file_name = sys.argv[1]
    min_score = float(sys.argv[2]) if 2 < len(sys.argv) else 0.0
    max_score = float(sys.argv[3]) if 3 < len(sys.argv) else 100.0
    default_assignment_score = float(sys.argv[4]) if 4 < len(sys.argv) else 80.0
    print(csv_to_js(csv_file_name, min_score, max_score, default_assignment_score))
