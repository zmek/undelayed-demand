import streamlit as st
import pandas as pd
import numpy as np
from patientflow.viz.undelayed_demand import generate_plot  
from patientflow.load import load_data

from patientflow.viz.arrival_rates import plot_arrival_rates
from patientflow.viz.aspirational_curve_plot import plot_curve


def generate_plot(df: pd.DataFrame,
                    x1: float,
                    y1: float,
                    x2: float,
                    y2: float,                  
                  time_interval: int = 60,
                  start_plot_index: int = 0, 
                  num_days: int = None
                  ):

    if not num_days:
        num_days = len(np.unique(df.index.date))

    # Set the plot to start at the 8th hour of the day (if not set the function will default to starting at midnight
    start_plot_index = 8

    # plot for weekdays
    title = f'Hourly arrival rates of admitted patients starting at {start_plot_index} am from {df.index.date.min()} to {df.index.date.max()}'
    fig = plot_arrival_rates(df, 
                    title, 
                    time_interval=60, 
                    start_plot_index=start_plot_index, 
                    num_days=num_days,
                    return_figure=True)
    
    return fig

    


def main():
    st.title("Understanding your un-delayed demand for emergency beds")

        # Introduction text
    st.markdown("""
    A tool for acute hospitals to understand when they need beds, if ED targets are met. 
                It helps you visualise the "un-delayed" demand for inpatient beds in your hospital from people coming via your Emergency Department. 
                It invites you to specific your aspirations for ED targets. It defaults to 80% of patients being admitted within 4 hours. You can change this. 
                Generate the charts and see your results. 
    """)
    st.subheader("Step 1: Upload your data")
    

    
    # File upload
    uploaded_file = st.file_uploader(
        """Upload a CSV file containing Emergency Department arrival data for admitted patients.

        Requirements:
        • The file must be in CSV format
        • Must include a column named exactly 'arrival_datetime'
        • Column should contain valid dates and times
        Example format: 03/01/2024 05:12:49

        Note: Most standard date/time formats will be accepted.""",
        type="csv"
    )
    
    
    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file, parse_dates=['arrival_datetime'])  
        df.set_index('arrival_datetime', inplace=True)

        # Add summary statistics
        st.markdown("#### Dataset Summary")
        st.write(f"Date Range: {df.index.date.min()} to {df.index.date.max()}")
        st.write(f"Total Number of patients: {len(df)}")
        # Calculate available days in dataset
        num_days = len(np.unique(df.index.date))
        
        # Add sidebar controls for parameters
        st.sidebar.header("Your aspirations for ED performance")
        
        # First target
        st.sidebar.subheader("Main target")
        x1 = st.sidebar.number_input("Target 1: Hours since ED arrival", value=4)
        y1 = st.sidebar.number_input("Target 1: Percentage of patients processed", value=80)/100
        
        # Second target
        st.sidebar.subheader("Mop up target")
        x2 = st.sidebar.number_input("Target 2: Hours since ED arrival", value=12)
        y2 = st.sidebar.number_input("Target 2: Percentage of patients processed", value=99)/100

        # Third target
        st.sidebar.subheader("Day by day performance")
        percentage_of_days = st.sidebar.number_input("Target 3: Percentage of days on which you want to hit those targets", value=90)/100

        # Start the charts at this hour of the day
        start_hour = st.sidebar.slider("Draw charts starting at this hour", 
                                min_value=0, 
                                max_value=23, 
                                value=8)
            

        # Main content area
        st.subheader("Step 2: Specify your aspirations for ED performance")
        st.write("Use the sidebar to set your target performance levels.")
        
        # Display targets and ask for confirmation
        st.write(f"""Please confirm your targets:
        - Target 1: Process {y1*100:.0f}% of patients within {x1} hours
        - Target 2: Process {y2*100:.0f}% of patients within {x2} hours""")


        
        confirm_targets = st.button("Confirm your targets")

        if confirm_targets:
            st.success("Plotting your ED targets as a curve")

                    # Plot targets
            title = 'Aspirational curve reflecting a ' + str(int(x1)) + ' hour target for ' + str(int(y1*100)) + \
                '% of patients\nand a '+ str(int(x2)) + ' hour target for ' + str(int(y2*100)) + '% of patients'
                # Place subsequent analysis code here

        
            try:
                fig = plot_curve(
                    title = title,
                    x1 = x1,
                    y1 = y1,
                    x2 = x2,
                    y2 = y2,
                    figsize = (10,6),
                    include_titles=True
                )
                # Display the plot
                st.pyplot(fig)
                        
            except Exception as e:
                st.error(f"Error generating plot: {str(e)}")

            
            st.subheader("Step 3: Displaying the number of beds you need, each hour of the day, on an average day")

            title = f'Hourly arrival rates of admitted patients starting at {start_hour} am from {df.index.date.min()} to {df.index.date.max()}'


        
        



            
            try:
                # Generate the plot
                fig = plot_arrival_rates(df, 
                                title, 
                                curve_params=(x1, y1, x2, y2), 
                                time_interval=60, 
                                start_plot_index=start_hour, 
                                num_days=num_days,
                                return_figure=True
                )
                
                # Display the plot
                st.pyplot(fig)
                

                
            except Exception as e:
                st.error(f"Error generating plot: {str(e)}")

if __name__ == "__main__":
    main()
