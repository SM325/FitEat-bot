-- CREATE database healthy_app;

-- USE healthy_app; 
drop database  healthy_app;
 -- drop TABLE user_day;
--  drop TABLE user;

-- CREATE TABLE user(
--     user_name varchar(50) not null  PRIMARY KEY,
--     name varchar(50),
--     is_init bit,
--     birth_date date,
--     weight float,
--     height float, 
--     max_calories float,
--     max_fat float,
--     max_carb float,
--     max_protein float,
--     current_state varchar(50),
--     gender ENUM('male', 'female')
--     );


-- CREATE TABLE user_day(
--     user_name varchar(50),
--     date_of_day date,
--     calories float,
--     fat float,
--     carb float,
--     protein float,

--     PRIMARY KEY (user_name, date_of_day),

--     FOREIGN KEY(user_name) REFERENCES user(user_name)
-- );

--  select * from user