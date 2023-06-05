document.addEventListener("DOMContentLoaded", function () {
    const completedCourseInput = document.getElementById("completed-course-input");
    const requiredCourseInput = document.getElementById("required-course-input");
    const completedCoursesTable = document.getElementById("completed-courses-table");
    const requiredCoursesTable = document.getElementById("required-courses-table");

    // Add completed course
    completedCourseInput.addEventListener("keyup", function (event) {
      if (event.keyCode === 13) {
        event.preventDefault();
        addCourse(completedCoursesTable, completedCourseInput.value);
        completedCourseInput.value = "";
      }
    });

    // Add required course
    requiredCourseInput.addEventListener("keyup", function (event) {
      if (event.keyCode === 13) {
        event.preventDefault();
        addCourse(requiredCoursesTable, requiredCourseInput.value);
        requiredCourseInput.value = "";
      }
    });

    // Remove course
    document.addEventListener("click", function (event) {
      if (event.target.classList.contains("remove-course")) {
        const courseRow = event.target.closest("tr");
        courseRow.remove();
      }
    });

    function addCourse(table, courseName) {
      const row = document.createElement("tr");
      sendCompletedCourse(courseName);
      const courseCell = document.createElement("td");
      const actionCell = document.createElement("td");
      const removeButton = document.createElement("button");

      courseCell.textContent = courseName;
      removeButton.classList.add("btn", "btn-danger", "remove-course");
      removeButton.textContent = "Remove";

      actionCell.appendChild(removeButton);
      row.appendChild(courseCell);
      row.appendChild(actionCell);
      table.querySelector("tbody").appendChild(row);
    }
  });

function sendCompletedCourse(courseName) {
    const url = "/completed-course"; // Replace with your server endpoint
  
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ course: courseName }),
    })
      .then((response) => {
        if (response.ok) {
          console.log("Completed course sent successfully");
          console.log(response)
        } else {
          throw new Error("Failed to send completed course");
        }
      })
      .catch((error) => {
        console.error(error);
      });
  }