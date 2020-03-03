from odoo import http

class Example(http.Controller):
    @http.route('/example', type='http', auth='public', website=True)
    def render_example_page(self):
        return http.request.render('first_webpage.example_page', {})