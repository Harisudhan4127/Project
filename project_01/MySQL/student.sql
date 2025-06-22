USE dummy;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    marks INT
);

INSERT INTO students (name, marks)
VALUES ('Hari', 90), ('Bala', 85);
