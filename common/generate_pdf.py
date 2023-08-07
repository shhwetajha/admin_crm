import pydf
from django.template.loader import get_template
from django.conf import settings

class GeneratePDF:

    def __init__(self, **kwargs):
        self.context = kwargs.get("context", None)
        self.type = kwargs.get("type", None)
        if self.type == "invoice":
            self.template_name = "receipt_template.html"
        # elif self.type == "ELECTRICAL SAFETY CERTIFICATE":
        #     self.template_name = "electrical_safety_certificate.html"
        # elif self.type == "Electricity Notice of Completion":
        #     self.template_name = "electricity_notice_of_completion.html"

    def __call__(self):
        return self.generate_pdf()

    def generate_pdf(self):
        context = self.context
        template = get_template(self.template_name)
        html_string = template.render(context)
        pdf = pydf.generate_pdf(html_string)
        return pdf
    