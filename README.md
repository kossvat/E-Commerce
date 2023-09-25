# Django Auctions

Django Auctions is a web application that allows users to create, bid on, and manage auction listings.

## Features

- **User Authentication**: Register, log in, and log out functionalities.
- **Auction Listings**: Create, view, and edit auction listings.
- **Bidding System**: Place bids on active listings.
- **Watchlist**: Users can add and remove listings to/from their watchlist.
- **Categories**: View listings by categories.
- **End Auction**: Auction creators or admins can end an auction early.

## Demo

Check out the video demo of the website: [Watch the video](https://youtu.be/03pXBFBR0wA)


## Installation & Setup

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your_username/repository_name.git
    cd repository_name
    ```

2. **Set Up a Virtual Environment**:
    ```bash
    python -m venv my_env
    source my_env/bin/activate  # On Windows use `my_env\Scripts\activate`
    ```

3. **Install Required Packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Database Migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Run the Development Server**:
    ```bash
    python manage.py runserver
    ```

## Usage

- Visit `http://127.0.0.1:8000/` in your browser to access the application.
- Register as a new user or log in.
- Navigate the site using the provided links and buttons to create listings, place bids, view categories, and more.

## Contribution

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

