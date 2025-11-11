# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Hospital Managment',
    'version': '18.0.0.0.0',
    'summary': 'Manage Patient and Doctor Details',

    'depends': [
        'base','mail',
    ],
    'data': [
         'data/sequence.xml',
         'security/ir.model.access.csv',
         'views/patient_view.xml',
         'views/doctor_view.xml',
         "wizard/patient_wizard_view.xml",
       ],  
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
