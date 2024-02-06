#!/usr/bin/python
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, json

from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import uuid

app = Flask(__name__)


app.secret_key = '42311dfstwer234huy456efwr234t2345gdft42345235'


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mobile_cabinet_db'


mysql = MySQL(app)


@app.route('/')
# def main():
#     return render_template('index .html')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	_login = 0
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password))
		account = cursor.fetchone()
		if account:
      
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			# flash('Logged in successfully2')
   			
			# msg = 'Logged in successfully !'
			_login = 0
			# return render_template('index.html', msg = msg, _login=_login)
			cursor.execute('INSERT INTO update_history SET user_update =% s, information =%s', (username,"Login"))
			mysql.connection.commit()
			return render_template('dashboard.html')
		else:
			_login = 1
			msg = 'Incorrect username / password !'
			# flash('Incorrect username / password !2')
	return render_template('login.html', msg = msg, _login=_login)

@app.route('/logout')
def logout():
    username = session['username']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO update_history SET user_update =% s, information =%s', (username,"Logout"))
    mysql.connection.commit()
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('nm_dokumen', None)
    return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'user' in request.form and 'pass' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form and 'pin' in request.form:
		username = request.form['user']
		password = request.form['pass']
		email = request.form['email']
		organisation = request.form['organisation']
		address = request.form['address']
		city = request.form['city']
		state = request.form['state']
		country = request.form['country']
		postalcode = request.form['postalcode']
		pin = request.form['pin']
		
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Data sudah ada Gunakan Username yang lain'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Alamat email harus sesuai format, contoh@web/com'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Nama hanya boleh mengandung karater huruf dan angka'
		else:
			cursor.execute('INSERT INTO update_history SET user_update =% s, information =%s', (username,"Register Account"))
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s, %s)', (username, password, email, organisation, address, city, state, country, postalcode, pin, ))
			mysql.connection.commit()
			msg = 'Data pengguna berhasil ditambahkan'
	elif request.method == 'POST':
		msg = 'Input data tidak boleh kosong'
	return render_template('register.html', msg = msg)

@app.route("/dashboard")
def dashboard():
	if 'loggedin' in session:
		return render_template("dashboard.html")
	return redirect(url_for('login'))

@app.route("/dashboard_menu")
def dashboard_menu():
	if 'loggedin' in session:
		return render_template("index_coba.html")
	return redirect(url_for('login'))


@app.route("/index")
def index():
	if 'loggedin' in session:
		return render_template("search.html")
	return redirect(url_for('login'))


@app.route("/display")
def display():
	if 'loggedin' in session:
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE id = % s', (session['id'], ))
		account = cursor.fetchone()
		return render_template("display.html", account = account)
	return redirect(url_for('login'))

@app.route("/document_option")
def document_option():
	if 'loggedin' in session:
		tombol = request.args.get('tombol')
		id_user = session['username']
		id_dokumen = session.get('id_dokumen', None)
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM list_dokumen WHERE id_dokumen = % s', (id_dokumen, ))
		list_dokumen = cursor.fetchone()
		if tombol == 'tombol1':
			cursor.execute('SELECT * FROM list_dokumen WHERE id_dokumen = % s', (id_dokumen, ))
			if (cursor.fetchone()['status_option'] == int(0)) :
				cursor.execute('INSERT INTO search_history SET user_name=% s, search_keyword =% s, information =%s', ( id_user , list_dokumen['nama_dokumen'], "Take"))
				cursor.execute('UPDATE list_dokumen SET status_option =% s WHERE id_dokumen= %s', (1, list_dokumen['id_dokumen']))
				mysql.connection.commit()
				return redirect(url_for('buka'))
			else:
				msg = '*Dokumen sudah di ambil silahkan melakukan pengembalian terlebih dahulu'
				return render_template("document_option.html", list_dokumen = list_dokumen,msg = msg )
		elif tombol == 'tombol2':
			cursor.execute('SELECT * FROM list_dokumen WHERE id_dokumen = % s', (id_dokumen, ))
			if (cursor.fetchone()['status_option'] == int(1)):
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('INSERT INTO search_history SET user_name=% s, search_keyword =% s, information =%s', ( id_user , list_dokumen['nama_dokumen'], "Restore"))
				cursor.execute('UPDATE list_dokumen SET status_option =% s WHERE id_dokumen= %s', (0, list_dokumen['id_dokumen']))
				mysql.connection.commit()
				return redirect(url_for('buka'))
			else:
				msg = '*Dokumen sudah di kembalikan silahkan melakukan pengembilan'
				return render_template("document_option.html", list_dokumen = list_dokumen,msg = msg )
		return render_template("document_option.html", list_dokumen = list_dokumen )
	return redirect(url_for('login'))


