-- Exercise: a school. Each teacher has one office and each office one teacher (1--1);
-- a teacher teaches many classes, a class has one teacher (1--*); students attend
-- many classes, classes have many students (*--*), through an association table.
CREATE TABLE office (office_id INTEGER PRIMARY KEY, room TEXT NOT NULL);
CREATE TABLE teacher (
  teacher_id INTEGER PRIMARY KEY,
  name       TEXT NOT NULL,
  office_id  INTEGER NOT NULL UNIQUE REFERENCES office(office_id));
CREATE TABLE class (
  class_id   INTEGER PRIMARY KEY,
  subject    TEXT NOT NULL,
  teacher_id INTEGER NOT NULL REFERENCES teacher(teacher_id));
CREATE TABLE student (student_id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE attends (
  student_id INTEGER REFERENCES student(student_id),
  class_id   INTEGER REFERENCES class(class_id),
  PRIMARY KEY (student_id, class_id));
INSERT INTO office VALUES (1, 'B12'), (2, 'B14');
INSERT INTO teacher VALUES (1, 'Rosa', 1);
INSERT INTO class VALUES (1, 'algebra', 1), (2, 'physics', 1);
INSERT INTO student VALUES (1, 'Tom'), (2, 'Lea');
INSERT INTO attends VALUES (1, 1), (1, 2), (2, 1);
-- Each of these must fail.
INSERT INTO teacher VALUES (2, 'Hugo', 1);
INSERT INTO class VALUES (3, 'music', 7);
INSERT INTO attends VALUES (2, 1);
INSERT INTO attends VALUES (3, 1);
INSERT INTO class VALUES (4, 'art', NULL);
