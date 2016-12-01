class DBRowWrapper:
    def __init__(self, db_result_wrapper, row):
        self.db_result_wrapper = db_result_wrapper
        self.row = row
    
    def __getitem__(self, field_name):
        return self.row[self.__getFieldIndex(field_name)]
    
    def __getFieldIndex(self, field_name):
        self.db_result_wrapper.getFieldIndex(field_name)
    
class DBResultWapper:
    def __init__(self, query_result):
        self.query_result = query_result
        self.tuples = self.__getTuples()
    
    def __getitem__(self, row_num):
        return DBRowWrapper(self, self.tuples[row_num])

    def getFieldIndex(self, field_name):
        return self.query_result.fieldnum(field_name)

    def __getTuples(self):
        return self.query_result.getresult()