from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
from datetime import date
class Patient(models.Model):

    _name ='hospital.patient'
    _description='patient details'
    # _inherit = ['mail.thread']

    name=fields.Char(string="Patient  Name")
    dob=fields.Date(string="Date Of Birth")
    age=fields.Integer(string="Age",compute="age_calculate")
    age_group=fields.Char(string="Age Group",compute="agegroup")
    mobile_no=fields.Char(string="Mobile Number")
    gender=fields.Selection([
        ('male','Male'),
        ('female','Female'),
        ('others','Others')
    ],default=False)
    doctor_ids=fields.Many2one('hospital.doctor',string="Doctor")
    ref=fields.Char(string="Referance" ,readonly=True)
    email_id=fields.Char(string="Email")
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer/Vendor",
        )
    appointment=fields.Char("appointment")

    
    # def _name_search(self,name='',args=None,operator='ilike',limit=100,name_get_uid=None):
    #     args=list(args or [])
    #     if name:
    #         args+=['|','|',
    #         ('gender',operator,name)
    #         ]
    #     return  super()._name_search(args,limit,access_rights_uid=name_get_uid)

   

    @api.model
    def create(self,val):
        print("selff",self)
        res=super(Patient,self).create(val) 
        print('create ',res)  
        val['ref']=self.env['ir.sequence'].next_by_code('hospital.patient')  
        print('valueee:',val)
        mobile = val.get('mobile_no')
        if mobile and len(mobile)!=10:
            raise ValidationError(_("mobile no must be 10 digit"))

        # if mobile:
        #     if len(mobile)>10 or len(mobile)<9:
        #         raise ValidationError(_("mobile no must be 10 digit")) 
        
        
        return res

        

    def write(self,val):
        res=super(Patient,self).write(val)
        print('-----res value---------',res)
        print('updated valuess',val)
        mobile = val.get('mobile_no')
       
        if mobile and len(mobile)!=10:
            raise ValidationError(_("mobile no must be 10 digit"))
        return 

    @api.onchange('partner_id')
    def onchange_mobile_email(self):
        if self.partner_id:
            self.mobile_no=self.partner_id.mobile
            self.email_id=self.partner_id.email
   

    @api.depends('dob')
    def age_calculate(self):
       today=date.today()
       for rec in self:
        if rec.dob:
            rec.age=today.year-rec.dob.year-((today.month,today.day)<(rec.dob.month,rec.dob.day))
        else:
            rec.age=0
    

    @api.onchange('gender')
    def onchange_gender(self):
        if self.gender and self.name:
            for prefix in ["Mr. ", "Mrs."]:
                if self.name.startswith(prefix):
                    self.name = self.name[len(prefix):]
                    break
            if self.gender=='male':
                self.name="Mr."+self.name
            elif self.gender=='female':
                self.name="Mrs."+self.name


    @api.depends('age')
    def agegroup(self):
        for rec in self:
            if rec.age:
                if rec.age <= 12:
                    rec.age_group = 'child'
                elif rec.age <= 19:
                    rec.age_group = 'teen'
                elif rec.age <= 59:
                    rec.age_group = 'adult'
                else:
                    rec.age_group = 'senior'
            else:
                rec.age_group = False

    





       
        



   


   

   

