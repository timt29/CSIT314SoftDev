-- Create cleaner table (child table with foreign key)
CREATE TABLE `cleaner` (
  `userid` INT NOT NULL PRIMARY KEY,
  `password` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `dob` DATE NOT NULL,
  `experience` DOUBLE NOT NULL COMMENT 'years of experience',
  `service_id` INT NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT `fk_cleaner_service` 
    FOREIGN KEY (`service_id`) REFERENCES `service` (`service_id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert sample data (must match service_ids from service table)
INSERT INTO `cleaner` 
(`userid`, `password`, `name`, `dob`, `experience`, `service_id`) VALUES 
(100, 'david', 'david', '1980-10-11', 3, 1),
(101, 'alice', 'alice', '1999-04-20', 1, 1),
(102, 'nancy', 'nancy', '1985-05-22', 5, 3),
(103, 'mary', 'mary', '1960-12-30', 20, 1);