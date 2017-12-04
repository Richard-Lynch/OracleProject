#!/bin/bash

touch test.txt;

sqlplus64 lynchri/A8DZk4A5@'(DESCRIPTION = (ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCP)(HOST=oracleserv2.scss.tcd.ie)(PORT = 1521)))(CONNECT_DATA = (SERVICE_NAME = orcl.scss.tcd.ie)))''select tablespace_name, table_name from user_tables;' ;
