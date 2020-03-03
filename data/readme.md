create a new environment named kh-env

create a new database named king_house:
    log in existing databse with psql: psal opportunity_youth
    run the command: `create database king_house;`

create table to import the csv data in bash:
    1, find the path of the csv file and find the columns names,
     ``$ head -n 1 EXTR_.csv | tr ',' '\n' `
    `$ head -n 1 EXTR_ResBldg.csv | tr ',' '\n' `
  
    2, create sql fils in visual studio, using all the columns names and add text at the end of each column name
    3, remove the ',' from the last column name
    
   4, back to the bash: psql king_house -f src/sql/01_create_extr_redsbdlg.sql 
   5, log in to the king_house databse: psql king_house: copy extr_resbldg from '/Users/daihongchen/Downloads/EXTR_ResBldg.csv'  DELIMITERS ',' CSV;
 

