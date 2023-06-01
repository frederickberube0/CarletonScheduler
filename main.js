const axios = require('axios');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

async function getCourseList() {
    const url = 'https://calendar.carleton.ca/undergrad/courses/';
    const response = await axios.get(url);
    const dom = new JSDOM(response.data);
    const document = dom.window.document;
    const courses = document.querySelectorAll('.course a');
    let my_list = [];
    for (let course of courses) {
        my_list.push(course.textContent);
    }
    console.log(my_list);
    return my_list
}

async function getCourseData(course) {
    const url = 'https://calendar.carleton.ca/undergrad/courses/' + course + '/';
    const response = await axios.get(url);
    const dom = new JSDOM(response.data);
    const document = dom.window.document;
    const courseblocks = document.querySelectorAll('.courseblock');

    for (let courseblock of courseblocks) {
        try {
            const course_identifier = courseblock.querySelector('.courseblockcode').textContent.replace(/\u00A0/g, ' ');
            const course_title = courseblock.querySelector('.courseblocktitle').textContent.split('\n')[0].replace(course_identifier, '').trim().replace(/\u00A0/g, '');
            const course_number = parseInt(course_identifier.split(' ')[1]);
            const course_desc = null;
            const prereq_elem = courseblock.querySelector('.coursedescadditional');
            let course_prerequisites;
            if (prereq_elem && prereq_elem.textContent.includes('Prerequisite(s):')) {
                course_prerequisites = prereq_elem.textContent.split('Prerequisite(s):')[1].split('.')[0].trim().replace(/\u00A0/g, '');
            } else {
                course_prerequisites = null;
            }

            const data = {
                "course_identifier": course_identifier,
                "course_code": course_identifier.slice(0, 4) + course_identifier.slice(5),
                "course_number": course_number,
                "course_title": course_title,
                "course_desc": course_desc,
                "course_prerequisites": course_prerequisites
            };

            console.log(JSON.stringify(data, null, 4));
        } catch (error) {
            continue;
        }
    }
}

async function main() {
    const courses = await getCourseList();
    console.log(courses)
    for (let course of courses) {
        await getCourseData(course);
    }
}

main();