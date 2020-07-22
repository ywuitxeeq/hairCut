# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Software: PyCharm
# __author__ == "YU HAIPENG"
# fileName: orginSql.py
# Month: 七月
# time: 2020/7/17 12:48
# noqa
"""
用户表 haircut_user
种类表 haircut_category
订单表 haircut_order_info
订单名细表 haircut_order_item
支付信息表 haircut_pay_info
购物车表 haircut_cart
产品表sku haircut_product_sku
产品表spu haircut_product_spu
轮播图表 haircut_carousel
"""

import tormysql
import asyncio

SQL = [
    """create table If Not Exists `haircut_product_spu`(
        id int not null primary key auto_increment comment '产品id',
        name varchar(16) not null comment '商品名称',
        particulars text default null comment '商品详情'
    ) engine=InnoDB default charset=UTF8MB4""",
    """create table If Not Exists `haircut_product_sku` (
     id int not null auto_increment comment '产品id',
     name varchar(100) not null comment '商品名称',
     `subtitle` varchar(200) default null comment '商品副标题',
     `main_image` varchar(500) default null comment '产品主图,url相对路径',
     `sub_images` text comment '图片地址,json格式,扩展用',
     `detail` text comment '商品详情',
     `price` decimal(20, 2) not null comment '价格',
     stock int not null comment '库存数量',
     status TINYINT default '1' comment '商品状态,1-在售,2-下架,3-删除',
     product_spu_id int comment 'spu 表',
     category_id int comment '种类id',
     create_time timestamp default CURRENT_TIMESTAMP  comment '创建时间',
    update_time timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP   comment '最后一次更新时间',
     primary key (`id`)
) engine=InnoDB default charset=UTF8MB4""",
    """create table If Not Exists haircut_user (
    id int not null auto_increment comment '用户表id',
    username varchar(50) not null comment '用户名',
    password varchar(128) not null comment '用户密码',
    email varchar(50) default null,
    phone char(11) default null,
    question varchar(100) default null comment '找回密码问题',
    answer varchar(100) default null comment '找回密码答案',
    role tinyint default 0 comment '角色0-管理员, 1-普通用户',
    stop tinyint default 0 comment '1启用',
    address varchar(255) default '' comment '地址',
    balance decimal(20, 2) default 0 comment '用户余额',
    create_time timestamp default CURRENT_TIMESTAMP  comment '创建时间',
    update_time timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP   comment '最后一次更新时间',
    find_pwd_time timestamp default null comment '找回密码时间',
    primary key (`id`),
    unique key `user_name_unique` (`username`) using btree,
    key `user_role_index` (`role`) using btree,
    unique key `user_phone_unique` (`phone`) using btree
) engine=InnoDB default charset=UTF8MB4""",

    """
    create table If Not Exists haircut_category (
        id int not null auto_increment comment '类别id',
        `parent_id` int default null comment '父类别id当 id=0说明是根节点',
        `name` varchar(50) default null comment '类别名称',
        `status` tinyint default '1' comment '类别状态 1-正常,2-废弃',
        sort_order tinyint default null comment '排序序号,同类展示顺序',
         create_time timestamp default CURRENT_TIMESTAMP  comment '创建时间',
        update_time timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP   comment '最后一次更新时间',
        primary key (`id`)
    
    ) engine=InnoDB default charset=UTF8MB4
    """,
    """create table If Not Exists `haircut_order_info` (
    id int not null auto_increment,
    `order_no` bigint  comment '订单号',
    `user_id` int default null comment '用户id',
    `shipping_id` int default null,
    `payment` decimal(20,2)  comment '实际支付金额 单位是元',
    payment_type tinyint comment '支付类型 1-线上支付',
    `postage` int  comment '运费',
    `status` int  comment '订单状态:0-已取消,10-未付款,20-已付款, 40-已发货, 50-交易成功,60-交易关闭',
    `send_time` datetime comment '发货时间',
    `end_time` datetime  comment '交易完成时间',
    `close_time` datetime default null comment '交易关闭时间',
    create_time timestamp default CURRENT_TIMESTAMP  comment '创建时间',
    update_time timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP   comment '最后一次更新时间',
      primary key (`id`),
      unique key `order_no_index` (`order_no`) USING BTREE
) engine=InnoDB default charset=UTF8MB4""",
    """
    create table If Not Exists `haircut_order_item` (
    id int not null auto_increment,
    `user_id` int,
    `order_no` bigint,
     `product_id` int comment '商品ID',
     `product_name` varchar(100) comment '商品名',
     `product_image` varchar(100) comment '商品名图片地址',
     `current_unit_price` decimal(20,2) comment '生成订单时商品单价',
     `quantity` int  comment '商品数量',
     `total_price` decimal(20,2) comment '商品总价',
     create_time timestamp default CURRENT_TIMESTAMP  comment '创建时间',
    update_time timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP   comment '最后一次更新时间',
     primary key (`id`),
      unique key `order_no_index` (`order_no`) USING BTREE,
      key `order_no_user_id_index` (`user_id`, `order_no`) using btree
) engine=InnoDB default charset=UTF8MB4""",
    """create table If Not Exists `haircut_pay_info` (
     id int not null auto_increment,
    `user_id` int not null comment '用户ID',
    `order_no` bigint not null comment '订单号',
    `pay_platform` tinyint default null comment '支付平台, 1-支付宝,',
    `platform_number` varchar(200) default null comment '支付宝支付流水号',
     platform_status varchar(20) default null comment '支付宝支付状态',
     create_time timestamp default CURRENT_TIMESTAMP  comment '创建时间',
     update_time timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP   comment '最后一次更新时间',
    primary key (`id`)
) engine=InnoDB default charset=UTF8MB4""",
    """create table If Not Exists `haircut_cart` (
    id int not null auto_increment,
    `uesr_id` BIGINT not null,
    `product_id` int default null comment '商品ID',
    `quantity` int default null comment '数量',
    `checked` TINYINT  comment '是否选择,1=勾选 2,未勾选',
    create_time timestamp default CURRENT_TIMESTAMP  comment '创建时间',
    update_time timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP   comment '最后一次更新时间',
     primary key (`id`)

) engine=InnoDB default charset=UTF8MB4""",
    """create table If Not Exists `haircut_carousel` (
        id smallint auto_increment comment '轮播图ID',
        product_id int not null,
        
        image varchar(128) comment '图片',
        `index` tinyint comment '轮播顺序',
        primary key (`id`)
    ) engine=InnoDB default charset=UTF8MB4
    """

]

