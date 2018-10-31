# EventPlanner

#### Features:

- Only be able to create an event when logged in
- When creating an event the author is attached to that event 
- Display the authors first and last name
- Filter the events by authors first name or last name

#### Features 2:

- Create a new model called category, which contains a name and ID
- Create an endpoint to view, edit, create and delete categories
- Change the event model to replace the category, so it is using the category model. Option to have several categories for each event
- Display in the event endpoint the list of categories using their name

#### Features 3:

- When you create an event you don’t have to add the categories to the events but you need an endpoint to add or remove the categories from event
- When you add a category provide a boolean option to apply the category to all the user events
- Make sure there is no unnecessary queries when listing the events

#### Features 4:

- Display the number of events in the categories
- Display when the last event is in the categories
- Add extra field to event model to show physical or online
- In the event list display the online and physical categories


#### Features 5: 
- When you create an event it will post a notification on slack stating this person has created an event for this date, so name of the author and the event
- When the event is starting you post a notification on slack, that this event is about to start


#### Features 6:

- Change the event endpoint, so it supports adding a parameter page number. returns 10 events per page, but it can also return more per page if you pass the parameter paginate_by()
- Change the models so you have two new classes that are called online event and physical event, they both inherit from the event class but the online event has a new attribute url and the physical event has a new attribute called location
- Remove the category type from the category model and just keep categories in the event model
- Create the migration, it should migrate the data, if the event has at least one physical event then it should be a physical event, otherwise it is an online event
- When you query the list of events make sure the object contain either url or the location if it is a physical event and also return the type of event
- Create another class which is called location with fields:
    - Address
    - City
    - Postcode
- Replace the physical event location with a foreign key to the location class

