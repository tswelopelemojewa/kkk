create table delays (
    id integer primary key AUTOINCREMENT,
    Delay real,
    laborers real,
    cash_flow real,
    Errors real,
    communication real,
    Change_schedule real,
    bid_price real,
    scope_change real,
    Weather_conditions real,
    Accidents real
);

drop TABLE tasks

delete from tasks where Duration = 21

create table tasks (
    id integer primary key AUTOINCREMENT,
    Name string,
    Duration real,
    AssignedTo String,
    status String
);

INSERT INTO tasks (Name, Duration, AssignedTo, status) VALUES ('Plumbing', 3, 'Mpho', 'Done')

SELECT * from tasks

SELECT 
    Delay,
    laborers,
    cash_flow,
    Errors,
    communication,
    Change_schedule,
    bid_price,
    scope_change,
    Weather_conditions,
    Accidents 
FROM delays ORDER BY id DESC LIMIT 10;
