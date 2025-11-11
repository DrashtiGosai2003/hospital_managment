from odoo import models, fields, api,_
from odoo.exceptions import UserError
import io
import xlsxwriter
import base64

class PatientWizard(models.TransientModel):
    _name = 'patient.wizard'
    _description = 'patient Wizard'


    start_date=fields.Date(string="Start Date",required=True)
    end_date=fields.Date(string="End Date",required=True)
 
    def action_print_xlsx(self):
        patients=self.env['hospital.patient'].search([
            ('create_date', '>=', self.start_date),
            ('create_date', '<=', self.end_date)

        ])
        if not patients:
            raise UserError("No patients found in this date range.")

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Patients")

        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, "ID", bold)
        sheet.write(0, 1, "Name", bold)
        sheet.write(0, 2, "Age", bold)
        sheet.write(0, 3, "Gender", bold)
    

        
        row = 1
        
        for patient in patients:
                sheet.write(row, 0, patient.id)
                sheet.write(row, 1, patient.name or "")
                sheet.write(row, 2, patient.age or 0)
                sheet.write(row, 3, patient.gender or "")
                
                row += 1

        workbook.close()
        output.seek(0)

        file_name = "Patient_Report.xlsx"
        attachment = self.env['ir.attachment'].create({
                'name': file_name,
                'type': 'binary',
                'datas': base64.b64encode(output.read()),
                'store_fname': file_name,
                'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            })

        return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{attachment.id}?download=true',
                'target': 'self',
            }   
    