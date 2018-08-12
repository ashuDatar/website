from datetime import datetime
from app.server import db, AppServer
from app.search import add_to_index, remove_from_index, query_index
#import flask_whooshalchemy 

#wa.whoosh_index(app, test_data_dummy_data)

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(Id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.Id.in_(ids)).order_by(
            db.case(when, value=cls.Id)), total
    
class SearchableIndex(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(Id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.Id.in_(ids)).order_by(
            db.case(when, value=cls.Id)), total 

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableIndex.before_commit)
db.event.listen(db.session, 'after_commit', SearchableIndex.after_commit)



class test_data_dummy_data (SearchableMixin, db.Model):
        __tablename__ = 'test_data_dummy_data'
        __searchable__ = ['Metric','Category']
        Id = db.Column(db.Integer,index=True,primary_key=True)
        Year = db.Column(db.Integer,index=True)
        Month = db.Column(db.Integer,index=True)
        Week = db.Column(db.String(120),index=True)
        Frequency = db.Column(db.String(120))
        Date = db.Column(db.Date)
        Datetime = db.Column(db.String(120))
        Category = db.Column(db.String(120))
        Sub_Category = db.Column(db.String(120))
        Metric = db.Column(db.String(120))
        Units = db.Column(db.String(120))
        Source = db.Column(db.String(120))
        Description = db.Column(db.String(500))
        Remarks = db.Column(db.String(500))
        Tag = db.Column(db.String(120))
        CHANDIGARH = db.Column(db.Float)
        HARYANA = db.Column(db.Float)
        HIMACHAL_PRADESH = db.Column(db.Float)
        JAMMU_KASHMIR = db.Column(db.Float)
        NCT_OF_DELHI = db.Column(db.Float)
        PUNJAB = db.Column(db.Float)
        RAJASTHAN = db.Column(db.Float)
        ARUNACHAL_PRADESH = db.Column(db.Float)
        ASSAM = db.Column(db.Float)
        MANIPUR = db.Column(db.Float)
        MEGHALAYA = db.Column(db.Float)
        MIZORAM = db.Column(db.Float)
        NAGALAND = db.Column(db.Float)
        TRIPURA = db.Column(db.Float)
        ANDAMAN_NICOBAR_ISLANDS = db.Column(db.Float)
        BIHAR = db.Column(db.Float)
        JHARKHAND = db.Column(db.Float)
        ODISHA = db.Column(db.Float)
        SIKKIM = db.Column(db.Float)
        WEST_BENGAL = db.Column(db.Float)
        CHHATTISGARH = db.Column(db.Float)
        MADHYA_PRADESH = db.Column(db.Float)
        UTTARAKHAND = db.Column(db.Float)
        UTTAR_PRADESH = db.Column(db.Float)
        DADRANAGAR_HAVELI = db.Column(db.Float)
        DAMAN_DIU = db.Column(db.Float)
        GOA = db.Column(db.Float)
        GUJARAT = db.Column(db.Float)
        MAHARASHTRA = db.Column(db.Float)
        ANDHRA_PRADESH = db.Column(db.Float)
        KARNATAKA = db.Column(db.Float)
        KERALA = db.Column(db.Float)
        LAKSHADWEEP = db.Column(db.Float)
        PUDUCHERRY = db.Column(db.Float)
        TAMIL_NADU = db.Column(db.Float)
        TELANGANA = db.Column(db.Float)
        All_India = db.Column(db.Float)


        def __repr__(self):
              return '<test_data_dummy_data {}>'.format(self.Metric, self.Category)

class search_index (SearchableIndex, db.Model):
      __tablename__ = 'search_index'
      __searchable__ = ['category','sub_category','description']
      Id = db.Column(db.Integer,index=True,primary_key=True)
      category = db.Column(db.String(50),index=True)
      sub_category = db.Column(db.String(50),index=True)
      description = db.Column(db.String(500),index=True)

      def __repr__(self):
            return '<search_index {}>'.format(self.category, self.sub_category, self.description)      
    
