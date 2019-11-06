from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('dn')
    password = PasswordField('Password*', validators=[DataRequired()])
    server_address = StringField('LDAP server address')
    port = StringField('LDAP server port')
    use_ssl = BooleanField('Use SSL')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Connect')


class IndexForm(FlaskForm):
    directory = SubmitField('Search')
    schema = SubmitField('Schema')
    add = SubmitField('Add entry')
    remove = SubmitField('Delete entry')
    modify = SubmitField('Modify entry')
    exit = SubmitField('Close connection')
    forget = SubmitField('Clear password and close')


class DirectoryForm(FlaskForm):
    search_path = StringField('Search path')
    search_filter = StringField('Search filter (objectclass)')
    search_attributes = StringField('Attributes*')
    search_start = SubmitField('Search')
    search_cancel = SubmitField('Cancel')


class AddForm(FlaskForm):
    path = StringField('Path to new entry', validators=[DataRequired()])
    sn = StringField('sn', validators=[DataRequired()])
    cn = StringField('cn', validators=[DataRequired()])
    telephone_number = StringField('Telephone Number')
    description = StringField('Description')
    add_password = PasswordField('Password', validators=[DataRequired()])
    add = SubmitField('Add entry')
    cancel = SubmitField('Cancel')


class ModifyForm(FlaskForm):
    mod_cn = StringField('cn of the entry to be modified', validators=[DataRequired()])
    mod_path = StringField('Entry path', validators=[DataRequired()])
    mod_sn = StringField('sn (leave empty if not to be modified)')
    mod_telephone_number = StringField('Telephone Number (leave empty if not to be modified)')
    mod_description = StringField('Description (leave empty if not to be modified)')
    mod_oldpass = PasswordField('Old password of this entry if you want to change it')
    mod_newpass = PasswordField('New password')
    mod_add = SubmitField('Add entry')
    mod_cancel = SubmitField('Cancel')


class DeleteForm(FlaskForm):
    del_cn = StringField('cn of the entry to be removed', validators=[DataRequired()])
    del_path = StringField('path of the entry to be removed', validators=[DataRequired()])
    del_confirm = SubmitField('Delete')
    del_cancel = SubmitField('Cancel')


class SchemaForm(FlaskForm):
    schema_objclass = StringField('Filter by objectclass. Leave empty for default')
    schema_get = SubmitField('Get schema')
    schema_back = SubmitField('Back')


class ResultsForm(FlaskForm):
    results_back_index = SubmitField('Return to index')
    results_back_search = SubmitField('New search/modification')


class ErrorForm(FlaskForm):
    return_index = SubmitField('Return to index')


class LoginErrorForm(FlaskForm):
    return_login = SubmitField('Return')


class SuccessForm(FlaskForm):
    return_index_add = SubmitField('Return to index')
    return_add = SubmitField('Add/modify one more entry')