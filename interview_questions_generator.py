import json
import logging
import os
import re
import datetime
import time

import pandas as pd
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, TIMESTAMP, delete


class InterviewDataProcessor:
    def __init__(self, config_file_path, log_file_path='std.log'):
        self.config_file_path = config_file_path
        self.log_file_path = log_file_path
        self.load_config()
        self.setup_logging()
        self.setup_database_connection()

    def load_config(self):
        with open(self.config_file_path, 'r') as config_file:
            self.config = json.load(config_file)

    def setup_logging(self):
        logging.basicConfig(filename=self.log_file_path,
                            format='\n%(asctime)s - %(name)s - %(levelname)s - %(message)s', filemode='a')
        self.logger = logging.getLogger("InterviewDataProcessor")
        self.logger.setLevel(logging.INFO)

    def setup_database_connection(self):
        self.openai_key = self.config['OpenAI']['api_key']
        self.host = self.config['MySQL']['server']
        self.database = self.config['MySQL']['database']
        self.user = self.config['MySQL']['username']
        self.password = self.config['MySQL']['password']
        self.engine = create_engine(f"mysql+mysqlconnector://{self.user}:{self.password}@{self.host}/{self.database}")
        self.connection = self.engine.connect()
        self.metadata = MetaData()

    def delete_old_records(self, timestamp):
        try:
            table = Table('interview_questions_generated', self.metadata, autoload=True)
            if table is not None:
                stmt = delete(table).where(table.c.time_stamp < timestamp)
                self.connection.execute(stmt)
                self.connection.commit()
                self.logger.info(f"Deleted old records before {timestamp}")
            else:
                self.logger.error("The 'interview_questions_generated' table does not exist in the database.")
        except Exception as e:
            self.logger.error(f"An exception occurred while deleting old records: {str(e)}")

    def generate_questions(self, skill, level, number_of_questions):
        try:
            os.environ['OPENAI_API_KEY'] = self.openai_key
            prompt_parameter_names = PromptTemplate(
                input_variables=['skill', 'Number_of_questions', 'Level_of_questions'],
                template="""Please generate {Number_of_questions} multiple choice questions with their Correct answer for {skill}. The questions should be fairly complex and targeted at highly skilled and experienced developers of {skill} with {Level_of_questions} {skill} development skills. These questions should enable distinguishing experienced developers from {Level_of_questions} level developers."""
            )
            llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.7)
            chain1 = LLMChain(llm=llm, prompt=prompt_parameter_names)

            prompt = prompt_parameter_names.format_prompt(
                skill=skill,
                Number_of_questions=number_of_questions,
                Level_of_questions=level)

            self.logger.info(f"Generated Prompt for {skill}: {prompt}")
            result = chain1.run(
                {'skill': skill, 'Number_of_questions': number_of_questions, 'Level_of_questions': level})
            self.logger.info(f"Generated Questions for {skill}: {result}")

            # Extract and format correct answers
            pattern_for_correct_answer = r'(Correct answer|Answer|Explanation):(.+)'
            correct_answers = re.findall(pattern_for_correct_answer, result)
            correct_answers_str = "; ".join(answer.strip() for _, answer in correct_answers)

            # Remove correct answers from questions
            final_result = re.sub(pattern_for_correct_answer, '', result).strip()

            return final_result, correct_answers_str
        except Exception as e:
            self.logger.error(f"An Exceptional error occurred for {skill}: {str(e)}")
            return None, None

    def process_interview_data(self):
        input_table_query = "SELECT * FROM interview_details"
        df_input_table = pd.read_sql(input_table_query, self.engine)

        interview_questions_generated = Table(
            'interview_questions_generated',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('skill', String),
            Column('level_of_question', String),
            Column('questions', String),
            Column('answers', String),
            Column('time_stamp', TIMESTAMP),
            mysql_bind=self.engine)

        deletion_threshold = datetime.datetime.now() - datetime.timedelta(days=2)
        # deletion_threshold = datetime.datetime.now()
        # Delete old records
        self.delete_old_records(deletion_threshold)

        for index, row in df_input_table.iterrows():
            row

        for skill_num in range(1, 4):
            start_time = time.time()
            skill_column = f'skill_{skill_num}'
            level_column = f'level_of_question_skill{skill_num}'

            skill = row[skill_column]
            level = row[level_column]

            if skill is not None:
                query = f"SELECT * FROM interview_questions_generated WHERE skill='{skill}' AND level_of_question='{level}'"
                existing_questions = pd.read_sql(query, self.engine)

                if existing_questions.empty:
                    questions, answers = self.generate_questions(skill, level, row['number_of_questions'])
                    if questions is not None and answers is not None:
                        self.connection.execute(interview_questions_generated.insert().values(
                                skill=skill, level_of_question=level, questions=questions, answers=answers,
                                time_stamp=datetime.datetime.now()))
                        self.connection.commit()
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Execution time of Skill-{skill_num}: {elapsed_time} seconds")

        self.connection.close()
        return "Interview questions generated"


if __name__ == "__main__":
    processor = InterviewDataProcessor('config.json')
    processor.process_interview_data()
