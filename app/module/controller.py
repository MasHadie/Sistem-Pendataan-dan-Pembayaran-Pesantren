from flask import render_template, request, redirect, flash, session,Markup, jsonify
import werkzeug.utils
import pandas as pd
from werkzeug import url_encode
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from app import app
from .models import db, engine, Users, Santri, Bendahara, Ajaran, Syariah, Pesantren
from forms import santri_F



@app.route('/', methods=['GET','POST'])
def index():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    if session.get('username'):
        santri = Santri.query.count()
        laki = Santri.query.filter_by(jenis_k="Laki-laki").count()
        cewe = Santri.query.filter_by(jenis_k="Perempuan").count()
        bayar = Syariah.query.all()
        bayarList= []
        for x in bayar:
            i = x.jml_bayar
            bayarList.insert(0,i)
        bayarList = sum(bayarList)
        if 10000 <= bayarList < 100000:
            bayarList =str(bayarList)[:2]+"K"
        elif 100000 <= bayarList < 1000000:
            bayarList = str(bayarList)[:3]+"K"
        elif bayarList >= 1000000:
            bayarList = bayarList/1000000
            bayarList = round(float(bayarList),2)
            bayarList = str(bayarList)+"M"
        else:
            bayarList = str(bayarList)
        cBayar = "Rp. " + bayarList
        # users = Users.query.with_entities(Users.nik, db.func.count()).all()
        print(cBayar)
        return render_template('dashboard.html',santri=santri,laki=laki,cewe=cewe, cBayar=cBayar, user=session['username'])
    # else:
    #     return render_template('eror.html')

@app.route('/tambah_santri', methods=['GET', 'POST'])
def tambah_santri():
    ajaran = Ajaran.query.all()
    form = santri_F()
    provinsi = pd.read_csv('app/data/wilayah/provinces.csv',encoding='utf-8', sep=';')
    provinsi = provinsi['name']
    
    if request.method == 'POST':
        nis = request.form['nis']
        nama_l = request.form['nama_l']
        jenis_k = request.form['jenis_k']
        tmpt_l = request.form['tmpt_l']
        tgl_l = request.form['tgl_l']
        alamat = request.form['alamat']
        th_ajar = request.form['th_ajar']
        ortu = request.form['ortu']
        no_hp = request.form['no_hp']
        status = request.form['status']
        th_masuk = request.form['th_masuk']
        try:
            addSantri = Santri(nis=nis,nama_l=nama_l,jenis_k=jenis_k,
            tmpt_l=tmpt_l,tgl_l=tgl_l,alamat=alamat,th_ajar=th_ajar,
            ortu=ortu,no_hp=no_hp,status=status,th_masuk=th_masuk)
            db.session.add(addSantri)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)
        # berhasil = Markup('<p class="alert alert-success" style="color:black">Data Berhasil Diinputkan</p>')
        # flash(berhasil)
    # listMhs = Mahasiswa.query.all()
    # print(listMhs)
    return render_template('santri/tambah_santri.html',ajaran=ajaran, form=form, provinsi=provinsi)

@app.route('/lihat_santri')
def lihat_santri():
    if session.get('username'):
        users = Santri.query.all()
        return render_template('santri/lihat_santri.html', users=users)
    else:
        return render_template('eror.html')

@app.route('/edit_santri/<int:id>')
def updateForm(id):
    santri = Santri.query.filter_by(id=id).first()
    return render_template("santri/edit_santri.html", data=santri)

@app.route('/edit_santri', methods=['POST'])
def update():
    if request.method == 'POST':
        id = request.form['id']
        nis = request.form['nis']
        nama_l = request.form['nama_l']
        jenis_k = request.form['jenis_k']
        tmpt_l = request.form['tmpt_l']
        tgl_l = request.form['tgl_l']
        alamat = request.form['alamat']
        th_ajar = request.form['th_ajar']
        ortu = request.form['ortu']
        no_hp = request.form['no_hp']
        status = request.form['status']
        th_masuk = request.form['th_masuk']
        try:
            santri = Santri.query.filter_by(id=id).first()
            santri.nis = nis
            santri.nama_l = nama_l
            santri.jenis_k = jenis_k
            santri.tmpt_l = tmpt_l
            santri.tgl_l =tgl_l
            santri.alamat = alamat
            santri.th_ajar = th_ajar
            santri.ortu = ortu
            santri.no_hp = no_hp
            santri.status = status
            santri.th_masuk = th_masuk
            db.session.commit()

        except Exception as e:
            print("Failed to update data")
            print(e)
        return redirect("/lihat_santri")
