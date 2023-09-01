document.addEventListener('DOMContentLoaded', function() {
  const calendarEl = document.getElementById('calendar');
  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    events: '/get_events', // Fetch events from the server
    eventClick: function(info) {
      // Get the event object from the clicked event
      const event = info.event;

      // Populate the update modal with event details
      document.getElementById('event-id').value = event.id;
      document.getElementById('update-task-name').value = event.title;
      document.getElementById('update-task-company').value = event.extendedProps.company;
      // ... similarly populate other fields ...

      // Show the update modal
      $('#updateTaskModal').modal('show');
    },
    // ... other options ...
  });
  calendar.render();

  // Show the task modal when the "Add Task" button is clicked
  const addTaskButton = document.getElementById('addTaskButton');
  addTaskButton.addEventListener('click', function() {
    $('#taskModal').modal('show');
  });

  // Handle form submission when the task form is submitted
  document.getElementById('task-form').addEventListener('submit', async function(event) {
    event.preventDefault();

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
      const response = await fetch('/create_task', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        console.log('Task added successfully');

        // Create an event object for the new task
        const newEvent = {
          title: taskName,
          start: dueDateObj,
          end: dueDateObj, // For simplicity, set end to the same as start
          extendedProps: {
            company: company,
            notes: notes
          }
        };

        // Add the new event to the calendar's events source
        calendar.addEvent(newEvent);

        console.log('Calendar Events after adding:', calendar.getEvents());

        // Refresh events on the calendar to display the new event
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

  // Handle form submission when the update task form is submitted
  document.getElementById('update-task-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const taskName = document.getElementById('update-task-name').value; 
    const company = document.getElementById('update-task-company').value; 
    const dueDate = document.getElementById('update-task-due-date').value; 
    const dueTime = document.getElementById('update-task-due-time').value; 
    const notes = document.getElementById('update-task-notes').value; 

    // Get the task_id from the clicked event
    const taskId = document.getElementById('event-id').value; 

    const formData = {
      task_id: taskId,
      task_name: taskName,
      company: company,
      due_date: dueDate,
      due_time: dueTime,
      notes: notes
    };

    try {
      const response = await fetch('/update_task', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      const taskId = parseInt(document.getElementById('event-id').value, 10);
      if (!isNaN(taskId)) {
        // Now you can use taskId in the formData and request.
      } else {
        console.error('Invalid task ID:', taskId);
        // Handle the error appropriately.
      }

      if (response.ok) {
        console.log('Task updated successfully');
        // Reload the events on the calendar after updating
        calendar.refetchEvents();
        // Clear the form and hide the modal
        document.getElementById('update-task-form').reset();
        $('#updateTaskModal').modal('hide');
      } else {
        console.error('Error updating task:', response.status, response.statusText);
      }
    } catch (error) {
      console.error('Error updating task:', error);
    }
  });

  document.getElementById('calendar').addEventListener('click', (info) => {
    if (info.event) {
      const clickedEvent = info.event; // Get the clicked event object
      const taskId = clickedEvent.id; // Get the task_id from the event object
      const taskName = clickedEvent.title;
      const company = clickedEvent.extendedProps.company;
      const dueDate = clickedEvent.start.toISOString().substr(0, 10);
      const dueTime = clickedEvent.start.toISOString().substr(11, 5);
      const notes = clickedEvent.extendedProps.notes;

      // Set the form fields with the task information
      document.getElementById('update-task-name').value = taskName;
      document.getElementById('update-task-company').value = company;
      document.getElementById('update-task-due-date').value = dueDate;
      document.getElementById('update-task-due-time').value = dueTime;
      document.getElementById('update-task-notes').value = notes;
      document.getElementById('event-id-update').value = taskId;

      // Show the update task modal
      $('#updateTaskModal').modal('show');
    }
  });
})