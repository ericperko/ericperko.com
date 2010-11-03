from flask import Flask
import settings

app = Flask('hipflask')
app.config.from_object('hipflask.default_settings')
app.config.from_object('settings')

import site
import views
