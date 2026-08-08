from __future__ import annotations

from sqlglot import exp, parse_one
from sqlglot.errors import ParseError

DEFAULT_LIMIT = 100

ALLOWED_TABLES = {
    "servers",
    "channels",
    "members",
    "messages",
    "daily_stats",
    "channel_daily_stats",
}


class SQLGuardError(Exception):
    """
    Raised when an SQL query violates one of the safety rules.
    """

    def __init__(
        self,
        message: str,
        retryable: bool = True,
    ):
        super().__init__(message)
        self.retryable = retryable


class SQLGuard:

    @staticmethod
    def validate(sql: str) -> str:
        sql = sql.strip()

        if not sql:
            raise SQLGuardError("Empty SQL query.")

        # Reject multiple statements
        if ";" in sql.rstrip(";"):
            raise SQLGuardError("Multiple SQL statements are not allowed.")

        try:
            tree = parse_one(sql, read="postgres")
        except ParseError as e:
            raise SQLGuardError(f"Invalid SQL: {e}") from e

        SQLGuard._validate_statement(tree)
        SQLGuard._validate_tables(tree)

        if not SQLGuard._has_limit(tree):
            tree = SQLGuard._inject_limit(tree)

        return tree.sql(dialect="postgres")

    @staticmethod
    def _validate_statement(tree: exp.Expression) -> None:

        if isinstance(tree, exp.Select):
            return

        if isinstance(tree, exp.With):
            return

        if isinstance(tree, exp.Union):
            return

        if isinstance(tree, exp.Subquery):
            return

        raise SQLGuardError(
            f"Only SELECT queries are allowed. Found {type(tree).__name__}"
        )

    @staticmethod
    def _validate_tables(tree: exp.Expression) -> None:
        tables = {
            table.name.lower()
            for table in tree.find_all(exp.Table)
        }

        if not tables:
            raise SQLGuardError("No tables referenced.")

        for table in tables:

            if table.startswith("pg_"):
                raise SQLGuardError(
                    "System catalog access is forbidden."
                )

            if table == "information_schema":
                raise SQLGuardError(
                    "System catalog access is forbidden."
                )

            if table not in ALLOWED_TABLES:
                raise SQLGuardError(
                    f"Table '{table}' is not allowed."
                )

    @staticmethod
    def _has_limit(tree: exp.Expression) -> bool:
        return tree.args.get("limit") is not None

    @staticmethod
    def _inject_limit(tree: exp.Expression) -> exp.Expression:
        tree.set(
            "limit",
            exp.Limit(
                expression=exp.Literal.number(DEFAULT_LIMIT)
            ),
        )
        return tree