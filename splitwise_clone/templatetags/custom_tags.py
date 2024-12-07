from django import template
from django.conf import settings
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from ..utils import decimals
import os

register = template.Library()

@register.simple_tag
def svg_icon(file_name):
    svg_path = os.path.join(
        settings.BASE_DIR, "splitwise_clone/static/icons", file_name + ".svg"
    )
    with open(svg_path, "r") as file:
        svg_code = file.read()

    svg_code = format_html(svg_code)
    return mark_safe(svg_code)


@register.inclusion_tag("splitwise_clone/components/input-group.html")
def custom_input(name, type, placeholder, label):
    return {"name": name, "type": type, "placeholder": placeholder, "label": label}


@register.inclusion_tag("splitwise_clone/components/error-input-group.html")
def custom_error_input(name, type, placeholder, label):
    return {"name": name, "type": type, "placeholder": placeholder, "label": label}


@register.inclusion_tag("splitwise_clone/components/submit-button.html")
def custom_submit_button(text):
    return {
        "text": text,
    }

@register.inclusion_tag("splitwise_clone/components/balance-summary.html")
def balance_summary(amount, summary_details):
    return {
        "amount": amount,
        "summary_details": summary_details,
    }


@register.inclusion_tag("splitwise_clone/components/balances-feed-item.html")
def balances_feed_item(char, username, balance, is_it_me):
    return {
        "char": char,
        "username": username,
        "balance": balance,
        "is_it_me": is_it_me,
    }

@register.inclusion_tag("splitwise_clone/components/expenses-feed-item.html")
def expenses_feed_item(date, icon, name, description, payer, amount):
    return {
        "date": date,
        "icon": icon,
        "name": name,
        "description": description,
        "payer": payer,
        "amount": amount,
    }


@register.inclusion_tag("splitwise_clone/components/footer-create-button.html")
def footer_create_button(id, visibility, form_url, text):
    return {
        "id": id,
        "visibility": visibility,
        "form_url": form_url,
        "text": text,
    }


@register.inclusion_tag("splitwise_clone/components/reimbursements-modal.html")
def reimbursements_modal(modal_id, close_modal_button_id, balance_summary, my_reimbursements, suggested_reimbursements, user_alias, group_id):
    return {
        "modal_id": modal_id,
        "close_modal_button_id": close_modal_button_id,
        "balance_summary": balance_summary,
        "my_reimbursements": my_reimbursements,
        "suggested_reimbursements": suggested_reimbursements,
        "user_alias": user_alias,
        "group_id": group_id,
    }


@register.inclusion_tag("splitwise_clone/components/dropdown.html")
def dropdown(input_name, label, button_id, dropdown_id, options, default_value):
    return {
        "input_name": input_name,
        "label": label,
        "button_id": button_id,
        "dropdown_id": dropdown_id,
        "options": options,
        "default_value": default_value
    }


@register.inclusion_tag("splitwise_clone/components/reimbursement-form.html")
def reimbursement_form(group_id, amount, sender, receiver):
    return {
        "group_id": group_id,
        "amount": amount,
        "sender": sender,
        "receiver": receiver,
    }


register.filter('decimals', decimals)


@register.filter
def abs_value(value):
    try:
        return decimals(abs(value))
    except (TypeError, ValueError):
        return value
