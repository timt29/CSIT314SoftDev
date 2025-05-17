-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: testingcsit314
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cleaner`
--

DROP TABLE IF EXISTS `cleaner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cleaner` (
  `UserId` int NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Role` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`UserId`),
  CONSTRAINT `cleaner_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `users` (`UserId`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cleaner`
--

LOCK TABLES `cleaner` WRITE;
/*!40000 ALTER TABLE `cleaner` DISABLE KEYS */;
INSERT INTO `cleaner` VALUES (201,'Sarah Vazquez','Cleaner'),(202,'Dawn Hodge','Cleaner'),(203,'Andrew Blankenship','Cleaner'),(204,'Sabrina Hendricks','Cleaner'),(205,'Carmen Robinson','Cleaner'),(206,'Cindy Boyd','Cleaner'),(207,'Danny Brandt','Cleaner'),(208,'Monique Edwards','Cleaner'),(209,'Catherine Sherman','Cleaner'),(210,'Tammy Berry','Cleaner'),(211,'Charles Salinas','Cleaner'),(212,'Duane Ferrell','Cleaner'),(213,'Matthew Wilson','Cleaner'),(214,'Robert Perez','Cleaner'),(215,'Mrs. Anita Hawkins','Cleaner'),(216,'Jimmy Day','Cleaner'),(217,'Brandon Blair','Cleaner'),(218,'Jonathon King','Cleaner'),(219,'William Key','Cleaner'),(220,'Andrea Owens','Cleaner'),(221,'Karen Sanders','Cleaner'),(222,'Dawn Porter','Cleaner'),(223,'Stephen Matthews','Cleaner'),(224,'Dillon Edwards','Cleaner'),(225,'David Miller','Cleaner'),(226,'Geoffrey Anderson','Cleaner'),(227,'Jason Middleton','Cleaner'),(228,'Emily Barrera','Cleaner'),(229,'Alyssa Oconnell','Cleaner'),(230,'Amy Patrick','Cleaner'),(231,'Donna Clark','Cleaner'),(232,'Kelly Steele','Cleaner'),(233,'Elizabeth Barrett','Cleaner'),(234,'Michael Collins','Cleaner'),(235,'Thomas Warren','Cleaner'),(236,'Heather Porter','Cleaner'),(237,'Amy Anderson','Cleaner'),(238,'Dr. Kayla Zavala','Cleaner'),(239,'Pamela Walker','Cleaner'),(240,'Dr. Austin Lin DDS','Cleaner'),(241,'Pamela Myers','Cleaner'),(242,'Christina Mcdonald','Cleaner'),(243,'Elizabeth Beck','Cleaner'),(244,'Lisa Evans','Cleaner'),(245,'Trevor Phillips','Cleaner'),(246,'James Davis','Cleaner'),(247,'Latoya Yang','Cleaner'),(248,'Nicole Hernandez','Cleaner'),(249,'Richard Anderson','Cleaner'),(250,'Alyssa Jones','Cleaner'),(251,'Jamie Riddle','Cleaner'),(252,'Timothy Morris','Cleaner'),(253,'Emily Phelps','Cleaner'),(254,'Charles Mendez','Cleaner'),(255,'Peter Parks','Cleaner'),(256,'Daniel Lee','Cleaner'),(257,'Megan Smith','Cleaner'),(258,'Matthew Jones','Cleaner'),(259,'Joshua Moore','Cleaner'),(260,'Jeffrey Garner','Cleaner'),(261,'Katelyn Mitchell','Cleaner'),(262,'Ashley Gonzales','Cleaner'),(263,'Cynthia Martinez','Cleaner'),(264,'Bianca Grimes','Cleaner'),(265,'Andrew Johnson','Cleaner'),(266,'Michael Nicholson','Cleaner'),(267,'Amanda Deleon','Cleaner'),(268,'Jacob Davis','Cleaner'),(269,'Andrea Estrada','Cleaner'),(270,'Lacey Anderson','Cleaner'),(271,'Richard White','Cleaner'),(272,'Steven Cruz','Cleaner'),(273,'Hannah Hammond','Cleaner'),(274,'Jennifer Ramirez','Cleaner'),(275,'Steven Washington','Cleaner'),(276,'Casey Chen','Cleaner'),(277,'Brandon Robertson','Cleaner'),(278,'Bethany James','Cleaner'),(279,'Thomas Brown','Cleaner'),(280,'Wesley Fuller','Cleaner'),(281,'Amanda Griffith','Cleaner'),(282,'William Ramirez','Cleaner'),(283,'Jason Reyes','Cleaner'),(284,'Mary Williams','Cleaner'),(285,'Angela Pham','Cleaner'),(286,'Angie Morales','Cleaner'),(287,'David Lewis','Cleaner'),(288,'Scott Reed','Cleaner'),(289,'Joseph Costa','Cleaner'),(290,'Andrew Brown','Cleaner'),(291,'Linda Gomez','Cleaner'),(292,'Vernon Anderson','Cleaner'),(293,'Wendy Donaldson','Cleaner'),(294,'Nathan Barnes','Cleaner'),(295,'Amy Reynolds','Cleaner'),(296,'Marissa Lindsey','Cleaner'),(297,'Catherine Maddox','Cleaner'),(298,'Gina Curry','Cleaner'),(299,'Philip Montes','Cleaner'),(300,'Richard Tucker','Cleaner');
/*!40000 ALTER TABLE `cleaner` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-18  0:51:33
