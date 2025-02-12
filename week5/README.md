# Assignment of Week 5

## Task 1
- Install MySQL Server.

## Task 2
### 1. Create a new database named website.
  ```SQL
  CREATE DATABASE website;
  ```
  ![website_database](/images/website_database.png)

### 2. Create a new table named member in the website database, designed as instruction.
  ```SQL
  USE website;
  CREATE TABLE member(
	id BIGINT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL, 
	password VARCHAR(255) NOT NULL,
    follower_count INT UNSIGNED NOT NULL DEFAULT 0,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
  );
  ```
  ![member_table](/images/member_table.png)

## Task 3
### 1. INSERT a new row to the member table where name, username and password must be set to test. INSERT additional 4 rows with arbitrary data.
  ```SQL
  INSERT INTO member(name, username, password, follower_count) 
  VALUES
  ('test', 'test', 'test', DEFAULT),
  ('Jessie', 'jchiu', '0220', 54),
  ('Emma', 'echen', '0522', 463),
  ('Stacey', 'sshih', '0813', 448),
  ('Karen', 'kliao', '0327', 217);
  ```
\* Please refer to the screenshot in the next question.
<br/>
<br/>
    
### 2. SELECT all rows from the member table.
  ```SQL
  SELECT * FROM member;
  ```
  ![rows_in_member](/images/rows_in_member.png)

### 3. SELECT all rows from the member table, in descending order of time.
  ```SQL
  SELECT * FROM member ORDER BY time DESC;
  ```
  ![select_by_time](/images/select_by_time.png)

### 4. SELECT total 3 rows, second to fourth, from the member table, in descending order of time.
  ```SQL
  SELECT * FROM member ORDER BY time DESC LIMIT 3 OFFSET 1;
  ```
  ![select_top](/images/select_top.png)

### 5. SELECT rows where username equals to test.
  ```SQL
  SELECT * FROM member WHERE username = 'test';
  ```
  ![select_test](/images/select_test.png)

### 6. SELECT rows where name includes the <u>es</u> keyword.
  ```SQL
  SELECT * FROM member WHERE name LIKE '%es%'; 
  ```
  ![select_name_es](/images/select_name_es.png)

### 7. SELECT rows where both username and password equal to <u>test</u>.
  ```SQL
  SELECT * FROM member WHERE username = 'test' AND password = 'test';
  ```
  ![select_both_test](/images/select_both_test.png)

### 8. UPDATE data in name column to <u>test2</u> where username equals to <u>test</u>.
  ```SQL
  UPDATE member SET name = 'test2' WHERE username = 'test';
  ```
  ![update_name](/images/update_name.png)

## Task 4
### 1. SELECT how many rows from the member table.
  ```SQL
  SELECT COUNT(*) FROM member;
  ```
  ![count_member_rows](/images/count_member_rows.png)

### 2. SELECT the sum of follower_count of all the rows from the member table.
  ```SQL
  SELECT SUM(follower_count) FROM member;
  ```
  ![sum_follower_count](/images/sum_follower_count.png)

### 3. SELECT the average of follower_count of all the rows from the member table.
  ```SQL
  SELECT AVG(follower_count) FROM member;
  ```
  ![avg_follower_count](/images/avg_follower_count.png)

### 4. SELECT the average of follower_count of the first 2 rows, in descending order of follower_count, from the member table.
```SQL
SELECT AVG(follower_count) AS Top_2_AVG
FROM(
  SELECT follower_count
  FROM member
  ORDER BY follower_count DESC
  LIMIT 2
)AS top_2;
```
![top_2_avg](/images/top_2_avg.png)

## Task 5
### 1. Create a new table named message, in the website database, designed as instruction.
  ```SQL
  CREATE TABLE message(
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  member_id BIGINT NOT NULL,
  content VARCHAR(255) NOT NULL,
  like_count INT UNSIGNED NOT NULL DEFAULT 0,
  time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(member_id) REFERENCES member(id)
  );
  ```
  ![msg_table](/images/msg_table.png)

### 2. SELECT all messages, including sender names. We have to JOIN the member table to get that.
  ```SQL
  SELECT member.name, message.content
  FROM member RIGHT JOIN message
  ON member.id = message.member_id;
  ```
  ![select_all_msgs](/images/select_all_msgs.png)

### 3. SELECT all messages, including sender names, where sender username equals to test. We have to JOIN the member table to filter and get that.
  ```SQL
  SELECT member.name, message.content
  FROM member INNER JOIN message
  ON member.id = message.member_id
  WHERE member.username = 'test';
  ```
  ![select_msgs_from_test](/images/select_msgs_from_test.png)

### 4. Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages where sender username equals to test.
  ```SQL
  SELECT AVG(like_count) AS "AVG like_count of 'test'"
  FROM member INNER JOIN message
  ON member.id = message.member_id
  WHERE member.username = 'test';
  ```
  ![test_avg_like](/images/test_avg_like.png)

### 5. Use SELECT, SQL Aggregation Functions with JOIN statement, get the average like count of messages GROUP BY sender username.
  ```SQL
  SELECT member.username, AVG(like_count)
  FROM member INNER JOIN message
  ON member.id = message.member_id
  GROUP BY member.username;
  ```
  ![user_avg_like](/images/user_avg_like.png)