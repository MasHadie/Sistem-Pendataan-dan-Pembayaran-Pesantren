from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import Tusers, Tsantri

class santri_F(FlaskForm):
    nis = StringField('Nomor Induk Santri',validators=[DataRequired(), Length(min=5, max=15)])
    nama_l = StringField('Nama Lengkap',validators=[DataRequired()])
    jenis_k = SelectField('Jenis Kelamin', choices=[('0', '--Pilih Jenis Kelamin--'),('Laki-Laki', 'Laki-Laki'), ('Perempuan', 'Perempuan')], validators=[DataRequired()])
    tmpt_l = StringField('Tempat Lahir',validators=[DataRequired()])
    tgl_l = StringField('Tanggal Lahir',validators=[DataRequired()])
    alamat = TextAreaField('Alamat', validators=[DataRequired()])
    th_ajar = StringField('Tahun Ajaran',validators=[DataRequired()])
    ortu = StringField('Nama Orang Tua',validators=[DataRequired()])
    no_hp = StringField('No Handphone/WA Orang Tua',validators=[DataRequired()])
    status = SelectField('Status',choices=[('0', '--Pilih Status Santri--'),('Aktif', 'Aktif'), ('Alumni', 'Alumni')], validators=[DataRequired()])
    th_masuk = StringField('Tahun Masuk',validators=[DataRequired()])
    submit= SubmitField('Simpan')

    def validate_nis(self, nis):
        cek_nis = Tsantri.query.filter_by(nis=nis.data).first()
        if cek_nis:
            raise ValidationError('NIS sudah terdaptar, silahkan gunakan NIS lain')

class editsantri_F(FlaskForm):
    nis = StringField('Nomor Induk Santri',validators=[DataRequired(), Length(min=5, max=15)])
    nama_l = StringField('Nama Lengkap',validators=[DataRequired()])
    jenis_k = SelectField('Jenis Kelamin', choices=[('0', '--Pilih Jenis Kelamin--'),('Laki-Laki', 'Laki-Laki'), ('Perempuan', 'Perempuan')], validators=[DataRequired()])
    tmpt_l = StringField('Tempat Lahir',validators=[DataRequired()])
    tgl_l = StringField('Tanggal Lahir',validators=[DataRequired()])
    alamat = TextAreaField('Alamat', validators=[DataRequired()])
    th_ajar = StringField('Tahun Ajaran',validators=[DataRequired()])
    ortu = StringField('Nama Orang Tua',validators=[DataRequired()])
    no_hp = StringField('No Handphone/WA Orang Tua',validators=[DataRequired()])
    status = SelectField('Status',choices=[('0', '--Pilih Status Santri--'),('Aktif', 'Aktif'), ('Alumni', 'Alumni')], validators=[DataRequired()])
    th_masuk = StringField('Tahun Masuk',validators=[DataRequired()])
    submit= SubmitField('Simpan')

    # def validate_nis(self, nis):
    #     if nis.data != nis:
    #         cek_nis = Tsantri.query.filter_by(nis=nis.data).first()
    #         if cek_nis:
    #             raise ValidationError('NIS sudah terdaptar, silahkan gunakan NIS lain')

class admin_F(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=5, max=15)])
    konf_pass = PasswordField('Konfirmasi Password',validators=[DataRequired(), EqualTo('password')])
    submit= SubmitField('Daftar')

    def validate_email(self, email):
        cek_email = Tusers.query.filter_by(email=email.data).first()
        if cek_email:
            raise ValidationError('Email sudah terdaptar, silahkan gunakan Email lain')

class editadmin_F(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=5, max=15)])
    konf_pass = PasswordField('Konfirmasi Password',validators=[DataRequired(), EqualTo('password')])
    submit= SubmitField('Ubah')

    def validate_email(self, email):
        if email.data != current_user.email:
            cek_email = Tusers.query.filter_by(email=email.data).first()
            if cek_email:
                raise ValidationError('Email sudah terdaptar, silahkan gunakan Email lain')


class loginadmin_F(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit= SubmitField('Login')


class syariah_F(FlaskForm):
    nis = StringField('Nomor Induk Santri',validators=[DataRequired()])
    nama_santri = StringField('Nama Santri',validators=[DataRequired()])
    bulan = StringField('Bulan Bayar',validators=[DataRequired()])
    tgl_bayar = StringField('Tanggal Transaksi',validators=[DataRequired()])
    thn_ajaran = StringField('Tahun Ajaran',validators=[DataRequired()])
    jml_bayar = StringField('Jumlah Bayar',validators=[DataRequired()])
    submit= SubmitField('BAYAR')
