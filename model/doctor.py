from odoo import models,fields,api

class Doctor(models.Model):

    _name ='hospital.doctor'
    _description='doctor details'

    name=fields.Char(string="Doctor Name")
    patient_ids=fields.One2many("hospital.patient","doctor_ids",string="Patient")
    specailization=fields.Char(string="Specialization")
    gender=fields.Selection([
        ('male','Male'),
        ('female','Female'),
        ('others','Others')
    ],default=False)

    # @api.model
    # def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
    #     print('name_searchh_uiddddddddddddddddddddd')
    #     args = args or []
    #     domain = []

    #     if name:
    #         domain = ['|',('name' , operator , name),('gender' , operator , name)]

    #     domain += args
    #     res=self._search(domain,limit=limit,access_rights_uid=name_get_uid)
    #     print('name_searchh_uiddddddddddddddddddddd',res)
    
    #     return res

   

    
    @api.model
    def _name_search(self,name: str = '',domain: list | None = None,operator: str = 'ilike',limit: int = 100,order: str | None = None,):
        
        domain = domain or []

        if name:
            domain = ['|', ('name', operator, name), ('gender', operator, name)]

        ids = self._search(domain, limit=limit)
        print('>>> Found IDs:', ids)

        # Must return (id, display_name) tuples for Many2one
        return self.browse(ids).name_get()
