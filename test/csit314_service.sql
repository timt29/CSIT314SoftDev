-- Create service table first (parent table)
CREATE TABLE `service` (
  `service_id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(45) NOT NULL UNIQUE,
  `pricing` DOUBLE NOT NULL,
  `duration` INT NOT NULL COMMENT 'in hours',
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert sample data
INSERT INTO `service` (`name`, `pricing`, `duration`) VALUES 
('cleaning', 25, 2),
('cooking', 100, 2),
('laundry', 10, 1),
('washing dishes', 20, 1);