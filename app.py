from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, date
from sqlalchemy import func
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# =========================
# LOAD ENVIRONMENT VARIABLES
# =========================

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = "change-this-secret-key-in-production"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expense_tracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# =========================
# EMAIL CONFIGURATION
# =========================

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True

app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")

mail = Mail(app)

db = SQLAlchemy(app)


# =========================
# DATABASE MODELS
# =========================

class User(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    transactions = db.relationship(
        "Transaction",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Transaction(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    type = db.Column(
        db.String(20),
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    transaction_date = db.Column(
        db.Date,
        nullable=False,
        default=date.today
    )

    note = db.Column(
        db.String(300)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# =========================
# LOGIN PROTECTION
# =========================

def login_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            return redirect(url_for("login"))

        return f(*args, **kwargs)

    return wrapper


# =========================
# CONSTANTS
# =========================

CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Education",
    "Entertainment",
    "Health",
    "Travel",
    "Salary",
    "Other"
]


# =========================
# HOME
# =========================

@app.route("/")
def index():

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm = request.form.get(
            "confirm_password",
            ""
        )

        if not name or not email or not password:

            flash(
                "Please fill in all required fields.",
                "error"
            )

        elif password != confirm:

            flash(
                "Passwords do not match.",
                "error"
            )

        elif len(password) < 6:

            flash(
                "Password must contain at least 6 characters.",
                "error"
            )

        elif User.query.filter_by(
            email=email
        ).first():

            flash(
                "An account with this email already exists.",
                "error"
            )

        else:

            user = User(
                name=name,
                email=email,
                password_hash=generate_password_hash(
                    password
                )
            )

            db.session.add(user)
            db.session.commit()

            flash(
                "Account created successfully. Please log in.",
                "success"
            )

            return redirect(
                url_for("login")
            )

    return render_template(
        "register.html"
    )


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        user = User.query.filter_by(
            email=email
        ).first()

        if user and check_password_hash(
            user.password_hash,
            password
        ):

            session["user_id"] = user.id
            session["user_name"] = user.name

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid email or password.",
            "error"
        )

    return render_template(
        "login.html"
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
@login_required
def dashboard():

    user_id = session["user_id"]

    transactions = (
        Transaction.query
        .filter_by(user_id=user_id)
        .order_by(
            Transaction.transaction_date.desc(),
            Transaction.id.desc()
        )
        .all()
    )

    income = db.session.query(
        func.coalesce(
            func.sum(Transaction.amount),
            0
        )
    ).filter_by(
        user_id=user_id,
        type="income"
    ).scalar()

    expense = db.session.query(
        func.coalesce(
            func.sum(Transaction.amount),
            0
        )
    ).filter_by(
        user_id=user_id,
        type="expense"
    ).scalar()

    balance = income - expense

    current_month = date.today().strftime(
        "%Y-%m"
    )

    monthly_income = db.session.query(
        func.coalesce(
            func.sum(Transaction.amount),
            0
        )
    ).filter(
        Transaction.user_id == user_id,
        Transaction.type == "income",
        func.strftime(
            "%Y-%m",
            Transaction.transaction_date
        ) == current_month
    ).scalar()

    monthly_expense = db.session.query(
        func.coalesce(
            func.sum(Transaction.amount),
            0
        )
    ).filter(
        Transaction.user_id == user_id,
        Transaction.type == "expense",
        func.strftime(
            "%Y-%m",
            Transaction.transaction_date
        ) == current_month
    ).scalar()

    monthly_balance = (
        monthly_income - monthly_expense
    )

    return render_template(
        "dashboard.html",
        transactions=transactions[:10],
        income=income,
        expense=expense,
        balance=balance,
        monthly_income=monthly_income,
        monthly_expense=monthly_expense,
        monthly_balance=monthly_balance,
        categories=CATEGORIES,
        today=date.today().isoformat()
    )


# =========================
# TRANSACTIONS
# =========================

@app.route("/transactions")
@login_required
def transactions():

    q = request.args.get(
        "q",
        ""
    ).strip()

    category = request.args.get(
        "category",
        ""
    ).strip()

    ttype = request.args.get(
        "type",
        ""
    ).strip()

    query = Transaction.query.filter_by(
        user_id=session["user_id"]
    )

    if q:

        query = query.filter(
            Transaction.title.ilike(
                f"%{q}%"
            )
        )

    if category:

        query = query.filter_by(
            category=category
        )

    if ttype in (
        "income",
        "expense"
    ):

        query = query.filter_by(
            type=ttype
        )

    rows = (
        query
        .order_by(
            Transaction.transaction_date.desc(),
            Transaction.id.desc()
        )
        .all()
    )

    return render_template(
        "transactions.html",
        transactions=rows,
        categories=CATEGORIES,
        q=q,
        selected_category=category,
        selected_type=ttype
    )


# =========================
# ADD TRANSACTION
# =========================

@app.route(
    "/transaction/add",
    methods=["POST"]
)
@login_required
def add_transaction():

    try:

        amount = float(
            request.form.get(
                "amount",
                0
            )
        )

        if amount <= 0:
            raise ValueError

    except ValueError:

        flash(
            "Enter a valid positive amount.",
            "error"
        )

        return redirect(
            request.referrer or
            url_for("dashboard")
        )

    title = request.form.get(
        "title",
        ""
    ).strip()

    ttype = request.form.get(
        "type",
        "expense"
    )

    category = request.form.get(
        "category",
        "Other"
    )

    tdate = request.form.get(
        "transaction_date"
    ) or date.today().isoformat()

    note = request.form.get(
        "note",
        ""
    ).strip()

    if not title:

        flash(
            "Transaction title is required.",
            "error"
        )

        return redirect(
            request.referrer or
            url_for("dashboard")
        )

    try:

        parsed_date = datetime.strptime(
            tdate,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        parsed_date = date.today()

    transaction = Transaction(
        user_id=session["user_id"],
        title=title,
        amount=amount,
        type=ttype,
        category=category,
        transaction_date=parsed_date,
        note=note
    )

    db.session.add(transaction)
    db.session.commit()

    flash(
        "Transaction added.",
        "success"
    )

    return redirect(
        request.referrer or
        url_for("dashboard")
    )


# =========================
# EDIT TRANSACTION
# =========================

@app.route(
    "/transaction/edit/<int:transaction_id>",
    methods=["GET", "POST"]
)
@login_required
def edit_transaction(
    transaction_id
):

    transaction = Transaction.query.filter_by(
        id=transaction_id,
        user_id=session["user_id"]
    ).first_or_404()

    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        category = request.form.get(
            "category",
            "Other"
        )

        ttype = request.form.get(
            "type",
            "expense"
        )

        note = request.form.get(
            "note",
            ""
        ).strip()

        tdate = request.form.get(
            "transaction_date"
        )

        try:

            amount = float(
                request.form.get(
                    "amount",
                    0
                )
            )

            if amount <= 0:
                raise ValueError

        except ValueError:

            flash(
                "Enter a valid positive amount.",
                "error"
            )

            return redirect(
                url_for(
                    "edit_transaction",
                    transaction_id=transaction.id
                )
            )

        if not title:

            flash(
                "Transaction title is required.",
                "error"
            )

            return redirect(
                url_for(
                    "edit_transaction",
                    transaction_id=transaction.id
                )
            )

        try:

            parsed_date = datetime.strptime(
                tdate,
                "%Y-%m-%d"
            ).date()

        except (
            ValueError,
            TypeError
        ):

            parsed_date = date.today()

        transaction.title = title
        transaction.amount = amount
        transaction.type = ttype
        transaction.category = category
        transaction.transaction_date = parsed_date
        transaction.note = note

        db.session.commit()

        flash(
            "Transaction updated successfully.",
            "success"
        )

        return redirect(
            url_for("transactions")
        )

    return render_template(
        "edit_transaction.html",
        transaction=transaction,
        categories=CATEGORIES
    )


# =========================
# DELETE TRANSACTION
# =========================

@app.route(
    "/transaction/delete/<int:transaction_id>",
    methods=["POST"]
)
@login_required
def delete_transaction(
    transaction_id
):

    row = Transaction.query.filter_by(
        id=transaction_id,
        user_id=session["user_id"]
    ).first_or_404()

    db.session.delete(row)
    db.session.commit()

    flash(
        "Transaction deleted.",
        "success"
    )

    return redirect(
        request.referrer or
        url_for("transactions")
    )


# =========================
# EMAIL TRANSACTION RECORDS
# =========================

@app.route(
    "/send-transactions-email",
    methods=["POST"]
)
@login_required
def send_transactions_email():

    user_id = session["user_id"]

    user = User.query.get_or_404(
        user_id
    )

    transactions = (
        Transaction.query
        .filter_by(
            user_id=user_id
        )
        .order_by(
            Transaction.transaction_date.desc(),
            Transaction.id.desc()
        )
        .all()
    )

    if not transactions:

        flash(
            "There are no transactions to send.",
            "error"
        )

        return redirect(
            url_for("transactions")
        )

    total_income = sum(
        t.amount
        for t in transactions
        if t.type == "income"
    )

    total_expense = sum(
        t.amount
        for t in transactions
        if t.type == "expense"
    )

    balance = (
        total_income -
        total_expense
    )

    report_lines = [

        "EXPENSE TRACKER - TRANSACTION REPORT",

        "",

        f"User: {user.name}",

        f"Account Email: {user.email}",

        "",

        f"Total Income: ₹{total_income:.2f}",

        f"Total Expenses: ₹{total_expense:.2f}",

        f"Balance: ₹{balance:.2f}",

        "",

        "TRANSACTIONS",

        "----------------------------------------"

    ]

    for t in transactions:

        report_lines.append(

            f"{t.transaction_date} | "
            f"{t.type.upper()} | "
            f"{t.title} | "
            f"₹{t.amount:.2f} | "
            f"{t.category}"

        )

    report = "\n".join(
        report_lines
    )

    email_address = app.config[
        "MAIL_USERNAME"
    ]

    if not email_address:

        flash(
            "Email address is not configured. Check your .env file.",
            "error"
        )

        return redirect(
            url_for("transactions")
        )

    try:

        message = Message(

            subject=(
                "Expense Tracker - "
                "Transaction Records"
            ),

            recipients=[
                email_address
            ],

            body=report

        )

        mail.send(message)

        flash(

            "Transaction records sent successfully to your configured Gmail address.",

            "success"

        )

    except Exception as e:

        print(
            "Email error:",
            e
        )

        flash(

            "Unable to send email. Please check your Gmail settings.",

            "error"

        )

    return redirect(
        url_for("transactions")
    )


# =========================
# CHART DATA API
# =========================

@app.route("/api/chart-data")
@login_required
def chart_data():

    user_id = session["user_id"]

    category_rows = db.session.query(

        Transaction.category,
        func.sum(
            Transaction.amount
        )

    ).filter_by(

        user_id=user_id,
        type="expense"

    ).group_by(

        Transaction.category

    ).all()

    month_rows = db.session.query(

        func.strftime(
            "%Y-%m",
            Transaction.transaction_date
        ),

        Transaction.type,

        func.sum(
            Transaction.amount
        )

    ).filter_by(

        user_id=user_id

    ).group_by(

        func.strftime(
            "%Y-%m",
            Transaction.transaction_date
        ),

        Transaction.type

    ).order_by(

        func.strftime(
            "%Y-%m",
            Transaction.transaction_date
        )

    ).all()

    categories = [

        {
            "label": category,
            "value": round(
                float(amount),
                2
            )
        }

        for category, amount
        in category_rows

    ]

    monthly = {}

    for month, ttype, amount in month_rows:

        monthly.setdefault(

            month,

            {
                "income": 0,
                "expense": 0
            }

        )

        monthly[month][ttype] = round(
            float(amount),
            2
        )

    return jsonify({

        "categories": categories,

        "monthly": [

            {
                "month": month,
                **values
            }

            for month, values
            in monthly.items()

        ]

    })


# =========================
# DEMO DATA
# =========================

def seed_demo():

    with app.app_context():

        # Create all database tables.
        # This is required when deploying with Gunicorn/Render.
        db.create_all()

        # Create demo account if it does not already exist.
        demo = User.query.filter_by(
            email="demo@example.com"
        ).first()

        if demo is None:

            demo = User(

                name="Demo User",

                email="demo@example.com",

                password_hash=generate_password_hash(
                    "demo123"
                )

            )

            db.session.add(
                demo
            )

            db.session.commit()

            sample = [

                (
                    "Monthly Salary",
                    45000,
                    "income",
                    "Salary",
                    "2026-09-01"
                ),

                (
                    "Hostel & Bills",
                    6500,
                    "expense",
                    "Bills",
                    "2026-09-03"
                ),

                (
                    "Groceries",
                    3200,
                    "expense",
                    "Food",
                    "2026-09-06"
                ),

                (
                    "Bus & Fuel",
                    1800,
                    "expense",
                    "Transport",
                    "2026-09-10"
                ),

                (
                    "Course Materials",
                    2400,
                    "expense",
                    "Education",
                    "2026-09-14"
                ),

                (
                    "Freelance Work",
                    8000,
                    "income",
                    "Other",
                    "2026-09-18"
                ),

                (
                    "Movie & Snacks",
                    900,
                    "expense",
                    "Entertainment",
                    "2026-09-20"
                )

            ]

            for title, amount, typ, cat, dt in sample:

                db.session.add(

                    Transaction(

                        user_id=demo.id,

                        title=title,

                        amount=amount,

                        type=typ,

                        category=cat,

                        transaction_date=datetime.strptime(
                            dt,
                            "%Y-%m-%d"
                        ).date()

                    )

                )

            db.session.commit()


# =========================
# INITIALIZE DATABASE
# =========================
#
# IMPORTANT:
# This runs when Gunicorn imports app.py.
# Therefore Render will create the SQLite
# tables before handling the first request.
#

seed_demo()


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    app.run(
        debug=True
    )