@app.route("/buka",  methods =['GET', 'POST'])
def buka():
	if 'loggedin' in session:
		id_dokumen = session.get('id_dokumen', None)
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM list_dokumen WHERE id_dokumen = % s', (id_dokumen, ))
		list_dokumen = cursor.fetchone()
		if request.method == 'POST' and 'pin_pintu' in request.form:
			pin_pintu = request.form['pin_pintu']
			id_user = session['id']
			cursor.execute('SELECT PIN FROM accounts WHERE id = % s', (id_user, ))
			if (cursor.fetchone()['PIN'] == int(pin_pintu)):
				id = uuid.uuid1().hex
				id = id[0:10]
				session['id_trans'] = id
				if (list_dokumen['status_option'] == int(0)) and (list_dokumen['status_document'] == int(1)) :
					cursor.execute('UPDATE list_dokumen SET status_document =% s WHERE id_dokumen= %s', (0, list_dokumen['id_dokumen']))
					mysql.connection.commit()
				elif (list_dokumen['status_option'] == int(1)) and (list_dokumen['status_document'] == int(1)) :
					cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
					cursor.execute('UPDATE list_dokumen SET status_document =% s WHERE id_dokumen= %s', (0, list_dokumen['id_dokumen']))
					mysql.connection.commit()
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('INSERT INTO data_trans SET id_dokumen =% s, id_user=% s', (id_dokumen, id_user))
				cursor.execute('UPDATE door_locks SET status_pintu=% s WHERE device_ke= %s AND rak_ke= %s', (1, list_dokumen['device_ke'], list_dokumen['rak_ke']))
				cursor.execute('UPDATE list_dokumen SET status_document=% s WHERE id_dokumen= %s', (1, list_dokumen['id_dokumen']))
				mysql.connection.commit()
				return redirect(url_for('tutup'))
			else :
				msg = '*Pin yang anda masukkan salah'
				return render_template("buka.html", msg = msg, list_dokumen = list_dokumen)
		return render_template("buka.html", list_dokumen = list_dokumen)
	return redirect(url_for('login'))

@app.route("/tutup", methods = ['GET', 'POST'])
def tutup():
	if 'loggedin' in session:
		id_dokumen = session.get('id_dokumen', None)
		
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM list_dokumen WHERE id_dokumen = % s', (id_dokumen, ))
		list_dokumen = cursor.fetchone()
		if request.method == 'POST':
			cursor.execute("SELECT id_transaksi FROM data_trans order by id_transaksi desc LIMIT 1")
			data1 = cursor.fetchone()
			cursor.execute('UPDATE data_trans SET status_dev1 =% s, status_dev2=% s, status_dev3 =% s WHERE id_transaksi=%s' , (1,1,1, data1['id_transaksi']))
			cursor.execute('UPDATE door_locks SET status_pintu=% s WHERE device_ke= %s AND rak_ke= %s', (0, list_dokumen['device_ke'], list_dokumen['rak_ke']))
			cursor.execute('UPDATE list_dokumen SET status_document=% s WHERE id_dokumen= %s', (0, list_dokumen['id_dokumen']))
			mysql.connection.commit()
			session.pop('id_dokumen', None)
			session.pop('id_trans', None)
			return redirect(url_for('search'))
		return render_template("tutup.html", list_dokumen = list_dokumen, msg = "Silahkan tunggu cabinet melakukan permintaan")
	return redirect(url_for('login'))

