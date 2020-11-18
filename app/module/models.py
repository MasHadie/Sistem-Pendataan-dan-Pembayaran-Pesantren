from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, table, column, func
import os
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "db_pelajarnu.db"))
engine = create_engine(database_file)

from app import app
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'tb_pengguna'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    pass_hash = db.Column(db.String, nullable=False)
    # level     = db.Column(db.Integer, nullable=False)


class Santri(db.Model):
    __tablename__ = 'tb_santri'

    id      = db.Column(db.Integer, primary_key=True)
    nis     = db.Column(db.Integer, nullable=False)
    nama_l  = db.Column(db.String, nullable=False)
    jenis_k = db.Column(db.String, nullable=False)
    tmpt_l  = db.Column(db.String, nullable=False)
    tgl_l   = db.Column(db.String, nullable=False)
    alamat  = db.Column(db.String, nullable=False)
    th_ajar = db.Column(db.String, nullable=False)
    ortu    = db.Column(db.String, nullable=False)
    no_hp   = db.Column(db.Integer, nullable=False)
    status  = db.Column(db.String, nullable=False)
    th_masuk= db.Column(db.String, nullable=False)

class Bendahara(db.Model):
    __tablename__ = 'tb_keuangan'

    id      = db.Column(db.Integer, primary_key=True)
    nama_k  = db.Column(db.String, nullable=False)
    nominal = db.Column(db.Integer, nullable=False)
    ket     = db.Column(db.String, nullable=False)

class Ajaran(db.Model):
    __tablename__ = 'tb_ajaran'

    id         = db.Column(db.Integer, primary_key=True)
    nama_ajar  = db.Column(db.String, nullable=False)
    ket_ajar   = db.Column(db.String, nullable=False)
    # def __repr__(self):
    #     return "<Name: {}>".format(self.nama_l)
class Syariah(db.Model):
    __tablename__ = 'tb_syariah'

    id         = db.Column(db.Integer, primary_key=True)
    nis        = db.Column(db.Integer, db.ForeignKey('tb_santri.nis'))
    nama_santri = db.Column(db.String, db.ForeignKey('tb_santri.nama_l'))
    bulan       = db.Column(db.String, nullable=False)
    tgl_bayar   = db.Column(db.String, nullable=False)
    thn_ajaran  = db.Column(db.String, nullable=False)
    jml_bayar   = db.Column(db.Integer, nullable=False)

class Pesantren(db.Model):
    __tablename__ = 'tb_pesantren'

    id         = db.Column(db.Integer, primary_key=True)
    nama_pesantren = db.Column(db.String, nullable=False)
    nama_pengasuh = db.Column(db.String, nullable=False)
    no_telp = db.Column(db.String, nullable=False)
    alamat = db.Column(db.String, nullable=False)
db.create_all()
