###
# app configuration
# https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/environment.html
###

[app:main]
use = egg:oereb_server

pyramid.reload_templates = true
pyramid.debug_authorization = false
pyramid.debug_notfound = false
pyramid.debug_routematch = false
pyramid.default_locale_name = en
pyramid_oereb.cfg.file = oereb_server.yml
pyramid_oereb.cfg.section = oereb_server
pyramid.includes = pyramid_debugtoolbar

# By default, the toolbar only appears for clients from IP addresses
# '127.0.0.1' and '::1'.
# debugtoolbar.hosts = 127.0.0.1 ::1
# debugtoolbar.active_panels = performance
# Das Performance-Panel macht Probleme, wenn via Tomcat ein PDF erstellt werden soll.
# Daher in diesem Fall deaktivieren.

###
# wsgi server configuration
###

[server:main]
use = egg:waitress#main
listen = localhost:6543
; use = egg:gunicorn#main
; host = 127.0.0.1
; port = 6543
; workers = 3

###
# logging configuration
# https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/logging.html
###

[loggers]
keys = root, json

[handlers]
keys = console, sqlalchemylogger

[formatters]
keys = generic

[logger_root]
level = DEBUG
handlers = console

[logger_json]
level = INFO
handlers = console, sqlalchemylogger
qualname = JSON
propagate = 0

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[handler_sqlalchemylogger]
class = c2cwsgiutils.sqlalchemylogger.handlers.SQLAlchemyHandler
args = ({'url':'postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_LOGGER_DATABASE}','tablename':'${POSTGRES_LOGGER_TABLE}','tableargs': {'schema':'${POSTGRES_LOGGER_SCHEMA}', 'extend_existing': 'True'}},'/version')
level = NOTSET
formatter = generic
propagate = 0

[formatter_generic]
format = %(asctime)s %(levelname)-5.5s [%(name)s:%(lineno)s][%(threadName)s] %(message)s
