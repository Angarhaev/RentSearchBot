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
            cursor.execute("CREATE TABLE IF NOT EXISTS`angarhaev`.`advertisements` ( "
                           "`id` INT(10) NOT NULL AUTO_INCREMENT , "
                           "`adv_id` INT(10) NOT NULL , "
                           "`date_adv` DATE NOT NULL , "
                           "`metro` VARCHAR(20) NOT NULL , "
                           "`rooms` VARCHAR(20) NOT NULL , "
                           "`floor` VARCHAR(20) NOT NULL , "
                           "`price` VARCHAR(20) NOT NULL , "
                           "`square` VARCHAR(20) NOT NULL , "
                           "`repair` VARCHAR(240) NOT NULL , "
                           "`furniture` VARCHAR(240) NOT NULL , "
                           "`description` VARCHAR(240) NOT NULL , "
                           "`address` VARCHAR(240) NOT NULL , "
                           "`phone` VARCHAR(20) NOT NULL , "
                           "`image_1` VARCHAR(240) NOT NULL , "
                           "`image_2` VARCHAR(240) NOT NULL , "
                           "`image_3` VARCHAR(240) NOT NULL , "
                           "`url` VARCHAR(240) NOT NULL , "
                           "PRIMARY KEY (`id`), "
                           "UNIQUE (`adv_id`)) ENGINE = InnoDB;")
            cursor.execute("CREATE TABLE IF NOT EXISTS `angarhaev`.`settings` ( "
                           "`id` INT(10) NOT NULL AUTO_INCREMENT , "
                           "`telegram_id` INT(20) NOT NULL , "
                           "`district` VARCHAR(20) NOT NULL , "
                           "`rooms` VARCHAR(20) NOT NULL , "
                           "`low_price`INT(10) NOT NULL , "
                           "`high_price`INT(10) NOT NULL , PRIMARY KEY (`id`) , "
                           "UNIQUE (`telegram_id`)) ENGINE = InnoDB;")
            cursor.execute("CREATE TABLE IF NOT EXISTS `angarhaev`.`sent_favorite` ( "
                           "`id` INT(10) NOT NULL AUTO_INCREMENT , "
                           "`telegram_id` INT(20) NOT NULL , "
                           "`adv_id` INT(10) NOT NULL , "
                           "`sent` INT(10) NOT NULL , "
                           "`favorite` INT(10) NOT NULL , "
                           "PRIMARY KEY (`id`)) ENGINE = InnoDB;")
            cursor.execute("ALTER TABLE `settings` ADD FOREIGN KEY (`telegram_id`) REFERENCES `users`(`telegram_id`) "
                           "ON DELETE CASCADE ON UPDATE CASCADE;")
            cursor.execute("ALTER TABLE `sent_favorite` ADD FOREIGN KEY (`telegram_id`) REFERENCES `users`(`telegram_id`) "
                           "ON DELETE CASCADE ON UPDATE CASCADE;")
            cursor.execute("ALTER TABLE `sent_favorite` ADD FOREIGN KEY (`adv_id`) REFERENCES `advertisements`(`adv_id`) "
                           "ON DELETE CASCADE ON UPDATE CASCADE;")
            database_connect.commit()
            print('База данных готова к работе')

            for data_bases in cursor:
                print(data_bases)
    except Exception as exc:
        print('Ошибка создания таблицы', exc)
    finally:
        database_connect.close()


