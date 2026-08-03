"""
Tests for the __is_parameter / __extract_parameters fix in decorators.py

The fix ensures that values starting with '-' (e.g. tokens like
-SO_meexAMP33Pletest) are NOT misclassified as CLI parameter keys.
"""

from unittest.mock import MagicMock

import pytest

from m3cli.utils import decorators as _mod

# =========================================================================
#  Accessing module-level double-underscore functions.
#
#  Python only name-mangles __attr inside *class bodies*, so at module
#  level these are stored literally as '__is_parameter' etc.
#  However, writing `_mod.__is_parameter` inside a class body (our test
#  classes) WOULD trigger mangling to `_mod._TestXxx__is_parameter`.
#  Using __dict__ lookup avoids that entirely.
# =========================================================================
_is_parameter = _mod.__dict__['__is_parameter']
_extract_parameters = _mod.__dict__['__extract_parameters']

# =========================================================================
#  Constants — reusable test values
#
#  Each value that resembles a secret/token/password intentionally
#  contains "test", "Test", or "example" so security scanners and
#  reviewers can immediately see these are NOT real credentials.
# =========================================================================

# --- dash-prefixed values (the core of the fix) ---
DASH_TOKEN_WITH_UNDERSCORE = "-SO_meexAMP33Pletest"      # underscore + digits
DASH_NEGATIVE_INT = "-100"                               # plain number
DASH_NEGATIVE_SMALL = "-5"                               # plain number
DASH_NEGATIVE_FLOAT = "-3.14"                            # plain number
DASH_SCIENTIFIC = "-1e5"                                 # plain number
DASH_ALPHA_DIGIT = "-t1"                                 # alpha + digit
DASH_UNDERSCORE_PREFIX = "-_test_private"                # underscore after dash
DASH_UPPER_DIGITS = "-TESTkey123"                        # uppercase + digits
DASH_BASE64_VALUE = "-Tst/tEsT+abc123=="                 # base64-like
DASH_PASSWORD_SPECIAL = "-T3st_p@ss!"                    # special chars
DASH_MIXED_SECRET = "-xK9_tEsT"                          # mixed case + digits
BARE_DASH = "-"
BARE_DOUBLE_DASH = "--"

# --- AWS-style credentials (official AWS documentation examples) ---
# Source: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html
SAMPLE_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
SAMPLE_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# --- other sample values ---
SAMPLE_API_ADDRESS = "https://api.test.example.com"
SAMPLE_CREDS_PATH = "/tmp/test_creds"
SAMPLE_INSTANCE_ID = "i-0test1234567890ab"


# =========================================================================
#  __is_parameter
# =========================================================================
class TestIsParameter:
    """Unit tests for the __is_parameter helper."""

    @pytest.mark.parametrize("token", [
        "--flag",
        "--long-option",
        "--access_key",
        "--api_address",
        "-c",
        "-v",
        "-du",
        "-abc",
    ])
    def test_recognises_parameters(self, token):
        assert _is_parameter(token) is True, (
            f"{token!r} should be recognised as a parameter"
        )

    @pytest.mark.parametrize("token,description", [
        (DASH_TOKEN_WITH_UNDERSCORE, "token with underscore and digits"),
        (DASH_NEGATIVE_INT, "negative integer"),
        (DASH_NEGATIVE_FLOAT, "negative float"),
        (DASH_SCIENTIFIC, "scientific notation"),
        (DASH_ALPHA_DIGIT, "alpha + digit mix"),
        (DASH_UNDERSCORE_PREFIX, "underscore after dash"),
        (DASH_UPPER_DIGITS, "uppercase + digits"),
        (DASH_BASE64_VALUE, "base64-like value"),
        (DASH_PASSWORD_SPECIAL, "password with special chars"),
        ("value", "plain value"),
        ("", "empty string"),
        ("123", "digits only"),
        (None, "None"),
        (42, "integer"),
        (BARE_DASH, "bare single dash"),
    ])
    def test_rejects_non_parameters(self, token, description):
        assert _is_parameter(token) is False, (
            f"{token!r} ({description}) should NOT be recognised as a parameter"
        )

    def test_bare_double_dash(self):
        """
        '--' (bare double-dash) is conventionally an end-of-options marker.
        Current implementation returns True — document as known behaviour.
        """
        result = _is_parameter(BARE_DOUBLE_DASH)
        assert result is True


