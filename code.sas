before /* Print the contents of the most recently used dataset using the PRINT procedure.*/ after

Libname   Input1 "/use_r/bin/harish/";
Libname Input2 '/this/is/te_st/location";
FileName     File '/test/file.txt';
Libname Input3 '/user/name/Libraay_one/';

%include '/user/name/Libraay_one/Test/newfile.sas';

proc sql;
    create table Work.Work1 as
    select *
    from Input1.Marks;
quit;
Data Input1.Final;
    Set Work.Test;
Run;

proc sql;
    create table Work.Work2 as
    select *
    from Input1.Final;
quit;

 PROC EXPORT DATA= datasetname

             OUTFILE= “/some/location/on/server/file.XLS"

             DBMS=EXCEL REPLACE;

      SHEET=“excel worksheet name"; 

PROC  IMPORT OUT=WORK.sample
		DATAFILE="/user/bin/home/home.xlsx"
		DBMS=EXCEL REPLACE;
	RANGE="Sheet1$";
	GETNAMES=YES;
	MIXED=YES;
	SCANTEXT=YES;
	USEDATE=YES;
	SCANTIME=YES;
QUIT;

Proc Sql;
    Connect to Terdata winid= id password=password;
    select * from connection to teradata(
        create table teradata_table
        as select * from Work.table1 
        inner join CDW.CDW_ACCS_PRODV t1 
        on t1.name=t2.name
        left join IDW_ACCS_PRODV t2
        ont T2.test=t1.test;

    )
Qui;


%include '/user/bin/macros/email_lookp.sas'