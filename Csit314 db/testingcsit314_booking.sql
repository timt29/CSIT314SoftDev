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
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking` (
  `BookingId` int NOT NULL AUTO_INCREMENT,
  `HomeOwnerId` int NOT NULL,
  `CleanerId` int NOT NULL,
  `ServiceId` int NOT NULL,
  PRIMARY KEY (`BookingId`),
  KEY `fkey1_idx` (`HomeOwnerId`),
  KEY `fkey2_idx` (`CleanerId`),
  KEY `fkey3_idx` (`ServiceId`),
  CONSTRAINT `fkey1` FOREIGN KEY (`HomeOwnerId`) REFERENCES `homeowner` (`UserId`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `fkey2` FOREIGN KEY (`CleanerId`) REFERENCES `cleaner` (`UserId`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `fkey3` FOREIGN KEY (`ServiceId`) REFERENCES `service` (`ServiceId`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking`
--

LOCK TABLES `booking` WRITE;
/*!40000 ALTER TABLE `booking` DISABLE KEYS */;
INSERT INTO `booking` VALUES (1,2,6,1),(2,2,6,2),(3,7,6,1),(4,7,6,2),(5,2,6,2),(6,2,6,2),(7,2,6,2),(8,2,6,3),(9,2,6,3),(10,2,6,3),(11,2,6,2),(12,2,6,2),(13,2,6,2),(14,2,6,2),(15,2,6,2),(16,2,6,2),(17,2,6,2),(18,2,6,3),(19,2,6,6),(20,2,6,7),(21,2,6,17),(22,2,6,2),(23,2,6,2),(24,2,6,3),(25,2,6,7),(26,2,6,2),(27,2,6,3),(28,2,6,2),(29,2,6,17),(30,2,6,17),(31,2,6,3),(32,2,6,2),(33,2,6,2),(34,2,6,1),(35,2,6,2),(36,2,6,17),(37,2,6,5);
/*!40000 ALTER TABLE `booking` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-14  1:59:55
