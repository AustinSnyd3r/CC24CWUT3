-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema apptracker
-- -----------------------------------------------------
-- If we already have a database, nuke it from orbit
DROP DATABASE IF EXISTS `apptracker`;
-- -----------------------------------------------------
-- Schema apptracker
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `apptracker` DEFAULT CHARACTER SET utf8mb4 ;
USE `apptracker` ;

-- -----------------------------------------------------
-- Table `apptracker`.`clientids`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `apptracker`.`clientids` (
  `clientid` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`clientid`),
  UNIQUE INDEX `clientid_UNIQUE` (`clientid` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `apptracker`.`clients`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `apptracker`.`clients` (
  `clientid` VARCHAR(45) NOT NULL,
  `clientoauth` VARCHAR(70) NOT NULL UNIQUE,
  `firstname` VARCHAR(20) NOT NULL,
  `lastname` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`clientid`),
  CONSTRAINT `fk_clients_clientid`
    FOREIGN KEY (`clientid`)
    REFERENCES `apptracker`.`clientids` (`clientid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `apptracker`.`applications`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `apptracker`.`applications` (
  `applicationid` INT NOT NULL AUTO_INCREMENT,
  `clientid` VARCHAR(45) NOT NULL,
  `company` VARCHAR(30) NOT NULL,
  `position` VARCHAR(30) NOT NULL,
  `date_submitted` DATE NOT NULL,
  `status` ENUM("WAITING", "REJECTED", "INTERVIEW", "OFFER", "ACCEPTED") NOT NULL,
  `has_update` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`applicationid`, `clientid`),
  INDEX `fk_applications_clientid_idx` (`clientid` ASC) VISIBLE,
  CONSTRAINT `fk_applications_clientid`
    FOREIGN KEY (`clientid`)
    REFERENCES `apptracker`.`clients` (`clientid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `apptracker`.`keywords`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `apptracker`.`keywords` (
  `clientid` VARCHAR(45) NOT NULL,
  `keyword` VARCHAR(20) NOT NULL,
  `keywordtype` ENUM("NEGATIVE", "POSITIVE", "INTERVIEW", "OFFER", "REJECTED", "ACCEPTED") NOT NULL,
  PRIMARY KEY (`clientid`, `keyword`),
  CONSTRAINT `fk_keywords_clientid`
    FOREIGN KEY (`clientid`)
    REFERENCES `apptracker`.`clients` (`clientid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
