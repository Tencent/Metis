SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for `train_task`
-- ----------------------------
DROP TABLE IF EXISTS `train_task`;
CREATE TABLE `train_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` char(255) DEFAULT NULL,
  `sample_num` int(11) DEFAULT NULL,
  `postive_sample_num` int(11) DEFAULT NULL,
  `negative_sample_num` int(11) DEFAULT NULL,
  `window` int(2) DEFAULT NULL,
  `model_name` varchar(20) DEFAULT NULL,
  `source` varchar(255) DEFAULT NULL,
  `start_time` timestamp NULL DEFAULT NULL,
  `end_time` timestamp NULL DEFAULT NULL,
  `status` varchar(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of train_task
-- ----------------------------
INSERT INTO `train_task` VALUES ('1', '1535790960079', '90675', '45228', '45447', '180', 'xgb_default_model', 'Metis', '2018-09-01 16:36:00', '2018-09-01 16:45:40', 'complete');
