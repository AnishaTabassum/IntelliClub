CREATE DATABASE  IF NOT EXISTS `intelliclub` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `intelliclub`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: intelliclub
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `alert`
--

DROP TABLE IF EXISTS `alert`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alert` (
  `Alert_ID` int NOT NULL AUTO_INCREMENT,
  `Club_ID` int DEFAULT NULL,
  `Subject` varchar(100) NOT NULL,
  `Message` varchar(255) DEFAULT NULL,
  `Created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Alert_ID`),
  KEY `fk_Alert_club` (`Club_ID`),
  CONSTRAINT `fk_Alert_club` FOREIGN KEY (`Club_ID`) REFERENCES `clubs` (`Club_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alert`
--

LOCK TABLES `alert` WRITE;
/*!40000 ALTER TABLE `alert` DISABLE KEYS */;
INSERT INTO `alert` VALUES (4,4,'Final Broadcast','NEVER AGAIN','2026-01-23 09:32:06');
/*!40000 ALTER TABLE `alert` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assets`
--

DROP TABLE IF EXISTS `assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assets` (
  `Asset_ID` int NOT NULL AUTO_INCREMENT,
  `Club_ID` int DEFAULT NULL,
  `Asset_Name` varchar(50) DEFAULT NULL,
  `Category` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Asset_ID`),
  KEY `fk_asset_clubs` (`Club_ID`),
  CONSTRAINT `fk_asset_clubs` FOREIGN KEY (`Club_ID`) REFERENCES `clubs` (`Club_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assets`
--

LOCK TABLES `assets` WRITE;
/*!40000 ALTER TABLE `assets` DISABLE KEYS */;
INSERT INTO `assets` VALUES (1,1,'Robot','Electronics'),(2,1,'Rocket','Electronics'),(3,1,'Mars Rover','Electronics'),(4,2,'Mic','Electronics');
/*!40000 ALTER TABLE `assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add users',19,'add_users'),(22,'Can change users',19,'change_users'),(23,'Can delete users',19,'delete_users'),(24,'Can view users',19,'view_users'),(25,'Can add alert',6,'add_alert'),(26,'Can change alert',6,'change_alert'),(27,'Can delete alert',6,'delete_alert'),(28,'Can view alert',6,'view_alert'),(29,'Can add assets',7,'add_assets'),(30,'Can change assets',7,'change_assets'),(31,'Can delete assets',7,'delete_assets'),(32,'Can view assets',7,'view_assets'),(33,'Can add clubs',8,'add_clubs'),(34,'Can change clubs',8,'change_clubs'),(35,'Can delete clubs',8,'delete_clubs'),(36,'Can view clubs',8,'view_clubs'),(37,'Can add clubs events',9,'add_clubsevents'),(38,'Can change clubs events',9,'change_clubsevents'),(39,'Can delete clubs events',9,'delete_clubsevents'),(40,'Can view clubs events',9,'view_clubsevents'),(41,'Can add event registration',12,'add_eventregistration'),(42,'Can change event registration',12,'change_eventregistration'),(43,'Can delete event registration',12,'delete_eventregistration'),(44,'Can view event registration',12,'view_eventregistration'),(45,'Can add events',13,'add_events'),(46,'Can change events',13,'change_events'),(47,'Can delete events',13,'delete_events'),(48,'Can view events',13,'view_events'),(49,'Can add expenses',14,'add_expenses'),(50,'Can change expenses',14,'change_expenses'),(51,'Can delete expenses',14,'delete_expenses'),(52,'Can view expenses',14,'view_expenses'),(53,'Can add loans',15,'add_loans'),(54,'Can change loans',15,'change_loans'),(55,'Can delete loans',15,'delete_loans'),(56,'Can view loans',15,'view_loans'),(57,'Can add roles',16,'add_roles'),(58,'Can change roles',16,'change_roles'),(59,'Can delete roles',16,'delete_roles'),(60,'Can view roles',16,'view_roles'),(61,'Can add students',18,'add_students'),(62,'Can change students',18,'change_students'),(63,'Can delete students',18,'delete_students'),(64,'Can view students',18,'view_students'),(65,'Can add volunteers',20,'add_volunteers'),(66,'Can change volunteers',20,'change_volunteers'),(67,'Can delete volunteers',20,'delete_volunteers'),(68,'Can view volunteers',20,'view_volunteers'),(69,'Can add clubs members',10,'add_clubsmembers'),(70,'Can change clubs members',10,'change_clubsmembers'),(71,'Can delete clubs members',10,'delete_clubsmembers'),(72,'Can view clubs members',10,'view_clubsmembers'),(73,'Can add clubs registration',11,'add_clubsregistration'),(74,'Can change clubs registration',11,'change_clubsregistration'),(75,'Can delete clubs registration',11,'delete_clubsregistration'),(76,'Can view clubs registration',11,'view_clubsregistration'),(77,'Can add skills',17,'add_skills'),(78,'Can change skills',17,'change_skills'),(79,'Can delete skills',17,'delete_skills'),(80,'Can view skills',17,'view_skills');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clubs`
--

DROP TABLE IF EXISTS `clubs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clubs` (
  `Club_ID` int NOT NULL AUTO_INCREMENT,
  `Club_Name` varchar(50) DEFAULT NULL,
  `Club_Funds` int DEFAULT NULL,
  `Reg_fee` int DEFAULT NULL,
  `Advisor_Name` varchar(50) DEFAULT NULL,
  `Advisor_Email` varchar(50) DEFAULT NULL,
  `Advisor_Initial` varchar(50) DEFAULT NULL,
  `Founded_Year` year DEFAULT NULL,
  `reg_open` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`Club_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clubs`
--

LOCK TABLES `clubs` WRITE;
/*!40000 ALTER TABLE `clubs` DISABLE KEYS */;
INSERT INTO `clubs` VALUES (1,'Robotics Club',5000,500,'Dr. Alan Turing','turing@uni.edu','AT',2015,1),(2,'Debate Society',3000,200,'Prof. Harvey Specter','specter@uni.edu','HS',2018,0),(3,'Art Club',2000,150,'Ms. Frida Kahlo','kahlo@uni.edu','FK',2020,1),(4,'Music Club',2500,180,'Mr. Ludwig Beethoven','beethoven@uni.edu','LB',2017,0);
/*!40000 ALTER TABLE `clubs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clubs_events`
--

DROP TABLE IF EXISTS `clubs_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clubs_events` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Club_ID` int DEFAULT NULL,
  `Event_ID` int DEFAULT NULL,
  `Role` varchar(50) DEFAULT NULL,
  `Budget_share` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_Clubs_Events_events` (`Event_ID`),
  KEY `fk_Clubs_Events_Clubs` (`Club_ID`),
  CONSTRAINT `fk_Clubs_Events_Clubs` FOREIGN KEY (`Club_ID`) REFERENCES `clubs` (`Club_ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_Clubs_Events_events` FOREIGN KEY (`Event_ID`) REFERENCES `events` (`Event_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clubs_events`
--

LOCK TABLES `clubs_events` WRITE;
/*!40000 ALTER TABLE `clubs_events` DISABLE KEYS */;
INSERT INTO `clubs_events` VALUES (1,1,1,'Host',5000),(2,1,2,'Host',2000),(3,2,2,'Partner',3000),(4,1,3,'Host',10000),(5,1,4,'Host',2000),(6,2,4,'Partner',1000),(7,1,5,'Host',5000),(8,4,5,'Partner',1000),(9,4,6,'Host',50000),(10,4,7,'Host',50000),(11,4,8,'Host',50000);
/*!40000 ALTER TABLE `clubs_events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clubs_members`
--

DROP TABLE IF EXISTS `clubs_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clubs_members` (
  `Member_ID` int NOT NULL AUTO_INCREMENT,
  `Club_ID` int DEFAULT NULL,
  `Student_ID` varchar(10) DEFAULT NULL,
  `Role` varchar(50) DEFAULT NULL,
  `Joining_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Member_ID`),
  KEY `fk_club_mem_clubs` (`Club_ID`),
  KEY `fk_club_mem_students` (`Student_ID`),
  CONSTRAINT `fk_club_mem_clubs` FOREIGN KEY (`Club_ID`) REFERENCES `clubs` (`Club_ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_club_mem_students` FOREIGN KEY (`Student_ID`) REFERENCES `students` (`Student_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clubs_members`
--

LOCK TABLES `clubs_members` WRITE;
/*!40000 ALTER TABLE `clubs_members` DISABLE KEYS */;
INSERT INTO `clubs_members` VALUES (1,1,'0152410011','President','2026-01-22 08:39:46'),(2,1,'0152410045','General Member','2026-01-22 02:44:58'),(3,2,'0152410045','President','2026-01-22 10:59:40'),(4,2,'0152410011','General Member','2026-01-22 05:00:14'),(5,1,'0152410013','General Member','2026-01-22 07:53:11'),(6,2,'0152410013','General Member','2026-01-22 10:45:42'),(7,4,'0152410013','President','2026-01-23 12:48:44'),(8,4,'0152410011','General Member','2026-01-23 08:19:50'),(9,4,'0152410012','General Member','2026-01-23 08:42:15'),(10,4,'0152410016','General Member','2026-01-23 09:14:28');
/*!40000 ALTER TABLE `clubs_members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clubs_registration`
--

DROP TABLE IF EXISTS `clubs_registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clubs_registration` (
  `reg_id` int NOT NULL AUTO_INCREMENT,
  `Club_ID` int DEFAULT NULL,
  `Student_ID` varchar(10) DEFAULT NULL,
  `Payment_status` enum('Unpaid','Success') DEFAULT 'Unpaid',
  PRIMARY KEY (`reg_id`),
  KEY `fk_club_reg_student` (`Student_ID`),
  KEY `fk_club_reg_clubs` (`Club_ID`),
  CONSTRAINT `fk_club_reg_clubs` FOREIGN KEY (`Club_ID`) REFERENCES `clubs` (`Club_ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_club_reg_student` FOREIGN KEY (`Student_ID`) REFERENCES `students` (`Student_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clubs_registration`
--

LOCK TABLES `clubs_registration` WRITE;
/*!40000 ALTER TABLE `clubs_registration` DISABLE KEYS */;
INSERT INTO `clubs_registration` VALUES (1,1,'0152410012','Unpaid'),(2,3,'0152410012','Unpaid');
/*!40000 ALTER TABLE `clubs_registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_User_Email` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_User_Email` FOREIGN KEY (`user_id`) REFERENCES `users` (`User_Email`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'contenttypes','contenttype'),(6,'dashboard','alert'),(7,'dashboard','assets'),(8,'dashboard','clubs'),(9,'dashboard','clubsevents'),(10,'dashboard','clubsmembers'),(11,'dashboard','clubsregistration'),(12,'dashboard','eventregistration'),(13,'dashboard','events'),(14,'dashboard','expenses'),(15,'dashboard','loans'),(16,'dashboard','roles'),(17,'dashboard','skills'),(18,'dashboard','students'),(19,'dashboard','users'),(20,'dashboard','volunteers'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'dashboard','0001_initial','2026-01-21 14:57:02.378945'),(2,'contenttypes','0001_initial','2026-01-21 14:57:02.444848'),(3,'admin','0001_initial','2026-01-21 14:57:02.689270'),(4,'admin','0002_logentry_remove_auto_add','2026-01-21 14:57:02.696064'),(5,'admin','0003_logentry_add_action_flag_choices','2026-01-21 14:57:02.703432'),(6,'contenttypes','0002_remove_content_type_name','2026-01-21 14:57:02.871207'),(7,'auth','0001_initial','2026-01-21 14:57:03.588250'),(8,'auth','0002_alter_permission_name_max_length','2026-01-21 14:57:03.681392'),(9,'auth','0003_alter_user_email_max_length','2026-01-21 14:57:03.689984'),(10,'auth','0004_alter_user_username_opts','2026-01-21 14:57:03.698881'),(11,'auth','0005_alter_user_last_login_null','2026-01-21 14:57:03.707132'),(12,'auth','0006_require_contenttypes_0002','2026-01-21 14:57:03.712876'),(13,'auth','0007_alter_validators_add_error_messages','2026-01-21 14:57:03.721231'),(14,'auth','0008_alter_user_username_max_length','2026-01-21 14:57:03.732209'),(15,'auth','0009_alter_user_last_name_max_length','2026-01-21 14:57:03.740868'),(16,'auth','0010_alter_group_name_max_length','2026-01-21 14:57:03.761410'),(17,'auth','0011_update_proxy_permissions','2026-01-21 14:57:03.775443'),(18,'auth','0012_alter_user_first_name_max_length','2026-01-21 14:57:03.783921'),(19,'sessions','0001_initial','2026-01-21 14:57:03.854222');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('fxlv4ikhnrr31re7vgfne6n2gkmmkcx7','.eJxVzMsOwiAQheF3YW0I9ALoyrj3GchMZ1paCyS9rIzvbkm60PX5_vMWHvYt-H3lxY8kbiJyWGCSEULMme5DhHGWXY7i8ksRuhen4mmCNORDpG0ZURYiz3WVz0w8P077dxBgDaVGxayVbcDo9qqwqSyBQ6aKeqBWUW07ttw74zQ6UzdoSGtXV456PlLx-QJlCUGe:1vjJ9J:IkzRrc2WH3jmU02bYxmasrZwo-LFtWdy09D_w6YcBV4','2026-02-06 15:32:37.573764');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_registration`
--

DROP TABLE IF EXISTS `event_registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_registration` (
  `Registration_ID` int NOT NULL AUTO_INCREMENT,
  `Student_ID` varchar(10) DEFAULT NULL,
  `Event_ID` int DEFAULT NULL,
  `Attendance_code` blob,
  `Attendance` enum('Absent','Present') DEFAULT 'Absent',
  `Attendance_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Rating` tinyint unsigned DEFAULT NULL,
  `Comment` varchar(255) DEFAULT NULL,
  `Payment_status` enum('Unpaid','Success') DEFAULT 'Unpaid',
  PRIMARY KEY (`Registration_ID`),
  KEY `fk_event_registrationr_students` (`Student_ID`),
  KEY `fk_event_registrationr_events` (`Event_ID`),
  CONSTRAINT `fk_event_registrationr_events` FOREIGN KEY (`Event_ID`) REFERENCES `events` (`Event_ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_event_registrationr_students` FOREIGN KEY (`Student_ID`) REFERENCES `students` (`Student_ID`) ON DELETE CASCADE,
  CONSTRAINT `event_registration_chk_1` CHECK (((`Rating` >= 1) and (`Rating` <= 5)))
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_registration`
--

LOCK TABLES `event_registration` WRITE;
/*!40000 ALTER TABLE `event_registration` DISABLE KEYS */;
INSERT INTO `event_registration` VALUES (1,'0152410045',3,NULL,'Absent',NULL,NULL,NULL,'Success'),(2,'0152410011',4,NULL,'Absent',NULL,5,'besty','Success'),(3,'0152410011',2,NULL,'Absent',NULL,5,'This was life changing, i will never look at robots the same way in my life','Success'),(4,'0152410013',4,NULL,'Absent',NULL,NULL,NULL,'Success'),(5,'0152410013',3,NULL,'Absent',NULL,NULL,NULL,'Success'),(6,'0152410013',2,NULL,'Absent',NULL,NULL,NULL,'Success'),(7,'0152410013',1,NULL,'Absent',NULL,NULL,NULL,'Success'),(8,'0152410011',5,NULL,'Absent',NULL,NULL,NULL,'Success'),(9,'0152410013',5,NULL,'Absent',NULL,NULL,NULL,'Success'),(10,'0152410045',5,NULL,'Absent',NULL,NULL,NULL,'Success'),(11,'0152410011',6,NULL,'Absent',NULL,NULL,NULL,'Success'),(13,'0152410011',7,NULL,'Absent',NULL,NULL,NULL,'Success'),(14,'0152410016',3,NULL,'Absent',NULL,NULL,NULL,'Unpaid');
/*!40000 ALTER TABLE `event_registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
  `Event_ID` int NOT NULL AUTO_INCREMENT,
  `Event_Name` varchar(50) DEFAULT NULL,
  `Event_Date` datetime DEFAULT NULL,
  `Event_details` varchar(255) DEFAULT NULL,
  `Event_type` varchar(50) DEFAULT NULL,
  `Event_fee` int DEFAULT NULL,
  `Venue` varchar(50) DEFAULT NULL,
  `Budget` int DEFAULT NULL,
  PRIMARY KEY (`Event_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (1,'test','2026-01-31 14:00:00','test','Workshop',0,'Room 126',5000),(2,'test-2','2026-01-25 17:04:00','test-2','Seminar',0,'Room 126',5000),(3,'test-3','2026-01-23 20:24:00','test-3','Workshop',100,'Room 126',10000),(4,'Test 4','2026-01-25 22:57:00','This is an event test','Competition',0,'Room 126',3000),(5,'Kaggle Workshop','2026-01-30 16:00:00','this is an event','Workshop',1000,'room 123',6000),(6,'Qr Scanner','2026-01-23 20:21:00','THIS IS IT ','Social',10000,'Online',50000),(7,'FINAL ','2026-01-23 21:09:00','THIS IS THE LAST THING WE DO','Workshop',0,'Online',50000),(8,'FINAL ','2026-01-23 21:09:00','THIS IS THE LAST THING WE DO','Workshop',0,'Online',50000);
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expenses`
--

DROP TABLE IF EXISTS `expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expenses` (
  `Expenses_ID` int NOT NULL AUTO_INCREMENT,
  `Volunteer_ID` int DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL,
  `Amount` int DEFAULT NULL,
  PRIMARY KEY (`Expenses_ID`),
  KEY `fk_expenses_volunteer` (`Volunteer_ID`),
  CONSTRAINT `fk_expenses_volunteer` FOREIGN KEY (`Volunteer_ID`) REFERENCES `volunteers` (`Volunteer_ID`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expenses`
--

LOCK TABLES `expenses` WRITE;
/*!40000 ALTER TABLE `expenses` DISABLE KEYS */;
INSERT INTO `expenses` VALUES (1,1,'Food',1000),(2,1,'decorations',1500);
/*!40000 ALTER TABLE `expenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loans`
--

DROP TABLE IF EXISTS `loans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loans` (
  `Loan_ID` int NOT NULL AUTO_INCREMENT,
  `Asset_ID` int DEFAULT NULL,
  `Lender_Member_ID` int DEFAULT NULL,
  `Borrower_Member_ID` int DEFAULT NULL,
  `Borrow_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `return_date` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `status` varchar(20) DEFAULT 'Pending',
  PRIMARY KEY (`Loan_ID`),
  KEY `fk_Loans_Assets` (`Asset_ID`),
  KEY `fk_loan_lender_club_member` (`Lender_Member_ID`),
  KEY `fk_loan_borrower_club_member` (`Borrower_Member_ID`),
  CONSTRAINT `fk_loan_borrower_club_member` FOREIGN KEY (`Borrower_Member_ID`) REFERENCES `clubs_members` (`Member_ID`) ON DELETE SET NULL,
  CONSTRAINT `fk_loan_lender_club_member` FOREIGN KEY (`Lender_Member_ID`) REFERENCES `clubs_members` (`Member_ID`) ON DELETE SET NULL,
  CONSTRAINT `fk_Loans_Assets` FOREIGN KEY (`Asset_ID`) REFERENCES `assets` (`Asset_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loans`
--

LOCK TABLES `loans` WRITE;
/*!40000 ALTER TABLE `loans` DISABLE KEYS */;
INSERT INTO `loans` VALUES (1,3,NULL,3,'2026-01-23 06:45:06',NULL,'Rejected'),(2,1,1,3,'2026-01-23 06:45:30','2026-01-23 06:46:58','Returned'),(3,4,3,1,'2026-01-23 06:47:45','2026-01-23 07:05:37','Returned'),(4,4,3,7,'2026-01-23 07:04:52','2026-01-23 07:10:18','Returned'),(5,4,3,1,'2026-01-23 07:06:25','2026-01-23 07:10:18','Returned'),(6,3,1,3,'2026-01-23 07:10:27','2026-01-23 07:20:52','Returned'),(7,3,1,7,'2026-01-23 07:20:26',NULL,'Rejected'),(8,4,3,1,'2026-01-23 07:21:49',NULL,'Approved');
/*!40000 ALTER TABLE `loans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `skills`
--

DROP TABLE IF EXISTS `skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skills` (
  `Skill_ID` int NOT NULL AUTO_INCREMENT,
  `Student_ID` varchar(10) DEFAULT NULL,
  `Skill` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Skill_ID`),
  KEY `fk_skills_students` (`Student_ID`),
  CONSTRAINT `fk_skills_students` FOREIGN KEY (`Student_ID`) REFERENCES `students` (`Student_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skills`
--

LOCK TABLES `skills` WRITE;
/*!40000 ALTER TABLE `skills` DISABLE KEYS */;
INSERT INTO `skills` VALUES (1,'0152410011','GOD GAMER');
/*!40000 ALTER TABLE `skills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `Student_ID` varchar(10) NOT NULL,
  `Name` varchar(50) DEFAULT NULL,
  `Email` varchar(50) DEFAULT NULL,
  `Department` varchar(50) DEFAULT NULL,
  `Personality_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Student_ID`),
  KEY `fk_students_users` (`Email`),
  CONSTRAINT `fk_students_users` FOREIGN KEY (`Email`) REFERENCES `users` (`User_Email`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES ('0152410011','Mehraj Mahmood','mehraj.mahmood@gmail.com','BSDS','INTJ'),('0152410012','Shazid','shazid@gmail.com','BSDS','INTJ'),('0152410013','Ekraj','ekraj@gmail.com','BSDS','INTJ'),('0152410016','Anisha','anisha@gmail.com','BSDS','INTJ'),('0152410045','Labib','Labib@gmail.com','BSDS','INTJ');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `User_Email` varchar(50) NOT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Account_Created` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `last_login` datetime DEFAULT NULL,
  PRIMARY KEY (`User_Email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('anisha@gmail.com','pbkdf2_sha256$1200000$uCHMjNzj9nxxvsZZ86pARm$XMHW3qNdU6RLlrzoBsDnR2PCSeZg+fJYPF4oHWLnklQ=','2026-01-23 01:40:17','2026-01-23 15:13:02'),('ekraj@gmail.com','pbkdf2_sha256$1200000$8v5Te0m8hsTosYxjdmfavK$nnekpe50Q78225pON0TmpujFo6cYKuxkWzDbG4Alzpg=','2026-01-22 07:52:08','2026-01-23 15:14:21'),('Labib@gmail.com','pbkdf2_sha256$1200000$3zmmPAsCazUmiJbyqxyB3v$z7fpQgBzH5fIiFNnPEolRMVHhyxm2OIuLesFWaj7BtI=','2026-01-22 02:39:21','2026-01-23 15:10:29'),('mehraj.mahmood@gmail.com','pbkdf2_sha256$1200000$A0ZD9Ok3ZkfE2JsUu3xEze$aES5GZCzQku7tsjkXunEM7vmWd41p4HnPxyFoOQVpKA=','2026-01-22 02:33:49','2026-01-23 15:32:38'),('shazid@gmail.com','pbkdf2_sha256$1200000$RRBGV9yGfyarsivG2oQ1PY$GGWqP8r2sgqEJ0eATtdnsxQozLVsVh2JHgE/VDo2Fkw=','2026-01-23 08:41:48','2026-01-23 14:41:55');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `volunteers`
--

DROP TABLE IF EXISTS `volunteers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `volunteers` (
  `Volunteer_ID` int NOT NULL AUTO_INCREMENT,
  `Event_ID` int DEFAULT NULL,
  `Student_ID` varchar(10) DEFAULT NULL,
  `Role` varchar(255) DEFAULT NULL,
  `Budget_allocated` int DEFAULT NULL,
  `Volunteer_Date` date DEFAULT NULL,
  PRIMARY KEY (`Volunteer_ID`),
  KEY `fk_volunteer_students` (`Student_ID`),
  KEY `fk_volunteer_events` (`Event_ID`),
  CONSTRAINT `fk_volunteer_events` FOREIGN KEY (`Event_ID`) REFERENCES `events` (`Event_ID`) ON DELETE CASCADE,
  CONSTRAINT `fk_volunteer_students` FOREIGN KEY (`Student_ID`) REFERENCES `students` (`Student_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `volunteers`
--

LOCK TABLES `volunteers` WRITE;
/*!40000 ALTER TABLE `volunteers` DISABLE KEYS */;
INSERT INTO `volunteers` VALUES (1,3,'0152410011','Approved',2500,'2026-01-23'),(2,1,'0152410011','Approved',10000,'2026-01-31'),(3,6,'0152410016','Approved',1000,'2026-01-23'),(4,7,'0152410045','Approved',5,'2026-01-23');
/*!40000 ALTER TABLE `volunteers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-23 21:35:52
