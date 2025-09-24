# CreativeFuse Installation and Setup Guide

## Backend Setup

1. Navigate to the backend folder:

    ```
    cd backend
    ```

2. Create and activate a Python virtual environment:

    - On Linux/macOS:

      ```
      python3 -m venv venv
      source venv/bin/activate
      ```

    - On Windows:

      ```
      python -m venv venv
      venv\Scripts\activate
      ```

3. Install backend dependencies:

    ```
    pip install -r requirements.txt
    ```

4. Create a `.env` file based on `.env.example`:

    ```
    OPENROUTER_API_KEY=your_openrouter_api_key_here
    ```

5. Run the backend server in development mode:

    ```
    uvicorn app.main:app --reload
    ```

6. Verify the backend is running by opening:

    ```
    http://localhost:8000/docs
    ```

    This is the interactive Swagger UI for API testing.


## Frontend Setup

1. Navigate to the frontend folder:

    ```
    cd frontend
    ```

2. Install frontend dependencies:

    ```
    npm install
    ```

3. Run the frontend development server:

    ```
    npm run dev
    ```

4. Open the displayed URL in your browser, typically:

    ```
    http://localhost:5173/
    ```

5. Use the UI to generate creative AI ideas by interacting with the backend API.


## Notes

- Make sure backend is running before using frontend.
- For production, update API URLs and environment configurations as needed.
- To stop servers, press CTRL+C in the terminal.

---
