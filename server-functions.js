const fs = require('fs');
const path = require('path');
function verifyCourse(course) {
    const pattern = /^[A-Za-z]{2,4}\s?\d{4}$/;

    // Test the string against the pattern
    if(!pattern.test(course)) return false;
    var filePath = path.join(__dirname, '', 'courses', course.substring(0,4));
    try {
        // Check if the file exists
        fs.accessSync(filePath, fs.constants.F_OK);
        return true; // File exists
    } catch (error) {
        
        //attempt with 3 letters
    }
    var filePath = path.join(__dirname, '', 'courses', course.substring(0,3));
    try {
        // Check if the file exists
        fs.accessSync(filePath, fs.constants.F_OK);
        return true; // File exists
    } catch (error) {
        console.log(error)
        return false;
    }
}

module.exports = verifyCourse;