# =========================================================================
#  __extract_parameters
# =========================================================================
class TestExtractParameters:
    """Integration-level tests for __extract_parameters."""

    def test_basic_long_option(self):
        args = ["--name", "Alice"]
        assert _extract_parameters(args) == {"name": "Alice"}

    def test_multiple_long_options(self):
        args = ["--region", "us-east-1", "--count", "5"]
        assert _extract_parameters(args) == {
            "region": "us-east-1",
            "count": "5",
        }

    def test_flag_without_value_followed_by_another_flag(self):
        args = ["--force", "--name", "Bob"]
        assert _extract_parameters(args) == {
            "force": None,
            "name": "Bob",
        }

    def test_last_flag_without_value(self):
        args = ["--name", "Bob", "--force"]
        assert _extract_parameters(args) == {
            "name": "Bob",
            "force": None,
        }

    # ---- THE KEY FIX: dash-prefixed values ----
    def test_value_starting_with_dash_and_mixed_chars(self):
        args = ["--token", DASH_TOKEN_WITH_UNDERSCORE]
        result = _extract_parameters(args)
        assert result == {"token": DASH_TOKEN_WITH_UNDERSCORE}

    def test_value_is_negative_number(self):
        args = ["--offset", DASH_NEGATIVE_INT]
        assert _extract_parameters(args) == {"offset": DASH_NEGATIVE_INT}

    def test_value_starts_with_dash_underscore(self):
        args = ["--secret", DASH_UNDERSCORE_PREFIX]
        assert _extract_parameters(args) == {"secret": DASH_UNDERSCORE_PREFIX}

    def test_mixed_normal_and_dash_value(self):
        args = [
            "--name", "test",
            "--token", DASH_TOKEN_WITH_UNDERSCORE,
            "--region", "eu-west-1",
        ]
        result = _extract_parameters(args)
        assert result == {
            "name": "test",
            "token": DASH_TOKEN_WITH_UNDERSCORE,
            "region": "eu-west-1",
        }

    def test_multiple_dash_values_in_a_row(self):
        args = [
            "--key1", DASH_UPPER_DIGITS,
            "--key2", DASH_NEGATIVE_INT,
        ]
        result = _extract_parameters(args)
        assert result == {
            "key1": DASH_UPPER_DIGITS,
            "key2": DASH_NEGATIVE_INT,
        }

    # ---- Short parameters ----
    # Note: __extract_parameters only strips the '--' prefix.
    #       Single-dash short params keep '-' in the key.
    def test_short_parameter_with_value(self):
        args = ["-n", "Alice"]
        assert _extract_parameters(args) == {"-n": "Alice"}

    def test_short_flag_without_value(self):
        args = ["-v", "--name", "Alice"]
        result = _extract_parameters(args)
        assert result == {"-v": None, "name": "Alice"}

    # ---- Repeated parameters → list ----
    def test_repeated_parameter_becomes_list(self):
        args = ["--tag", "a", "--tag", "b", "--tag", "c"]
        result = _extract_parameters(args)
        assert result == {"tag": ["a", "b", "c"]}

    def test_repeated_parameter_two_values(self):
        args = ["--tag", "a", "--tag", "b"]
        result = _extract_parameters(args)
        assert result == {"tag": ["a", "b"]}

    # ---- Empty / no-param cases ----
    def test_empty_args(self):
        assert _extract_parameters([]) == {}

    def test_no_parameters_only_values(self):
        args = ["hello", "world"]
        assert _extract_parameters(args) == {}

    # ---- Known limitation: purely-alphabetic dash value ----
    def test_pure_alpha_dash_value_treated_as_param(self):
        """
        Known limitation: -abc (all-alpha) is classified as a short
        parameter, so if it's intended as a value it will be mis-parsed.
        Single-dash prefix is kept in the key.
        """
        args = ["--password", "-abc"]
        result = _extract_parameters(args)
        assert result == {"password": None, "-abc": None}


