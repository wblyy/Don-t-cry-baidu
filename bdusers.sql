-- MySQL dump 10.13  Distrib 5.5.35, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: myusers
-- ------------------------------------------------------
-- Server version	5.5.35-0ubuntu0.13.10.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bdusers`
--

DROP TABLE IF EXISTS `bdusers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bdusers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `passwd` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `ustatus` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `u_user` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=109 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bdusers`
--

LOCK TABLES `bdusers` WRITE;
/*!40000 ALTER TABLE `bdusers` DISABLE KEYS */;
INSERT INTO `bdusers` VALUES (1,'jovixiao','xxg83115','jxxlxg83115@163.com',1),(2,'justdiy3','230227sdz','justdiy10@163.com',4),(3,'eternalcxx0302','yanhuai0202','eternalcxx0302@163.com',4),(4,'a68327749','68327749','a58873556@163.com',4),(5,'baoxi198431','lengkudewo','baoxi198431@163.com',1),(6,'cyanext','372244068','cyjjyc1@163.com',1),(7,'doyu1316366','doy1316366','doyu1316366@163.com',1),(8,'hanna200312','mylove032','hanna200312@163.com',1),(9,'hbqhdmj','3212332125','gstmj@163.com',4),(10,'jlc0191777','jlc19880422','0191777@163.com',1),(11,'langreng001','16899161','jtxjflxx@163.com',1),(12,'lariejose','westlife','zhjxt1983@163.com',1),(13,'petfirefox168','85960068','i_super6610@163.com',1),(14,'xaily2010','xaily2011','xaily@163.com',1),(15,'kevinwooo','23306127','wangshuai0318@live.cn',1),(16,'chuxuecao','959598lyj','chuxuecao@163.com',1),(17,'wenbinljy','121521denwen','wenbin-ljy@163.com',1),(18,'sgjose','hai83721','sgjose@163.com',1),(19,'yeyu20101','19861018','yeyu2010@163.com',1),(20,'xiefeng5145','378068025','kingdu8@163.com',1),(21,'toumingrenjj','198518yujiajun','hanwudiliuche@live.com',3),(22,'boonewong','12010301','blackmilk@live.com',4),(23,'alomsong','shinning','alom@live.com',1),(24,'hzrchome','kk310012','hzrc@live.com',4),(25,'ajaxer009','jatools123','ajaxer009@sina.com',1),(26,'zheshiwodehaoa','baotongqq','haorenbt@163.com',1),(27,'dugujiujian07','nck780087kcn','njcqk170830@163.com',4),(28,'xiaxiaohui456','xiaxiaohui123','xiaxiaohui456@126.com',4),(29,'kedanansheng','andylau001','andy20060001@126.com',1),(30,'fengkuangfuhuo','wodehaoma','renbaohui@126.com',1),(31,'jijiechina','Jijie1989','jijiechina@126.com',1),(32,'wl_5545831','tscwangliang','tscwangliang@126.com',4),(33,'ttb_899','ttb461067','ttb_899@126.com',4),(34,'jiajianxue','03105959739','jiajianxue40016@163.com',1),(35,'heilonghui','36855952','jfr9@163.com',1),(36,'suliyaa','kaishidongle','suliyaaa@163.com',1),(37,'stingtao','1qaz2wsx','stingtao@gmail.com',4),(38,'lijie_zhzx','lijiehit','lijie_zhzx@yahoo.com.cn',1),(39,'zkwait123','19851219zk','zk_life@sina.com',1),(40,'mxyour','19920807','mxyour@163.com',1),(41,'lotsunhim','miss2688','lotsunhim@sina.com',4),(42,'acerphoenix','jm44kjm44k','li.acerphoenix@gmail.com',1),(43,'qc269','66823333','qc269@tom.com',3),(44,'ybdiypcb','19700312','ybdiypcb@163.com',1),(45,'mzhzv','02465409','46884754@qq.com',1),(46,'chen777ah','1816637011','qb966@163.com',1),(47,'a3353651','3353651412','824210165@qq.com',1),(48,'chaorensup','83118264','chaorensuperman@yahoo.com.cn',1),(49,'mplcoco','168010mpl','suanlihe@163.com',1),(50,'jh2869','jh197400','jh2869@163.com',1),(51,'lizb1985','ljlovelzb','lizb1985@163.com',4),(52,'lvshengjun888','www12301230520','361979895@163.com',4),(53,'arnold162002','0240416','arnold162002@163.com',1),(54,'lioner626','64553085','lioner626@163.com',4),(55,'tanlangpo','299792458','tanlangpo@sina.com',4),(56,'wangfei4812','mm7262571','wangfei4812@sina.com',1),(57,'lonely_wudong','wudong0408','lonely_wudong@sina.com',4),(58,'phpup','51352788','phpup@126.com',3),(59,'hkbisme','5942hkbb','huangkb123@126.com',1),(60,'liqiansong_888','sain1791132.','liqiansong_888@126.com',4),(61,'renmenok','m80b_913','renmenok@gmail.com',1),(62,'corsairchenrui','atiradeon','corsairchenrui@gmail.com',4),(63,'caimeike','7218301223','caimeike@gmail.com',4),(64,'zhaoyn03','59000000','zhaoyunan-js@163.com',1),(65,'liu801121','lxj801121','lxj801121@163.com',1),(66,'j877506773','jhcal0995','j877506773@163.com',1),(67,'shjfeng630','sjf159753','shjfeng630@163.com',1),(68,'gujianyang08','gu851027','gujianyang0.8@163.com',1),(69,'mq1103','19841103','mq1103@163.com',1),(70,'luojiancc','luohaijian','luo-hai-jian@163.com',1),(71,'suifeng1987617','huaxiang','zhanglingyi521@163.com',4),(72,'jhwzznx6','jsfxznx6','jhwzznx6@163.com',1),(73,'ycjwiner','13998812277','changjun2277@163.com',1),(74,'clanlovenad','tianqing','sanbnank@163.com',1),(75,'las0216','lx051216','liuxing19830512@163.com',4),(76,'ahdyqxj','qxj58225','ahdyqxj@163.com',1),(77,'mff2008','mff7667241','mff7667241@163.com',1),(78,'zhoukaiooo','zhoukaizk','zkxiaozk@163.com',1),(79,'yangmars123','210001199','yangmars123@163.com',4),(80,'tonvavi','tonvavi55','tonvavi@163.com',1),(81,'theodore08','087415157','shzhangxd@yahoo.com.cn',1),(82,'viviany2601','wen539999','huimengluo2601@yahoo.com.cn',1),(83,'mintpc','panchao025','pennyroyalx0@yahoo.com.cn',1),(84,'gyfott1','65031257','yuefeng.gu@yahoo.com.cn',1),(85,'icyTour','professorZ','ice.thebestone@yahoo.com.cn',1),(86,'tokogg1','milutoko','great87921@yahoo.com.cn',1),(87,'munu1009','huaguoshan','kisa13959148@yahoo.com.cn',4),(88,'chuanyanyin','it_fairic','chuanyanyin@yahoo.com.cn',1),(89,'dabidadiao','05574211112','huizi6417@163.com',1),(90,'wengshaohe','528119421','wengshaohe@163.com',1),(91,'pnmrbo','kgdiceihc','pnmrbo@163.com',4),(92,'cscs6947','sj8878106','87gf@163.com',1),(93,'tjkjdxrjsjs','151561614','tjkjdxrjsjs@163.com',1),(94,'ahhaomaple','liulihao','liulihao2003@yahoo.com.cn',1),(95,'yuehua415','198445927','yuehua415@yahoo.com.cn',1),(96,'pmem1126','18811126','pmem1126@yahoo.com.cn',1),(97,'gentleyan','yl6680356','gentleyan0427@yahoo.com.cn',1),(98,'leveret2','65862778','leveret88@yahoo.com.cn',1),(99,'feiming9413','14821911','qfm9413qfm@yahoo.com.cn',1),(100,'max_jone','iloveyou','six_jone@yahoo.com.cn',1),(101,'dircncncom','111983111983','dircncncom@yahoo.com.cn',4),(102,'ArthurBZhou','Smoking007','arthur_b_zhou@yahoo.com.cn',1),(103,'Langresser8873','19880730','tianmolin@yahoo.com.cn',1),(104,'CDDYLEC','307391701','cddylec@yahoo.com.cn',1),(105,'windy4055','90613469061346','windy4055@yahoo.com.cn',1),(106,'jay19118isme','331017543192','jay19118isme@yahoo.com.cn',1),(107,'zhenabyss','zhenabyss909','zhenabyss@yahoo.com.cn',1),(108,'zhangxinhui85','zhxh3903149','zhangxinhui85@yahoo.com.cn',1);
/*!40000 ALTER TABLE `bdusers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-09-14 13:24:04
