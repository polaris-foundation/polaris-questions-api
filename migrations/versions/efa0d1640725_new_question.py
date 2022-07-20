"""new question

Revision ID: efa0d1640725
Revises: 14cfdfb9447a
Create Date: 2018-06-19 08:27:41.075751

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from dhos_questions_api.models.question import Question

# revision identifiers, used by Alembic.
revision = 'efa0d1640725'
down_revision = '14cfdfb9447a'
branch_labels = None
depends_on = None

Session = sessionmaker()
bind = op.get_bind()
session = Session(bind=bind)


def upgrade():
    op.add_column('answer', sa.Column(
        'created_by_', sa.String(), nullable=False, server_default='sys'))
    op.add_column('answer', sa.Column(
        'modified_by_', sa.String(), nullable=False, server_default='sys'))

    op.add_column('group', sa.Column(
        'created_by_', sa.String(), nullable=False, server_default='sys'))
    op.add_column('group', sa.Column(
        'modified_by_', sa.String(), nullable=False, server_default='sys'))

    op.add_column('question', sa.Column(
        'created_by_', sa.String(), nullable=False, server_default='sys'))
    op.add_column('question', sa.Column(
        'modified_by_', sa.String(), nullable=False, server_default='sys'))

    op.add_column('question_group', sa.Column(
        'created_by_', sa.String(), nullable=False, server_default='sys'))
    op.add_column('question_group', sa.Column(
        'modified_by_', sa.String(), nullable=False, server_default='sys'))

    op.add_column('question_option', sa.Column(
        'created_by_', sa.String(), nullable=False, server_default='sys'))
    op.add_column('question_option', sa.Column(
        'modified_by_', sa.String(), nullable=False, server_default='sys'))

    op.add_column('question_option_type', sa.Column(
        'created_by_', sa.String(), nullable=False, server_default='sys'))
    op.add_column('question_option_type', sa.Column(
        'modified_by_', sa.String(), nullable=False, server_default='sys'))

    op.add_column('question_type', sa.Column(
        'created_by_', sa.String(), nullable=False, server_default='sys'))
    op.add_column('question_type', sa.Column(
        'modified_by_', sa.String(), nullable=False, server_default='sys'))

    op.add_column('survey', sa.Column(
        'created_by_', sa.String(), nullable=False, server_default='sys'))
    op.add_column('survey', sa.Column(
        'modified_by_', sa.String(), nullable=False, server_default='sys'))

    connection = op.get_bind()
    truncate = ('truncate table "answer" cascade;'
                'truncate table "group" cascade;'
                'truncate table question cascade;'
                'truncate table question_group cascade;'
                'truncate table question_option cascade;'
                'truncate table question_option_type cascade;'
                'truncate table question_type cascade;'
                'truncate table survey cascade;')
    connection.execute(truncate)
    connection.execute("""
        INSERT INTO question_type VALUES ('free_text', '2018-06-19 14:47:23.201704', '2018-06-19 14:47:23.201967', 0, NULL, 'SYSTEM', 'SYSTEM');
        INSERT INTO question_type VALUES ('integer', '2018-06-19 14:47:23.20213', '2018-06-19 14:47:23.202295', 1, NULL, 'SYSTEM', 'SYSTEM');
        INSERT INTO question_type VALUES ('checkbox', '2018-06-19 14:47:23.202457', '2018-06-19 14:47:23.202655', 2, NULL, 'SYSTEM', 'SYSTEM');
        INSERT INTO question_type VALUES ('radio', '2018-06-19 14:47:23.202885', '2018-06-19 14:47:23.203105', 3, NULL, 'SYSTEM', 'SYSTEM');
        INSERT INTO question_type VALUES ('drop_down', '2018-06-19 14:47:23.203316', '2018-06-19 14:47:23.20352', 4, NULL, 'SYSTEM', 'SYSTEM');
        INSERT INTO question_type VALUES ('range', '2018-06-19 14:47:23.203716', '2018-06-19 14:47:23.203909', 5, NULL, 'SYSTEM', 'SYSTEM');
        INSERT INTO question_type VALUES ('multi_select', '2018-06-19 14:47:23.204103', '2018-06-19 14:47:23.204299', 6, NULL, 'SYSTEM', 'SYSTEM');

        INSERT INTO question_option_type VALUES ('fixed', '2018-06-19 14:47:23.196447', '2018-06-19 14:47:23.196786', 0, NULL, 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option_type VALUES ('free_text', '2018-06-19 14:47:23.197014', '2018-06-19 14:47:23.197234', 1, NULL, 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option_type VALUES ('range_start', '2018-06-19 14:47:23.19745', '2018-06-19 14:47:23.197635', 2, NULL, 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option_type VALUES ('range_end', '2018-06-19 14:47:23.197829', '2018-06-19 14:47:23.198016', 3, NULL, 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option_type VALUES ('interval', '2018-06-19 14:47:23.198203', '2018-06-19 14:47:23.198391', 4, NULL, 'SYSTEM', 'SYSTEM');

        INSERT INTO "group" VALUES ('66854d92-616f-4f98-ab32-b396ffa0e94e', '2018-06-19 14:47:23.220197', '2018-06-19 14:47:23.220451', 'patient_satisfaction_survey', NULL, 'SYSTEM', 'SYSTEM');

        INSERT INTO question VALUES ('0ec8e6f9-97d4-4531-88cf-bfd4acee4b24', '2018-06-19 14:47:23.22216', '2018-06-19 14:47:23.222334', 'I am satisfied with my current treatment.', NULL, 'range', 'SYSTEM', 'SYSTEM');
        INSERT INTO question VALUES ('c77a2c51-b638-48dc-bbc6-4f33f301a889', '2018-06-19 14:47:23.247876', '2018-06-19 14:47:23.248108', 'I am satisfied that the treatment I am receiveing is the best for me.', NULL, 'range', 'SYSTEM', 'SYSTEM');
        INSERT INTO question VALUES ('1895cd66-467f-47d6-ac7b-d070d0c1c6b3', '2018-06-19 14:47:23.274356', '2018-06-19 14:47:23.27464', 'I am satisfied with my understanding of diabetes.', NULL, 'range', 'SYSTEM', 'SYSTEM');
        INSERT INTO question VALUES ('dbb4a586-c8e7-4cc3-a0ee-1569e5e081bf', '2018-06-19 14:47:23.296559', '2018-06-19 14:47:23.296768', 'I feel my maternity diabetes team knows enough about my current level of diabetes control.', NULL, 'range', 'SYSTEM', 'SYSTEM');
        INSERT INTO question VALUES ('f22edd8a-e94f-43cd-a965-a28f6190585d', '2018-06-19 14:47:23.316897', '2018-06-19 14:47:23.317133', 'I feel I have a good relationship with my maternity diabetes team.', NULL, 'range', 'SYSTEM', 'SYSTEM');
        INSERT INTO question VALUES ('09dbfa8e-be83-489e-8724-470530ebd8ca', '2018-06-19 14:47:23.337466', '2018-06-19 14:47:23.337664', 'I am satisfied with my maternity diabetes team''s understanding of my diabetes.', NULL, 'range', 'SYSTEM', 'SYSTEM');
        INSERT INTO question VALUES ('39339d8b-87aa-4e92-af77-a616229acfb1', '2018-06-19 14:47:23.359264', '2018-06-19 14:47:23.359458', 'I find the equipment I use to check my blood sugars is convenient.', NULL, 'range', 'SYSTEM', 'SYSTEM');
        INSERT INTO question VALUES ('dee1ce2c-ac4f-4b12-8bbe-bfc4413f3bc9', '2018-06-19 14:47:23.378382', '2018-06-19 14:47:23.378597', 'I feel the equipment I use to check my blood sugars is reliable.', NULL, 'range', 'SYSTEM', 'SYSTEM');
        INSERT INTO question VALUES ('cf1dcb4f-71eb-4420-b321-65efc47562a9', '2018-06-19 14:47:23.399469', '2018-06-19 14:47:23.399728', 'My blood sugar monitoring fits with my lifestyle.', NULL, 'range', 'SYSTEM', 'SYSTEM');
        INSERT INTO question VALUES ('d8568cc0-3c3a-4c84-872b-1e245f2ca582', '2018-06-19 14:47:23.42286', '2018-06-19 14:47:23.423043', 'I enjoy using this app.', NULL, 'range', 'SYSTEM', 'SYSTEM');

        INSERT INTO question_group VALUES ('0ec8e6f9-97d4-4531-88cf-bfd4acee4b24', '66854d92-616f-4f98-ab32-b396ffa0e94e', 'sys', 'sys');
        INSERT INTO question_group VALUES ('c77a2c51-b638-48dc-bbc6-4f33f301a889', '66854d92-616f-4f98-ab32-b396ffa0e94e', 'sys', 'sys');
        INSERT INTO question_group VALUES ('1895cd66-467f-47d6-ac7b-d070d0c1c6b3', '66854d92-616f-4f98-ab32-b396ffa0e94e', 'sys', 'sys');
        INSERT INTO question_group VALUES ('dbb4a586-c8e7-4cc3-a0ee-1569e5e081bf', '66854d92-616f-4f98-ab32-b396ffa0e94e', 'sys', 'sys');
        INSERT INTO question_group VALUES ('f22edd8a-e94f-43cd-a965-a28f6190585d', '66854d92-616f-4f98-ab32-b396ffa0e94e', 'sys', 'sys');
        INSERT INTO question_group VALUES ('09dbfa8e-be83-489e-8724-470530ebd8ca', '66854d92-616f-4f98-ab32-b396ffa0e94e', 'sys', 'sys');
        INSERT INTO question_group VALUES ('39339d8b-87aa-4e92-af77-a616229acfb1', '66854d92-616f-4f98-ab32-b396ffa0e94e', 'sys', 'sys');
        INSERT INTO question_group VALUES ('dee1ce2c-ac4f-4b12-8bbe-bfc4413f3bc9', '66854d92-616f-4f98-ab32-b396ffa0e94e', 'sys', 'sys');
        INSERT INTO question_group VALUES ('cf1dcb4f-71eb-4420-b321-65efc47562a9', '66854d92-616f-4f98-ab32-b396ffa0e94e', 'sys', 'sys');
        INSERT INTO question_group VALUES ('d8568cc0-3c3a-4c84-872b-1e245f2ca582', '66854d92-616f-4f98-ab32-b396ffa0e94e', 'sys', 'sys');

        INSERT INTO question_option VALUES ('934f22a2-2025-4b53-8f4d-752872d0dc55', '2018-06-19 14:47:23.225897', '2018-06-19 14:47:23.226156', 'Strongly Disagree', '1', NULL, NULL, '0ec8e6f9-97d4-4531-88cf-bfd4acee4b24', 'range_start', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('a60ef76c-9bc4-4ab3-b79a-bd81ede539a1', '2018-06-19 14:47:23.226347', '2018-06-19 14:47:23.226558', 'Strongly Agree', '5', NULL, NULL, '0ec8e6f9-97d4-4531-88cf-bfd4acee4b24', 'range_end', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('449128cb-cab7-4ca4-b8bf-3dc5fa7e8966', '2018-06-19 14:47:23.226789', '2018-06-19 14:47:23.226957', NULL, '1', NULL, NULL, '0ec8e6f9-97d4-4531-88cf-bfd4acee4b24', 'interval', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('7d4ec6a2-22dc-490a-b529-2679961ed038', '2018-06-19 14:47:23.24966', '2018-06-19 14:47:23.249992', 'Strongly Disagree', '1', NULL, NULL, 'c77a2c51-b638-48dc-bbc6-4f33f301a889', 'range_start', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('0cfbf815-cfeb-46b1-a153-c1b4f57b7570', '2018-06-19 14:47:23.250301', '2018-06-19 14:47:23.250519', 'Strongly Agree', '5', NULL, NULL, 'c77a2c51-b638-48dc-bbc6-4f33f301a889', 'range_end', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('0122b1ec-825d-473a-af54-92a9081af84a', '2018-06-19 14:47:23.250743', '2018-06-19 14:47:23.250933', NULL, '1', NULL, NULL, 'c77a2c51-b638-48dc-bbc6-4f33f301a889', 'interval', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('a87848c5-189d-4568-94b1-9ef316d3b6a4', '2018-06-19 14:47:23.276571', '2018-06-19 14:47:23.276834', 'Strongly Disagree', '1', NULL, NULL, '1895cd66-467f-47d6-ac7b-d070d0c1c6b3', 'range_start', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('672a24d5-d66d-49d2-a3d5-922eb3b2eb23', '2018-06-19 14:47:23.277107', '2018-06-19 14:47:23.277309', 'Strongly Agree', '5', NULL, NULL, '1895cd66-467f-47d6-ac7b-d070d0c1c6b3', 'range_end', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('57e54cc6-115d-4237-b3d9-c66fa95fe74a', '2018-06-19 14:47:23.277493', '2018-06-19 14:47:23.277688', NULL, '1', NULL, NULL, '1895cd66-467f-47d6-ac7b-d070d0c1c6b3', 'interval', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('f8d84167-ff55-4644-883b-2c63d0a24f8c', '2018-06-19 14:47:23.298593', '2018-06-19 14:47:23.298764', 'Strongly Disagree', '1', NULL, NULL, 'dbb4a586-c8e7-4cc3-a0ee-1569e5e081bf', 'range_start', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('80b6d9a8-7457-49e5-8626-fe64865fb18a', '2018-06-19 14:47:23.299024', '2018-06-19 14:47:23.299228', 'Strongly Agree', '5', NULL, NULL, 'dbb4a586-c8e7-4cc3-a0ee-1569e5e081bf', 'range_end', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('e184b7f8-90ef-4f75-9f57-d278a71f309a', '2018-06-19 14:47:23.299438', '2018-06-19 14:47:23.299621', NULL, '1', NULL, NULL, 'dbb4a586-c8e7-4cc3-a0ee-1569e5e081bf', 'interval', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('7373823a-a68b-4c2f-8da2-107d95344ba7', '2018-06-19 14:47:23.318889', '2018-06-19 14:47:23.3191', 'Strongly Disagree', '1', NULL, NULL, 'f22edd8a-e94f-43cd-a965-a28f6190585d', 'range_start', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('f5c9e504-eef7-45d7-9014-39fa1fe55c91', '2018-06-19 14:47:23.319225', '2018-06-19 14:47:23.319342', 'Strongly Agree', '5', NULL, NULL, 'f22edd8a-e94f-43cd-a965-a28f6190585d', 'range_end', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('25c6d3a9-9da9-4ce6-9fae-4108fcfcd0cd', '2018-06-19 14:47:23.319465', '2018-06-19 14:47:23.31957', NULL, '1', NULL, NULL, 'f22edd8a-e94f-43cd-a965-a28f6190585d', 'interval', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('b8706caa-6e68-4d81-9687-20b3bc5f4e23', '2018-06-19 14:47:23.339511', '2018-06-19 14:47:23.339715', 'Strongly Disagree', '1', NULL, NULL, '09dbfa8e-be83-489e-8724-470530ebd8ca', 'range_start', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('43ded548-514a-4ed8-863d-b84c634360fc', '2018-06-19 14:47:23.339997', '2018-06-19 14:47:23.340252', 'Strongly Agree', '5', NULL, NULL, '09dbfa8e-be83-489e-8724-470530ebd8ca', 'range_end', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('d9bec6bc-10fc-4c04-b8ae-a27b5f950be3', '2018-06-19 14:47:23.34043', '2018-06-19 14:47:23.34058', NULL, '1', NULL, NULL, '09dbfa8e-be83-489e-8724-470530ebd8ca', 'interval', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('a6a02cec-f41b-4f32-a1c1-0e226822eb74', '2018-06-19 14:47:23.360769', '2018-06-19 14:47:23.360959', 'Strongly Disagree', '1', NULL, NULL, '39339d8b-87aa-4e92-af77-a616229acfb1', 'range_start', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('2c4fd81f-102f-4efe-98f0-79db94c897a0', '2018-06-19 14:47:23.361211', '2018-06-19 14:47:23.361375', 'Strongly Agree', '5', NULL, NULL, '39339d8b-87aa-4e92-af77-a616229acfb1', 'range_end', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('eaf39588-da8e-4f8d-98d4-21567408142e', '2018-06-19 14:47:23.361571', '2018-06-19 14:47:23.361756', NULL, '1', NULL, NULL, '39339d8b-87aa-4e92-af77-a616229acfb1', 'interval', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('9bf6f373-e7b2-4c67-8c66-1411e11fc312', '2018-06-19 14:47:23.380499', '2018-06-19 14:47:23.380678', 'Strongly Disagree', '1', NULL, NULL, 'dee1ce2c-ac4f-4b12-8bbe-bfc4413f3bc9', 'range_start', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('80fec7d6-6de1-4fba-9bac-9d09f9948dd9', '2018-06-19 14:47:23.380877', '2018-06-19 14:47:23.381027', 'Strongly Agree', '5', NULL, NULL, 'dee1ce2c-ac4f-4b12-8bbe-bfc4413f3bc9', 'range_end', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('ea6bf899-0a12-4411-8819-9d673fbb2771', '2018-06-19 14:47:23.381193', '2018-06-19 14:47:23.38136', NULL, '1', NULL, NULL, 'dee1ce2c-ac4f-4b12-8bbe-bfc4413f3bc9', 'interval', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('39e3ecc0-0a44-4472-b4b1-d5cbf80617a5', '2018-06-19 14:47:23.401674', '2018-06-19 14:47:23.401975', 'Strongly Disagree', '1', NULL, NULL, 'cf1dcb4f-71eb-4420-b321-65efc47562a9', 'range_start', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('6edbced7-03f8-4345-b0a9-f7f3a491b251', '2018-06-19 14:47:23.402216', '2018-06-19 14:47:23.402432', 'Strongly Agree', '5', NULL, NULL, 'cf1dcb4f-71eb-4420-b321-65efc47562a9', 'range_end', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('a417af00-8c56-4b4c-8b3c-31c3c9aebeb9', '2018-06-19 14:47:23.402581', '2018-06-19 14:47:23.402734', NULL, '1', NULL, NULL, 'cf1dcb4f-71eb-4420-b321-65efc47562a9', 'interval', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('ed047c6b-fd55-4dc4-9f48-85d3453bcb72', '2018-06-19 14:47:23.424315', '2018-06-19 14:47:23.424468', 'Strongly Disagree', '1', NULL, NULL, 'd8568cc0-3c3a-4c84-872b-1e245f2ca582', 'range_start', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('b2d0070d-da15-455e-85e3-f28777e01091', '2018-06-19 14:47:23.424638', '2018-06-19 14:47:23.424877', 'Strongly Agree', '5', NULL, NULL, 'd8568cc0-3c3a-4c84-872b-1e245f2ca582', 'range_end', 'SYSTEM', 'SYSTEM');
        INSERT INTO question_option VALUES ('0a2cc5e5-0015-465b-98d7-f5168af914d5', '2018-06-19 14:47:23.425065', '2018-06-19 14:47:23.425282', NULL, '1', NULL, NULL, 'd8568cc0-3c3a-4c84-872b-1e245f2ca582', 'interval', 'SYSTEM', 'SYSTEM');
    """)


def downgrade():
    q = Question.filter_by(question="I enjoy using this app.")
    q.delete()
    session.commit()
