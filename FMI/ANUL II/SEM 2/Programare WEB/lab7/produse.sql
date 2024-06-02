-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: produse
-- ------------------------------------------------------
-- Server version	8.0.36-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `produse`
--

DROP TABLE IF EXISTS `produse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produse` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nume` varchar(50) DEFAULT NULL,
  `descriere` varchar(255) DEFAULT NULL,
  `pret` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produse`
--

LOCK TABLES `produse` WRITE;
/*!40000 ALTER TABLE `produse` DISABLE KEYS */;
INSERT INTO `produse` VALUES (1,'Product 1','Description 1',10.99),(2,'Product 2','Description 2',20.99),(3,'Product 3','Description 3',30.99),(4,'Product 4','Description 4',40.99),(5,'Product 5','Description 5',50.99),(6,'Product 6','Description 6',60.99),(7,'Product 7','Description 7',70.99),(8,'Product 8','Description 8',80.99),(9,'Product 9','Description 9',90.99),(10,'Product 10','Description 10',100.99),(11,'Product 11','Description 11',110.99),(12,'Product 1','Description 1',10.99),(13,'Product 2','Description 2',20.99),(14,'Product 3','Description 3',30.99),(15,'Product 4','Description 4',40.99),(16,'Product 5','Description 5',50.99),(17,'Product 6','Description 6',60.99),(18,'Product 7','Description 7',70.99),(19,'Product 8','Description 8',80.99),(20,'Product 9','Description 9',90.99),(21,'Product 10','Description 10',100.99),(22,'Product 11','Description 11',110.99),(23,'Product 1','Description 1',10.99),(24,'Product 2','Description 2',20.99),(25,'Product 3','Description 3',30.99),(26,'Product 4','Description 4',40.99),(27,'Product 5','Description 5',50.99),(28,'Product 6','Description 6',60.99),(29,'Product 7','Description 7',70.99),(30,'Product 8','Description 8',80.99),(31,'Product 9','Description 9',90.99),(32,'Product 10','Description 10',100.99),(33,'Product 11','Description 11',110.99),(34,'Product 1','Description 1',10.99),(35,'Product 2','Description 2',20.99),(36,'Product 3','Description 3',30.99),(37,'Product 4','Description 4',40.99),(38,'Product 5','Description 5',50.99),(39,'Product 6','Description 6',60.99),(40,'Product 7','Description 7',70.99),(41,'Product 8','Description 8',80.99),(42,'Product 9','Description 9',90.99),(43,'Product 10','Description 10',100.99),(44,'Product 11','Description 11',110.99),(45,'Product 1','Description 1',10.99),(46,'Product 2','Description 2',20.99),(47,'Product 3','Description 3',30.99),(48,'Product 4','Description 4',40.99),(49,'Product 5','Description 5',50.99),(50,'Product 6','Description 6',60.99),(51,'Product 7','Description 7',70.99),(52,'Product 8','Description 8',80.99),(53,'Product 9','Description 9',90.99),(54,'Product 10','Description 10',100.99),(55,'Product 11','Description 11',110.99),(56,'Product 1','Description 1',10.99),(57,'Product 2','Description 2',20.99),(58,'Product 3','Description 3',30.99),(59,'Product 4','Description 4',40.99),(60,'Product 5','Description 5',50.99),(61,'Product 6','Description 6',60.99),(62,'Product 7','Description 7',70.99),(63,'Product 8','Description 8',80.99),(64,'Product 9','Description 9',90.99),(65,'Product 10','Description 10',100.99),(66,'Product 11','Description 11',110.99),(67,'Product 1','Description 1',10.99),(68,'Product 2','Description 2',20.99),(69,'Product 3','Description 3',30.99),(70,'Product 4','Description 4',40.99),(71,'Product 5','Description 5',50.99),(72,'Product 6','Description 6',60.99),(73,'Product 7','Description 7',70.99),(74,'Product 8','Description 8',80.99),(75,'Product 9','Description 9',90.99),(76,'Product 10','Description 10',100.99),(77,'Product 11','Description 11',110.99);
/*!40000 ALTER TABLE `produse` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-30  8:17:05
