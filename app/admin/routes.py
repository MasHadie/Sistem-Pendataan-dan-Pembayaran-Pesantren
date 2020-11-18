from flask import render_template, request, redirect, flash, session,Markup, jsonify, Blueprint, url_for
import werkzeug.utils
import pandas as pd
from werkzeug import url_encode
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from flask_login import login_user, current_user, logout_user, login_required
from app import app
from app.admin.forms import santri_F, admin_F, editadmin_F, loginadmin_F, editsantri_F, syariah_F
from app.models import Tusers, Tsantri, Tsyariah, Tajaran
from app import db, bcrypt

radmin = Blueprint('radmin', __name__)

@radmin.route('/', methods=['GET','POST'])
def index():
    form = loginadmin_F()
    return render_template("index.html", form=form)

@radmin.route('/dashboard')
@login_required
def dashboard():
    santri = Tsantri.query.count()
    laki = Tsantri.query.filter_by(jenis_k="Laki-Laki").count()
    cewe = Tsantri.query.filter_by(jenis_k="Perempuan").count()
    bayar = Tsyariah.query.all()
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
    return render_template('dashboard.html',santri=santri,laki=laki,cewe=cewe, cBayar=cBayar)


@radmin.route('/register',methods=['GET','POST'] )
def register():
    form = admin_F()
    if form.validate_on_submit():
        pass_hash = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        add_user = Tusers(username=form.username.data,email=form.email.data, password=pass_hash)
        db.session.add(add_user)
        db.session.commit()
        flash(f'Akun {form.username.data} berhasil terdaftar', 'success')
        return redirect(url_for('radmin.register'))
    return render_template('register.html',form=form)