@app.route("/update", methods =['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organisation' in request.form and 'pin' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            organisation = request.form['organisation']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            country = request.form['country']
            postalcode = request.form['postalcode']
            pin = request.form['pin']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO update_history SET user_update =% s, information =%s', (username,"Update Account"))
            cursor.execute('UPDATE accounts SET username =% s, password =% s, email =% s, organisation =% s, address =% s, city =% s, state =% s, country =% s, postalcode =% s, pin =% s WHERE id =% s', (username, password, email, organisation, address, city, state, country, postalcode, pin, (session['id'], ), ))
            mysql.connection.commit()
            flash('Data berhasil di perbaharui !')   
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = % s', (session['id'], ))
        account = cursor.fetchone()
        return render_template("update.html", account = account)
            
    return redirect(url_for('login'))



@app.route("/search_user", methods =['GET', 'POST'])
def search_user():
    status_update = 0;
    if 'loggedin' in session:
        if request.method == 'POST' and 'username' in request.form:
            username = request.form['username']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
            account = cursor.fetchone()
            print(account)
            if account:
                print(account)
                return render_template("update.html", account = account)
            flash('Data tidak ditemukan')
            return render_template("search_user.html")
        msg = "Data tidak boleh kosong"    
        return render_template("search_user.html", msg = msg)
    return redirect(url_for('login'))

@app.route("/search", methods =['GET', 'POST'])
def search():
	msg_search = ''
	
	if 'loggedin' in session:
		if request.method == 'POST' and 'nama_dokumen' in request.form:
			id_user = session['username']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT PIN FROM accounts WHERE username = % s', (id_user, ))
			try:
				nama_dokumen = request.form['nama_dokumen']
				cursor.execute('SELECT id_dokumen FROM list_dokumen WHERE nama_dokumen = % s', (nama_dokumen, ))
				id_dokumen = cursor.fetchone()['id_dokumen']
				session['id_dokumen'] = id_dokumen
				cursor.execute('SELECT * FROM list_dokumen WHERE id_dokumen = % s', (id_dokumen, ))
				list_dokumen = cursor.fetchone()
				if (list_dokumen['status_option'] == int(0)) and (list_dokumen['status_document'] == int(1)) :
					cursor.execute('UPDATE list_dokumen SET status_option =% s WHERE id_dokumen= %s', (1, list_dokumen['id_dokumen']))
					mysql.connection.commit()
				elif (list_dokumen['status_option'] == int(1)) and (list_dokumen['status_document'] == int(1)) :
					cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
					cursor.execute('UPDATE list_dokumen SET status_option =% s WHERE id_dokumen= %s', (0, list_dokumen['id_dokumen']))
					mysql.connection.commit()
				cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
				cursor.execute('INSERT INTO search_history SET user_name=% s, search_keyword =% s, information =%s', ( id_user , nama_dokumen, "Search"))
				mysql.connection.commit()
				return redirect(url_for('document_option'))
			except:
				session['nm_dokumen'] = request.form['nama_dokumen']
				session['msg_search'] = "*Dokumen yang Anda Cari Tidak Ada, Silahkan Tambahkan Data Terlebih Dahulu"
				
				return redirect(url_for('store'))
		return render_template("search.html", msg_search = msg_search)
	return redirect(url_for('login'))

@app.route("/store", methods =['GET', 'POST'])
def store():

	msg_search = ''
	if 'loggedin' in session:
		msg_search = session.get('msg_search', None)
		
		if (msg_search == None):
			msg_search = ''
		session.pop('msg_search', None)
  
		
		if request.method == 'POST' and 'nama_dokumen' in request.form and 'device_ke' in request.form and 'rak_ke' in request.form and 'baris_ke' in request.form and 'kolom_ke' in request.form:
			session.pop('nm_dokumen', None)
			nama_dokumen = request.form['nama_dokumen']
			device_ke = request.form['device_ke']
			rak_ke = request.form['rak_ke']
			baris_ke = request.form['baris_ke']
			kolom_ke = request.form['kolom_ke']
			id_user = session['username']
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT PIN FROM accounts WHERE username = % s', (id_user, ))
			id = uuid.uuid1().hex
			print ()
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute('SELECT * FROM list_dokumen WHERE nama_dokumen = % s', (nama_dokumen, ))
			account = cursor.fetchone()
			if account:
				msg_search = 'Dokumen gagal disimpan, Nama Dokumen sudah ada, silahkan input dengan nama yang lain'
				msg_type = 0
				print (msg_search)
				return render_template("store.html", msg_search = msg_search, msg_type=msg_type)
				
			elif not re.match(r'[A-Za-z0-9]+', nama_dokumen):
				msg_search = 'Nama dokumen hanya boleh terdiri dari huruf and angka !'
				msg_type = 0
				print (msg_search)
				return render_template("store.html", msg_search = msg_search, msg_type=msg_type)
			else :
				x = cursor.execute('INSERT INTO list_dokumen VALUES (% s, % s, % s, % s, % s, % s, %s, %s)', (id[:9], nama_dokumen, device_ke, rak_ke, baris_ke, kolom_ke,1,0 ))
				##cursor.execute('INSERT INTO store_history SET user_store=% s, store_keyword =% s', ( id_user , nama_dokumen ))##
				cursor.execute('INSERT INTO search_history SET user_name=% s, search_keyword =% s, information = %s', ( id_user , nama_dokumen,"Store"))
				mysql.connection.commit()
				print (x)
				
				if x:
					msg_search = 'Dokumen Berhasil ditambahkan !'
					msg_type = 1
					print (msg_search)
					return render_template("search.html", msg_search = msg_search, msg_type=msg_type)
				else :
					msg_search = 'Penambahan data dokumen gagal'
					msg_type = 0
					print (msg_search)
					return render_template("store.html", msg_search = msg_search, msg_type=msg_type)
		elif request.method == 'POST':
			msg_search = 'Data tidak boleh kosong  !'
			msg_type = 0
			print (msg_search)
			return render_template("store.html", msg_search = msg_search, msg_type=msg_type)
		
		print (msg_search)
		msg_type = 0
		return render_template("store.html", msg_search = msg_search, msg_type=msg_type)

@app.route("/read_dev1")
def read_dev1():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "SELECT id_transaksi, id_dokumen, status_dev1 FROM data_trans order by id_transaksi desc LIMIT 1")
    data1 = cursor.fetchone()

    cursor.execute(
        'SELECT device_ke, rak_ke, baris_ke, kolom_ke FROM list_dokumen WHERE id_dokumen = % s', (data1['id_dokumen'], ))
    data2 = cursor.fetchone()
    cursor.execute('SELECT status_pintu FROM door_locks WHERE device_ke = % s AND rak_ke = %s',
                   (data2['device_ke'], data2['rak_ke'], ))
    data3 = cursor.fetchone()

    data_kirim = "*" + str(data1['status_dev1']) + "," + str(data2['device_ke']) + "," + str(data2['rak_ke']) + "," + str(data2['baris_ke']) + "," + str(data2['kolom_ke']) + "," + str(data3['status_pintu']) + "#"

    return data_kirim


@app.route("/read_dev2")
def read_dev2():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "SELECT id_transaksi, id_dokumen, status_dev2 FROM data_trans order by id_transaksi desc LIMIT 1")
    data1 = cursor.fetchone()

    cursor.execute(
        'SELECT device_ke, rak_ke, baris_ke, kolom_ke FROM list_dokumen WHERE id_dokumen = % s', (data1['id_dokumen'], ))
    data2 = cursor.fetchone()
    cursor.execute('SELECT status_pintu FROM door_locks WHERE device_ke = % s AND rak_ke = %s',
                   (data2['device_ke'], data2['rak_ke'], ))
    data3 = cursor.fetchone()
    
    data_kirim = "*" + str(data1['status_dev2']) + "," + str(data2['device_ke']) + "," + str(data2['rak_ke']) + "," + str(data2['baris_ke']) + "," + str(data2['kolom_ke']) + "," + str(data3['status_pintu']) + "#"
    return data_kirim


