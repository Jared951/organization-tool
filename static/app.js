document.addEventListener('DOMContentLoaded', function() {
  const calendarEl = document.getElementById('calendar');
  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    events: [], // Initialize with empty events array
    // ... other options ...
  });
  calendar.render();

  // Show the task modal when the "Add Task" button is clicked
  const addTaskButton = document.getElementById('addTaskButton');
  addTaskButton.addEventListener('click', function() {
    $('#taskModal').modal('show');
  });

  // Handle form submission when the task form is submitted
  document.getElementById('task-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Capture user input from the form
    const taskName = document.getElementById('task-name').value;
    const company = document.getElementById('task-company').value;
    const dueDate = document.getElementById('task-due-date').value;
    const dueTime = document.getElementById('task-due-time').value;
    const notes = document.getElementById('task-notes').value;

    // Create a combined datetime string from due date and due time
    const combinedDueDateTime = dueDate + 'T' + dueTime;

    // Create an event object
    const eventObj = {
      title: taskName,
      start: combinedDueDateTime,
      end: combinedDueDateTime, // For simplicity, set end to the same as start
      extendedProps: {
        company: company,
        notes: notes
      }
    };

    // Add the event to the calendar
    calendar.addEvent(eventObj);

    // Clear the form and hide the modal
    document.getElementById('task-form').reset();
    $('#taskModal').modal('hide');
  });
});