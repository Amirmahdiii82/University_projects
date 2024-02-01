-- ایجاد تریگر برای بررسی کد صدور شناسنامه
create TRIGGER CheckFormEntries
ON RegistrationDetails
INSTEAD OF INSERT
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (SELECT 1 FROM INSERTED WHERE INSERTED.FirstName IS NULL OR INSERTED.FirstName = '')
    BEGIN
        THROW 50000, 'خطا: نام نمی تواند خالی باشد', 1;
    END
	
    IF EXISTS (SELECT 1 FROM INSERTED WHERE INSERTED.LastName IS NULL OR INSERTED.LastName = '')
    BEGIN
        THROW 50001, 'خطا: نام خانوادگی نمی تواند خالی باشد.', 1;
    END

    IF EXISTS (SELECT 1 FROM INSERTED WHERE INSERTED.FatherName IS NULL OR INSERTED.FatherName = '')
    BEGIN
        THROW 50002, 'خطا: نام پدر نمی تواند خالی باشد', 1;
    END
    IF EXISTS (SELECT 1 FROM INSERTED WHERE LEN(INSERTED.codemelli) != 8)
    BEGIN
        THROW 50003, 'خطا: شماره ملی باید دقیقا 8 رقم باشد', 1;
    END
    IF EXISTS (
        SELECT 1 FROM RegistrationDetails 
        WHERE codemelli IN (SELECT codemelli FROM INSERTED)
    )
    BEGIN
        THROW 50004, 'این کدملی قبلا ثبت شده است', 1;
    END
    IF EXISTS (SELECT 1 FROM INSERTED WHERE LEN(INSERTED.shomareh_shenasnameh) != 8)
    BEGIN
        THROW 50005, 'خطا: شماره شناسنامه باید دقیقا 8 رقم باشد', 1;
    END
    IF EXISTS (SELECT 1 FROM INSERTED WHERE INSERTED.sodoor_shensnameh_id IS NULL OR INSERTED.sodoor_shensnameh_id = '')
    BEGIN
        THROW 50006, 'خطا: محل صدور شناسنامه نمی تواند خالی باشد.', 1;
    END
    IF NOT EXISTS (
        SELECT 1
        FROM INSERTED
        JOIN sodoor_shensnameh ON INSERTED.sodoor_shensnameh_id = sodoor_shensnameh.sodoor_shensnameh_id
    )
    BEGIN
        THROW 50007, N'کد محل صدور شناسنامه نامعتبر است', 1;
    END
    --IF EXISTS (SELECT 1 FROM INSERTED WHERE INSERTED.gender IS NULL OR INSERTED.gender = '')
    --BEGIN
    --    THROW 50008, 'خطا: فیلد جنسیت نمی‌تواند خالی باشد.', 1;
    --END
    --IF NOT EXISTS (
    --SELECT 1
    --FROM INSERTED
    --WHERE INSERTED.birthdate LIKE '13[0-9][0-9]/[0-1][0-9]/[0-3][0-9]'
	--	)
	--BEGIN
	--	THROW 50009, N'تاریخ معتبر نیست. مثال معتبر: 1380/01/11', 1;
	--END

    IF NOT EXISTS (
        SELECT 1
        FROM INSERTED
        JOIN EducationCodes ON INSERTED.EducationCode_id = EducationCodes.EducationCode_id
    )
    BEGIN
        THROW 50010, N'کد رشته تحصیلی نامتعبر است.', 1;
    END
    IF NOT EXISTS (
        SELECT 1
        FROM INSERTED
        WHERE INSERTED.email LIKE '_%@gmail.com'
    )
    BEGIN
        THROW 50014, N'ایمیل نامتعبر می باشد.', 1;
    END
  IF EXISTS (
        SELECT 1 FROM RegistrationDetails 
        WHERE shomareh_shenasnameh IN (SELECT shomareh_shenasnameh FROM INSERTED)
    )
    BEGIN
        THROW 50015, 'این شماره شناسنامه قبلا ثبت شده است', 1;
    END

    
    INSERT INTO RegistrationDetails (
        codemelli,
        FirstName,
        LastName,
        FatherName,
        shomareh_shenasnameh,
        sodoor_shensnameh_id,
        gender,
        birthdate,
        EducationCode_id,
        examcode_id,
        PostalCode,
        MobilePhone,
        HomePhone,
        email
    )
    SELECT
        INSERTED.codemelli,
        INSERTED.FirstName,
        INSERTED.LastName,
        INSERTED.FatherName,
        INSERTED.shomareh_shenasnameh, 
        INSERTED.sodoor_shensnameh_id,
        INSERTED.gender,
        INSERTED.birthdate,
        INSERTED.EducationCode_id,
        INSERTED.examcode_id,
        INSERTED.PostalCode,
        INSERTED.MobilePhone,
        INSERTED.HomePhone,
        INSERTED.email
    FROM INSERTED
END
go

DROP TRIGGER CheckFormEntries;
