# Clothify

Clothify is a Django clothing e-commerce project with product browsing, customer accounts, saved delivery addresses, and a shopping cart. It includes checkout, payment selection, and order pages that are still under development.

## Features

- Browse products by category: Sleeves, Shirts, Shorts, and Jackets.
- View product images, descriptions, and regular and discounted prices.
- Register, sign in, change passwords, and access password reset pages.
- Create, update, and delete customer delivery addresses with Philippine province choices.
- Add products to the cart, update quantities, and remove items.
- View checkout totals and select Cash on Delivery or Pick Up on the payment form.
- Manage products, customers, carts, payments, and order records through Django Admin.

## Tech stack

| Component | Technology |
| --- | --- |
| Backend | Python and Django 4.2 |
| Database | SQLite |
| Frontend | Django templates, Bootstrap 5.3.2, jQuery 3.7.1, and custom CSS/JavaScript |
| Product images | Pillow and Django media uploads |

The existing local environment uses Python 3.12.10, Django 4.2.30, and Pillow 13.0.0. Bootstrap and jQuery load from CDNs, so an internet connection is needed for those assets.

## Local setup

Run the following commands in **PowerShell**, starting from the repository root (`Clothify-Ecomm`). Python 3.12 and pip should be installed.

### 1. Create a virtual environment and install dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install "Django==4.2.30" "Pillow==13.0.0"
```

If a working `.venv` already exists, skip creating it. These commands use the virtual environment's Python directly, so activation is optional. There is currently no `requirements.txt` in the repository.

### 2. Apply database migrations

```powershell
.\.venv\Scripts\python.exe ec/manage.py migrate
```

The database is stored at `ec/db.sqlite3`. If you are using an existing database, back it up before applying migrations. A new database will need products added through the admin interface.

### 3. Create an administrator account

```powershell
.\.venv\Scripts\python.exe ec/manage.py createsuperuser
```

Choose your own username and password when prompted.

### 4. Start the development server

```powershell
.\.venv\Scripts\python.exe ec/manage.py runserver
```

Open [Clothify](http://127.0.0.1:8000/) or [Django Admin](http://127.0.0.1:8000/admin/). Press `Ctrl+C` in the terminal to stop the server.

## Using the project

1. Sign in to `/admin/` with your administrator account and add products with images, prices, descriptions, and categories.
2. Register a customer at `/registration/` and sign in at `/account/login/`.
3. Save a delivery address at `/profile/`; manage saved addresses at `/address/`.
4. Browse a category, open a product, and add it to the cart.
5. Open `/cart/` to adjust quantities, then proceed to `/checkout/`.

Uploaded product images are stored in `ec/media/product/` and served under `/media/` during local development.

## Project structure

```text
Clothify-Ecomm/
|-- README.md
|-- ec/
|   |-- manage.py
|   |-- db.sqlite3             # Local SQLite database
|   |-- ec/                    # Django project configuration
|   |   |-- settings.py
|   |   |-- urls.py
|   |   |-- asgi.py
|   |   `-- wsgi.py
|   |-- app/                   # Store application
|   |   |-- admin.py
|   |   |-- forms.py
|   |   |-- models.py
|   |   |-- urls.py
|   |   |-- views.py
|   |   |-- migrations/
|   |   |-- templates/app/
|   |   `-- static/app/
|   `-- media/product/         # Uploaded product images
`-- .venv/                     # Local Python environment, if created
```

## Development checks

```powershell
.\.venv\Scripts\python.exe ec/manage.py check
```

This runs Django's system checks. The current `app/tests.py` contains no test cases, so it does not provide automated coverage of shopping or checkout behavior.

## Current limitations

- Payment form submission does not yet save or process a payment, and no online payment gateway is connected.
- Order placement is unfinished: `/checkout/` is declared twice, the active checkout view only renders order information on submission, and the alternate order-placement function references an undefined `AddressModel`. Treat checkout and order pages as a work in progress.
- Cart and checkout calculations currently add a fixed amount of `100` to the product subtotal.
- Password reset uses the console email backend. Email output goes to the server terminal; outbound email is not configured. The default password reset email template is also absent, so the full reset flow needs completion.
- Settings are configured for local development (`DEBUG=True`, a development secret key, and SQLite). Production deployment requires separate configuration and a review of authentication and ownership checks on customer and cart actions.
