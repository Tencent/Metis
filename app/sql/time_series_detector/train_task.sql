SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for `train_task`
-- ----------------------------
DROP TABLE IF EXISTS `train_task`;
CREATE TABLE `train_task` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `task_id` varchar(20) NOT NULL DEFAULT '' comment '训练任务id',
  `sample_num` int(10) NOT NULL DEFAULT 0 comment '训练总样本数',
  `postive_sample_num` int(10) NOT NULL DEFAULT 0 comment '训练正样本数',
  `negative_sample_num` int(10) NOT NULL DEFAULT 0 comment '训练负样本数',
  `window` int(10) NOT NULL DEFAULT 0 comment '窗口值，目前支持180',
  `model_name` varchar(20) NOT NULL DEFAULT '' comment '模型名',
  `source` varchar(255) NOT NULL DEFAULT '' comment '样本来源',
  `start_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP comment '训练任务开始时间',
  `end_time` timestamp NULL DEFAULT NULL comment '训练任务结束时间',
  `status` varchar(11) NOT NULL DEFAULT '' comment 'complete:任务完成、running:任务正在运行、failed：任务失败',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of train_task
-- ----------------------------
INSERT INTO `train_task` VALUES ('1', '1535790960079', '90675', '45228', '45447', '180', 'xgb_default_model', 'Metis', '2018-09-01 16:36:00', '2018-09-01 16:45:40', 'complete');
