-- Active: 1762504411111@@127.0.0.1@3306@grilled_kim

CREATE DATABASE grilled_kim;

# 사용장에게 데이터베이스 사용권한 부여
GRANT ALL PRIVILEGES ON grilled_kim.* to 'skn22'@'%';


            select *
              from charger_station
where station_id = 'CU310054'