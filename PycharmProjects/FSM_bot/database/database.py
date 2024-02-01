import sqlite3


class BotDB:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self.db = db

    def user_exists(self, user_id):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        result = self.cursor.execute('''SELECT id FROM database WHERE user_id = ?''', (user_id,))
        a = len(result.fetchall())
        self.conn.close()
        return bool(a)

    def get_user_id(self, user_id):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        result = self.cursor.execute('''SELECT user_id FROM database WHERE user_id = ?''', (user_id,))
        a = result.fetchone()[0]
        self.conn.close()
        return a

    def add_user(self, user_id):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''INSERT INTO database (user_id) VALUES (?)''', (user_id,))
        self.conn.commit()
        self.conn.close()

    def add_id(self, ch_id, msg_id):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''UPDATE database SET ch_id = ?, msg_id = ? WHERE user_id = ?''', (ch_id, msg_id, ch_id))
        self.conn.commit()
        self.conn.close()

    def add_data(self, data_surname, data_grade, data_first_test, ch_id, msg_id, scores, page, last_page, scores2, user_id):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''UPDATE database SET surname = ?, grade = ?, first_test = ?, ch_id = ?, msg_id = ?,
        first_test_scores = ?, num_of_page = ?, last_page = ?, second_test_scores = ? WHERE user_id = ?''',
                            (data_surname, data_grade, data_first_test, ch_id, msg_id, scores, page, last_page, scores2, user_id))
        self.conn.commit()
        self.conn.close()

    def get_ch_id(self, user_id):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        result = self.cursor.execute('''SELECT ch_id FROM database WHERE user_id = ?''', (user_id,))
        a = result.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return a

    def get_msg_id(self, user_id):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        result = self.cursor.execute('''SELECT msg_id FROM database WHERE user_id = ?''', (user_id,))
        a = result.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return a

    def add_scores(self, user_id):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        result = self.cursor.execute('''SELECT first_test_scores FROM database WHERE user_id = ?''', (user_id,))
        a = result.fetchone()[0]
        self.cursor.execute('''UPDATE database SET first_test_scores = ? WHERE user_id = ?''',
                            (a + 1, user_id))
        self.conn.commit()
        self.conn.close()

    def add_scores2(self, user_id):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        result = self.cursor.execute('''SELECT second_test_scores FROM database WHERE user_id = ?''', (user_id,))
        a = result.fetchone()[0]
        self.cursor.execute('''UPDATE database SET second_test_scores = ? WHERE user_id = ?''',
                            (a + 1, user_id))
        self.conn.commit()
        self.conn.close()

    def del_row(self, user_id):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''DELETE FROM database WHERE user_id = ?''', (user_id,))
        self.conn.commit()
        self.conn.close()

    def get_scores(self, user_id):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        result = self.cursor.execute('''SELECT first_test_scores FROM database WHERE user_id = ?''', (user_id,))
        a = result.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return a

    def get_scores2(self, user_id):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        result = self.cursor.execute('''SELECT second_test_scores FROM database WHERE user_id = ?''', (user_id,))
        a = result.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return a

    def backward_page(self, user_id):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        result = self.cursor.execute('''SELECT num_of_page FROM database WHERE user_id = ?''', (user_id,))
        a = result.fetchone()[0]
        self.cursor.execute('''UPDATE database SET num_of_page = ? WHERE user_id = ?''',
                            (a - 1, user_id))
        self.conn.commit()
        self.conn.close()

    def forward_page(self, user_id):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        result = self.cursor.execute('''SELECT num_of_page FROM database WHERE user_id = ?''', (user_id,))
        a = result.fetchone()[0]
        self.cursor.execute('''UPDATE database SET num_of_page = ? WHERE user_id = ?''',
                            (a + 1, user_id))
        self.conn.commit()
        self.conn.close()

    def get_page(self, user_id):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        result = self.cursor.execute('''SELECT num_of_page FROM database WHERE user_id = ?''', (user_id,))
        a = result.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return a

    def get_last_page(self, user_id):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        result = self.cursor.execute('''SELECT last_page FROM database WHERE user_id = ?''', (user_id,))
        a = result.fetchone()[0]
        self.cursor.execute('''UPDATE database SET last_page = ? WHERE user_id = ?''',
                            (a + 1, user_id))
        self.conn.commit()
        self.conn.close()
        return a