@app.route("/read_dev3")
def read_dev3():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "SELECT id_transaksi, id_dokumen, status_dev3 FROM data_trans order by id_transaksi desc LIMIT 1")
    data1 = cursor.fetchone()

    cursor.execute(
        'SELECT device_ke, rak_ke, baris_ke, kolom_ke FROM list_dokumen WHERE id_dokumen = % s', (data1['id_dokumen'], ))
    data2 = cursor.fetchone()
    cursor.execute('SELECT status_pintu FROM door_locks WHERE device_ke = % s AND rak_ke = %s',
                   (data2['device_ke'], data2['rak_ke'], ))
    data3 = cursor.fetchone()
    
    data_kirim = "*" + str(data1['status_dev3']) + "," + str(data2['device_ke']) + "," + str(data2['rak_ke']) + "," + str(data2['baris_ke']) + "," + str(data2['kolom_ke']) + "," + str(data3['status_pintu']) + "#"
    return data_kirim


@app.route("/history")
def history():
	if 'loggedin' in session:
		# cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		# cursor.execute('SELECT * FROM data_trans ORDER BY waktu_trans DESC')
		# history_data = cursor.fetchall()
		# cursor.execute('SELECT * FROM search_history ORDER BY search_time DESC')
		# search_history = cursor.fetchall()
		# return render_template("history.html", history_data = history_data, search_history = search_history  )
		return render_template("history.html")
	return redirect(url_for('login'))

