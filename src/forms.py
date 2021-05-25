from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired, Length


class MMSI_Number(FlaskForm):
    MMSI_Number = IntegerField('MMSI No.')
    