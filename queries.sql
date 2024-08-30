-- Get all tasks for a specific user.
SELECT t.user_id, u.fullname, t.title, t.descriptions, s.name  
FROM tasks AS t
LEFT JOIN users AS u ON u.id = t.user_id 
LEFT JOIN status AS s ON s.id = t.status_id
WHERE t.user_id = 2
ORDER BY t.id;

-- Select tasks by a specific status.
SELECT t.id, t.title, t.descriptions, s.name
FROM tasks AS t
LEFT JOIN status AS s ON s.id = t.status_id
WHERE s.name = 'new';

-- Update the status of a specific task.
UPDATE tasks SET status_id = 3 WHERE id = 20;

-- Get a list of users who have no tasks.
SELECT u.id, u.fullname  
FROM users AS u
WHERE u.id NOT IN (SELECT user_id FROM tasks);

-- Add a new task for a specific user.
INSERT INTO tasks (title, descriptions, status_id, user_id)
VALUES ('Do homework', '', 1, 1);

-- Get all tasks that are not yet completed.
SELECT id, title, descriptions
FROM tasks
WHERE status_id = 2;

-- Delete a specific task.
DELETE FROM tasks WHERE id = 2;

-- Find users with a specific email.
SELECT id, fullname, email 
FROM users
WHERE email = 'boleslav93@example.com';

-- Update the user's name.
UPDATE users SET fullname = 'Harry Potter' WHERE id = 5;

-- Get the number of tasks for each status.
SELECT t.status_id, s.name , COUNT(t.status_id)
FROM tasks AS t
LEFT JOIN status AS s ON s.id = t.status_id
GROUP BY t.status_id;

-- Get tasks assigned to users with a specific email domain.
SELECT t.title, u.fullname, u.email
FROM tasks AS t
LEFT JOIN users AS u ON u.id = t.user_id 
WHERE u.email LIKE '%@example.org';

-- Get a list of tasks that have no description.
SELECT id, title
FROM tasks
WHERE descriptions IS NULL;

-- Select users and their tasks that are in the 'in progress' status.
SELECT t.id, u.fullname, t.title, s.name 
FROM users AS u
LEFT JOIN tasks AS t ON t.user_id = u.id
LEFT JOIN status AS s ON s.id = t.status_id 
WHERE t.status_id = 2;

-- Get users and the number of their tasks.
SELECT  u.fullname, COUNT(t.status_id)
FROM users AS u
LEFT JOIN tasks AS t ON t.user_id = u.id
GROUP BY u.fullname;
