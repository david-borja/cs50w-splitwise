from django import template
from django.conf import settings
from django.utils.html import format_html
from django.utils.safestring import mark_safe
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
def balance_summary(icon, amount_str, summary_details):
    return {
        "icon": icon,
        "amount_str": amount_str,
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
def expenses_feed_item(date, icon, transaction_type, description, author, amount):
    return {
        "date": date,
        "icon": icon,
        "transaction_type": transaction_type,
        "description": description,
        "author": author,
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
