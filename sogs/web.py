import flask
from . import config

app = flask.Flask(__name__)
app.logger.setLevel(config.LOG_LEVEL)

# Monkey-patch app.get/post/etc. for Flask <2 compatibility; this has to be before the imports,
# below, because they depend on this existing.
if not hasattr(flask.Flask, 'post'):

    def _add_flask_method(name):
        def meth(self, rule: str, **options):
            return self.route(rule, methods=[name.upper()], **options)

        setattr(flask.Flask, name, meth)

    for method in ('get', 'post', 'put', 'delete', 'patch'):
        _add_flask_method(method)

from . import routes
from . import onion_request
from . import legacy_routes
from . import cleanup
