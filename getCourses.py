import requests, re, json
from bs4 import BeautifulSoup as bs

def main():
    """This python script will create a text file with every course from a major using request for web scraping."""
    for major in getMajors():
        writeCourses(major, getCourses(major))

def writeCourses(major: str, content: str) -> None:
    """Write content into file named based on the major."""
    file_name = "courses/"+major
    file = open(file_name, "w+")
    file.write(content)

def getMajors() -> list[str]:
    """Returns list of every major at Carleton University in it's four letter code format (COMP, BUSI, HIST...)"""
    major_request = requests.get('https://calendar.carleton.ca/undergrad/courses/')
    parsed_major_request = str(bs(major_request.content, 'html.parser').find_all(class_="course"))
    
    #Using Regex, get all four letter codes
    list_of_majors = re.findall(r'href="(\w+)/', parsed_major_request) 
    return list_of_majors

def getCourses(major: str) -> str:
    """Return every courses from a major in JSON format, in a long string"""
    courses = ""
    url_of_major = 'https://calendar.carleton.ca/undergrad/courses/' + major + '/'
    request = requests.get(url_of_major)
    parsed_page = bs(request.content, 'html.parser').find_all(class_="courseblock")

    for courseblock in parsed_page:
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
            courses = courses + json_data
            courses = courses + "\n\n"
        except:
            continue
    return courses

main()