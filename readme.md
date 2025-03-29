# Django Project

## Installation

Follow these steps to set up the project locally:

```sh
# Clone the repository
git clone https://github.com/justinnonso05/VoteSpark.git


# Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run the development server
python manage.py runserver
