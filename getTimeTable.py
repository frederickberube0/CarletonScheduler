#https://central.carleton.ca/prod/bwysched.p_select_term?wsea_code=EXT
#https://github.com/uScheduleMe/uoapi
#https://central.carleton.ca/prod/bwysched.p_search_fields?wsea_code=EXT&session_id=2&term_code=202320

import requests

def getTimetable(course: str, term_code: str):
    program_request = requests.get('https://central.carleton.ca/prod/bwysched.p_search_fields?wsea_code=EXT&session_id=2&term_code='+term_code)
    print(str(program_request.content))

getTimetable("", "202320")