from flask import Flask
from GestorTareas import db
import datetime

class Tareas(db.Model):
    id_tarea =db.Column(db.integer,Primary_key=True)
    Nom_Tarea= db.Column(db.String(100), nullable=False)
    FechaInicio= db.Column(db.DateTime,default=datetime.utcnow)
    FechaFinal= db.Column(db.DateTime)
    Estado=db.Column(db.String(20),default='No Asignada') 