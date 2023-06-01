import requests, re, json
from bs4 import BeautifulSoup as bs

def main():
    print(getPrograms())

def getPrograms() -> list[dict[str, str]]:
    """This function return a list of objects which contain program title and its url"""
    program_request = requests.get('https://calendar.carleton.ca/undergrad/undergradprograms/')
    parsed_major_request = bs(program_request.content, 'html.parser').find_all(class_="page_content")
    
    list_of_programs = []

    for line in (str(list(parsed_major_request)[0]).split("\n")):
        try:
            #print(line)
            pattern = r'<a href="([^"]+)">([^<]+)<'
            match = re.search(pattern, line)

            url = match.group(1)
            course = match.group(2)
            list_of_programs.append({
                "course": course,
                "url": url
            })
        except:
            pass
    return list_of_programs
    #print(list(parsed_major_request)[0].split("\n"))

#TODO
def getSpecializations(list_of_program_object: list[dict[str, str]]):
    pass

main()