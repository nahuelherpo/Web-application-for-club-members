from flask import render_template


def not_found_error(error):
    """Implementación personalizada del manejo del error 404"""
    kwargs = {
        'error_name': '404 Not Found Error',
        'error_description': 'URL Does Not Exist'
    }
    return render_template('error.html', **kwargs), 404


def generic_error(error):
    """Implementación personalizada del manejo del error 500"""

    kwargs = {
        'error_name': '500 Internal Server Error',
        'error_description': 'Internal error in the server'
    }
    return render_template('error.html', **kwargs), 500


def unauthorized_error(error):
    """Implementación personalizada del manejo del error 401"""

    kwargs = {
        'error_name': '401 Unauthorized',
        'error_description': 'You do not have the permissions to access this page'
    }
    return render_template('error.html', **kwargs), 401
