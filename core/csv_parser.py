"""CSV parsing utilities for bone rename mappings."""
from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO


@dataclass
class CSVParseResult:
    """Result of CSV parsing operation."""
    mappings: dict[str, str]  # old_name -> new_name
    total_rows: int
    skipped_rows: int
    error: str | None = None

    @property
    def is_valid(self) -> bool:
        """Check if parsing was successful."""
        return self.error is None

    @property
    def mapping_count(self) -> int:
        """Get number of valid mappings."""
        return len(self.mappings)


class CSVParser:
    """
    CSV parser for bone rename mappings.

    Stateless parser that converts CSV files into rename dictionaries.
    Supports multiple encodings including UTF-8, UTF-16, and system defaults.
    """

    # Encoding detection order - try most common first
    ENCODINGS = ['utf-8-sig', 'utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'cp1252', 'latin1']

    @staticmethod
    def _try_encodings(file_path: Path) -> tuple[str | None, str | None]:
        """
        Try multiple encodings to read the file.

        Args:
            file_path: Path to CSV file

        Returns:
            Tuple of (file_content, successful_encoding) or (None, None) if all fail
        """
        for encoding in CSVParser.ENCODINGS:
            try:
                with open(file_path, 'r', encoding=encoding, newline='') as f:
                    content = f.read()
                    return content, encoding
            except (UnicodeDecodeError, UnicodeError):
                continue
            except Exception:
                # Other errors (permission, etc.) should be handled by caller
                break
        return None, None

    @staticmethod
    def parse_file(file_path: str | Path) -> CSVParseResult:
        """
        Parse CSV file into rename mappings with robust encoding support.

        Expected format:
        - Two columns: source_name, target_name
        - First row is header (skipped)
        - Empty source names are skipped
        - Empty target names are skipped

        Encoding strategy:
        1. Try UTF-8 with BOM detection (utf-8-sig)
        2. Try UTF-8 without BOM
        3. Fallback to UTF-16 variants (Excel exports)
        4. Fallback to Western encodings (cp1252, latin1)

        All exceptions are caught and converted to user-friendly error messages.

        Args:
            file_path: Path to CSV file

        Returns:
            CSVParseResult with mappings or error
        """
        try:
            path = Path(file_path)

            # Validate file exists
            if not path.exists():
                return CSVParseResult({}, 0, 0, f"File not found: {file_path}")

            if not path.is_file():
                return CSVParseResult({}, 0, 0, f"Not a file: {file_path}")

            # Try multiple encodings
            content, encoding = CSVParser._try_encodings(path)

            if content is None:
                return CSVParseResult(
                    {}, 0, 0,
                    f"Unable to read file with any supported encoding. "
                    f"Please save CSV as UTF-8"
                )

            # Parse CSV from string content
            return CSVParser._parse_stream(io.StringIO(content))

        except PermissionError:
            return CSVParseResult({}, 0, 0, f"Permission denied: {file_path}")
        except OSError as e:
            return CSVParseResult({}, 0, 0, f"File access error: {e}")
        except Exception as e:
            return CSVParseResult({}, 0, 0, f"Unexpected error reading file: {e}")

    @staticmethod
    def _parse_stream(stream: TextIO) -> CSVParseResult:
        """
        Parse CSV from text stream.

        Args:
            stream: Text stream containing CSV data

        Returns:
            CSVParseResult with mappings or error
        """
        try:
            reader = csv.reader(stream)
            mappings: dict[str, str] = {}
            total_rows = 0
            skipped_rows = 0

            # Skip header row
            try:
                next(reader)
            except StopIteration:
                return CSVParseResult({}, 0, 0, "Empty CSV file")

            # Process data rows
            for row_num, row in enumerate(reader, start=2):  # start=2 (after header)
                total_rows += 1

                # Validate row structure
                if len(row) < 2:
                    skipped_rows += 1
                    continue

                source_name = row[0].strip()
                target_name = row[1].strip()

                # Skip empty source or target
                if not source_name or not target_name:
                    skipped_rows += 1
                    continue

                # Add to mappings (later entries override earlier ones)
                mappings[source_name] = target_name

            return CSVParseResult(mappings, total_rows, skipped_rows, None)

        except csv.Error as e:
            return CSVParseResult({}, 0, 0, f"CSV parsing error: {e}")
        except Exception as e:
            return CSVParseResult({}, 0, 0, f"Unexpected error parsing CSV: {e}")

    @staticmethod
    def validate_mappings(
        mappings: dict[str, str],
        available_names: set[str]
    ) -> tuple[dict[str, str], int]:
        """
        Filter mappings to only include names that exist.

        Args:
            mappings: Full mapping dictionary
            available_names: Set of names that actually exist

        Returns:
            Tuple of (valid_mappings, skipped_count)
        """
        valid_mappings = {
            old: new for old, new in mappings.items()
            if old in available_names
        }
        skipped = len(mappings) - len(valid_mappings)
        return valid_mappings, skipped
