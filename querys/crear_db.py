DLL_QUERY = """
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema grocery_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema grocery_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `grocery_db` DEFAULT CHARACTER SET utf8 ;
USE `grocery_db` ;

-- -----------------------------------------------------
-- Table `grocery_db`.`Region`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `grocery_db`.`Region` (
  `idRegion` INT NOT NULL AUTO_INCREMENT,
  `region` VARCHAR(45) NULL,
  PRIMARY KEY (`idRegion`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `grocery_db`.`City`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `grocery_db`.`City` (
  `idCity` INT NOT NULL AUTO_INCREMENT,
  `city` VARCHAR(45) NULL,
  `state` VARCHAR(45) NULL,
  `idRegion` INT NOT NULL,
  PRIMARY KEY (`idCity`),
  INDEX `fk_City_Region1_idx` (`idRegion` ASC) VISIBLE,
  CONSTRAINT `fk_City_Region1`
    FOREIGN KEY (`idRegion`)
    REFERENCES `grocery_db`.`Region` (`idRegion`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `grocery_db`.`Customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `grocery_db`.`Customer` (
  `idCustomer` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `idCity` INT NOT NULL,
  PRIMARY KEY (`idCustomer`),
  INDEX `fk_Customer_City_idx` (`idCity` ASC) VISIBLE,
  CONSTRAINT `fk_Customer_City`
    FOREIGN KEY (`idCity`)
    REFERENCES `grocery_db`.`City` (`idCity`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `grocery_db`.`Order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `grocery_db`.`Order` (
  `idOrder` INT NOT NULL AUTO_INCREMENT,
  `orderNumber` VARCHAR(45) NULL,
  `sales` FLOAT NULL,
  `discount` FLOAT NULL,
  `profit` FLOAT NULL,
  `date` DATE NULL,
  `idCustomer` INT NOT NULL,
  `sub_category_id` INT NULL,
  PRIMARY KEY (`idOrder`),
  INDEX `fk_Order_Customer1_idx` (`idCustomer` ASC) VISIBLE,
  CONSTRAINT `fk_Order_Customer1`
    FOREIGN KEY (`idCustomer`)
    REFERENCES `grocery_db`.`Customer` (`idCustomer`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

"""