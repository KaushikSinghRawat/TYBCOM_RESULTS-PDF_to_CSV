from os import remove, path

def is_number(s): #Checks whether the data is a number or not
    try:
        float(s)
        return True
    except ValueError:
        return False

def delete_file(file_name): #Deletes file
    if path.exists(file_name):
        remove(file_name)

def main():

    #Extracting data relating to students only
    with open("files/TYBCOM 2023 Semester 5 Marksheet (PDF Converted to Text).txt", "r") as file:
        lines = file.readlines()
    
    student_data_check = False #Used to check whether the current line is related to student data (Marks of students)
    
    #Extracts data relating to students and adds it to 'finalised.txt' file
    for line in lines:
            
            # Check for the start of student data section
            if '(23120) 10: Comp. Sys & Appl.-I' in line:
                student_data_check = True
                continue
            
            if '(Th:75/30, In:25/10,Cr.Pt.: 3)' in line:
                continue

            # Check for the end of student data section
            if '#:0.229; @:O.5042A/O.5043A/O.5044A; *:O.5045A; /:FEMALE; AA/ABS: ABSENT; P: PASSES; F: FAIL; E: EXMP CAN BE CLAIMED;' in line or '(23114) 1: Commerce-V' in line:
                student_data_check = False
                continue

            # Extract student information only when within the student data section
            if student_data_check and line.strip():
                with open("files/finalised.txt", "a") as file:
                    file.write(line)

    #Cleaning data
    with open('files/finalised.txt', 'r') as file:
        lines = file.readlines()

    #Cleans data by removing unwanted strings, and stores it in 'csv' format to a 'finalised.csv' file
        
    for line in lines:
        if '------------------------------------------------------------------------------------------------------------------------------------------------' in line:
            line = line.replace('-', '')

            with open("files/finalised.csv", "a") as file:
                    file.write('\n')
                    line_values = line.split()
                    
                    name = '' #Stores name of a person

                    #Extracts the name by using string slices
                    for i in line_values[1:-2]:
                        name += f'{i} '
                    name += line_values[-1]
                    
                    if '/' in name:
                        name = name[1:]
                    
                    line_values = [line_values[0], name]
                    for i in line_values:
                          file.write(f'{i},')
            continue
        
        line_values = line.split()
        
        #Removes '@' sign used to denote additional/grace marks, adds the additional/grace marks to the total marks
        if '@' in line_values[0]:
            line_values[0] = str(sum(map(int, line_values[0].split('@'))))

        if is_number(line_values[0]) and len(line_values[0]) >= 3: 
            with open("files/finalised.csv", "a") as file:
                    file.write(f'{line_values[0]},')

    with open('files/finalised.csv', 'r') as file:
        lines = file.readlines()
    
    #Appends the headings of columns
    with open("files/final_2.csv", "a") as file:
            file.write('SEAT_NO,NAME,COLLEGE_CODE,TOTAL,GPA,RESULT\n')

    #Adds whether the student has passed or not
    for line in lines[1:]:
        line = line[:-2]
        temp_line = line.split(',')

        #1023397,BREED VINAYAK ARPANA,1122,
        if len(temp_line) < 4: #Certain students don't have total marks (Due to being Absent - 'ABS')'
            temp_line.append('ABSENT')
            line = ",".join(temp_line)
    
        if len(temp_line) < 5:
            line += ',0,F'
        else:
            line += ',P'

        with open("files/final_2.csv", "a") as file:
            file.write(f'{line}\n')
    
    #Adds additional info such as College Name, College Nickname, and Location in the csv based on College Code.
    #Also formats the csv to include college code, etc. in the end of a line.
    
    college_codes_info = {
        435: ("K. M. Agrawal College of Arts,Commerce and Science", "K.M. Agarwal College", "Kalyan"),
        645: ("The East Kalyan Welfare Society's Model College of Science & Commerce",  "Model College", "Kalyan"),
        1122: ("B. K. Birla College of Arts, Science & Commerce",   "B.K. Birla College",	"Kalyan"), 
        616: ("Mohindar Singh Kabal Singh Degree College of Arts & Commerce",   "M.K. College", "Kalyan"),
        920: ("Kamaladevi College of Arts and Commerce",    "Kamaladevi College",  "Kalyan"),
        584: ("Seth Hirachand Mutha College",	"Hirachand College",	"Kalyan"),
        225: ("Sonopant Dandekar Arts, V.S. Apte Commerce and M. H. Mehta Science College",	"SDSM College",	"Palghar"),
        363: ("Shree Panchal Samaj Madhyavarti Mandal's Yeshwantrao Chaphekar College of Arts and Commerce",	"Yeshwantrao College",	"Palghar"),
        361: ("Annasaheb Vartak College of Arts, Kedarnath Malhotra College of Commerce, E. S. Andrades College of Science",	"Vartak College",	"Vasai"),
        548: ("Bhaskar Waman Thakur College of Science, Yashwant Keshav Patil College of Commerce, Vidhya Dayanand Patil College of Arts",	"VIVA College",	"Virar"),
        149: ("Our Lady of Grace Trusts St.Gonsalo Garcia College of Arts and Commerce",	"G.G. College",	"Vasai"),
        952: ("Sahyadri Shikshan Seva Mandal's Arts and Commerce College",	"Sahyadri Shikshan College",	"Naigaon"),
        893: ("Dr Babasaheb Ambedkar College of Science and Advocate Gurunath Kulkarni College of Commerce",	"Ambedkar College",	"Vasai"),
        430: ("Dyandeep Mandal's St. Joseph Arts & Commerce",	"St. Joseph College",	"Virar")
        }
    
    #SEAT_NO,NAME,TOTAL,GPA,RESULT,COLLEGE_CODE,COLLEGE_NAME,COLLEGE_NICKNAME,COLLEGE_LOCATION
    #1023356,TEJAS VAISHALI,167,0,F,435,K. M. Agrawal College of Arts,Commerce and Science,K.M. Agarwal College,Kalyan

    delete_file("files/TYBCOM 2023 Semester 5 Marksheet.csv") #Checks if file exists, if yes then deletes it

    with open("files/TYBCOM 2023 Semester 5 Marksheet.csv", "a") as file:
            file.write('SEAT_NO,NAME,TOTAL,GPA,RESULT,COLLEGE_CODE,COLLEGE_NAME,COLLEGE_NICKNAME,COLLEGE_LOCATION\n')

    with open('files/final_2.csv', 'r') as file:
        lines = file.readlines()
    
    for line in lines[1:]:
        line = line[:-1]
        temp_line = line.split(',')

        college_code = int(temp_line.pop(2))
        temp_line.append(str(college_code))
        
        for college_info in college_codes_info[college_code]:
            temp_line.append(college_info)

        line = ",".join(temp_line)

        with open("files/TYBCOM 2023 Semester 5 Marksheet.csv", "a") as file:
            file.write(f"{line}\n")
        

    
    #Deletes temp files created for cleaning in stages
    delete_file("files/finalised.txt")
    delete_file("files/finalised.csv")
    delete_file("files/final_2.csv")

if __name__ == "__main__":
    main()