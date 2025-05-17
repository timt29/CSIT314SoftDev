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
-- Table structure for table `cleanerservice`
--

DROP TABLE IF EXISTS `cleanerservice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cleanerservice` (
  `UserId` int NOT NULL,
  `ServiceId` int NOT NULL,
  `View_Count` int NOT NULL DEFAULT '0',
  `Shortlist_Count` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`UserId`,`ServiceId`),
  KEY `ServiceId` (`ServiceId`),
  CONSTRAINT `cleanerservice_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `cleaner` (`UserId`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `cleanerservice_ibfk_2` FOREIGN KEY (`ServiceId`) REFERENCES `service` (`ServiceId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cleanerservice`
--

LOCK TABLES `cleanerservice` WRITE;
/*!40000 ALTER TABLE `cleanerservice` DISABLE KEYS */;
INSERT INTO `cleanerservice` VALUES (201,1,1,2),(201,8,2,2),(202,2,3,3),(203,3,4,4),(204,4,5,6),(205,5,6,5),(206,6,7,7),(207,7,8,2),(208,9,9,1),(209,1,10,3),(210,2,1,6),(211,3,2,5),(212,4,3,4),(213,5,4,7),(214,6,5,1),(215,7,6,23),(216,8,7,8),(217,9,8,54),(218,1,9,2),(219,2,10,2),(220,3,1,1),(221,4,2,4),(222,5,3,6),(223,6,4,5),(224,7,5,7),(225,8,6,3),(226,9,7,2),(227,1,8,1),(228,2,9,4),(229,3,10,3),(230,4,1,1),(231,5,2,2),(232,6,3,3),(233,7,4,6),(234,8,5,7),(235,9,6,4),(236,1,7,3),(237,2,8,4),(238,3,9,2),(239,4,10,1),(240,5,1,1),(241,6,2,1),(242,7,3,2),(243,8,4,3),(244,9,5,4),(245,1,6,5),(246,2,7,6),(247,3,8,7),(248,4,9,8),(249,5,10,9),(250,6,1,10);
/*!40000 ALTER TABLE `cleanerservice` ENABLE KEYS */;
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
