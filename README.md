# Interview Questions Generator
## Overview
The Interview Questions Generator is a Python script that automates the process of generating interview questions using the OpenAI API and stores the results in a MySQL database. This tool is designed to assist in creating challenging and skill-specific questions for interviews, targeting experienced developers in various domains.

## Getting Started
### Prerequisites
1. Python 3.x installed

2. Dependencies listed in requirements.txt installed

3. Access to a MySQL database

4. OpenAI API key

### Installation
#### 1. Clone the repository:
   git clone - https://github.com/RehanYT7/Question-Generator.git
#### 2. Install dependencies:
pip install -r requirements.txt
### Configuration
#### Create a configuration file named config.json in the root directory with the following format:

      { 

        "MySQL": {
  
          "server": "localhost",
    
          "database": "your_database_name",
    
          "username": "your_mysql_username",
    
          "password": "your_mysql_password"
    
      },
  
      "OpenAI": {
  
          "api_key": "your_openai_api_key"
    
         }
  
      }

### Code Explaination
#### Class: InterviewDataProcessor
This class is designed to handle the processing of interview data, including the generation of interview questions using the OpenAI API and the storage of generated questions and answers in a MySQL database.
#### __init__(self, config_file_path, log_file_path='std.log')
Constructor method that initializes an instance of the InterviewDataProcessor class.

Parameters:

      config_file_path: Path to the configuration file (config.json).

      log_file_path: Path to the log file (default is 'std.log').
#### load_config(self)
Method to load the configuration from the specified config_file_path (assumed to be in JSON format).

#### setup_logging(self)

Method to set up logging configuration. It configures a logger named "InterviewDataProcessor" to log messages to a file specified by log_file_path.

#### setup_database_connection(self)
Method to set up the database connection using information from the loaded configuration.
It establishes a connection to a MySQL database using the sqlalchemy library.

#### delete_old_records(self, timestamp)

Method to delete old records from the interview_questions_generated table in the MySQL database based on a given timestamp.
It uses the sqlalchemy library to execute a SQL DELETE statement.

#### generate_questions(self, skill, level, number_of_questions)

Method to generate interview questions using the OpenAI API.
It uses the langchain library for natural language processing.
The method sets the OpenAI API key in the environment variable, defines a prompt template, and uses the GPT-3.5-turbo model to generate questions.
Extracts correct answers from the generated text using regular expressions.

#### process_interview_data(self)
Main method to process interview data.
It reads input data from a MySQL table named interview_details using pandas.
Defines the schema for the interview_questions_generated table and deletes old records.
Iterates over skills and skill levels, generates questions if they don't exist in the database, and inserts them into the interview_questions_generated table.
Prints the execution time for each skill.

### Main Block
The script includes a main block that creates an instance of InterviewDataProcessor and calls the process_interview_data method.

      if __name__ == "__main__":
      processor = InterviewDataProcessor('config.json')
      processor.process_interview_data()
### Database Schema
The script uses a MySQL database with the following table schema:

      CREATE TABLE interview_questions_generated (
     id INT PRIMARY KEY AUTO_INCREMENT,
     skill VARCHAR(255),
     level_of_question VARCHAR(255),
     questions TEXT,
     answers TEXT,
     time_stamp TIMESTAMP
      );
This table structure stores information about the generated interview questions, including the skill, skill level, actual questions, correct answers, and the timestamp of the generation.

### Summary
The script performs the following steps:

#### Load Configuration:

Loads configuration settings from config.json.
#### Setup Logging:

Initializes logging to a file specified in the configuration.
#### Database Connection:

Establishes a connection to the MySQL database using the provided credentials.
#### Delete Old Records:

Deletes old records from the interview_questions_generated table based on a specified timestamp. This helps maintain a relevant dataset.
#### Generate Interview Questions:

Iterates over the input data, generating interview questions for each skill and skill level using the OpenAI API.
#### Insert into Database:

Inserts the generated questions and answers into the interview_questions_generated table along with a timestamp.


 
