import requests, re, json
from bs4 import BeautifulSoup as bs

r = requests.get('https://calendar.carleton.ca/undergrad/courses/')
#print(r.content)

soup = bs(r.content, 'html.parser')
my_string = str(soup.find_all(class_="course"))

my_list = re.findall(r'href="(\w+)/', my_string)
#print(my_list)
for s in my_list:
    fileName = "courses/"+s
    f = open(fileName, "w+")
    str_to_use = 'https://calendar.carleton.ca/undergrad/courses/' + s + '/'
    r = requests.get(str_to_use)
    soup = bs(r.content, 'html.parser').find_all(class_="courseblock")
    #for s in my_string:
    for courseblock in soup:
        try:
            course_identifier = courseblock.find('span', {'class': 'courseblockcode'}).text.replace(u"\u00A0", " ")
            course_title = courseblock.find('span', {'class': 'courseblocktitle'}).text.split('\n')[0].replace(course_identifier, '').strip().replace(u"\u00A0", "")
            course_number = int(course_identifier.split()[-1])
            course_desc = courseblock.text.replace(u"\u00A0", " ")
            prereq_elem = courseblock.find('div', {'class': 'coursedescadditional'})
            if prereq_elem and 'Prerequisite(s):' in prereq_elem.text:
                course_prerequisites = prereq_elem.text.split('Prerequisite(s):')[1].split('.')[0].strip().replace(u"\u00A0", "")
            else:
                course_prerequisites = None

            data = {
                "course_identifier": course_identifier,
                "course_code": course_identifier[0:4] + course_identifier[5:],
                "course_number": course_number,
                "course_title": course_title,
                "course_desc": course_desc,
                "course_prerequisites": course_prerequisites
            }

            json_data = json.dumps(data, indent=4)
            f.write(json_data)
            f.write("\n\n")
        except:
            continue
    #print(soup)



#for s in my_list:


#print(better.find_all("<a"))