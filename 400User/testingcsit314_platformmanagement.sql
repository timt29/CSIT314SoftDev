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
-- Table structure for table `platformmanagement`
--

DROP TABLE IF EXISTS `platformmanagement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platformmanagement` (
  `UserId` int NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Role` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`UserId`),
  CONSTRAINT `platformmanagement_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `users` (`UserId`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `platformmanagement`
--

LOCK TABLES `platformmanagement` WRITE;
/*!40000 ALTER TABLE `platformmanagement` DISABLE KEYS */;
INSERT INTO `platformmanagement` VALUES (101,'Justin Jensen','Platform Management'),(102,'Kenneth Anderson','Platform Management'),(103,'Kenneth Wells','Platform Management'),(104,'Douglas Hayes','Platform Management'),(105,'Denise Hancock','Platform Management'),(106,'Jennifer Burns','Platform Management'),(107,'Jordan Parker','Platform Management'),(108,'Madison Chaney','Platform Management'),(109,'Michael Berry','Platform Management'),(110,'William Garcia','Platform Management'),(111,'Patricia Burke','Platform Management'),(112,'Amber White','Platform Management'),(113,'Amber Andrews','Platform Management'),(114,'Lauren Calhoun','Platform Management'),(115,'Joshua Bishop','Platform Management'),(116,'Karen Wong','Platform Management'),(117,'Ashley Stafford','Platform Management'),(118,'Melissa Hudson','Platform Management'),(119,'William Gibbs','Platform Management'),(120,'Ashley Curtis MD','Platform Management'),(121,'Alexander Donaldson','Platform Management'),(122,'Robert Martinez','Platform Management'),(123,'Marcus Costa','Platform Management'),(124,'Erica Guerrero DDS','Platform Management'),(125,'Joanne Hart','Platform Management'),(126,'David Guerrero','Platform Management'),(127,'Carrie Jimenez','Platform Management'),(128,'Luis Shah','Platform Management'),(129,'Brett Fowler','Platform Management'),(130,'Jonathan Macias','Platform Management'),(131,'Jack Griffin','Platform Management'),(132,'Kelsey Howe','Platform Management'),(133,'Kimberly Horn','Platform Management'),(134,'Erica Conway','Platform Management'),(135,'Christopher Long','Platform Management'),(136,'Brenda Garcia','Platform Management'),(137,'Kathleen Davis','Platform Management'),(138,'Casey Miller','Platform Management'),(139,'Jennifer Mahoney','Platform Management'),(140,'Diamond Dyer','Platform Management'),(141,'Angela Spence','Platform Management'),(142,'Roger Smith','Platform Management'),(143,'Damon Rios','Platform Management'),(144,'Jeffrey Hill','Platform Management'),(145,'Albert Randall','Platform Management'),(146,'Randy Collier','Platform Management'),(147,'Steven Lyons','Platform Management'),(148,'Ryan Grimes','Platform Management'),(149,'Janice May','Platform Management'),(150,'Tracy Hernandez','Platform Management'),(151,'Christopher Hogan','Platform Management'),(152,'Lindsay White','Platform Management'),(153,'Kaitlin Young','Platform Management'),(154,'Kristin Johnson','Platform Management'),(155,'Blake Mills','Platform Management'),(156,'Samantha Haynes','Platform Management'),(157,'Allen Miller','Platform Management'),(158,'Joseph Robinson','Platform Management'),(159,'Melody Flores','Platform Management'),(160,'Mary Vargas','Platform Management'),(161,'Walter Garza','Platform Management'),(162,'Ruth Flores','Platform Management'),(163,'Adam Harris','Platform Management'),(164,'Carl Rice','Platform Management'),(165,'Patricia Cordova','Platform Management'),(166,'Patrick Boone','Platform Management'),(167,'Bradley Villanueva','Platform Management'),(168,'Leslie Christensen','Platform Management'),(169,'Brandon Perez','Platform Management'),(170,'Suzanne Love','Platform Management'),(171,'Robert Bush','Platform Management'),(172,'David Williams','Platform Management'),(173,'Deanna Barnes','Platform Management'),(174,'Amanda Gonzales','Platform Management'),(175,'Ryan Cordova','Platform Management'),(176,'Robert Payne','Platform Management'),(177,'Lauren Alvarado','Platform Management'),(178,'Alicia Williams','Platform Management'),(179,'Kevin Johnson','Platform Management'),(180,'Emily Carey','Platform Management'),(181,'Joseph Knight','Platform Management'),(182,'Megan Holmes','Platform Management'),(183,'Darren Baker','Platform Management'),(184,'Richard Diaz','Platform Management'),(185,'Lori Lewis','Platform Management'),(186,'Joanne Rangel','Platform Management'),(187,'Ryan Ayala','Platform Management'),(188,'Joel Kim','Platform Management'),(189,'Tiffany Perry','Platform Management'),(190,'Jaime Levy','Platform Management'),(191,'Sarah Jones','Platform Management'),(192,'Scott Gibson','Platform Management'),(193,'David Stewart','Platform Management'),(194,'Yesenia Dunn','Platform Management'),(195,'Judith Ellis','Platform Management'),(196,'Andrew Gibbs','Platform Management'),(197,'Brian Escobar','Platform Management'),(198,'John Schmidt','Platform Management'),(199,'Kevin Richards','Platform Management'),(200,'Kenneth Campbell','Platform Management');
/*!40000 ALTER TABLE `platformmanagement` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-16 19:13:54