pool = tormysql.ConnectionPool(
    max_connections=1,  # max open connections
    idle_seconds=7200,  # conntion idle timeout time, 0 is not timeout
    wait_connection_timeout=3,  # wait connection timeout
    host="127.0.0.1",
    user="root",
    passwd="123456",
    db="haircut",
    charset="utf8",
    cursorclass=tormysql.DictCursor
)


async def create_table(delete=False):
    """
    创建表
    :param delete:
    :return:
    """
    async with await pool.Connection() as conn:
        async with conn.cursor() as cursor:
            if delete:
                for sql in SQL:
                    table = sql[sql.find('haircut'):sql.find('(', sql.find('haircut'))].replace('`', '')
                    await cursor.execute(f"drop table if exists  {table}")

            else:
                for sql in SQL:
                    await cursor.execute(sql)
            await conn.commit()
    await pool.close()

import random
async def test_data():
    data = [
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),
        (''.join(random.sample("abcdjiwerihjvds", 7)), 'xcqwredas', 'fd2easd', ''.join(random.sample("12345678901", 11)), '1'),


    ]
    sql = "INSERT INTO `haircut_user` (`username`, `password`, `email`, `phone`, `address`) VALUES (%s,%s,%s, %s, %s)"
    async with await pool.Connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.executemany(sql, data)

            await conn.commit()
    await pool.close()


if __name__ == '__main__':
    drop = False
    loop = asyncio.get_event_loop()
    task = [
        # create_table(drop)
        test_data()
    ]
    loop.run_until_complete(asyncio.wait(task))
