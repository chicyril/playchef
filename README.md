# PlayChef

PlayChef is a web application that allows users to
discover, save, and share their favorite recipes.
With a user-friendly interface and a vast collection
of recipes, PlayChef aims to inspire and empower home
cooks to explore new culinary adventures.

## Features

- Recipe Filter: Users can filter and view recipes by
  categories.
- Recipe Details: Each recipe includes detailed instructions,
  ingredients and steps.
- Save and Favorite: Users can save their favorite recipes for
  quick access in the future.

#### Upcoming Features

- Recipe Searche: Users can search for recipes based on
  keywords, ingredients, or dietary preferences.
- Share: Users can share recipes with friends and family
  through social media platforms.
- Recipe Details: Recipe details will contain cooking 
  time, and nutritional information.
- User Profiles: Users can create profiles, customize their
  preferences, and track their cooking journey.

## Technologies Used

- Front-end: HTML, CSS, JavaScript
- Back-end: Python, Flask
- Database: MySQL, SQLAlchemy

## Download and setup

To download and setup the PlayChef web application, follow
these steps:

1. Clone the repository:  
   `git clone https://github.com/chicyril/playchef.git`
2. Create and activate a python virtual environment:  
   `python3 -m venv <venv>`  
   `source <venv>/bin/activate`
3. Install the dependencies:  
   `pip3 install -r requirements.txt`
4. Navigate to the project directory: `cd playchef`
5. Modify the file `app/app_config.py` to set
   configuration settings to your preference or leave
   default.
6. Setup the database: See [Database Setup](#database-setup).

## Database Setup

To set up the database for PlayChef, follow these steps:

1. Make sure you have MySQL installed and running on
   your machine.
2. Make sure you're in the `Playchef` directory.
3. Run the following command on the terminal to set up
   database:
   > First, make sure the value for any database config settings modified in `app/app_config.py` is substituted in the `models/storage/setup_playchef_db.sql` file.

    `cat models/storage/setup_playchef_db.sql | sudo mysql` or  
    `cat models/storage/setup_playchef_db.sql | mysql -u<user> -p`

## Starting the Application and Testing

To start the PlayChef application, follow these steps:

- Make sure the virtual environment is activated:
  `source <venv>/bin/activate`
- Start the application: `python3 -m app.run`
- Open your web browser and navigate to `http://localhost:5000/home` to access the PlayChef application.

## Contributing

We welcome contributions from the community to enhance PlayChef. To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch:
  `git checkout -b feature/your-feature`  
3. Make your changes and commit them:
  `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or feedback, Send me a mail: [Mail](mailto:cyrildaniels20@gmail.com)