@app.route("/search_history")
def search_history():
	if 'loggedin' in session:
		# cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		# cursor.execute('SELECT * FROM search_history ORDER BY search_time DESC')
		# search_history = cursor.fetchall()
		return render_template("search_history.html")
	return redirect(url_for('login'))

@app.route("/store_history")
def store_history():
	if 'loggedin' in session:
		# cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		# cursor.execute('SELECT * FROM store_history ORDER BY store_time DESC')
		# store_history = cursor.fetchall()
		# return render_template("store_history.html", store_history = store_history  )
		return render_template("store_history.html")	
	return redirect(url_for('login'))

@app.route("/update_history")
def update_history():
	if 'loggedin' in session:
		# cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		# cursor.execute('SELECT * FROM update_history ORDER BY update_time DESC')
		# update_history = cursor.fetchall()
		# return render_template("update_history.html", update_history = update_history  )
		return render_template("update_history.html")
	return redirect(url_for('login'))

@app.route("/register_history")
def register_history():
	if 'loggedin' in session:
		# cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		# cursor.execute('SELECT * FROM register_history ORDER BY register_time DESC')
		# register_history = cursor.fetchall()
		# return render_template("register_history.html", register_history = register_history  )
		return render_template("register_history.html")
	return redirect(url_for('login'))


@app.route("/ajaxfile",methods=["POST","GET"])
def ajaxfile():
    try:
        # conn = mysql.connect()
        # cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            draw = request.form['draw'] 
            row = int(request.form['start'])
            rowperpage = int(request.form['length'])
            searchValue = request.form["search[value]"]
            print(draw)
            print(row)
            print(rowperpage)
            print(searchValue)
            # cursor.execute('SELECT * FROM data_trans ORDER BY waktu_trans DESC')
            # history_data = cursor.fetchall()

            
            ## Total number of records without filtering
            cursor.execute("select count(*) as allcount from data_trans")
            rsallcount = cursor.fetchone()
            totalRecords = rsallcount['allcount']
            print(totalRecords) 
 
            ## Total number of records with filtering
            likeString = "%" + searchValue +"%"
            cursor.execute("SELECT count(*) as allcount from data_trans WHERE id_transaksi LIKE %s OR waktu_trans LIKE %s OR id_user LIKE %s OR id_dokumen LIKE %s", (likeString, likeString, likeString, likeString))
            rsallcount = cursor.fetchone()
            totalRecordwithFilter = rsallcount['allcount']
            print(totalRecordwithFilter) 
 
            ## Fetch records
            if searchValue=='':
                cursor.execute("SELECT * FROM data_trans ORDER BY waktu_trans asc limit %s, %s;", (row, rowperpage))
                data_translist = cursor.fetchall()
            else:        
                cursor.execute("SELECT * FROM data_trans WHERE id_transaksi LIKE %s OR waktu_trans LIKE %s OR id_user LIKE %s limit %s, %s;", (likeString, likeString, likeString, row, rowperpage))
                data_translist = cursor.fetchall()
 
            data = []
            for row in data_translist:
                data.append({
                    'id_transaksi': row['id_transaksi'],
                    'waktu_trans': row['waktu_trans'],
                    'id_user': row['id_user'],
                    'id_dokumen': row['id_dokumen'],
                })
 
            response = {
                'draw': draw,
                'iTotalRecords': totalRecords,
                'iTotalDisplayRecords': totalRecordwithFilter,
                'aaData': data,
            }
            return jsonify(response)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        # conn.close()
        
        
