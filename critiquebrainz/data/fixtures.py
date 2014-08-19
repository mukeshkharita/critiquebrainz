from critiquebrainz.data import db, create_tables
from critiquebrainz.data.model.license import License


def install(app, *args):
    db.init_app(app)
    create_tables(app)
    for arg in args:
        for key, entity in arg.__dict__.iteritems():
            if not key.startswith("__"):
                try:
                    db.session.add(entity)
                    db.session.flush()
                except:
                    print('Failed to add %s!' % key)
                    db.session.rollback()
                else:
                    print('Added %s.' % key)
    db.session.commit()


class LicenseData(object):
    """Licenses that can be used with reviews.

    If you add new ones or remove existing, make sure to update forms,
    views, and other stuff that needs to be updated.
    """
    cc_by_sa_3 = License(
        id=u"CC BY-SA 3.0",
        full_name=u"Creative Commons Attribution-ShareAlike 3.0 Unported",
        info_url=u"https://creativecommons.org/licenses/by-sa/3.0/")
    cc_by_nc_sa_3 = License(
        id=u"CC BY-NC-SA 3.0",
        full_name=u"Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported",
        info_url=u"https://creativecommons.org/licenses/by-nc-sa/3.0/")


# Include all objects into this tuple.
all_data = (LicenseData, )
