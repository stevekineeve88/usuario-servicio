CREATE TABLE IF NOT EXISTS `user_refresh_token` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `token` VARCHAR(255) NOT NULL,
  `user_id` INT NOT NULL,
  `created_timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `user_refresh_token_token_UNIQUE` (`token` ASC),
  INDEX `user_refresh_token_user_id_fk` (`user_id` ASC),
  CONSTRAINT `user_refresh_token_user_id_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);