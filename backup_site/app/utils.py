import sys

from django.core.mail import EmailMultiAlternatives


def envia_email(
    txt_body,
    html_body,
    subject="E-mail de Contato",
    from_sender="",
    to=[],
    attach=False,
    c_file=None,
):
    msg = EmailMultiAlternatives(
        subject, txt_body, from_sender, to, headers={"Reply-To": from_sender}
    )

    msg.attach_alternative(html_body, "text/html")
    if attach:
        msg.attach(attach.name, attach.read(), attach.content_type)
    msg.body = html_body
    msg.content_subtype = "html"
    return msg.send()


def reload_sys():
    """
		reload sys with utf-8 as default encoding.
	"""
    reload(sys)
    sys.setdefaultencoding("utf8")
