from typing import Any
from unittest.suite import TestSuite

from django.test.runner import DiscoverRunner


class V1DiscoverRunner(DiscoverRunner):
    def build_suite(
        self,
        test_labels: list[str] | None = None,
        **kwargs: Any,
    ) -> TestSuite:
        return super().build_suite(test_labels or ["myapp"], **kwargs)
