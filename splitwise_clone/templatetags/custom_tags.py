from django import template
register = template.Library()

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


@register.inclusion_tag("splitwise_clone/components/balance-feed-item.html")
def balance_feed_item(char, username, balance, is_it_me):
    return {
        "char": char,
        "username": username,
        "balance": balance,
        "is_it_me": is_it_me,
    }
