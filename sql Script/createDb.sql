CREATE DATABASE `web`;

CREATE TABLE `logininfo` (
  `loginId` int NOT NULL AUTO_INCREMENT,
  `account` varchar(50) NOT NULL,
  `password` char(32) NOT NULL,
  `role` varchar(50) DEFAULT 'user',
  `status` varchar(50) DEFAULT 'open',
  `token` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`loginId`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `personalinfo` (
  `userId` int NOT NULL AUTO_INCREMENT,
  `firstName` varchar(50) DEFAULT NULL,
  `lastName` varchar(50) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phoneNumber` varchar(20) DEFAULT NULL,
  `loginId` int DEFAULT NULL,
  PRIMARY KEY (`userId`),
  KEY `loginId` (`loginId`),
  CONSTRAINT `personalinfo_ibfk_1` FOREIGN KEY (`loginId`) REFERENCES `logininfo` (`loginId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `category` (
  `categoryId` int NOT NULL AUTO_INCREMENT,
  `main` varchar(50) NOT NULL,
  `sub` varchar(50) NOT NULL,
  PRIMARY KEY (`categoryId`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `product` (
  `Pid` int NOT NULL AUTO_INCREMENT,
  `categoryId` int DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `status` varchar(50) DEFAULT 'open',
  `price` decimal(10,2) DEFAULT NULL,
  `description` text,
  `recommend` tinyint(1) DEFAULT '0',
  `cooktime` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`Pid`),
  KEY `categoryId` (`categoryId`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`categoryId`) REFERENCES `category` (`categoryId`)
) ENGINE=InnoDB AUTO_INCREMENT=111 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `image` (
  `imageID` int NOT NULL AUTO_INCREMENT,
  `Image` longblob,
  `Pid` int DEFAULT NULL,
  PRIMARY KEY (`imageID`),
  KEY `Pid` (`Pid`),
  CONSTRAINT `image_ibfk_1` FOREIGN KEY (`Pid`) REFERENCES `product` (`Pid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `order` (
  `OrderID` int NOT NULL AUTO_INCREMENT,
  `Pid` int NOT NULL,
  `quantity` int NOT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`OrderID`),
  KEY `Pid` (`Pid`),
  CONSTRAINT `order_ibfk_1` FOREIGN KEY (`Pid`) REFERENCES `product` (`Pid`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `cart` (
  `UserId` int NOT NULL,
  `OrderId` int NOT NULL,
  PRIMARY KEY (`UserId`,`OrderId`),
  KEY `OrderId` (`OrderId`),
  CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`OrderId`) REFERENCES `order` (`OrderID`),
  CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`UserId`) REFERENCES `personalinfo` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DELIMITER //
CREATE TRIGGER update_order_price BEFORE INSERT ON `order`
FOR EACH ROW
BEGIN
    DECLARE product_price DECIMAL(10, 2);
    SELECT price INTO product_price FROM product WHERE Pid = NEW.Pid;
    SET NEW.price = NEW.quantity * product_price;
END;
//
DELIMITER ;

