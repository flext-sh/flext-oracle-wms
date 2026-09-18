# from flext-oracle-wms_docs/troubleshooting.md:151
from __future__ import annotations


def test_real_connection():
    # This test expects to fail with test settings
    try:
        result = client.test_connection()
    except Exception:
        pass  # Expected with fake URLs
