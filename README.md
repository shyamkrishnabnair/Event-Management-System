# Event Management System  

This is an assignment covering DB schema, API design and workflows.  

---

## Project Understanding  
I began by understanding what the project is:  

1. An Admin Portal  
2. A Student App  
3. Database with required tables  

---

## Assumptions  
- Multiple colleges with multiple events  
- Only single registration to a single event by a single student  
- Attendance will be marked only for registered students  
- Only attended students can give feedback  

---

## Decisions  
- Prevent duplicate events and student registrations  
- MySQL as database and Flask as backend  
- Data model with required tables  

---

## Schema Design  
- A **College table** and **Student table** for college and students respectively, with `college_id` and `student_id` as unique identifiers.  
- An **Events table** linked to college via `college_id`.  
- A **Registration table** to handle registrations and attendance.  
- A **Feedback table** to handle feedback easily.  

---

## API Endpoints  

### Admin Portal  
- **POST** – Create events  
- **GET** – View events  
- **PUT** – Update events  
- **DELETE** – Remove events  

### Student App  
- **POST** – Register to event, feedback if marked present  
- **GET** – View events  
- **DELETE** – Withdraw registration  

---

## Workflow  
Once this was complete, a workflow diagram was made to demonstrate the flow of events.  

---

## Prototype Implementation  
- A prototype code was generated to show working of this system and API endpoints, utilizing **MySQL** as database and **Postman** to view them.  
- A reporting mechanism was also implemented using queries.  
