# Interview Questions Generator
## Overview
The Interview Questions Generator is a Python script that automates the process of generating interview questions using the OpenAI API and stores the results in a MySQL database. This tool is designed to assist in creating challenging and skill-specific questions for interviews, targeting experienced developers in various domains.

## Getting Started
### Prerequisites
Python 3.x installed
Dependencies listed in requirements.txt installed
Access to a MySQL database
OpenAI API key
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



 