@app.route("/ajaxfile_regHistory",methods=["POST","GET"])
def ajaxfile_regHistory():
    try:

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            draw = request.form['draw'] 
            row = int(request.form['start'])
            rowperpage = int(request.form['length'])
            searchValue = request.form["search[value]"]
            print(draw)
            print(row)
            print(rowperpage)
            print(searchValue)
            
            ## Total number of records without filtering
            cursor.execute("select count(*) as allcount from register_history")
            rsallcount = cursor.fetchone()
            totalRecords = rsallcount['allcount']
            print(totalRecords) 
 
            ## Total number of records with filtering
            likeString = "%" + searchValue +"%"
            cursor.execute("SELECT count(*) as allcount from register_history WHERE register_time LIKE %s OR user_register LIKE %s", (likeString, likeString))
            rsallcount = cursor.fetchone()
            totalRecordwithFilter = rsallcount['allcount']
            print(totalRecordwithFilter) 
 
            ## Fetch records
            if searchValue=='':
                cursor.execute("SELECT * FROM register_history ORDER BY register_time asc limit %s, %s;", (row, rowperpage))
                data_reg_history_list = cursor.fetchall()
            else:        
                cursor.execute("SELECT * FROM register_history WHERE register_time LIKE %s OR register_time LIKE %s limit %s, %s;", (likeString, likeString, row, rowperpage))
                data_reg_history_list = cursor.fetchall()
 
            data = []
            for row in data_reg_history_list:
                data.append({
                    'register_time': row['register_time'],
                    'user_register': row['user_register'],

                })
 
            response = {
                'draw': draw,
                'iTotalRecords': totalRecords,
                'iTotalDisplayRecords': totalRecordwithFilter,
                'aaData': data,
            }
            return jsonify(response)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
                
        
@app.route("/ajaxfile_searchHistory",methods=["POST","GET"])
def ajaxfile_searchHistory():
    try:

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            draw = request.form['draw'] 
            row = int(request.form['start'])
            rowperpage = int(request.form['length'])
            searchValue = request.form["search[value]"]
            print(draw)
            print(row)
            print(rowperpage)
            print(searchValue)
            
            ## Total number of records without filtering
            cursor.execute("select count(*) as allcount from search_history")
            rsallcount = cursor.fetchone()
            totalRecords = rsallcount['allcount']
            print(totalRecords) 
 
            ## Total number of records with filtering
            likeString = "%" + searchValue +"%"
            cursor.execute("SELECT count(*) as allcount from search_history WHERE search_time LIKE %s OR user_name LIKE %s OR search_keyword LIKE %s OR information LIKE %s", (likeString, likeString, likeString,likeString))
            rsallcount = cursor.fetchone()
            totalRecordwithFilter = rsallcount['allcount']
            print(totalRecordwithFilter) 
            

            ## Fetch records
            if searchValue=='':
                cursor.execute("SELECT * FROM search_history ORDER BY search_time asc limit %s, %s;", (row, rowperpage))
                data_search_history_list = cursor.fetchall()
            else:        
                cursor.execute("SELECT * FROM search_history WHERE search_time LIKE %s OR user_name LIKE %s OR search_keyword LIKE %s OR information LIKE %s limit %s, %s;", (likeString, likeString, likeString, likeString, row, rowperpage))
                data_search_history_list = cursor.fetchall()
 
            data = []
            for row in data_search_history_list:
                data.append({
                    'search_time': row['search_time'],
                    'user_name': row['user_name'],
                    'search_keyword': row['search_keyword'],
                    'information' : row ['information']

                })
 
            response = {
                'draw': draw,
                'iTotalRecords': totalRecords,
                'iTotalDisplayRecords': totalRecordwithFilter,
                'aaData': data,
            }
            return jsonify(response)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        

