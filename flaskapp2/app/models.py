from app import db

class Record(db.Model):
	rowid = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String)
	short_description = db.Column(db.String)
	long_description = db.Column(db.String)
	sdg_code = db.Column(db.String)

	def __repr__(self):
		return 'Record {}: {}'.format(self.rowid, self.title)


class sdg_truncated(db.Model):
	rowid = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String)
	short_description = db.Column(db.String)
	long_description = db.Column(db.String)
	sdg_code = db.Column(db.String)

	def __repr__(self):
		return '{} {} {} {} {}'.format(self.rowid, self.title, self.short_description, self.long_description, self.sdg_code)