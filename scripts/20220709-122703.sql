CREATE TABLE user_status (
  id INT NOT NULL AUTO_INCREMENT,
  const VARCHAR(45) NOT NULL,
  description VARCHAR(255) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX `user_status_const_UNIQUE` (`const` ASC)
);

INSERT INTO user_status (const, description)
VALUES ("ACTIVE", "User currently active"),
("INACTIVE", "User currently inactive"),
("DELETED", "User currently deleted");