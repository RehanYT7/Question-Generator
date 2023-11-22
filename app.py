from flask import Flask, jsonify
from werkzeug.exceptions import RequestEntityTooLarge, NotFound, BadRequest, InternalServerError
from interview_questions_generator import InterviewDataProcessor

app = Flask(__name__)

# Create an instance of InterviewDataProcessor
processor = InterviewDataProcessor('config.json')

# Custom exception for invalid configuration
class InvalidConfigurationException(Exception):
    pass

@app.route('/generate_interview_questions', methods=['GET'])
def generate_interview_questions():
    try:
        result = processor.process_interview_data()
        return result
    except RequestEntityTooLarge:
        # HTTP error code occurs when the size of a client's request exceeds the server's file size limit
        return jsonify({"message": "The request entity is too large."}), 413
    except NotFound:
        # HTTP error code occurs when a user attempts to access a webpage that does not exist, has been moved, or has a dead or broken link
        return jsonify({"message": "Resource not found."}), 404
    except BadRequest:
        # HTTP Bad Request response status code indicates that the server cannot or will not process the request due to something that is perceived to be a client error
        return jsonify({"message": "Bad request."}), 400
    except InvalidConfigurationException as e:
        # HTTP error code occurs when there is an Invalid configuration of server or connectivity
        return jsonify({"message": "Invalid configuration.", "error": str(e)}), 400
    except InternalServerError:
        # HTTP error code occurs when the server has encountered an unexpected condition or configuration problem that prevents it from fulfilling the request made by the browser or client
        return jsonify({"message": "Internal Server Error."}), 500
    except Exception as e:
        return jsonify({"message": "Internal Server Error.", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
