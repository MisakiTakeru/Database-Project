DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS teaches;
DROP TABLE IF EXISTS roles;

create table courses (
	CourseID integer primary key autoincrement,
	name text not null,
	Total_hours integer not null
);

create table users (
	UserID integer primary key autoincrement,
	name text not null,
	mail text,
	Total_hours integer
);

create table teaches (
	TeachID integer primary key autoincrement,
	hours integer not null,
	CourseID integer not null,	
	UserID integer not null,
	FOREIGN KEY(UserID) REFERENCES users(UserID),
	FOREIGN KEY(CourseID) REFERENCES courses(CourseID)
);

create table roles (
	RoleID integer primary key autoincrement,
	roles text not null,
	Hours integer not null,
	UserID integer not null,
	FOREIGN KEY(UserID) REFERENCES users(UserID)
);
