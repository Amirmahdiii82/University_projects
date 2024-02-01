-- ایجاد دیتابیس
CREATE DATABASE KonkorRegistration;
GO

USE KonkorRegistration;
GO

-- ایجاد جدول کاربران
CREATE TABLE Users (
  UserID INT IDENTITY(1,1) PRIMARY KEY,
  Username NVARCHAR(50) NOT NULL,
  Password NVARCHAR(50) NOT NULL,
  Email NVARCHAR(100) NOT NULL
);
GO

-- ایجاد جدول صدور شناسنامه
CREATE TABLE sodoor_shensnameh(
  sodoor_shensnameh_id INT PRIMARY KEY IDENTITY NOT NULL,
  code_place INT NOT NULL,
  name_place NVARCHAR(30) NOT NULL
);
INSERT INTO sodoor_shensnameh(code_place, name_place) VALUES
  (1111, N'تهران'),
  (2222, N'تهران'),
  (3333, N'گیلان'),
  (4444, N'شیراز'),
  (5555, N'اصفهان');
GO

-- ایجاد جدول کدهای رشته‌های تحصیلی
CREATE TABLE EducationCodes(
  EducationCode_id INT PRIMARY KEY IDENTITY NOT NULL,
  EducationCode INT NOT NULL,
  FieldName NVARCHAR(30) NOT NULL
);
INSERT INTO EducationCodes(EducationCode, FieldName) VALUES
  (110, N'مهندسی کامپیوتر'),
  (111, N'مهندسی برق'),
  (112, N'مهندسی صنایع'),
  (113, N'مهندسی پزشکی'),
  (114, N'مهندسی نفت');
GO

-- ایجاد جدول کدهای رشته‌های امتحانی
CREATE TABLE ExamCodes (
  Examcode_id INT PRIMARY KEY IDENTITY NOT NULL,
  ExamCode INT NOT NULL,
  ExamName NVARCHAR(100) NOT NULL,
  EducationCode_id INT NOT NULL,
  FOREIGN KEY(EducationCode_id) REFERENCES EducationCodes(EducationCode_id)
);
INSERT INTO ExamCodes(ExamCode, ExamName, EducationCode_id) VALUES
  (200, N'هوش مصنوعی', 1),
  (201, N'امنیت', 1),
  (202, N'الکتروینک', 2),
  (203, N'قدرت', 2),
  (204, N'بهینه سازی سیستم ها', 3),
  (205, N'مدیریت نوآوری و فناوری', 3),
  (206, N'بیوالکتریک', 4),
  (207, N'بیومکانیک', 4),
  (208, N'اکتشاف', 5),
  (209, N'بهره برداری', 5);
GO

-- ایجاد جدول مشخصات ثبت‌نامی
CREATE TABLE RegistrationDetails(
  codemelli VARCHAR(10) NOT NULL PRIMARY KEY,
  FirstName NVARCHAR(50) NOT NULL,
  LastName NVARCHAR(50) NOT NULL,
  FatherName NVARCHAR(50) NOT NULL,
  shomareh_shenasnameh INT NOT NULL, -- Adjusted to INT for better integrity
  sodoor_shensnameh_id INT NOT NULL,
  gender NVARCHAR(5) NOT NULL,
  BirthDate char(10) NOT NULL, -- Adjusted to DATE data type for consistency
  EducationCode_id INT NOT NULL,
  ExamCode_id INT NULL,
  PostalCode VARCHAR(10) NOT NULL,
  MobilePhone VARCHAR(15) NOT NULL,
  HomePhone VARCHAR(15) NULL,
  Email NVARCHAR(100) NOT NULL,
  FOREIGN KEY(EducationCode_id) REFERENCES EducationCodes(EducationCode_id),
  FOREIGN KEY(sodoor_shensnameh_id) REFERENCES sodoor_shensnameh(sodoor_shensnameh_id),
  FOREIGN KEY(ExamCode_id) REFERENCES ExamCodes(ExamCode_id)
);
GO

select * from RegistrationDetails;
select * from Users;
SELECT * FROM sodoor_shensnameh;

TRUNCATE TABLE Users;
TRUNCATE TABLE RegistrationDetails;


select *
from RegistrationDetails