from flask import Flask
import settings

app = Flask('hipflask')
app.config.from_object('settings')

import site
import views
