/*all depts whose average salary is greater than 40k*/
select Dno, count(*) from Employee group by Dno having avg(Salary) > 40000;