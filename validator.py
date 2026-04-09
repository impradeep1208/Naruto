import ipaddress
from config import ALLOWED_TOOLS, ALLOWED_PRIVATE_IPS, WHITELISTED_DOMAINS, SCAN_TYPES

class ValidationError(Exception):
    pass

def validate_tool(tool):
    """Validate if tool is whitelisted."""
    if tool not in ALLOWED_TOOLS:
        raise ValidationError(f"Tool '{tool}' not whitelisted. Allowed: {ALLOWED_TOOLS}")
    return True

def validate_target(target):
    """Validate target is either private IP or whitelisted domain."""
    # Check if it's an IP address
    try:
        ip = ipaddress.ip_address(target)
        # Check if it's in private ranges
        for private_range in ALLOWED_PRIVATE_IPS:
            if ip in ipaddress.ip_network(private_range):
                return True
        raise ValidationError(f"IP {target} is not in allowed private ranges")
    except ValueError:
        # Not an IP, check if it's a whitelisted domain
        if target in WHITELISTED_DOMAINS:
            return True
        raise ValidationError(f"Domain '{target}' not whitelisted. Allowed: {WHITELISTED_DOMAINS}")

def validate_scan_type(scan_type):
    """Validate scan type is recognized."""
    if scan_type not in SCAN_TYPES:
        raise ValidationError(f"Scan type '{scan_type}' not recognized. Allowed: {list(SCAN_TYPES.keys())}")
    return True

def parse_command(command_text):
    """Parse voice command into target, tool, and scan_type."""
    command_lower = command_text.lower()
    
    tool = None
    scan_type = None
    target = None
    
    # Extract tool
    for allowed_tool in ALLOWED_TOOLS:
        if allowed_tool in command_lower:
            tool = allowed_tool
            break
    
    # Extract scan type (check both with spaces and underscores)
    for stype in SCAN_TYPES.keys():
        # Check both "all_ports" and "all ports" formats
        if stype in command_lower or stype.replace("_", " ") in command_lower:
            scan_type = stype
            break
    
    # Extract target (simple extraction - looks for IP or domain)
    words = command_text.split()
    for word in words:
        # Remove punctuation
        word = word.strip('.,!?;:"\'')
        try:
            validate_target(word)
            target = word
            break
        except ValidationError:
            continue
    
    return {
        "target": target,
        "tool": tool or "nmap",
        "scan_type": scan_type or "basic"
    }