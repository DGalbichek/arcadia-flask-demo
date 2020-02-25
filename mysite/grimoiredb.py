from calendar import monthrange

import datetime
import itertools
import json
import os
import sqlite3


class GrimoireDb():
    def __init__(self,dbfile=''):
        self.DBFILE='grimoiredb.sqlite'
        self.db = sqlite3.connect(self.DBFILE)
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS spells( id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL,
                        type TEXT,
                        level TEXT,
                        components TEXT,
                        castingtime TEXT,
                        range TEXT,
                        area TEXT,
                        duration TEXT,
                        savingthrow TEXT,
                        spellresistance TEXT,
                        description TEXT);
                ''')
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e


    def getSpell(self, name, format='bool'):
        sp = self.cursor.execute("SELECT * FROM spells WHERE name=?;", (name,)).fetchone()
        if format=='bool':
            return False if not sp else True
        else:
            cols = ['id', 'name', 'type', 'level', 'components', 'castingtime', 'range',
                    'area', 'duration', 'savingthrow', 'spellresistance', 'description']
            return {x: sp[n] for n,x in enumerate(cols)}


    def addSpell(self,name,spelldata={}):
        if self.getSpell(name):
            return False
        else:
            #print(len(spelldata.values()))
            #print(spelldata)
            spelltup = (spelldata[x] for x in ['name', 'type', 'level', 'components', 'castingtime', 'range',
                    'area', 'duration', 'savingthrow', 'spellresistance', 'description'])
            #print(spelltup)
            self.cursor.execute('''
                INSERT INTO spells( name, type, level, components, castingtime, range, area,
                duration, savingthrow, spellresistance, description) VALUES (?,?,?,?,?,?,?,?,?,?,?);''',
                                tuple(spelltup))
            self.db.commit()
        return {'success': name + ' added to the db.'}


    def spellNames(self):
        return [x[0].upper() for x in self.cursor.execute("SELECT name FROM spells ORDER BY name ASC;").fetchall()]


if __name__=='__main__':
    gdb=GrimoireDb()

    #prepop
    with open('spells_json.txt', 'r+', encoding='utf8') as f:
        spells = json.load(f)
    for spell in spells:
        spell['description'] = '<br>'.join(spell['description'])
        gdb.addSpell(spell['name'], spell)
    #print(gdb.getSpell('TRANSMUTE MUD TO ROCK', format='dict'))
    #for spell in gdb.cursor.execute("SELECT * FROM spells;").fetchall():
    #    print(spell)
    #for spellname in gdb.spellNames():
    #    print(spellname)

    gdb.db.close()
