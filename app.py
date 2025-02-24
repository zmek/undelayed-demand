import streamlit as st
import pandas as pd
import numpy as np

from patientflow.viz.arrival_rates import (
    plot_arrival_rates,
    plot_cumulative_arrival_rates,
)
from patientflow.viz.aspirational_curve_plot import plot_curve

# Set up session states for step completion and plot storage
if "step2_completed" not in st.session_state:
    st.session_state.step2_completed = False
if "step4_completed" not in st.session_state:
    st.session_state.step4_completed = False
if "plots" not in st.session_state:
    st.session_state.plots = {}


def generate_and_store_plot(plot_function, plot_key, *args, **kwargs):
    """Helper function to generate and store plots in session state"""
    try:
        fig = plot_function(*args, **kwargs)
        st.session_state.plots[plot_key] = fig
        return fig
    except Exception as e:
        st.error(f"Error generating plot: {str(e)}")
        return None


def main():
    st.title("Understand your emergency demand")
    st.header("Find out *when* beds need to be ready, to meet ED targets.")

    # Introduction text
    st.markdown(
        """
    This tool illuminates the "un-delayed" demand for inpatient beds in your hospital. You provide information about when admitted patients first arrive at your ED front door. 
    The tool applies 4-hour targets to their arrival times, to show when those patients would leave your ED, if you were meeting targets.
    """
    )

    st.subheader("Step 1: Uploading your data")

    # File upload
    st.markdown(
        """Upload a CSV file containing Emergency Department arrival data. Be sure to only include arrival times for patients who are later admitted.<br><br>
    Requirements:<br>
    - The file must be in CSV format<br>
    - It must include a column named 'arrival_datetime'<br>
    - That column should contain valid dates and times<br><br>
    Example format for arrival_datetime column: 03/01/2024 05:12:49<br>
    Note: Most standard date/time formats will be accepted.""",
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        label="Upload your CSV file",
        type="csv",
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file, parse_dates=["arrival_datetime"])
        df.set_index("arrival_datetime", inplace=True)

        # More robust date handling
        start_date = df.index.to_series().dt.date.min()
        end_date = df.index.to_series().dt.date.max()
        num_days = len(df.index.to_series().dt.date.unique())

        st.write(
            f"""The uploaded dataset starts on {start_date} and ends on {end_date}, 
                 and contains {len(df):,} inpatient arrivals over {num_days} days. 
                 The chart below shows the average number of patients arriving each hour of the day who are later admitted."""
        )

        # Sidebar controls
        st.sidebar.header("Chart preferences")
        start_hour = st.sidebar.slider(
            "Draw charts starting at this hour", min_value=0, max_value=23, value=8
        )

        # Initial arrival rates plot
        title = f"Hourly arrival rates of admitted patients starting at {start_hour} am from {df.index.date.min()} to {df.index.date.max()}"
        initial_plot = generate_and_store_plot(
            plot_arrival_rates,
            "initial_plot",
            df,
            title,
            time_interval=60,
            start_plot_index=start_hour,
            num_days=num_days,
            return_figure=True,
        )
        if initial_plot:
            st.pyplot(initial_plot)

        # Sidebar controls for ED performance
        st.sidebar.header("Your aspirations for ED performance")
        st.sidebar.subheader("Main target")
        x1 = st.sidebar.number_input("Main target: Hours since ED arrival", value=4)
        y1 = (
            st.sidebar.number_input(
                "Main target: Percentage of patients processed", value=80
            )
            / 100
        )

        st.sidebar.subheader("Mop-up target")
        x2 = st.sidebar.number_input("Mop-up target: Hours since ED arrival", value=12)
        y2 = (
            st.sidebar.number_input(
                "Mop-up target: Percentage of patients processed", value=99
            )
            / 100
        )

        st.sidebar.subheader("Consistency target")
        percentage_of_days = (
            st.sidebar.number_input(
                "Consistency target: Percentage of days on which you want to hit those targets",
                value=90,
            )
            / 100
        )

        # Decision-making window controls
        st.sidebar.header("Decision-making window")
        start_of_window = st.sidebar.number_input(
            "Start of window: Decision-makers are on wards from this hour", value=8
        )
        end_of_window = st.sidebar.number_input(
            "End of window: Decision-makers are on wards until this hour", value=20
        )

        # Step 2: ED Performance Targets
        st.subheader("Step 2: Specify your aspirations for ED performance")
        st.write(
            """You have the option to specify your own ED targets. The default is 80% of patients being admitted within 4 hours and 99% within 12 hours. Use the sidebar to change this."""
        )

        st.markdown(
            f"Please confirm your ED performance targets:<br>"
            f"- **Main target:** Process {y1*100:.0f}% of admitted patients within {x1} hours<br>"
            f"- **Mop-up target:** Process {y2*100:.0f}% of admitted patients within {x2} hours",
            unsafe_allow_html=True,
        )

        if st.button("Confirm your targets") or st.session_state.step2_completed:
            st.session_state.step2_completed = True
            st.success("Plotting your ED targets as a curve")

            # Display all Step 2 plots
            title = f"Aspirational curve reflecting a {int(x1)} hour target for {int(y1*100)}% of patients\nand a {int(x2)} hour target for {int(y2*100)}% of patients"
            curve_plot = generate_and_store_plot(
                plot_curve,
                "curve_plot",
                title=title,
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
                figsize=(10, 6),
                include_titles=True,
                return_figure=True,
            )
            if curve_plot:
                st.pyplot(curve_plot)

            # Step 3: Beds needed per hour
            st.subheader(
                "Step 3: Displaying the number of beds you need, each hour of the day, on an average day"
            )
            st.write(
                """The chart below uses the same arrival rates as the first chart - as a dotted line - for reference.
                     The solid line shows the average number of beds needed each hour."""
            )

            hourly_beds_plot = generate_and_store_plot(
                plot_arrival_rates,
                "hourly_beds_plot",
                df,
                title,
                curve_params=(x1, y1, x2, y2),
                time_interval=60,
                start_plot_index=start_hour,
                num_days=num_days,
                return_figure=True,
            )
            if hourly_beds_plot:
                ax = hourly_beds_plot.gca()
                ax.set_ylabel("Number of beds needed each hour, on average")
                ax.set_title(
                    "Number of beds needed each hour to hit ED targets for admitted patients"
                )
                st.pyplot(hourly_beds_plot)

            st.write(
                """The next chart presents the same information in a different way. Each hour's number of beds has been added cumulatively. 
                     The chart shows how, over the course of a 24 hour period, the total number builds up."""
            )

            cumulative_plot = generate_and_store_plot(
                plot_cumulative_arrival_rates,
                "cumulative_plot",
                df,
                f"Cumulative number of beds needed, by hour of the day",
                curve_params=(x1, y1, x2, y2),
                start_plot_index=start_hour,
                num_days=num_days,
                return_figure=True,
            )
            if cumulative_plot:
                st.pyplot(cumulative_plot)

            # Step 4: Consistency targets
            st.subheader(
                "Step 4: Specifying your aspirations for meeting ED targets consistently"
            )
            st.write(
                "The charts above show your average demand for emergency beds. "
                "If you were to have this number of beds ready, you would hit ED targets on days when the number of admitted patients is average or below. "
                "On all other days, you would not hit targets. You need some slack in the system to cater for those days."
            )

            st.write(
                "The chart below shows how many beds you would need to have ready to hit targets consistently. "
                "The default is 90% of days. Use the sidebar to change this."
            )

            st.markdown(
                f"Please confirm your target for consistency:<br>"
                f"- **Consistency target:** You want to meet your ED targets on **{percentage_of_days*100:.0f}% of days**",
                unsafe_allow_html=True,
            )

            if (
                st.button("Confirm your consistency target")
                or st.session_state.step4_completed
            ):
                st.session_state.step4_completed = True

                consistency_plot = generate_and_store_plot(
                    plot_cumulative_arrival_rates,
                    "consistency_plot",
                    df,
                    f"Cumulative number of beds needed on weekends, by hour of day if ED targets are to be met on {percentage_of_days*100:.0f}% of days",
                    curve_params=(x1, y1, x2, y2),
                    start_plot_index=start_hour,
                    num_days=num_days,
                    return_figure=True,
                    annotation_prefix=f"To hit targets on {percentage_of_days*100:.0f}% of days",
                    plot_centiles=True,
                    highlight_centile=percentage_of_days,
                    centiles=[percentage_of_days],
                    markers=["o"],
                    line_styles_centiles=["-.", "--", ":", "-", "-"],
                )
                if consistency_plot:
                    st.pyplot(consistency_plot)

                # Step 5: Decision-making window
                st.subheader("Step 5: Specifying your decision-making window")
                st.write(
                    "Finally, consider your staffing patterns. Are the people with responsibility for discharging patients only present during the day? "
                    "If so, all discharges must happen before these decision-makers go home. "
                    "Otherwise, if no beds are available for incoming patients overnight, those patients will have to wait in ED until decision-makers return in the morning."
                )

                st.write(
                    "The chart below shows how many beds you would need to have ready by the end of the decision-making window, to hit targets consistently. "
                    f"The default is a decision-making window that begins at {start_of_window:02d}:00 and ends at {end_of_window:02d}:00. Use the sidebar to change this."
                )

                st.markdown(
                    f"Please confirm the times when decision-makers are available to discharge patients:<br>"
                    f"- **Start of window:** Decision-makers are on wards from {start_of_window:02d}:00<br>"
                    f"- **End of window:** Decision-makers are on wards until {end_of_window:02d}:00<br><br>",
                    unsafe_allow_html=True,
                )

                if st.button("Confirm your decision-making window"):
                    final_plot = generate_and_store_plot(
                        plot_cumulative_arrival_rates,
                        "final_plot",
                        df,
                        f"Cumulative number of beds needed, by hour of day, if ED targets are to be met on {percentage_of_days*100:.0f}% of days",
                        curve_params=(x1, y1, x2, y2),
                        start_plot_index=start_hour,
                        num_days=num_days,
                        return_figure=True,
                        annotation_prefix=f"To hit targets on {percentage_of_days*100:.0f}% of days",
                        draw_window=(start_of_window, end_of_window),
                        hour_lines=[12, end_of_window],
                        plot_centiles=True,
                        highlight_centile=percentage_of_days,
                        centiles=[percentage_of_days],
                        markers=["o"],
                        line_styles_centiles=["-.", "--", ":", "-", "-"],
                    )
                    if final_plot:
                        st.pyplot(final_plot)


if __name__ == "__main__":
    main()
