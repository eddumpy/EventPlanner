# EventPlanner

####Features:

- Only be able to create an event when logged in
- When creating an event the author is attached to that event 
- Display the authors first and last name
- Filter the events by authors first name or last name

####Features 2:

- Create a new model called category, which contains a name and ID
- Create an endpoint to view, edit, create and delete categories
- Change the event model to replace the category, so it is using the category model. Option to have several categories for each event
- Display in the event endpoint the list of categories using their name

####Features 3:

- When you create an event you don’t have to add the categories to the events but you need an endpoint to add or remove the categories from event
- When you add a category provide a boolean option to apply the category to all the user events
- Make sure there is no unnecessary queries when listing the events

####Features 4:

- Display the number of events in the categories
- Display when the last event is in the categories
- Add extra field to event model to show physical or online
- In the event list display the online and physical categories
