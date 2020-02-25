import grimoiredb

##
## FLASK
import datetime
import glob
import json
import markdown
import random
from flask import Flask, Markup, Response
from flask import render_template, send_from_directory, request, url_for
app = Flask(__name__)
app.config.from_object('config')


from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired


class SpellLookupForm(FlaskForm):
    spellname=StringField('Spell', id='spell_autocomplete', validators=[DataRequired()])


gdb = grimoiredb.GrimoireDb()
SPELLS = gdb.spellNames()
gdb.db.close()


@app.route("/spellname_auto", methods=['GET'])
def spellname_auto():
    search = request.args.get('term')
    return Response(json.dumps(SPELLS), mimetype='application/json')


@app.route("/grimoire/spell", methods=['GET', 'POST'])
@app.route("/grimoire/spell/", methods=['GET', 'POST'])
def grimoire_spell_lookup(msg=[]):
    gdb = grimoiredb.GrimoireDb()
    form = SpellLookupForm()
    gdb.db.close()

    if form.validate_on_submit():
        gdb = grimoiredb.GrimoireDb()
        gdb.db.close()
        msg="""<p class="larger">"""+m['duna']+"""</p><br><a href="/ptime/add">+</a>"""
        return msg
        

    return render_template('grimoire.html',
                           title='Grimoire',
                           form=form,)


if __name__ == "__main__":
        app.run()
