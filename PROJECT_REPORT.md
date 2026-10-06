# EXPENSE TRACKER SYSTEM
## Mini Project Report

### 1. Title
**Expense Tracker System – A Web-Based Personal Finance Management Application**

### 2. Abstract
The Expense Tracker System is a web application designed to help users record, organize and analyze personal income and expenses. The system provides secure user registration and login, transaction management, category-wise spending analysis, monthly financial charts, search and filtering, and a responsive dashboard. SQLite is used for persistent storage and Flask provides the server-side application layer. The project demonstrates practical implementation of authentication, database operations, REST-style JSON data delivery, responsive front-end design and data visualization.

### 3. Problem Statement
People often record expenses informally or do not maintain a consistent record of their spending. This makes it difficult to understand spending patterns, compare income and expenses, and maintain a clear view of available balance. The proposed system provides a centralized digital solution for recording transactions and visualizing financial information.

### 4. Objectives
- Develop a simple personal finance management application.
- Provide secure user registration and login.
- Store transactions in a relational database.
- Calculate total income, total expenses and balance.
- Categorize expenses for better analysis.
- Provide graphical representations of spending and monthly trends.
- Provide search, filtering and deletion of transactions.
- Build a responsive and user-friendly interface.

### 5. Scope
The system is suitable for students, employees and individuals who want a basic personal finance tracker. It can be extended with budgets, recurring transactions, CSV/PDF export, notifications and cloud deployment.

### 6. Technologies Used
| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python Flask |
| Database | SQLite |
| ORM | Flask-SQLAlchemy |
| Authentication | Werkzeug password hashing + Flask sessions |
| Charts | Chart.js |
| Editor | VS Code / any Python IDE |
| Platform | Windows/Linux/macOS |

### 7. System Modules
1. **Authentication Module** – registration, login and logout.
2. **Dashboard Module** – income, expenses, balance and charts.
3. **Transaction Module** – add, view and delete transactions.
4. **Search/Filter Module** – filter by title, category and type.
5. **Analytics Module** – category breakdown and monthly income/expense visualization.
6. **Database Module** – persistent storage using SQLite.

### 8. Database Design
**User**
- id – Primary Key
- name
- email – Unique
- password_hash
- created_at

**Transaction**
- id – Primary Key
- user_id – Foreign Key
- title
- amount
- type
- category
- transaction_date
- note
- created_at

Relationship: One User can have many Transactions (1:N).

### 9. Functional Requirements
- User can create an account.
- User can authenticate using email and password.
- User can add income or expense transactions.
- User can select a category and date.
- User can view recent transactions.
- User can search and filter transactions.
- User can delete transactions.
- System calculates totals automatically.
- System displays charts based on stored data.

### 10. Non-Functional Requirements
- Responsive UI
- Passwords stored as hashes rather than plain text
- Simple navigation
- Fast local database operations
- Maintainable modular code
- Clear error messages

### 11. System Flow
User → Register/Login → Dashboard → Add Transaction → SQLite Database → Calculate Totals → Generate Charts → User Analysis

### 12. Testing
**Test 1:** Valid registration → Account created successfully.  
**Test 2:** Duplicate email → Error message displayed.  
**Test 3:** Correct login → Dashboard opens.  
**Test 4:** Wrong password → Login rejected.  
**Test 5:** Add expense → Database and totals update.  
**Test 6:** Add income → Balance increases.  
**Test 7:** Search/filter → Matching transactions displayed.  
**Test 8:** Delete transaction → Record removed.  
**Test 9:** Chart loading → Category and monthly charts render.  
**Test 10:** Logout → Session cleared and login page shown.

### 13. Advantages
- Easy to use
- Low-cost and lightweight
- Private local database
- Visual spending analysis
- Suitable for student demonstration
- Easy to extend

### 14. Limitations
- SQLite is intended for small/local deployments.
- No online bank synchronization.
- No automated receipt scanning.
- No multi-device cloud synchronization in the base version.

### 15. Future Enhancements
- Monthly budget limits
- Budget alerts
- CSV/PDF report export
- Recurring payments
- Receipt image upload and OCR
- Cloud database
- Mobile application
- Email notifications
- Advanced forecasting

### 16. Conclusion
The Expense Tracker System successfully provides a practical solution for managing personal financial records. It combines secure authentication, database-backed transaction management and visual analytics in a responsive web application. The project demonstrates important full-stack development concepts and provides a strong foundation for future financial-management features.

### 17. Viva Questions
1. Why is Flask used?
2. Why is SQLite suitable for this project?
3. What is ORM?
4. How are passwords protected?
5. What is the relationship between User and Transaction?
6. How is the balance calculated?
7. Why is Chart.js used?
8. What is session-based authentication?
9. What are functional and non-functional requirements?
10. How can this project be deployed online?
