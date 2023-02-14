-- part 2

-- query 1
SELECT Staff.ssNo, Staff.name, Staff.phone, Staff.role, Staff.status, Vaccination.organization
FROM Staff, Vaccination, Shift
WHERE Vaccination.eventdate = DATE('2021-05-10')
    AND EXTRACT(dow FROM Vaccination.eventDate) = Shift.weekday
    AND Vaccination.organization = Shift.org
    AND Shift.ssNo = Staff.ssNo;
	
-- query 2
SELECT * FROM Staff
WHERE ssNo IN
(SELECT Staff.ssNo
FROM Staff, Organization, Shift
WHERE Staff.org = Organization.name
    AND Organization.address LIKE '%HELSINKI%'
    AND Staff.ssNo = Shift.ssNo
    AND Shift.weekday = 3);

-- query 3
SELECT l.batchid, o.name, o.telephone
FROM organization AS o,
(
SELECT batchid, org
FROM batch
WHERE batchid not IN
(SELECT batchid FROM transportation)
UNION
SELECT t1.batchid, arrorg
FROM transportation AS t1,
(
SELECT batchid, max(arrdate) AS maxarr
FROM transportation
GROUP BY batchid
) AS t2
WHERE t1.batchid = t2.batchid
	AND t1.arrdate = t2.maxarr
) AS l
WHERE o.name = l.org
ORDER BY l.batchid
;


-- query 4
SELECT Diagnose.patient,Diagnose.symptom, Diagnose.reportDate,
Batch.batchID,Batch.vaccID,
Vaccine.name AS vaccineType,
Attendance.eventdate AS vaccinatedDate,
Attendance.org AS vaccnationPlace
FROM Diagnose, Symptom, Attendance, Vaccination, Batch, Vaccine
WHERE Diagnose.symptom = Symptom.name
	AND Symptom.critical = True
	AND Diagnose.reportDate > '2021-05-10'
	AND Diagnose.patient = Attendance.ssNo
	AND Attendance.eventdate = Vaccination.eventdate
	AND Vaccination.batchID = Batch.batchID
	AND Batch.vaccID = Vaccine.id
;


-- query 5
drop view if exists vstatus;

create view vstatus as
select p.ssno, p.name, p.birthday, p.gender,
    case when (count(att.eventdate) >= 2) then 1 else 0 end vaccinationStatus
from patient as p, attendance as att, vaccination as ve, batch as b, vaccine as v
where p.ssno = att.ssno
	and att.eventdate = ve.eventdate
	and att.org = ve.organization
	and ve.batchid = b.batchid
	and b.vaccid = v.id
group by p.ssno, p.name;

select * from vstatus;



-- query 6
SELECT org, vaccid, v.name, sum(amount)
FROM
(
SELECT t1.batchid, t1.arrorg AS org, b.amount, b.vaccid
FROM transportation AS t1,
(SELECT batchid,max(arrdate) AS maxarr
FROM transportation
GROUP BY batchid) AS t2,
batch AS b
WHERE t1.batchid = t2.batchid 
	AND t1.arrdate = t2.maxarr
	AND t1.batchid = b.batchid
UNION
SELECT batchid, org, amount, vaccid
FROM batch
WHERE batchid not IN
(SELECT batchid FROM transportation)
) AS s,
vaccine AS v
WHERE s.vaccid = v.id
GROUP BY s.org, s.vaccid, v.name
ORDER BY s.org
;

SELECT org, sum(amount)
FROM
(
SELECT t1.batchid, t1.arrorg AS org, b.amount, b.vaccid
FROM transportation AS t1,
(SELECT batchid,max(arrdate) AS maxarr
FROM transportation
GROUP BY batchid) AS t2,
batch AS b
WHERE t1.batchid = t2.batchid 
	AND t1.arrdate = t2.maxarr
	AND t1.batchid = b.batchid
UNION
SELECT batchid, org, amount, vaccid
FROM batch
WHERE batchid not IN
(SELECT batchid FROM transportation)
) AS s,
vaccine AS v
WHERE s.vaccid = v.id
GROUP BY s.org
ORDER BY s.org
;


-- query 7
SELECT vaccid, vtype, symptom, COUNT(patient) AS frequency
FROM 
(
SELECT d.patient, d.symptom, d.reportdate, att.eventdate, v.id AS vaccid, v.name AS vtype
FROM diagnose AS d , attendance AS att, vaccination AS ve, batch AS b, vaccine AS v
WHERE d.patient = att.ssno
	AND att.eventdate = ve.eventdate
	AND att.org = ve.organization
	AND ve.batchid = b.batchid
	AND b.vaccid = v.id
AND d.reportdate >= att.eventdate
) AS s
GROUP BY vaccid, vtype, symptom
;
