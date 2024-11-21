import pandas as pd
import streamlit as st
import sqlite3
import plotly.express as px


# Function to fetch total number of employees from the database
def get_num_employees_from_db():
    db_connection = sqlite3.connect('./db/utsc-exercise.db')
    query = "SELECT COUNT(DISTINCT EmployeeId) AS total_employees FROM EMPLOYEE"
    result = pd.read_sql(query, db_connection)
    db_connection.close()
    return result['total_employees'][0]


# Function to fetch employee data from the database
def get_employee_dataframe():
    db_connection = sqlite3.connect('./db/utsc-exercise.db')
    query = """
        SELECT 
            e.EmployeeId, 
            e.JobTitle, 
            s.YearlyCompensation, 
            cm.Country, 
            e.FirstName || ' ' || e.LastName as FullName
        FROM EMPLOYEE e
        LEFT JOIN Salary s ON e.EmployeeId = s.EmployeeId
        LEFT JOIN OfficeCountryMapping cm ON cm.OfficeId = e.OfficeId
    """
    employee_salary_df = pd.read_sql(query, db_connection)
    db_connection.close()
    return employee_salary_df


# Function to create the "Average Salary by Job Title" chart
def get_avg_salary_by_job_title(employee_salary_df, selected_titles):
    filtered_df = employee_salary_df[employee_salary_df['JobTitle'].isin(selected_titles)]
    avg_salary = filtered_df.groupby('JobTitle')['YearlyCompensation'].mean().reset_index()

    fig = px.bar(
        avg_salary,
        x='JobTitle',
        y='YearlyCompensation',
        title='Average Salary by Job Title',
        labels={'JobTitle': 'Job Title', 'YearlyCompensation': 'Average Salary'},
        text_auto=True
    )
    st.plotly_chart(fig)


# Function to create the "Number of Employees by Job Title" chart
def get_num_employees_by_job_title(employee_salary_df, selected_titles):
    filtered_df = employee_salary_df[employee_salary_df['JobTitle'].isin(selected_titles)]
    num_employees = filtered_df.groupby('JobTitle')['EmployeeId'].nunique().reset_index()

    fig = px.bar(
        num_employees,
        x='JobTitle',
        y='EmployeeId',
        title='Number of Employees by Job Title',
        labels={'JobTitle': 'Job Title', 'EmployeeId': 'Number of Employees'},
        text_auto=True
    )
    st.plotly_chart(fig)


# Function to create the "Average Salary by Country" chart
def get_avg_salary_by_country(employee_salary_df, selected_countries):
    filtered_df = employee_salary_df[employee_salary_df['Country'].isin(selected_countries)]
    avg_salary = filtered_df.groupby('Country')['YearlyCompensation'].mean().reset_index()

    fig = px.bar(
        avg_salary,
        x='Country',
        y='YearlyCompensation',
        title='Average Salary by Country',
        labels={'Country': 'Country', 'YearlyCompensation': 'Average Salary'},
        text_auto=True
    )
    st.plotly_chart(fig)


# Function to create the "Number of Employees by Country" chart
def get_num_employees_by_country(employee_salary_df, selected_countries):
    filtered_df = employee_salary_df[employee_salary_df['Country'].isin(selected_countries)]
    num_employees = filtered_df.groupby('Country')['EmployeeId'].nunique().reset_index()

    fig = px.bar(
        num_employees,
        x='Country',
        y='EmployeeId',
        title='Number of Employees by Country',
        labels={'Country': 'Country', 'EmployeeId': 'Number of Employees'},
        text_auto=True
    )
    st.plotly_chart(fig)


# Main Streamlit app
def main():
    st.title("Employee Salary Analysis")

    # Fetch total number of employees
    num_employees = get_num_employees_from_db()
    st.write(f"Total number of employees: {num_employees}")

    # Load the employee DataFrame
    employee_salary_df = get_employee_dataframe()

    # Job Title Analysis
    st.subheader("Analysis by Job Title")
    job_titles = employee_salary_df['JobTitle'].dropna().unique()
    selected_titles = st.multiselect("Select Job Titles", job_titles, default=job_titles)

    if selected_titles:
        get_avg_salary_by_job_title(employee_salary_df, selected_titles)
        get_num_employees_by_job_title(employee_salary_df, selected_titles)
    else:
        st.warning("Please select at least one job title.")

    # Country Analysis
    st.subheader("Analysis by Country")
    countries = employee_salary_df['Country'].dropna().unique()
    selected_countries = st.multiselect("Select Countries", countries, default=countries)

    if selected_countries:
        get_avg_salary_by_country(employee_salary_df, selected_countries)
        get_num_employees_by_country(employee_salary_df, selected_countries)
    else:
        st.warning("Please select at least one country.")


if __name__ == "__main__":
    main()
