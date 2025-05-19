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
-- Table structure for table `homeowner`
--

DROP TABLE IF EXISTS `homeowner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `homeowner` (
  `UserId` int NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Role` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`UserId`),
  CONSTRAINT `homeowner_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `users` (`UserId`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `homeowner`
--

LOCK TABLES `homeowner` WRITE;
/*!40000 ALTER TABLE `homeowner` DISABLE KEYS */;
INSERT INTO `homeowner` VALUES (301,'Rebecca Jenkins','Home Owner'),(302,'Maria Christensen','Home Owner'),(303,'Ebony Roberts','Home Owner'),(304,'Kimberly Gray','Home Owner'),(305,'Nicholas Freeman','Home Owner'),(306,'Misty Wood','Home Owner'),(307,'Danielle Smith','Home Owner'),(308,'Rodney Garcia','Home Owner'),(309,'Brian Oliver','Home Owner'),(310,'Margaret Santos','Home Owner'),(311,'John Armstrong','Home Owner'),(312,'Lisa Lyons','Home Owner'),(313,'Nathan Davis','Home Owner'),(314,'Connie Cherry','Home Owner'),(315,'Raymond Hodges','Home Owner'),(316,'Michele Williams','Home Owner'),(317,'Julie Graham','Home Owner'),(318,'Raymond Clark','Home Owner'),(319,'Jill Baker','Home Owner'),(320,'Lisa Smith','Home Owner'),(321,'Tammy Hughes','Home Owner'),(322,'Jesse Park','Home Owner'),(323,'Jennifer Carr','Home Owner'),(324,'Angela Flores','Home Owner'),(325,'Lindsey Palmer','Home Owner'),(326,'Lisa Long','Home Owner'),(327,'Jose Lopez','Home Owner'),(328,'Justin Heath','Home Owner'),(329,'Kyle Suarez','Home Owner'),(330,'Beth Simpson','Home Owner'),(331,'Shelly Wilson','Home Owner'),(332,'Michael Miller','Home Owner'),(333,'Scott Wilson','Home Owner'),(334,'David Howard','Home Owner'),(335,'Rhonda Rodriguez','Home Owner'),(336,'Gabrielle Crawford','Home Owner'),(337,'Ashlee Vasquez','Home Owner'),(338,'April Anderson DDS','Home Owner'),(339,'Gregory Lowery','Home Owner'),(340,'Andrew Morales','Home Owner'),(341,'Heather Murphy','Home Owner'),(342,'Matthew Martin','Home Owner'),(343,'Laurie Smith','Home Owner'),(344,'Vincent Oconnor','Home Owner'),(345,'Hayley Adams','Home Owner'),(346,'Jenny Baker','Home Owner'),(347,'Ebony Moore PhD','Home Owner'),(348,'Thomas Chavez','Home Owner'),(349,'Molly Rice','Home Owner'),(350,'Sarah Murray','Home Owner'),(351,'Thomas Buchanan','Home Owner'),(352,'Tony Gonzalez','Home Owner'),(353,'Allison Roberts','Home Owner'),(354,'Ryan Mcpherson','Home Owner'),(355,'Joshua Nelson','Home Owner'),(356,'Jean Bridges','Home Owner'),(357,'Anna Lopez','Home Owner'),(358,'Joshua Mejia','Home Owner'),(359,'Deborah May','Home Owner'),(360,'Jeffrey Sexton','Home Owner'),(361,'Lance Garcia','Home Owner'),(362,'Kayla Mayer','Home Owner'),(363,'John Simon','Home Owner'),(364,'Daniel Hunt','Home Owner'),(365,'Cassandra Morris','Home Owner'),(366,'Jacob Martinez','Home Owner'),(367,'Rachel Mcdonald','Home Owner'),(368,'Austin Patel','Home Owner'),(369,'Erica Jimenez','Home Owner'),(370,'Alexandria Mullins','Home Owner'),(371,'Bradley Chavez','Home Owner'),(372,'Robert Gutierrez','Home Owner'),(373,'Tony Baxter','Home Owner'),(374,'Kevin Summers','Home Owner'),(375,'Kimberly Reed','Home Owner'),(376,'Eric Hammond','Home Owner'),(377,'Amber Smith','Home Owner'),(378,'Michael Wilson','Home Owner'),(379,'Jeanne Fernandez','Home Owner'),(380,'Ashley Espinoza','Home Owner'),(381,'Jill May','Home Owner'),(382,'Diana Cardenas','Home Owner'),(383,'Brandi Cole','Home Owner'),(384,'Don Le','Home Owner'),(385,'Lindsay Howell','Home Owner'),(386,'Ian Russell','Home Owner'),(387,'Richard Bell','Home Owner'),(388,'Regina Hall','Home Owner'),(389,'Amy Rowe','Home Owner'),(390,'Michael Harris','Home Owner'),(391,'Benjamin Castro','Home Owner'),(392,'Kevin Swanson','Home Owner'),(393,'Dalton Lee','Home Owner'),(394,'Mario Newman','Home Owner'),(395,'Brandon Ellis','Home Owner'),(396,'Stephanie Cline','Home Owner'),(397,'Ethan Hamilton','Home Owner'),(398,'Robin Lowe','Home Owner'),(399,'John Wright','Home Owner'),(400,'Michael Hart','Home Owner');
/*!40000 ALTER TABLE `homeowner` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-19 20:59:57
