/*
 Navicat Premium Data Transfer

 Source Server         : mydb
 Source Server Type    : MySQL
 Source Server Version : 50744
 Source Host           : 127.0.0.1:3306
 Source Schema         : comic

 Target Server Type    : MySQL
 Target Server Version : 50744
 File Encoding         : 65001

 Date: 22/09/2025 08:19:49
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for category
-- ----------------------------
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `sort` tinyint(1) NOT NULL DEFAULT 0,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for chapter
-- ----------------------------
DROP TABLE IF EXISTS `chapter`;
CREATE TABLE `chapter`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comic_id` int(11) NOT NULL COMMENT '漫画id',
  `source_comic_id` int(11) NOT NULL COMMENT '采集-漫画id',
  `source_chapter_id` int(11) NOT NULL COMMENT '采集-章节id',
  `source_image_id` int(11) NOT NULL COMMENT '采集-图片id',
  `cover` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '封面',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '标题',
  `sort` int(11) NOT NULL DEFAULT 0,
  `images` json NOT NULL,
  `source` json NOT NULL,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `source_chapter_id`(`source_chapter_id`) USING BTREE,
  UNIQUE INDEX `source_image_id`(`source_image_id`) USING BTREE,
  INDEX `comic_id`(`comic_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '章节' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for comic
-- ----------------------------
DROP TABLE IF EXISTS `comic`;
CREATE TABLE `comic`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source_comic_id` int(11) NOT NULL COMMENT '采集-漫画id',
  `cover` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '封面',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '标题',
  `author` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '作者',
  `label` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '标签',
  `category` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '分类',
  `region` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '地区',
  `chapter_count` int(11) NOT NULL DEFAULT 0 COMMENT '章节数量',
  `like` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '喜欢',
  `popularity` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0' COMMENT '人气热度',
  `view` int(11) NOT NULL DEFAULT 0 COMMENT '观看量',
  `subscribe` int(11) NOT NULL DEFAULT 0 COMMENT '订阅量',
  `is_finish` tinyint(1) NOT NULL DEFAULT 0 COMMENT '0连载 1完结',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '描述',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_chapter_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最新章节更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `comic_id`(`source_comic_id`) USING BTREE,
  INDEX `category`(`category`) USING BTREE,
  INDEX `region`(`region`) USING BTREE,
  INDEX `is_finish`(`is_finish`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '漫画' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for series
-- ----------------------------
DROP TABLE IF EXISTS `series`;
CREATE TABLE `series`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `ids` json NOT NULL,
  `sort` tinyint(3) NOT NULL DEFAULT 0,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for source_chapter
-- ----------------------------
DROP TABLE IF EXISTS `source_chapter`;
CREATE TABLE `source_chapter`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comic_id` int(11) NOT NULL,
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '源url',
  `cover` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '封面',
  `title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '标题',
  `sort` int(11) NOT NULL DEFAULT 0,
  `status` tinyint(1) NOT NULL DEFAULT 0 COMMENT '0未审核 1通过',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `source_unique`(`comic_id`, `source_url`) USING BTREE,
  INDEX `status`(`status`) USING BTREE,
  INDEX `comic_id`(`comic_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4251 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '采集-漫画章节' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for source_comic
-- ----------------------------
DROP TABLE IF EXISTS `source_comic`;
CREATE TABLE `source_comic`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source` tinyint(1) NOT NULL DEFAULT 1 COMMENT '采集源 1:快看 2:腾讯',
  `source_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '源url',
  `cover` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '封面',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '标题',
  `author` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '作者',
  `label` json NOT NULL COMMENT '标签',
  `category` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '分类',
  `region` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '地区',
  `chapter_count` int(11) NOT NULL DEFAULT 0 COMMENT '章节数量',
  `chapter_count_download` int(11) NOT NULL DEFAULT 0 COMMENT '章节数量(已下载)',
  `like` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '喜欢',
  `popularity` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '0' COMMENT '人气热度',
  `is_finish` tinyint(1) NOT NULL DEFAULT 0 COMMENT '0连载 1完结',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '' COMMENT '描述',
  `status` tinyint(1) NOT NULL DEFAULT 0 COMMENT '0未审核 1通过',
  `last_chapter_update_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最新章节更新时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `status`(`status`) USING BTREE,
  INDEX `category`(`category`) USING BTREE,
  INDEX `finish`(`is_finish`) USING BTREE,
  UNIQUE INDEX `source_url`(`source_url`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 72 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '采集-漫画' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for source_image
-- ----------------------------
DROP TABLE IF EXISTS `source_image`;
CREATE TABLE `source_image`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comic_id` int(11) NOT NULL DEFAULT 0,
  `chapter_id` int(11) NOT NULL,
  `images` json NOT NULL,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `chapter_id`(`chapter_id`) USING BTREE,
  INDEX `comic_id`(`comic_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4246 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `sort` tinyint(1) NOT NULL DEFAULT 0,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `title`(`title`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Function structure for CountChapterDone
-- ----------------------------
DROP FUNCTION IF EXISTS `CountChapterDone`;
delimiter ;;
CREATE FUNCTION `CountChapterDone`(comic_id INT)
 RETURNS int(11)
  DETERMINISTIC
BEGIN
DECLARE result INT;

IF comic_id > 0 THEN
SELECT count(1) INTO result FROM source_chapter INNER JOIN source_image ON source_chapter.id = source_image.chapter_id WHERE source_chapter.comic_id = comic_id;
ELSE
SELECT count(1) INTO result FROM source_chapter INNER JOIN source_image ON source_chapter.id = source_image.chapter_id;
END IF;

	RETURN result;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
