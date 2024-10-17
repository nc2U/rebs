import random


class MasterSlaveRouter:
    def db_for_read(self, model, **hints):
        """
        읽기 작업은 slave1 또는 slave2에서 처리
        """
        return random.choice(['slave1', 'slave2'])

    def db_for_write(self, model, **hints):
        """
        쓰기 작업은 master에서 처리
        """
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        두 객체가 동일한 DB에 있을 때 관계 허용
        """
        db_list = ('default', 'slave1', 'slave2')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        마이그레이션 작업은 master에서만 실행
        """
        return db == 'default'
