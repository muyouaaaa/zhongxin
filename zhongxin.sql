DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(50) NOT NULL COMMENT '用户密码，MD5加密',
  `realname` varchar(50) DEFAULT  NULL COMMENT  '用户真实姓名',
  `id_card` int(20) DEFAULT NULL COMMENT '用户身份证号码',
  image longblob DEFAULT NULL COMMENT '用户图片',
  `phone` varchar(20) DEFAULT NULL,
  `role` int(4) NOT NULL COMMENT '角色0-管理员,1-普通用户',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `product`;
CREATE TABLE `product` (
  `goods_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '商品id',
  `name` varchar(100) NOT NULL COMMENT '商品名称',
  `productor`  varchar(100) NOT NULL COMMENT '供应商',
  `detail` text COMMENT '商品详情',
  `price` decimal(20,2) NOT NULL COMMENT '价格,单位-元保留两位小数',
  `purchase_price` decimal(20,2) NOT NULL COMMENT '进货价格,单位-元保留两位小数',
  `stock` int(11) NOT NULL COMMENT '库存数量',
  `status` int(6) DEFAULT '1' COMMENT '商品状态.1-在售 2-下架 3-删除',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`goods_id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `employee`;
CREATE TABLE `employee` (
  `employee_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '员工id',
  `employeename` varchar(50) NOT NULL COMMENT '员工名',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`employee_id`)
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `shipping`;
CREATE TABLE `shipping` (
`shipping_id` int(11) NOT NULL AUTO_INCREMENT,
`user_id` int(11) DEFAULT NULL COMMENT '用户id',
`receiver_name` varchar(20) DEFAULT NULL COMMENT '收货姓名',
`receiver_phone` varchar(20) DEFAULT NULL COMMENT '收货固定电话',
`receiver_mobile` varchar(20) DEFAULT NULL COMMENT '收货移动电话',
`receiver_province` varchar(20) DEFAULT NULL COMMENT '省份',
`receiver_city` varchar(20) DEFAULT NULL COMMENT '城市',
`receiver_district` varchar(20) DEFAULT NULL COMMENT '区/县',
`receiver_address` varchar(200) DEFAULT NULL COMMENT '详细地址',
`receiver_zip` varchar(6) DEFAULT NULL COMMENT '邮编',
`create_time` datetime DEFAULT NULL,
`update_time` datetime DEFAULT NULL,
PRIMARY KEY (`shipping_id`),
constraint FK_user foreign key (user_id) references user(user_id) on delete cascade on update cascade
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `order`;
CREATE TABLE `order` (
  `order_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '订单id',
  `order_no` bigint(20) DEFAULT NULL COMMENT '订单号',
  `user_id` int(11) NOT NULL COMMENT '用户id',
  `goods_id` int(11) NOT NULL COMMENT '产品id',
  `referrer_id` int(11) DEFAULT NULL COMMENT '推荐码',
  `shipping_id` int(11) DEFAULT NULL COMMENT '收货地址',
  `payment` decimal(20,2) DEFAULT NULL COMMENT '实际付款金额,单位为元,保留两位小数',
  `payment_time` datetime DEFAULT NULL COMMENT '支付时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`order_id`),
  UNIQUE KEY `order_no_index` (`order_no`) USING BTREE,
  constraint FK_user foreign key (user_id) references user(user_id) on delete cascade on update cascade,
  constraint FK_goods foreign key (goods_id) references product(goods_id) on delete cascade on update cascade
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8;

