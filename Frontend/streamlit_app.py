import streamlit as st
import requests

from tasks_page import tasks_page
from users_page import users_page
from login_page import login_page

API_BASE = "http://localhost:8000"


def init_state():
    st.session_state.setdefault("API_BASE", API_BASE)
    st.session_state.setdefault("jwt", None)
    st.session_state.setdefault("token_type", "bearer")
    st.session_state.setdefault("current_user", None)
    st.session_state.setdefault("data_loaded", False)
    st.session_state.setdefault("tasks", [])
    st.session_state.setdefault("users", [])


def _auth_headers() -> dict:
    token = st.session_state.get("jwt")
    return {"Authorization": f"Bearer {token}"} if token else {}


def load_data_once():
    if not st.session_state.get("jwt") or st.session_state.get("data_loaded"):
        return

    try:
        r = requests.get(f"{st.session_state['API_BASE']}/tasks", headers=_auth_headers(), timeout=10)
        st.session_state.tasks = r.json()["result"] if r.status_code == 200 else []
        if r.status_code != 200:
            st.session_state.tasks_error = f"GET /tasks failed: {r.status_code}"
    except Exception as e:
        st.session_state.tasks = []
        st.session_state.tasks_error = f"GET /tasks error: {e}"

    try:
        r = requests.get(f"{st.session_state['API_BASE']}/users", headers=_auth_headers(), timeout=10)
        if r.status_code == 200:
            st.session_state.users = r.json()["result"]
        elif r.status_code in (401, 403):
            st.session_state.users = []
        else:
            st.session_state.users = []
            st.session_state.users_error = f"GET /users failed: {r.status_code}"
    except Exception as e:
        st.session_state.users = []
        st.session_state.users_error = f"GET /users error: {e}"

    st.session_state.data_loaded = True


def main():
    st.title("Task Management Dashboard")
    init_state()

    with st.sidebar:
        user = st.session_state.get("current_user")
        if st.session_state.get("jwt"):
            label = f"{user['username']} (admin: {user.get('is_admin', False)})" if user else "Logged in"
            st.success(f"Logged in as {label}")
            if st.button("Logout"):
                for k in ("jwt", "token_type", "current_user", "data_loaded",
                          "tasks", "users", "tasks_error", "users_error"):
                    st.session_state.pop(k, None)
                st.rerun()
        else:
            st.info("Please log in to continue.")

    if not st.session_state.get("jwt"):
        login_page(api_base=st.session_state["API_BASE"])
        return

    load_data_once()

    menu = st.sidebar.selectbox("Choose an option", ["Tasks", "Users"])
    if menu == "Tasks":
        tasks_page(st.session_state.get("tasks", []))
        if err := st.session_state.get("tasks_error"):
            st.warning(err)
    elif menu == "Users":
        users_page(st.session_state.get("users", []))
        if err := st.session_state.get("users_error"):
            st.info("Users may be restricted by the API.")
            st.warning(err)


if __name__ == "__main__":
    main()
