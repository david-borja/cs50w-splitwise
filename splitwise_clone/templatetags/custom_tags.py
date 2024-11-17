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

