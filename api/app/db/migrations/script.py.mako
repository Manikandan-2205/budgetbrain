<%!
    import re

    # extract table name from branch_label, e.g. "create_table_foo_bar" -> "foo_bar"
    def extract_table_name(branch_label):
        return re.sub(r'^create_table_', '', branch_label)

%>
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n(none)}
Create Date: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: str = ${repr(down_revision)}
branch_labels: str | Sequence[str] | None = ${repr(branch_labels)}
depends_on: str | Sequence[str] | None = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}