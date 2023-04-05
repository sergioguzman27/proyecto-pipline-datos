DLL_QUERY = """
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema grocery_dw
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema grocery_dw
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `grocery_dw` DEFAULT CHARACTER SET utf8 ;
USE `grocery_dw` ;

-- -----------------------------------------------------
-- Table `grocery_dw`.`DateDim`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `grocery_dw`.`DateDim` (
  `idDate` INT NOT NULL,
  `fullDate` DATE NULL,
  `dayOfWeek` BIGINT NULL,
  `dayNumInMonth` BIGINT NULL,
  `dayNumOverall` BIGINT NULL,
  `dayName` VARCHAR(45) NULL,
  `dayAbbrev` VARCHAR(45) NULL,
  `weekdayFlag` TINYINT NULL,
  `weekNumInYear` BIGINT NULL,
  `weekNumOverall` BIGINT NULL,
  `weekBeginDate` DATE NULL,
  `month` BIGINT NULL,
  `monthNumOverall` BIGINT NULL,
  `monthName` VARCHAR(45) NULL,
  `monthAbbrev` VARCHAR(45) NULL,
  `quarter` BIGINT NULL,
  `year` BIGINT NULL,
  PRIMARY KEY (`idDate`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `grocery_dw`.`CategoryDim`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `grocery_dw`.`CategoryDim` (
  `idSubCategory` INT NOT NULL,
  `subCategory` VARCHAR(45) NULL,
  `category` VARCHAR(45) NULL,
  PRIMARY KEY (`idSubCategory`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `grocery_dw`.`CustomerDim`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `grocery_dw`.`CustomerDim` (
  `idCustomer` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  `city` VARCHAR(45) NULL,
  `state` VARCHAR(45) NULL,
  `region` VARCHAR(45) NULL,
  PRIMARY KEY (`idCustomer`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `grocery_dw`.`OrderFact`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `grocery_dw`.`OrderFact` (
  `idOrderFact` INT NOT NULL,
  `idDate` INT NOT NULL,
  `idCustomer` INT NOT NULL,
  `idSubCategory` INT NOT NULL,
  `orderNumber` VARCHAR(45) NULL,
  `sales` FLOAT NULL,
  `discount` FLOAT NULL,
  `profit` FLOAT NULL,
  PRIMARY KEY (`idOrderFact`, `idDate`, `idCustomer`, `idSubCategory`),
  INDEX `fk_OrderFact_DateDim_idx` (`idDate` ASC) VISIBLE,
  INDEX `fk_OrderFact_CustomerDim1_idx` (`idCustomer` ASC) VISIBLE,
  INDEX `fk_OrderFact_CategoryDim1_idx` (`idSubCategory` ASC) VISIBLE,
  CONSTRAINT `fk_OrderFact_DateDim`
    FOREIGN KEY (`idDate`)
    REFERENCES `grocery_dw`.`DateDim` (`idDate`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_OrderFact_CustomerDim1`
    FOREIGN KEY (`idCustomer`)
    REFERENCES `grocery_dw`.`CustomerDim` (`idCustomer`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_OrderFact_CategoryDim1`
    FOREIGN KEY (`idSubCategory`)
    REFERENCES `grocery_dw`.`CategoryDim` (`idSubCategory`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
"""