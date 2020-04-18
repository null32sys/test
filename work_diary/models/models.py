# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class SummaryCategory(models.Model):
    _name = 'summary.category'

    name = fields.Char('Name')


class work_diary(models.Model):
    _name = 'workdiary'
    _rec_name = 'creator'

    creator = fields.Many2one('res.users', 'Creator', default=lambda self: self.env.user, readonly=True)
    user = fields.Many2one('res.users', default=lambda self: self.env.user)
    date_created = fields.Date('Date Created',readonly=True, default=lambda self: fields.datetime.now())
    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)
    week_summary = fields.Html('Week Summary', required=True)
    plan = fields.Html('Plan for Next Week', required=True)
    suggestions = fields.Html('Suggestions for Improvements / Challenges Faced')
    summary_category = fields.Many2many('summary.category', string='Summary Category')

class ConfigSetting(models.TransientModel):
    _name = 'workdiary.config.setting'
    _rec_name = 'groups_to_submit'

    groups_to_submit = fields.Many2many('access.rights.group',string="Groups to Submit")

class SubmissionWizard(models.TransientModel):
    _name = "submission.report"

    @api.multi
    def get_date_from(self):
        today = datetime.date.today()
        previos_monday = today - datetime.timedelta(days=today.weekday()+7)
        return previos_monday

    @api.multi
    def get_date_to(self):
        today = datetime.date.today()
        previos_sunday = today - datetime.timedelta(days=today.weekday()+1)
        return previos_sunday

    @api.multi
    def get_default_groups(self):
        config = self.env['workdiary.config.setting'].search([])
        if config:
            return config[-1].groups_to_submit.ids

    date_from = fields.Date('Date From', default=lambda self: self.get_date_from())
    date_to = fields.Date('Date To', default=lambda self: self.get_date_to())
    groups_to_submit = fields.Many2many('access.rights.group',string="Groups to Submit", default=lambda self:self.get_default_groups())

    def get_report_data(self):
        workdiary = self.env['workdiary'].search([
            ('date_created', '>=', self.date_from),
            ('date_created', '<=', self.date_to),
        ])
        users = self.env['res.users'].search([])
        not_submitted_user_list = []
        wk_users = [wk.creator.id for wk in workdiary]
        for user in users:
            if not user.id in wk_users and user.access_rights_id.id in self.groups_to_submit.ids:
                not_submitted_user_list.append(user)

        wk_diary = workdiary.sorted(key=lambda r:r.creator.name)

        submitted_group = [{
            gp.name : [
                user for user in wk_diary if user.creator.access_rights_id == gp
                ]} for gp in self.groups_to_submit
            ]
        values = {
                'not_submitted': not_submitted_user_list,
                'submitted' : submitted_group
            }
        return values

    def print_report(self):
        """Call when button 'Get Report' clicked."""
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_from,
                'date_end': self.date_to,
                'groups_to_submit': self.groups_to_submit.ids,
            },
        }
        return self.env['report'].get_action(self, 'work_diary.work_diary_template')