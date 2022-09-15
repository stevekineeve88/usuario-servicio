CREATE TABLE IF NOT EXISTS `password_reset` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `token` VARCHAR(255) NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `password_reset_user_id_UNIQUE` (`user_id` ASC),
  UNIQUE INDEX `password_reset_token_UNIQUE` (`token` ASC),
  INDEX `password_reset_user_id_fk` (`user_id` ASC),
  CONSTRAINT `password_reset_user_id_fk`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);