@radmin.route('/edit_user',methods=['GET','POST'] )
def edit_user():
    form = editadmin_F()
    if form.validate_on_submit():
        pass_hash = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.password = pass_hash
        db.session.commit()
        flash('Data user berhasil diubah', 'success')
        return redirect(url_for('radmin.edit_user'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.password.data = current_user.password
    return render_template('edituser.html',form=form)

@radmin.route('/login',methods=['GET','POST'] )
def login():
    if current_user.is_authenticated:
        return redirect(url_for('radmin.index'))
    form = loginadmin_F()
    if form.validate_on_submit():
        cekemail=Tusers.query.filter_by(email=form.email.data).first()
        if cekemail and bcrypt.check_password_hash(cekemail.password, form.password.data):
            login_user(cekemail)
            print(cekemail)
            return redirect(url_for('radmin.dashboard'))
        else:
            flash('Login Gagal, pastikan email dan password benar', 'danger')
    return render_template('index.html',form=form)

@radmin.route('/logout',)
def logout():
    logout_user()
    return redirect(url_for('radmin.index'))

@radmin.route('/tambah_santri',methods=['GET','POST'] )
@login_required
def tambah_santri():
    form = santri_F()
    if form.validate_on_submit():
        add_santri = Tsantri(nis=form.nis.data, nama_l=form.nama_l.data, jenis_k=form.jenis_k.data, tmpt_l=form.tmpt_l.data,tgl_l=form.tgl_l.data,  alamat=form.alamat.data, th_ajar=form.th_ajar.data, ortu=form.ortu.data,no_hp=form.no_hp.data, status=form.status.data, th_masuk=form.th_masuk.data)
        db.session.add(add_santri)
        db.session.commit()
        flash(f'Santi dengan nama: "{form.nama_l.data}" berhasil ditambahkan!', 'success')
        return redirect(url_for('radmin.tambah_santri'))
    return render_template('santri/tambah_santri.html', form=form)

@radmin.route('/lihat_santri')
@login_required
def lihat_santri():
    santri = Tsantri.query.all()
    return render_template('santri/lihat_santri.html',santri=santri)

@radmin.route('/edit_santri/<int:id>')
@login_required
def updateForm(id):
    form = editsantri_F()
    santri = Tsantri.query.filter_by(id=id).first()
    print(santri)
    return render_template("santri/edit_santri.html", data=santri, form=form)

@radmin.route('/edit_santri', methods=['POST'])
@login_required
def edit_santri():
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
            santri = Tsantri.query.filter_by(id=id).first()
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

@radmin.route('/hapus_santri/<int:id>')
@login_required
def hapus_santri(id):
    try:
        santri = Tsantri.query.filter_by(id=id).first()
        db.session.delete(santri)
        db.session.commit()
        flash('Santri berhasil dihapus', 'success')
    except Exception as e:
        print("Failed delete mahasiswa")
        print(e)
    return redirect(url_for('radmin.lihat_santri'))

#BAYAR SYARIAH / SPP PESANTREN
@radmin.route('/tambah_syariah', methods=['GET', 'POST'])
@login_required
def tambah_syariah():
    nomor = request.form.get('nomor')
    santri = Tsantri.query.filter_by(nis=nomor).first()
    ajar = Tajaran.query.all()
    print(santri)
    return render_template('syariah/tambah_syariah.html', santri=santri, ajar=ajar)

@radmin.route('/bayar',methods=['GET','POST'] )
@login_required
def bayar():
    if request.method == 'POST':
        nis = request.form['nis']
        nama_santri = request.form['nama_santri']
        bulan = request.form['bulan']
        tgl_bayar = request.form['tgl_bayar']
        thn_ajaran = request.form['thn_ajaran']
        jml_bayar = request.form['jml_bayar']
        try:
            addBayar = Tsyariah(nis=nis,nama_santri=nama_santri, bulan=bulan, tgl_bayar=tgl_bayar,
            thn_ajaran=thn_ajaran, jml_bayar=jml_bayar)
            db.session.add(addBayar)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)
    return redirect('/lihat_bayar')


@radmin.route('/lihat_bayar')
@login_required
def lihat_bayar():
    syariah = Tsyariah.query.all()
    return render_template('syariah/lihat_bayar.html', syariah=syariah)

@radmin.route('/edit_syariah/<string:nis>')
@login_required
def bayarForm(nis):
    ajar = Tajaran.query.all()
    syariah = Tsyariah.query.filter_by(nis=nis).first()
    print(syariah)
    return render_template("syariah/edit_syariah.html", syariah=syariah, ajar=ajar)

@radmin.route('/edit_syariah', methods=['POST'])
@login_required
def updateBayar():
    if request.method == 'POST':
        nis = request.form['nis']
        nama_santri = request.form['nama_santri']
        bulan = request.form['bulan']
        tgl_bayar = request.form['tgl_bayar']
        thn_ajaran = request.form['thn_ajaran']
        jml_bayar = request.form['jml_bayar']
        try:
            syariah = Tsyariah.query.filter_by(nis=nis).first()
            syariah.nis = nis
            syariah.nama_santri = nama_santri
            syariah.bulan = bulan
            syariah.tgl_bayar = tgl_bayar
            syariah.thn_ajaran = thn_ajaran
            syariah.jml_bayar = jml_bayar
            db.session.commit()
            flash(f'Pembayaran dengan nama: "{form.nama_santri.data}" berhasil di edit!', 'success')
        except Exception as e:
            print("Failed to update data")
            print(e)
        return redirect('/lihat_bayar')

@radmin.route('/hapus_syariah/<string:nis>')
@login_required
def hapus_syariah(nis):
    try:
        syariah = Tsyariah.query.filter_by(nis=nis).first()
        db.session.delete(syariah)
        db.session.commit()
        flash(f'Pembayaran dengan nama: "{form.nama_santri.data}" berhasil dihapus!', 'success')

    except Exception as e:
        print("Failed delete mahasiswa")
        print(e)
    return redirect(url_for('radmin.lihat_bayar'))


#CRUD TAHUN AJARAN

@radmin.route('/tambah_ajaran', methods=['GET', 'POST'])
def tambah_ajaran():
    if request.method == 'POST':
        # id = request.form['id']
        nama_ajar = request.form['nama_ajar']
        ket_ajar = request.form['ket_ajar']
        try:
            addAjaran = Tajaran(nama_ajar=nama_ajar, ket_ajar=ket_ajar)
            db.session.add(addAjaran)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)

    return render_template('ajaran/tambah_ajaran.html')

@radmin.route('/lihat_ajaran')
@login_required
def lihat_ajaran():
    ajar = Tajaran.query.all()
    return render_template('ajaran/lihat_ajaran.html', ajar=ajar)


@radmin.route('/hapus_ajaran/<int:id>')
@login_required
def hapus_ajaran(id):
    try:
        ajaran = Tajaran.query.filter_by(id=id).first()
        db.session.delete(ajaran)
        db.session.commit()

    except Exception as e:
        print("Failed delete mahasiswa")
        print(e)
    return redirect("/lihat_ajaran")
