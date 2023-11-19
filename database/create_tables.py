from config_data.config import db_host, db_user_name, db_password, db_db_name
from database.my_connect import create_connection


def start_create_table():
    database_connect = create_connection(db_host, db_user_name, db_password, db_db_name)
    try:
        with database_connect.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS`angarhaev`.`users` ( "
                           "`id` INT(10) NOT NULL AUTO_INCREMENT , "
                           "`telegram_id` INT(20) NOT NULL , "
                           "`user_name` VARCHAR(20) NOT NULL , "
                           "PRIMARY KEY (`id`), "
                           "UNIQUE (`telegram_id`)) ENGINE = InnoDB;")
            cursor.execute("CREATE TABLE IF NOT EXISTS`angarhaev`.`districts` ( "
                           "`id` INT(10) NOT NULL AUTO_INCREMENT , "
                           "`district_name` VARCHAR(20) NOT NULL , "
                           "`telegram_id` INT(20) NOT NULL , "
                           "PRIMARY KEY (`id`),"
                           "UNIQUE (`district_name`))  ENGINE = InnoDB;")
            cursor.execute("CREATE TABLE IF NOT EXISTS`angarhaev`.`rooms` ( "
                           "`id` INT(10) NOT NULL AUTO_INCREMENT , "
                           "`rooms_amount` VARCHAR(20) NOT NULL , "
                           "`telegram_id` INT(20) NOT NULL , "
                           "PRIMARY KEY (`id`),"
                           "UNIQUE (`rooms_amount`))  ENGINE = InnoDB;")
            cursor.execute("CREATE TABLE IF NOT EXISTS `angarhaev`.`settings` ( "
                           "`id` INT(10) NOT NULL AUTO_INCREMENT , "
                           "`telegram_id` INT(20) NOT NULL , "
                           "`dist_id` VARCHAR(20) NOT NULL , "
                           "`rooms_id` VARCHAR(20) NOT NULL , "
                           "`low_price`INT(10) NOT NULL , "
                           "`high_price`INT(10) NOT NULL , PRIMARY KEY (`id`) , "
                           "UNIQUE (`telegram_id`)) ENGINE = InnoDB;")
            cursor.execute("ALTER TABLE `settings` ADD FOREIGN KEY (`telegram_id`) REFERENCES `users`(`telegram_id`) "
                           "ON DELETE RESTRICT ON UPDATE RESTRICT;")
            database_connect.commit()
            print('База данных готова к работе')

            for data_bases in cursor:
                print(data_bases)
    except Exception as exc:
        print('Ошибка создания таблицы', exc)
    finally:
        database_connect.close()


