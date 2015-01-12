#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
from flask import jsonify, current_app
import pip
from pip.exceptions import BadCommand
from pip.util import find_command
from werkzeug.utils import cached_property
from util.flask_extensions.base import FlaskExtension


class Health(FlaskExtension):

    def init_app(self, app, **kwargs):
        self.register_view(app, **kwargs)

    @cached_property
    def git_info(self):
        try:
            find_command('git')
        except BadCommand:
            return {
                'error': '"git" not available'
            }
        else:
            cwd = os.getcwd()
            os.chdir(current_app.root_path)
            r = {
                'rev': subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip('\n'),
                'branch': subprocess.check_output([
                    'git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip('\n'),
                'message': subprocess.check_output([
                    'git', 'log', '-1', '--pretty=%B']).strip('\n'),
            }
            os.chdir(cwd)
            return r

    @cached_property
    def pip_info(self):
        packages = pip.get_installed_distributions()
        return sorted('%s==%s' % (p.key, p.version) for p in packages)

    @staticmethod
    def get_app_info():
        return {
            'debug': current_app.debug
        }

    def health_view(self):
        return jsonify({
            'status': 'ok',
            'git': self.git_info,
            'app': self.get_app_info(),
            'packages': self.pip_info,
        })

    def register_view(self, app, **kwargs):
        app.add_url_rule(
            '/_health', view_func=self.health_view, **kwargs)
