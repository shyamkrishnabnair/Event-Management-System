# Event Management System
This is an assignment covering DB schema, API design and workflows

I began by understanding what the project is-

1- An Admin Portal
2- A Student App
3- Database with required tables 

ASSUMPTIONS:

Multiple colleges with multiple events 
Only single registration to single event by a single student 
Attendance will be marked only for registered students
Only Attended students can give feedback 

Decisons:

Prevent Duplicate Events and Student Registrations 
MySQL as Database and Flask as backend
Data Model with required tables

Then came schema design where i decided we'll have a college table and student table for college and students respectively, the college_id and student_id would be unique

Proceeded with an Events table which would be linked to college via college_id 

A Registration table to handle registrations and attendance 
A Feedback table to handle feedbacks easily 

Moving on I layed out the API endpoints-

ADMIN PORTAL:

Post    - Create events 
Get     - View Events
Put     - Update Events
Delete  - Remove Events


STUDENT APP:

Post    - Register to Event, Feedback if marked Present 
Get     - View Events 
Delete  - Withdraw Registration  

Once this was complete a Workflow Diagram was made to demonstrate flow of events

A prototype code was generated to show working of this system and API endpoints utilising MySQL as Database and Postman to view them 
A reporting mechanism was also implemented using QUERIES

