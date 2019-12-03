DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(50) NOT NULL COMMENT '用户密码，MD5加密',
  `realname` varchar(50) DEFAULT  NULL COMMENT  '用户真实姓名',
  `user_id` int(11) DEFAULT NULL COMMENT '用户身份证号码',
  `phone` varchar(20) DEFAULT NULL,
  `purchasedNum` decimal(20,2) NOT NULL COMMENT '用户购买总金额',
  `role` int(4) NOT NULL COMMENT '角色0-管理员,1-普通用户',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`username`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `product`;
CREATE TABLE `product` (
  `goods_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '商品id',
  `category_id` int(11) NOT NULL COMMENT '分类id',
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
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '员工id',
  `employeename` varchar(50) NOT NULL COMMENT '员工名',
  `performance` decimal(20,2)  DEFAULT NULL COMMENT '员工业绩',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `order`;
CREATE TABLE `order` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '订单id',
  `order_no` bigint(20) DEFAULT NULL COMMENT '订单号',
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `goods_id` int(11) NOT NULL COMMENT '产品id',
  `referrer_id` int(11) DEFAULT NULL COMMENT '推荐码',
  `payment` decimal(20,2) DEFAULT NULL COMMENT '实际付款金额,单位是元,保留两位小数',
  `payment_time` datetime DEFAULT NULL COMMENT '支付时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_no_index` (`order_no`) USING BTREE,
  constraint FK_user foreign key (username) references user(username) on delete cascade on update cascade,
  constraint FK_goods foreign key (goods_id) references product(goods_id) on delete cascade on update cascade,
  constraint FK_employee foreign key (referrer_id) references employee(id) on delete cascade on update cascade
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8;




