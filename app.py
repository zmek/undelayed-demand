import streamlit as st
import pandas as pd
import numpy as np
from patientflow.viz.undelayed_demand import generate_plot  

def main():
    st.title("Patient Arrival Rate Analysis")
    
    # File upload
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file, parse_dates=['datetime_column'])  
# Replace 'datetime_column' with your actual column name
        df.set_index('datetime_column', inplace=True)
        
        # Add sidebar controls for parameters
        st.sidebar.header("Plot Parameters")
        
        # Coordinate inputs
        x1 = st.sidebar.number_input("X1 Coordinate", value=0.0)
        y1 = st.sidebar.number_input("Y1 Coordinate", value=0.0)
        x2 = st.sidebar.number_input("X2 Coordinate", value=1.0)
        y2 = st.sidebar.number_input("Y2 Coordinate", value=1.0)
        
        # Time parameters
        time_interval = st.sidebar.slider("Time Interval (minutes)", 
                                        min_value=15, 
                                        max_value=120, 
                                        value=60, 
                                        step=15)
        
        start_hour = st.sidebar.slider("Start Hour", 
                                     min_value=0, 
                                     max_value=23, 
                                     value=8)
        
        # Calculate available days in dataset
        available_days = len(np.unique(df.index.date))
        num_days = st.sidebar.slider("Number of Days to Plot", 
                                   min_value=1, 
                                   max_value=available_days, 
                                   value=min(7, available_days))
        
        try:
            # Generate the plot
            fig = generate_plot(
                df=df,
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
                time_interval=time_interval,
                start_plot_index=start_hour,
                num_days=num_days
            )
            
            # Display the plot
            st.plotly_chart(fig)
            
            # Add summary statistics
            st.markdown("### Dataset Summary")
            st.write(f"Date Range: {df.index.date.min()} to {df.index.date.max()}")
            st.write(f"Total Days: {available_days}")
            st.write(f"Total Records: {len(df)}")
            
        except Exception as e:
            st.error(f"Error generating plot: {str(e)}")

if __name__ == "__main__":
    main()
