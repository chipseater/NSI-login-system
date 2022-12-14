def db_func(func):
    def inner(self, *args, **kwargs):
        try:
            cursor = self.conn.cursor()
            returnObj = func(self, cursor, *args, **kwargs)
            self.conn.commit()
            if returnObj:
                returnObj['error'] = None
            else:
                returnObj = {'error': None}
            return returnObj
        except Exception as e:
            print(e)
            return {'error': e.args}
    return inner
