# fix_handshake_assert.py

from datetime import datetime

def assert_fix_handshake(FIX_REG, required_fixes):
    """
    Enforces that all required FIX modules are PASSED before proceeding.

    Parameters:
    - FIX_REG (dict): The current FIX module status registry.
    - required_fixes (list): List of FIX IDs that must be PASSED.

    Raises:
    - AssertionError: If any required FIX is not PASSED.
    """

    for fix_id in required_fixes:
        status = FIX_REG.get(fix_id, {}).get("status")
        timestamp = FIX_REG.get(fix_id, {}).get("timestamp", "N/A")
        if status != "PASSED":
            raise AssertionError(
                f"[❌ FIX HANDSHAKE BLOCKED] {fix_id} is {status or 'MISSING'} — "
                f"required for FIX-3. Last updated: {timestamp}."
            )
        print(f"[✅ FIX HANDSHAKE OK] {fix_id} PASSED at {timestamp}")
