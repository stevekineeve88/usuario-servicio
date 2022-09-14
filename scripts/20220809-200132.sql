CREATE TABLE IF NOT EXISTS `user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `uuid` BINARY(16) DEFAULT (uuid_to_bin(uuid())),
  `email` VARCHAR(100) NOT NULL,
  `first_name` VARCHAR(100) NOT NULL,
  `last_name` VARCHAR(100) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `status_id` INT NOT NULL,
  `created_timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_uuid_UNIQUE` (`uuid` ASC),
  UNIQUE INDEX `user_email_UNIQUE` (`email` ASC),
  INDEX `user_status_id_fk` (`status_id` ASC),
  CONSTRAINT `user_status_id_fk`
    FOREIGN KEY (`status_id`)
    REFERENCES `user_status` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);