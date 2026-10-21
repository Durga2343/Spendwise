def format_inr(amount):
    """
    Format a number as Indian Rupee (INR).
    Example: 1234567.89 -> ₹12,34,567.89
    """
    try:
        amount = float(amount)
        is_negative = amount < 0
        amount = abs(amount)
        
        s, *d = str(amount).partition(".")
        if len(s) > 3:
            r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
        else:
            r = s
            
        decimal_part = "".join(d)[:3]
        if not decimal_part:
            decimal_part = ".00"
        elif len(decimal_part) == 2:
            decimal_part += "0"
            
        formatted = f"₹{r}{decimal_part}"
        return f"-{formatted}" if is_negative else formatted
    except (ValueError, TypeError):
        return "₹0.00"
