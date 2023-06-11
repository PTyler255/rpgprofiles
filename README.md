# Character Profile Manager

A full stack website that manages Player Character profiles for Table Top RPGs. Includes user authentication and session stores. Can create new accounts and add, edit or delete player characters within the database. Frontend is Javascript, backend is Python with some SQLite for database management.

## Data Objects

**CHARACTER**

* Name (string)
* Class (string)
* Level (integer)
* Money (float)
* Resource (integer)
* Notes (string)

**USER**

* Email (string)
* First Name (string)
* Last Name (string)
* Password (60 character salted hash)

## SCHEMA

```sql
CREATE TABLE players (
id INTEGER PRIMARY KEY,
name TINYTEXT,
class TINYTEXT,
level TINYINT,
money FLOAT,
resource INT,
Notes TEXT);
```

```sql
CREATE TABLE users (
id INTEGER PRIMARY KEY,
email TEXT,
fname TEXT,
lname TEXT,
pw CHAR(60));
```

## REST ENDPOINTS

Name 			      	 | Method | Path
---------------------------------|--------|---------------
Retrieve character collection    | GET    | /PLAYERS
Retrieve single character member | GET	  | /PLAYERS/*\<id\>*
Create character member 	 | POST	  | /PLAYERS
Create user			 | POST	  | /USERS
Create session			 | POST	  | /SESSIONS
Update character member 	 | PUT	  | /PLAYERS/*\<id\>*
Delete character member 	 | DELETE | /PLAYERS/*\<id\>*

