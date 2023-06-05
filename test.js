const fs = require('fs');

// Read the file
fs.readFile('courses/AERO', 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading file:', err);
    return;
  }

  try {
    // Parse the JSON data
    const courses = JSON.parse(data);

    // Iterate over each course object
    courses.forEach((course) => {
      // Perform your desired operations on each course object
      console.log(course.course_title);
      console.log(course.course_desc);
      console.log('---');
    });
  } catch (error) {
    console.error('Error parsing JSON:', error);
  }
});