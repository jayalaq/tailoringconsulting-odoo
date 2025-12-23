from odoo import api, models, fields

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    @api.model
    def _get_batch_available_journals(self, batch_result):
        """
            This function is used to get the available journals for the batch.
            It is used to restrict the journals that are accessible to the user.
        """
        res = super()._get_batch_available_journals(batch_result)
        user = self.env.user
        if not user.has_group("add_user_by_journal.res_groups_admin_journal_access"):
            new_res = self.env['account.journal']
            for journal in res:
                if journal.assign_to_ids and user.id in journal.assign_to_ids.ids:
                    new_res += journal
            res = new_res
        return res
