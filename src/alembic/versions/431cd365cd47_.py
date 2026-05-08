"""empty message

Revision ID: 431cd365cd47
Revises: 7d4dae1571fd
Create Date: 2026-05-08 11:12:26.749135

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TSVECTOR

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '431cd365cd47'
down_revision: Union[str, Sequence[str], None] = '7d4dae1571fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column('tasks', sa.Column('search_vector', TSVECTOR, nullable=True))
    op.add_column('projects', sa.Column('search_vector', TSVECTOR, nullable=True))

    op.create_index('idx_tasks_search_vector', 'tasks', ['search_vector'], postgresql_using='gin')
    op.create_index('idx_projects_search_vector', 'projects', ['search_vector'], postgresql_using='gin')

    op.execute(
        """
            CREATE OR REPLACE FUNCTION update_task_search_vector()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.search_vector :=
                    setweight(to_tsvector('english', coalesce(NEW.title, '')), 'A') ||
                    setweight(to_tsvector('english', coalesce(NEW.description, '')), 'B');
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
            CREATE TRIGGER tasks_search_vector_update
            BEFORE INSERT OR UPDATE ON tasks
            FOR EACH ROW EXECUTE FUNCTION update_task_search_vector();
        """
    )

    op.execute(
        """
            CREATE OR REPLACE FUNCTION update_project_search_vector()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.search_vector :=
                    setweight(to_tsvector('english', coalesce(NEW.title, '')), 'A') ||
                    setweight(to_tsvector('english', coalesce(NEW.description, '')), 'B');
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
            CREATE TRIGGER projects_search_vector_update
            BEFORE INSERT OR UPDATE ON projects
            FOR EACH ROW EXECUTE FUNCTION update_project_search_vector();
        """
    )

    op.execute(
        """
            UPDATE tasks SET search_vector =
                setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
                setweight(to_tsvector('english', coalesce(description, '')), 'B')
        """
    )
    op.execute(
        """
            UPDATE projects SET search_vector =
                setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
                setweight(to_tsvector('english', coalesce(description, '')), 'B')
        """
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.execute('DROP TRIGGER IF EXISTS tasks_search_vector_update ON tasks')
    op.execute('DROP TRIGGER IF EXISTS projects_search_vector_update ON tasks')

    op.execute('DROP FUNCTION IF EXISTS update_task_search_vector()')
    op.execute('DROP FUNCTION IF EXISTS update_project_search_vector()')

    op.drop_index('idx_tasks_search_vector', table_name='tasks')
    op.drop_index('idx_projects_search_vector', table_name='projects')

    op.drop_column('tasks', 'search_vector')
    op.drop_column('projects', 'search_vector')
