from flask import Flask, g, request, session, redirect, url_for, render_template, flash
from forms import *
from ldap_helper import *
import db_works
import security


app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

username_t = ''
pwd_t = ''
server_address_t = ''
server_port_t = ''
use_ssl_t = ''
logged_with_password = 0
credentials = []
cn = ''


@app.route("/", methods=["GET", "POST"])
def sign_up():
    form = LoginForm()
    global logged_with_password #Flag which determines where we will get credentials from
    global credentials
    credentials = []
    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        server_address = form.server_address.data
        server_port = form.port.data
        use_ssl = form.use_ssl.data
        remember_me = form.remember_me.data
        print(username, pwd, server_address,server_port,use_ssl)
        print("data from DB: ", db_works.get())
        if len(username) == 0 or len(server_address) == 0 or len(server_port) == 0:
            data = db_works.get()
            encrypted_pwd = security.encrypt(form.password.data)
            print("encrypted password: ", encrypted_pwd)
            if db_works.match_pass(encrypted_pwd)[0][0] == "error":
                return redirect('/connection_error')
            print("received pwd hash: ", db_works.match_pass(encrypted_pwd)[0])
            print("type of received pwd hash: ", type(db_works.match_pass(encrypted_pwd)[0][0]))
            if encrypted_pwd == db_works.match_pass(encrypted_pwd)[0][0]:
                print("Passwords matching")
                params = db_works.get()
                if params[0][0] == 0:
                    return redirect('/connection_error')
                print("params: ", params)
                print("type of params: ", type(params))
                server_address = params[0][3]
                print(server_address)
                username = params[0][1]
                print("username: ", username)
                server_port = params[0][4]
                if params[0][5] == 1:
                    use_ssl = True
                else:
                    use_ssl = False
                logged_with_password = 1
            else:
                return redirect('/connection_error')
        if ldap3_connection(server_address, username, pwd, server_port, use_ssl):
            conn = ldap3_connection(server_address, username, pwd, server_port, use_ssl)
            print("CONN = ", conn)
            print(conn)
            try:
                res = conn
                if res == 'fail':
                    return redirect('/connection_error')
            except:
                pass
            # if 'no socket' in conn.socket:
            #     return redirect('/connection_error')
            # if not conn.bind():
            #     print('error in bind', conn.result)
            #     print("HOUSTON HELLO")
            print("ldap3 connected")
            db_works.table_create()
            if form.remember_me.data:
                ssl_val = 0
                if form.use_ssl.data:
                    ssl_val = 1
                else:
                    ssl_val = 0
                pwd_e = security.encrypt(pwd)
                print("encrypted password: ", pwd_e)
                db_works.add(username, pwd_e, server_address, server_port, ssl_val)
            else:
                if logged_with_password == 0:
                    db_works.clear()
                username_t = username
                pwd_t = pwd
                server_address_t = server_address
                server_port_t = server_port
                use_ssl_t = use_ssl

            credentials = [server_address, username, pwd, server_port, use_ssl]
            print("credentials : ", credentials)
            return redirect('/index')
        else:
            return redirect('/connection_error')
    return render_template('login.html', title='Connect to server', form=form)


@app.route("/connection_error", methods=["GET", "POST"])
def connection_error():
    form = LoginErrorForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('error_login.html', title='Connection error', form=form)


@app.route("/index", methods=["GET", "POST"])
def index():
    form = IndexForm()
    if form.validate_on_submit():
        if form.add.data:
            return redirect('/add_entry')
        if form.directory.data:
            return redirect('/directory')
        if form.forget.data:
            db_works.clear()
            return redirect('/')
        if form.modify.data:
            return redirect('/mod')
        if form.remove.data:
            return redirect('/del')
        if form.exit.data:
            return redirect('/')
        if form.forget.data:
            db_works.clear()
            return redirect('/')
        if form.schema.data:
            return redirect('/schema')
    return render_template('index.html', server_val=credentials[0], title='Connected server', form=form)


@app.route("/add_entry", methods=["GET", "POST"])
def add_entry():
    form = AddForm()
    print("credential from add entry :", credentials)
    if form.validate_on_submit():
        if form.add.data:
            path = form.path.data
            sn = form.sn.data
            global cn
            cn = form.cn.data
            telephone_number = form.telephone_number.data
            description = form.description.data
            user_dn = "cn=" + cn + "," + path
            pwd = form.add_password.data
            pwd_hashed = security.encrypt(pwd)
            print("PATH : ", path)
            print("SN : ", sn)
            print("USER DN : ", user_dn)
            add(user_dn, sn, telephone_number, description, cn, credentials, pwd_hashed)
            form_s = SuccessForm()
            if form_s.return_index_add.data:
                return redirect('/index')
            if form_s.return_add.data:
                return redirect('/add_entry')
            return render_template('success_var.html', p1='Successfully added', p2=str(cn), title='Success', form=form_s)
        if form.cancel.data:
            return redirect('/index')
    return render_template('add_entry.html', title='Connected server', form=form)


@app.route('/directory', methods=["GET", "POST"])
def directory():
    form = DirectoryForm()
    if form.validate_on_submit():
        if form.search_start.data:
            atb_s = form.search_attributes.data
            atb_list = atb_s.replace(" ", "").split(",")
            obj_class = form.search_filter.data
            results_s = display(credentials[0], credentials[1], credentials[2], atb_list, obj_class)
            form = ResultsForm()
            return render_template('directory_results.html', len = len(results_s), results=results_s, title='Directory results', form=form)
        elif form.search_cancel.data:
            return redirect('/index')

    return render_template('directory.html', title='Directory', form=form)


@app.route('/mod', methods=["GET", "POST"])
def modify():
    form = ModifyForm()
    print("Modify started")
    if form.validate_on_submit():
        if form.mod_add.data:
            old_pass = form.mod_oldpass.data
            new_pass = form.mod_newpass.data
            path = form.mod_path.data
            sn = form.mod_sn.data
            global cn
            cn = form.mod_cn.data
            telephone_number = form.mod_telephone_number.data
            description = form.mod_description.data
            user_dn = "cn=" + cn + "," + path
            mod(user_dn, sn, telephone_number, description, cn, credentials, old_pass, new_pass)
            form = SuccessForm()
            if form.return_add.data:
                return redirect('/mod')
            return render_template('success_var.html', p1='Successfully modified', p2=str(cn), title='Success', form=form)
        if form.mod_cancel.data:
            return redirect('/index')
    return render_template('modification.html', p1='Success', p2=str(cn), title='Success', form=form)


@app.route('/del', methods=["GET", "POST"])
def delete():
    form = DeleteForm()
    if form.validate_on_submit():
        if form.del_confirm.data:
            cn = form.del_cn.data
            path = form.del_path.data
            c_p = "cn=" + cn + "," + path
            delete_entry(c_p)
            form = SuccessForm()
            if form.return_add.data:
                return redirect('/del')
            return render_template('success_var.html', p1='Successfully deleted', p2=str(cn), title='Success', form=form)
        if form.del_cancel.data:
            return redirect('/index')
    return render_template('del.html', title='Delete', form=form)


@app.route('/schema', methods=["GET", "POST"])
def schema():
    form = SchemaForm()
    if form.validate_on_submit():
        if form.schema_get.data:
            schema_filter = form.schema_objclass.data
            schema_res = get_schema(schema_filter)
            return render_template('schema.html', param=schema_res, title='Schema', form=form)
        if form.schema_back:
            return redirect('/index')
    return render_template('schema.html', title='Schema', form=form)
