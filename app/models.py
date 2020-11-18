from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(email):
    return Tusers.query.get(email)


class Tusers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Tusers('{self.username}','{self.password}')"
class Tsantri(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    nis     = db.Column(db.String(100),unique=True, nullable=False)
    nama_l  = db.Column(db.String(200), nullable=False)
    jenis_k = db.Column(db.String(15), nullable=False)
    tmpt_l  = db.Column(db.String(200), nullable=False)
    tgl_l   = db.Column(db.String(100), nullable=False)
    alamat  = db.Column(db.String(200), nullable=False)
    th_ajar = db.Column(db.String(100), nullable=False)
    ortu    = db.Column(db.String(200), nullable=False)
    no_hp   = db.Column(db.Integer, nullable=False)
    status  = db.Column(db.String(100), nullable=False)
    th_masuk= db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Tsantri('{self.nis}','{self.nama_l}','{self.jenis_k}','{self.tmpt_l}','{self.tgl_l}','{self.alamat}','{self.th_ajar}','{self.ortu}','{self.no_hp}','{self.status}','{self.th_masuk}')"

class Tajaran(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    nama_ajar  = db.Column(db.String, nullable=False)
    ket_ajar   = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Tajaran('{self.nama_ajar}','{self.ket_ajar}')"

class Tsyariah(db.Model):

    id         = db.Column(db.Integer, primary_key=True)
    nis        = db.Column(db.String(50), nullable=False)
    nama_santri = db.Column(db.String(200), nullable=False)
    bulan       = db.Column(db.String(50), nullable=False)
    tgl_bayar   = db.Column(db.String(50), nullable=False)
    thn_ajaran  = db.Column(db.String(50), nullable=False)
    jml_bayar   = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Tsyariah('{self.nis}','{self.nama_santri}', '{self.bulan}', '{self.tgl_bayar}','{self.thn_ajaran}', '{self.jml_bayar}')"


db.create_all()
