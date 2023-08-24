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

    // Create a Date object for the due date
    const dueDateObj = new Date(dueDate);

    // Parse the due time to get hours and minutes
    const [hours, minutes] = dueTime.split(':');

    // Set the time to the due date
    dueDateObj.setHours(hours);
    dueDateObj.setMinutes(minutes);

    // Create an event object
    const eventObj = {
      title: taskName,
      start: dueDateObj,
      end: dueDateObj, // For simplicity, set end to the same as start
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

// Handle form submission when the task form is submitted
document.getElementById('task-form').addEventListener('submit', async function(event) {
  event.preventDefault();

  const taskName = document.getElementById('task-name').value;
  const company = document.getElementById('task-company').value;
  const dueDate = document.getElementById('task-due-date').value;
  const dueTime = document.getElementById('task-due-time').value;
  const notes = document.getElementById('task-notes').value;

  // Create a data object with the form values
  const formData = {
    task_name: taskName,
    company: company,
    due_date: dueDate,
    due_time: dueTime,
    notes: notes
  };

  try {
    // Send a POST request to the server to add the task
    const response = await fetch('/static/create_task', { // Update the URL to reflect the correct path
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    });

    if (response.ok) {
      // Task added successfully, reload the calendar to show the updated events
      calendar.refetchEvents();
      // Clear the form and hide the modal
      document.getElementById('task-form').reset();
      $('#taskModal').modal('hide');
    } else {
      console.error('Error adding task:', response.status, response.statusText);
    }
  } catch (error) {
    console.error('Error adding task:', error);
  }
});