# =========================================================================
#  check_args_for_non_interactive_access
# =========================================================================
class TestCheckArgsForNonInteractiveAccess:
    """Tests for the 'm3 access' argument parser."""

    @staticmethod
    def _make_ctx(args_list):
        ctx = MagicMock()
        ctx.args = args_list
        return ctx

    def test_all_required_params(self):
        ctx = self._make_ctx([
            "access",
            "--access_key", SAMPLE_ACCESS_KEY,
            "--secret_key", SAMPLE_SECRET_KEY,
        ])
        result = _mod.check_args_for_non_interactive_access(ctx)
        assert result == [SAMPLE_ACCESS_KEY, SAMPLE_SECRET_KEY]

    def test_all_params_including_optional(self):
        ctx = self._make_ctx([
            "access",
            "--access_key", SAMPLE_ACCESS_KEY,
            "--secret_key", SAMPLE_SECRET_KEY,
            "--api_address", SAMPLE_API_ADDRESS,
            "--path", SAMPLE_CREDS_PATH,
        ])
        result = _mod.check_args_for_non_interactive_access(ctx)
        assert result == [
            SAMPLE_ACCESS_KEY,
            SAMPLE_SECRET_KEY,
            SAMPLE_API_ADDRESS,
            SAMPLE_CREDS_PATH,
        ]

    def test_missing_required_param_raises(self):
        ctx = self._make_ctx([
            "access",
            "--access_key", SAMPLE_ACCESS_KEY,
        ])
        with pytest.raises(AssertionError, match='--secret_key.*missing'):
            _mod.check_args_for_non_interactive_access(ctx)

    def test_unknown_param_raises(self):
        ctx = self._make_ctx([
            "access",
            "--access_key", SAMPLE_ACCESS_KEY,
            "--secret_key", SAMPLE_SECRET_KEY,
            "--bogus", "val",
        ])
        with pytest.raises(AssertionError, match="Unknown parameter"):
            _mod.check_args_for_non_interactive_access(ctx)

    def test_secret_key_starting_with_dash(self):
        """
        Verify that check_args_for_non_interactive_access correctly
        handles a secret_key value starting with '-'.
        """
        ctx = self._make_ctx([
            "access",
            "--access_key", SAMPLE_ACCESS_KEY,
            "--secret_key", DASH_TOKEN_WITH_UNDERSCORE,
        ])
        result = _mod.check_args_for_non_interactive_access(ctx)
        assert result == [SAMPLE_ACCESS_KEY, DASH_TOKEN_WITH_UNDERSCORE]


# =========================================================================
#  Real-world command scenarios
# =========================================================================
class TestRealWorldScenarios:
    """
    Simulate the arg lists that Click hands over in ctx.args[1:]
    for various m3 commands.
    """

    def test_create_credentials_with_dash_token(self):
        args = ["--token", DASH_TOKEN_WITH_UNDERSCORE, "--region", "eu"]
        result = _extract_parameters(args)
        assert result == {
            "token": DASH_TOKEN_WITH_UNDERSCORE,
            "region": "eu",
        }

    def test_schedule_with_negative_offset(self):
        args = ["--offset", DASH_NEGATIVE_SMALL, "--name", "myjob"]
        result = _extract_parameters(args)
        assert result == {"offset": DASH_NEGATIVE_SMALL, "name": "myjob"}

    def test_param_value_with_embedded_dashes(self):
        args = ["--instance_id", SAMPLE_INSTANCE_ID]
        result = _extract_parameters(args)
        assert result == {"instance_id": SAMPLE_INSTANCE_ID}

    def test_base64_encoded_value_with_leading_dash(self):
        args = ["--data", DASH_BASE64_VALUE]
        result = _extract_parameters(args)
        assert result == {"data": DASH_BASE64_VALUE}

    def test_password_with_special_chars(self):
        args = ["--password", DASH_PASSWORD_SPECIAL]
        result = _extract_parameters(args)
        assert result == {"password": DASH_PASSWORD_SPECIAL}

    def test_many_params_one_dash_value(self):
        args = [
            "--name", "test",
            "--cloud", "AWS",
            "--secret", DASH_MIXED_SECRET,
            "--region", "us-east-1",
            "--count", "3",
            "--force",
        ]
        result = _extract_parameters(args)
        assert result == {
            "name": "test",
            "cloud": "AWS",
            "secret": DASH_MIXED_SECRET,
            "region": "us-east-1",
            "count": "3",
            "force": None,
        }
