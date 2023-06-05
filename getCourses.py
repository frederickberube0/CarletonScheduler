import requests, re, json
from bs4 import BeautifulSoup as bs

def main():
    """This python script will create a text file with every course from a major using request for web scraping."""
    i = 0
    for major in getMajors():
        print(f"Completed {i}/108 majors. Currently loading {major}.")
        i += 1
        writeCourses(major, getCourses(major))
    print("Course loading complete.")

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
        course_identifier = courseblock.find('span', {'class': 'courseblockcode'}).text.replace(u"\u00A0", " ")
        course_title = courseblock.find('span', {'class': 'courseblocktitle'}).text.split('\n')[0].replace(course_identifier, '').strip().replace(u"\u00A0", "")
        course_number = int(course_identifier.split()[-1])
        course_desc = courseblock.text.split("\n")[3].replace(u"\u00A0", " ")
        prereq_elem = courseblock.find('div', {'class': 'coursedescadditional'})
        if prereq_elem:
            for br in prereq_elem.find_all('br'):
                br.replace_with('\n')
            
            course_extra_details = prereq_elem.text.replace(u"\u00A0", "")
            start = course_extra_details.find('Prerequisite(s):') + len("Prerequisite(s):")
            end = course_extra_details.find('\n', start)
            prerequisites = course_extra_details[start:end].lstrip()
            if course_extra_details.find("Prerequisite(s):") == -1: prerequisites = None
        else:
            course_extra_details = None
            prerequisites = None
        
        year_standing = 0
        def findYearStanding(prerequisites: str) -> int:
            """Return year standing"""
            if prerequisites.find("first-year") >= 0: return 1
            if prerequisites.find("second-year") >= 0: return 2
            if prerequisites.find("third-year") >= 0: return 3
            if prerequisites.find("fourth-year") >= 0: return 4
            return 0
        if prerequisites: year_standing = findYearStanding(prerequisites)


        data = {
            "course_identifier": course_identifier,
            "course_code": course_identifier[0:4] + course_identifier[5:],
            "course_number": course_number,
            "course_title": course_title,
            "course_desc": course_desc,
            "course_extra_details": course_extra_details,
            "course_prerequisites": prerequisites,
            "year_standing": year_standing
        }

        json_data = json.dumps(data, indent=4)
        courses = courses + json_data
        courses = courses + "\n\n"
    return courses

main()