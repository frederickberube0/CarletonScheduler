import requests, re, json
from bs4 import BeautifulSoup as bs

def main():
    for obj in getPrograms():
        for specialization in getSpecializations(obj):
            makeTablesFromSpecialization(specialization)

def getPrograms() -> list[dict[str, str]]:
    """This function return a list of programs in dictionary form which contain program title and its url"""
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

def getSpecializations(program: dict[str, str]) -> list[dict[str, str]]:
    """Takes a an program (COMP, BUSI) object in form {course, url} and returns it's specialization in form {link, program_name, url}"""
    #/undergrad/undergradprograms/undeclared/
    
    url = "https://calendar.carleton.ca" + program["url"]
    program_request = requests.get(url)
    
    #Page content
    program_request_page_content = bs(program_request.content, 'html.parser').find_all(id="textcontainer")
    specialization_list = bs(str(program_request_page_content[0]), 'html.parser').find_all('li')

    object_list = []
    for specialization in specialization_list:
        #print(line)
        parsed_line = bs(str(specialization), 'html.parser')
        link = parsed_line.find('a')['href']
        program_name = parsed_line.find('a').text
        result = {'link': link, 'program_name': program_name, 'page_content': program_request_page_content}
        object_list.append(result)

    return object_list

def makeTablesFromSpecialization(obj: dict[str, str]):
    """Takes a specialization object in form {link, program_name, page_content} and write to file"""
    print(obj['link'][1:])
    h3_tag = bs(str(obj['page_content']), 'html.parser').find('h3', {'id': obj['link'][1:]})
    table = h3_tag.find_next_sibling()#('div', {'class': 'table-container'}).find('table')
    #print(table)
    for row in table.find_all('tr'):
        cells = row.find_all(['th', 'td'])
        print([cell.text.strip() for cell in cells])


main()