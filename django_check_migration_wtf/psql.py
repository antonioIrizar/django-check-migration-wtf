from .rules import AbstractSQLRule


class RenameColumnSQLRule(AbstractSQLRule):

    @property
    def pattern(self) -> str:
        return r'alter table .* rename column .* to .*;'

    @property
    def error_info(self) -> str:
        return 'You cannot rename a column, it is an blocking operation. ' \
               'You should create a new column and copy their values'


class RenameTableSQLRule(AbstractSQLRule):
    @property
    def pattern(self) -> str:
        return r'alter table .* rename to .*;'

    @property
    def error_info(self) -> str:
        return 'You cannot rename a table, it is an blocking operation. ' \
               'You should create a new table and copy their values'


class AddColumnNotNullSQLRule(AbstractSQLRule):
    @property
    def pattern(self) -> str:
        return r'alter table .* add column .* not null( .*;|;)'

    @property
    def error_info(self) -> str:
        return 'You cannot add column to table with not null. Because old instance will old code will dead. ' \
               'You should add column with nullable'


class AddColumnDefaultSQLRule(AbstractSQLRule):
    @property
    def pattern(self) -> str:
        return r'alter table .* add column .* default .*;'

    @property
    def error_info(self) -> str:
        return 'You cannot add column to table with default value, ' \
               'It is a blocking operation because all rows will be populate with this value. ' \
               'You should add column without default and then alter column to set default value.'


class AddColumnPrimaryKeySQLRule(AbstractSQLRule):
    @property
    def pattern(self) -> str:
        return r'alter table .* add column .* primary key( .*;|;)'

    @property
    def error_info(self) -> str:
        return 'You cannot add column to table with primary key , ' \
               'It is a blocking operation because it will create a index. ' \
               'You should add column without primary key, ' \
               'then create a unique index concurrently and finally add the constraint.'


class AddColumnUniqueSQLRule(AbstractSQLRule):
    @property
    def pattern(self) -> str:
        return r'alter table .* add column .* unique( .*;|;)'

    @property
    def error_info(self) -> str:
        return 'You cannot add column to table with unique , ' \
               'It is a blocking operation because it will create a index. ' \
               'You should add column without unique, ' \
               'then create a unique index concurrently and finally add the constraint.'


class AlterColumnTypeSQLRule(AbstractSQLRule):
    # TODO add support for types that they are secures
    @property
    def pattern(self) -> str:
        return r'alter table .* alter column .* (set data type|type) .*(,|;).*'

    @property
    def error_info(self) -> str:
        return 'You cannot alter type of column, ' \
               'It is a blocking operation because it will need check all items of column are valid. ' \
               'in some case it can be safe, but this functionality is not support at this moment. ' \
               'You should create a new column and copy the data to it.'


class AlterColumnAddConstraintSQLRule(AbstractSQLRule):
    @property
    def pattern(self) -> str:
        return r'alter table .* add constraint ((".*").)*((?!not valid( |;))(?!using index ).)*;'

    @property
    def error_info(self) -> str:
        return 'You cannot add constraint without using a index or adding it with not valid, ' \
               'It is a blocking operation because it will need check all items to validate the constraint.'


class AlterColumnAddPrimaryKeySQLRule(AbstractSQLRule):
    @property
    def pattern(self) -> str:
        return r'alter table .* add primary key .*;'

    @property
    def error_info(self) -> str:
        return 'You cannot add primary key, ' \
               'It is a blocking operation because it will need create a unique index and validate it.' \
               'You should be create a unique index (concurrently) and then add constraint using index'


class CreateIndexSQLRule(AbstractSQLRule):
    @property
    def pattern(self) -> str:
        return r'create (unique )*index((?! concurrently ).)* on .*;'

    @property
    def error_info(self) -> str:
        return 'You cannot create a index without concurrently. It is a blocking operation.'
