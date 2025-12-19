"""
Custom exceptions for D0010 import and processing.

These exceptions provide detailed error information for better
debugging and user feedback.
"""


class D0010ImportError(Exception):
    """Base exception for D0010 import errors."""

    def __init__(self, message: str, filename: str = None, line_number: int = None):
        self.message = message
        self.filename = filename
        self.line_number = line_number
        super().__init__(self.format_message())

    def format_message(self) -> str:
        """Format error message with context."""
        parts = [self.message]
        if self.filename:
            parts.append(f"File: {self.filename}")
        if self.line_number:
            parts.append(f"Line: {self.line_number}")
        return " | ".join(parts)


class InvalidD0010FormatError(D0010ImportError):
    """Raised when file doesn't match D0010 specification."""

    def __init__(
        self,
        message: str,
        filename: str = None,
        line_number: int = None,
        expected: str = None,
        got: str = None,
    ):
        self.expected = expected
        self.got = got
        super().__init__(message, filename, line_number)

    def format_message(self) -> str:
        """Format error with expected vs actual values."""
        msg = super().format_message()
        if self.expected and self.got:
            msg += f" | Expected: {self.expected}, Got: {self.got}"
        return msg


class DuplicateFileError(D0010ImportError):
    """Raised when attempting to import an already-imported file."""

    pass


class MeterPointNotFoundError(D0010ImportError):
    """Raised when referenced meter point doesn't exist."""

    def __init__(self, mpan: str, filename: str = None, line_number: int = None):
        self.mpan = mpan
        super().__init__(
            f"Meter point not found: {mpan}",
            filename=filename,
            line_number=line_number,
        )


class MeterNotFoundError(D0010ImportError):
    """Raised when referenced meter doesn't exist."""

    def __init__(
        self, serial_number: str, filename: str = None, line_number: int = None
    ):
        self.serial_number = serial_number
        super().__init__(
            f"Meter not found: {serial_number}",
            filename=filename,
            line_number=line_number,
        )


class InvalidMPANError(D0010ImportError):
    """Raised when MPAN format is invalid."""

    def __init__(self, mpan: str, filename: str = None, line_number: int = None):
        self.mpan = mpan
        super().__init__(
            f"Invalid MPAN format: {mpan} (must be 13 digits)",
            filename=filename,
            line_number=line_number,
        )


class ParsingError(D0010ImportError):
    """Raised when unable to parse a specific record."""

    def __init__(
        self,
        record_type: str,
        raw_data: str = None,
        filename: str = None,
        line_number: int = None,
    ):
        self.record_type = record_type
        self.raw_data = raw_data
        message = f"Failed to parse {record_type} record"
        if raw_data:
            message += f": {raw_data[:50]}..."
        super().__init__(message, filename=filename, line_number=line_number)
