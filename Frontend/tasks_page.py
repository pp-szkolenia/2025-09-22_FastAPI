import streamlit as st
import pandas as pd
import requests


def _api_base() -> str:
    return st.session_state.get("API_BASE", "http://localhost:8000")


def _auth_headers() -> dict:
    token = st.session_state.get("jwt")
    return {"Authorization": f"Bearer {token}"} if token else {}


def _refetch_tasks():
    try:
        r = requests.get(f"{_api_base()}/tasks", headers=_auth_headers(), timeout=10)
        if r.status_code == 200:
            st.session_state.tasks = r.json()["result"]
        else:
            st.error(f"GET /tasks failed: {r.status_code}")
    except Exception as e:
        st.error(f"GET /tasks error: {e}")


def tasks_page(tasks):
    st.header("Manage Tasks")

    df_tasks = pd.DataFrame(tasks)
    st.write("### Existing Tasks")
    st.dataframe(df_tasks, use_container_width=True)

    col_top = st.columns(3)
    with col_top[0]:
        if st.button("Refresh tasks"):
            _refetch_tasks()
            st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        with st.form("new_task_form"):
            st.subheader("Add New Task")
            description = st.text_input("Description")
            priority = st.selectbox("Priority", [1, 2, 3])
            is_completed = st.checkbox("Completed")
            submit_task = st.form_submit_button("Add Task")
            if submit_task:
                try:
                    payload = {"description": description, "priority": priority, "is_completed": is_completed}
                    r = requests.post(f"{_api_base()}/tasks", json=payload, headers=_auth_headers(), timeout=10)
                    if r.status_code in (200, 201):
                        _refetch_tasks()
                        st.success("Task added successfully.")
                        st.rerun()
                    else:
                        st.error(f"POST /tasks failed: {r.status_code} {r.text}")
                except Exception as e:
                    st.error(f"POST /tasks error: {e}")

    with col2:
        with st.form("update_task_form"):
            st.subheader("Update Task")
            options = {f"{t.get('task_id')} – {t.get('description','')}": t for t in tasks}
            selected_label = st.selectbox("Select Task", list(options.keys()) if options else [])
            selected_task = options[selected_label] if options else None
            description_new = st.text_input("New Description", value="")
            priority_new = st.selectbox("New Priority", [1, 2, 3], 0)
            is_completed_new = st.checkbox("Completed", value=False)
            submit_update = st.form_submit_button("Update Task")
            if submit_update and selected_task:
                try:
                    task_id = selected_task["task_id"]
                    payload = {"description": description_new, "priority": priority_new, "is_completed": is_completed_new}
                    r = requests.put(f"{_api_base()}/tasks/{task_id}", json=payload, headers=_auth_headers(), timeout=10)
                    if r.status_code in (200, 204):
                        _refetch_tasks()
                        st.success(f"Task {task_id} updated successfully.")
                        st.rerun()
                    else:
                        st.error(f"PUT /tasks/{task_id} failed: {r.status_code} {r.text}")
                except Exception as e:
                    st.error(f"PUT /tasks error: {e}")

    st.subheader("Delete Task")
    options_del = {f"{t.get('task_id')} – {t.get('description','')}": t for t in tasks}
    selected_label_del = st.selectbox("Select Task to delete", list(options_del.keys()) if options_del else [], key="delete_task_select")
    if st.button("Delete Task"):
        if options_del:
            try:
                task_id = options_del[selected_label_del]["task_id"]
                r = requests.delete(f"{_api_base()}/tasks/{task_id}", headers=_auth_headers(), timeout=10)
                if r.status_code in (200, 204):
                    _refetch_tasks()
                    st.success(f"Task {task_id} deleted successfully.")
                    st.rerun()
                else:
                    st.error(f"DELETE /tasks/{task_id} failed: {r.status_code} {r.text}")
            except Exception as e:
                st.error(f"DELETE /tasks error: {e}")