@app.route("/ajaxfile_storeHistory",methods=["POST","GET"])
def ajaxfile_storeHistory():
    try:

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            draw = request.form['draw'] 
            row = int(request.form['start'])
            rowperpage = int(request.form['length'])
            searchValue = request.form["search[value]"]
            print(draw)
            print(row)
            print(rowperpage)
            print(searchValue)
            
            ## Total number of records without filtering
            cursor.execute("select count(*) as allcount from store_history")
            rsallcount = cursor.fetchone()
            totalRecords = rsallcount['allcount']
            print(totalRecords) 
 
            ## Total number of records with filtering
            likeString = "%" + searchValue +"%"
            cursor.execute("SELECT count(*) as allcount from store_history WHERE store_time LIKE %s OR user_store LIKE %s OR store_keyword LIKE %s", (likeString, likeString, likeString))
            rsallcount = cursor.fetchone()
            totalRecordwithFilter = rsallcount['allcount']
            print(totalRecordwithFilter) 
 
            ## Fetch records
            if searchValue=='':
                cursor.execute("SELECT * FROM store_history ORDER BY store_time asc limit %s, %s;", (row, rowperpage))
                data_search_history_list = cursor.fetchall()
            else:        
                cursor.execute("SELECT * FROM store_history WHERE store_time LIKE %s OR user_store LIKE %s OR store_keyword LIKE %s limit %s, %s;", (likeString, likeString, likeString, row, rowperpage))
                data_search_history_list = cursor.fetchall()
 
            data = []
            for row in data_search_history_list:
                data.append({
                    'store_time': row['store_time'],
                    'user_store': row['user_store'],
                    'store_keyword': row['store_keyword']

                })
 
            response = {
                'draw': draw,
                'iTotalRecords': totalRecords,
                'iTotalDisplayRecords': totalRecordwithFilter,
                'aaData': data,
            }
            return jsonify(response)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        
        

@app.route("/ajaxfile_updateHistory",methods=["POST","GET"])
def ajaxfile_updateHistory():
    try:

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        if request.method == 'POST':
            draw = request.form['draw'] 
            row = int(request.form['start'])
            rowperpage = int(request.form['length'])
            searchValue = request.form["search[value]"]
            print(draw)
            print(row)
            print(rowperpage)
            print(searchValue)
            
            ## Total number of records without filtering
            cursor.execute("select count(*) as allcount from update_history")
            rsallcount = cursor.fetchone()
            totalRecords = rsallcount['allcount']
            print(totalRecords) 
 
            ## Total number of records with filtering
            likeString = "%" + searchValue +"%"
            cursor.execute("SELECT count(*) as allcount from update_history WHERE update_time LIKE %s OR user_update LIKE %s OR information LIKE %s", (likeString, likeString,likeString))
            rsallcount = cursor.fetchone()
            totalRecordwithFilter = rsallcount['allcount']
            print(totalRecordwithFilter) 
 
            ## Fetch records
            if searchValue=='':
                cursor.execute("SELECT * FROM update_history ORDER BY update_time asc limit %s, %s;", (row, rowperpage))
                data_update_history_list = cursor.fetchall()
            else:        
                cursor.execute("SELECT * FROM update_history WHERE update_time LIKE %s OR user_update LIKE %s OR information LIKE %s limit %s, %s;", (likeString, likeString, likeString, row, rowperpage))
                data_update_history_list = cursor.fetchall()
 
            data = []
            for row in data_update_history_list:
                data.append({
                    'update_time': row['update_time'],
                    'user_update': row['user_update'],
                    'information' : row['information']
                })
 
            response = {
                'draw': draw,
                'iTotalRecords': totalRecords,
                'iTotalDisplayRecords': totalRecordwithFilter,
                'aaData': data,
            }
            return jsonify(response)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 


if __name__ == "__main__":
	# app.run(host ="localhost", port = int("5000"))
	app.run(host ="0.0.0.0", debug = True, port = int("5000"))
