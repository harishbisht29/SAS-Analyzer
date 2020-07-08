before /* Print the contents of the most recently used dataset using the PRINT procedure.*/ after

Libname   Input1 "/user/bin/harish/test";
Libname Input2 '/this/is/test/location";

* Check the variables in the most recently used dataset using the CONTENTS procedure;
Data    D1;
    Set     Input1.Data;
Run;

Data Input2.Output;
    Set D1;
Run;
