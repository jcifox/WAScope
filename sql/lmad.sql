SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for request_record
-- ----------------------------
DROP TABLE IF EXISTS `request_record`;
CREATE TABLE `request_record`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `flow_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT '',
  `host` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT '',
  `port` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT '',
  `hash` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT '',
  `method` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT '',
  `referer` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `url` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `content_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT '',
  `response` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `response_exists_sensitive` int(9) NULL DEFAULT 0,
  `response_sensitive` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `path` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `path_exist_sensitive` tinyint(9) NULL DEFAULT 0,
  `path_sensitive` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `get_params` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `get_exist_sensitive` int(9) NULL DEFAULT 0,
  `get_sensitive` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `post_params` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `post_exist_sensitive` int(9) NULL DEFAULT 0,
  `post_sensitive` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `create_time` int(11) UNSIGNED NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for request_record_second
-- ----------------------------
DROP TABLE IF EXISTS `request_record_second`;
CREATE TABLE `request_record_second`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `host` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT '',
  `hash` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT '',
  `method` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT '',
  `content_type` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT '',
  `referer` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `origin_url` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `url` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `gen_params` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `response_hash` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT '',
  `response` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `response_exists_sensitive` int(9) NULL DEFAULT 0,
  `response_sensitive` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `create_time` int(11) UNSIGNED NULL DEFAULT 0,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
