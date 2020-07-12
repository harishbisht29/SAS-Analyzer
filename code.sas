before /* Print the contents of the most recently used dataset using the PRINT procedure.*/ after

Libname   Input1 "/use_r/bin/harish/test.txt";
Libname Input2 '/this/is/te_st/location";
FileName     File '/test/file.txt';
Libname Input3 '/user/name/Libraay_one/';

%include '/user/name/Libraay_one/Test.xlsmdns';

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
Data    D1;
    Set     Input1.Data;
Run;

Data Input2.Output;
    Set D1;
Run;

Unix_Path_Regular_Expression= r'(/[a-zA-Z0-9_]+)+/*'