#
@app.route('/hapus_santri/<int:id>')
def hapus_santri(id):
    try:
        santri = Santri.query.filter_by(id=id).first()
        db.session.delete(santri)
        db.session.commit()

    except Exception as e:
        print("Failed delete mahasiswa")
        print(e)
    return redirect("/lihat_santri")


@app.route('/tambah_ajaran', methods=['GET', 'POST'])
def tambah_ajaran():
    if request.method == 'POST':
        # id = request.form['id']
        nama_ajar = request.form['nama_ajar']
        ket_ajar = request.form['ket_ajar']
        try:
            addAjaran = Ajaran(nama_ajar=nama_ajar, ket_ajar=ket_ajar)
            db.session.add(addAjaran)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)

    return render_template('ajaran/tambah_ajaran.html')

@app.route('/lihat_ajar')
def lihat_ajar():
    if session.get('username'):
        ajar = Ajaran.query.all()
        return render_template('ajaran/lihat_ajaran.html', ajar=ajar)
    else:
        return render_template('eror.html')

@app.route('/hapus_ajaran/<int:id>')
def hapus_ajaran(id):
    try:
        ajaran = Ajaran.query.filter_by(id=id).first()
        db.session.delete(ajaran)
        db.session.commit()

    except Exception as e:
        print("Failed delete mahasiswa")
        print(e)
    return redirect("/lihat_ajar")

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    nomor = request.form.get('nomor')
    print(nomor)
    # print(nomor)
    cari = Santri.query.filter_by(nis=nomor).first()
    print("nis :",cari.nis, "nama:", cari.nama_l)
    return redirect('/tambah_syariah')

@app.route('/tambah_syariah', methods=['GET', 'POST'])
def tambah_syariah():
    # santri =  Santri.query.all()
    # print(santri)
    nomor = request.form.get('nomor')
    santri = Santri.query.filter_by(nis=nomor).first()
    ajar = Ajaran.query.all()

    return render_template('syariah/tambah_syariah.html', santri=santri,ajar=ajar)

@app.route('/bayar', methods=['GET', 'POST'])
def bayar():
    if request.method == 'POST':
        nis = request.form['nis']
        nama_santri = request.form['nama_santri']
        bulan = request.form['bulan']
        tgl_bayar = request.form['tgl_bayar']
        thn_ajaran = request.form['thn_ajaran']
        jml_bayar = request.form['jml_bayar']
        try:
            addBayar = Syariah(nis=nis,nama_santri=nama_santri, bulan=bulan, tgl_bayar=tgl_bayar,
            thn_ajaran=thn_ajaran, jml_bayar=jml_bayar)
            db.session.add(addBayar)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)
    return redirect('/lihat_bayar')

@app.route('/lihat_bayar')
def lihat_bayar():
    if session.get('username'):
        syariah = Syariah.query.all()
        return render_template('syariah/lihat_bayar.html', syariah=syariah)
    else:
        return render_template('eror.html')

@app.route('/hapus_bayar/<int:id>')
def hapus_bayar(id):
    try:
        syariah = Syariah.query.filter_by(id=id).first()
        db.session.delete(syariah)
        db.session.commit()

    except Exception as e:
        print("Failed delete mahasiswa")
        print(e)
    return redirect("/lihat_bayar")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password = password.strip()
        hashed_pwd = generate_password_hash(password, 'sha256')
        try:
            adduser = Users(username=username,pass_hash=hashed_pwd)
            db.session.add(adduser)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)
    # listMhs = Mahasiswa.query.all()
    # print(listMhs)
    return render_template('register.html')

@app.route('/data_user')
def data_user():
    if session.get('username'):
        users = Users.query.all()
        return render_template('lihat_user.html', users=users)
    else:
        return render_template('eror.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not (username and password):
            kosong = Markup('<p class="alert alert-warning" style="color:black">Username atau Password tidak boleh kosong</p>')
            flash(kosong)
            return redirect('/login')
        else:
            username = username.strip()
            password = password.strip()
        user = Users.query.filter_by(username=username).first()
        if user and check_password_hash(user.pass_hash, password):
            session['username'] = username
            return redirect("/dashboard")
        else:
            invalid = Markup('<p class="alert alert-danger" style="color:black">Username atau password salah</>')
            flash(invalid)

    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect('/')
