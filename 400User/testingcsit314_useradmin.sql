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
-- Table structure for table `useradmin`
--

DROP TABLE IF EXISTS `useradmin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `useradmin` (
  `UserId` int NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Role` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`UserId`),
  CONSTRAINT `useradmin_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `users` (`UserId`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `useradmin`
--

LOCK TABLES `useradmin` WRITE;
/*!40000 ALTER TABLE `useradmin` DISABLE KEYS */;
INSERT INTO `useradmin` VALUES (1,'Richard Vasquez','Admin User'),(2,'Heather Lopez','Admin User'),(3,'Carla Crawford','Admin User'),(4,'Chad Brown Jr.','Admin User'),(5,'Pamela Smith','Admin User'),(6,'Samantha Rios','Admin User'),(7,'Christina Gregory','Admin User'),(8,'James Miles','Admin User'),(9,'Jasmin Hendricks','Admin User'),(10,'Karen Gomez','Admin User'),(11,'Patricia Hill','Admin User'),(12,'Diane Lee','Admin User'),(13,'Steven Carroll','Admin User'),(14,'Michael Smith','Admin User'),(15,'Michael Thompson','Admin User'),(16,'Patrick Ho','Admin User'),(17,'Kevin Evans','Admin User'),(18,'Gabriel Klein','Admin User'),(19,'Kayla Smith','Admin User'),(20,'David Hutchinson','Admin User'),(21,'Susan Stewart','Admin User'),(22,'Daniel Blair','Admin User'),(23,'Teresa Horne DVM','Admin User'),(24,'Lisa Hernandez','Admin User'),(25,'Lance Miller','Admin User'),(26,'Julie Daniels','Admin User'),(27,'Allen Hernandez','Admin User'),(28,'Christopher Ryan','Admin User'),(29,'Jose Humphrey','Admin User'),(30,'Katherine Miller','Admin User'),(31,'Anthony Fisher','Admin User'),(32,'Maria Brown','Admin User'),(33,'Shannon Case','Admin User'),(34,'Sarah Gilbert','Admin User'),(35,'Amy Howard','Admin User'),(36,'Evelyn Stark','Admin User'),(37,'James Kline','Admin User'),(38,'Katherine Smith','Admin User'),(39,'Kyle Chavez','Admin User'),(40,'Joanne Hudson','Admin User'),(41,'Tanya Thompson','Admin User'),(42,'Courtney Davis','Admin User'),(43,'Denise Mccormick','Admin User'),(44,'Monica Russell','Admin User'),(45,'Evan Reed','Admin User'),(46,'Angela Jones','Admin User'),(47,'Amanda Curry','Admin User'),(48,'Anthony Jenkins','Admin User'),(49,'Aaron Bryant','Admin User'),(50,'Mary Moran','Admin User'),(51,'Gregory Hammond','Admin User'),(52,'Miss Brandy Williams','Admin User'),(53,'Joseph Preston','Admin User'),(54,'John Davis II','Admin User'),(55,'Aaron Hoover','Admin User'),(56,'Kenneth Hughes','Admin User'),(57,'Mark Carr','Admin User'),(58,'Cody Brown','Admin User'),(59,'Cassandra Ford','Admin User'),(60,'Joseph Ramos','Admin User'),(61,'Wayne Andrews','Admin User'),(62,'Joshua Hickman','Admin User'),(63,'Erica Perkins','Admin User'),(64,'John Johnson','Admin User'),(65,'Victoria Thompson','Admin User'),(66,'Krystal Cruz','Admin User'),(67,'Edwin Green','Admin User'),(68,'Nicholas Grimes','Admin User'),(69,'Vanessa Clark','Admin User'),(70,'Chad Gaines','Admin User'),(71,'Joseph Harper','Admin User'),(72,'Douglas Young','Admin User'),(73,'Cody Castillo','Admin User'),(74,'Mr. Roger Cooper','Admin User'),(75,'Victor Hernandez','Admin User'),(76,'Christine Mcmahon','Admin User'),(77,'Alexander Carrillo','Admin User'),(78,'Ashley Booker','Admin User'),(79,'Dawn Hernandez','Admin User'),(80,'Sue Jones','Admin User'),(81,'Randall Friedman','Admin User'),(82,'Mr. James Smith','Admin User'),(83,'Laura Alvarado','Admin User'),(84,'Jared Rios','Admin User'),(85,'Austin Castro','Admin User'),(86,'Colleen Johnson','Admin User'),(87,'Kathleen Berry','Admin User'),(88,'Katherine Dixon','Admin User'),(89,'Kevin Gomez','Admin User'),(90,'Amanda Sullivan','Admin User'),(91,'Tara Smith','Admin User'),(92,'Sophia Gallagher','Admin User'),(93,'Hunter Li','Admin User'),(94,'Amy Morris','Admin User'),(95,'James Moore','Admin User'),(96,'Anna Clay','Admin User'),(97,'Roberto Waller','Admin User'),(98,'Andrew Cline','Admin User'),(99,'Tammy Johnson','Admin User'),(100,'George Smith','Admin User');
/*!40000 ALTER TABLE `useradmin` ENABLE KEYS */;
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
