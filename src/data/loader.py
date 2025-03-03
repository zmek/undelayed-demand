import pandas as pd


def load_arrival_data(file_path):
    """
    Load arrival datetime data from a CSV file.

    Parameters:
    -----------
    file_path : str or Path
        Path to the CSV file containing arrival data

    Returns:
    --------
    pd.DataFrame
        DataFrame with arrival_datetime as index
    """
    try:
        # First attempt with default parsing
        df = pd.read_csv(file_path, parse_dates=["arrival_datetime"])
    except:
        # If default parsing fails, try multiple common formats
        df = pd.read_csv(file_path)
        for date_format in [
            "%d/%m/%Y %H:%M",  # UK/European
            "%d/%m/%Y %H:%M:%S",
            "%m/%d/%Y %H:%M",  # US
            "%Y-%m-%d %H:%M",  # ISO
            "%d-%m-%Y %H:%M",
            "%d.%m.%Y %H:%M",
            "%d/%m/%y %H:%M",
        ]:
            try:
                df["arrival_datetime"] = pd.to_datetime(
                    df["arrival_datetime"], format=date_format, errors="coerce"
                )
                if not df["arrival_datetime"].isna().any():
                    break
            except:
                continue

    if df["arrival_datetime"].isna().any():
        raise ValueError(
            """Some dates could not be parsed. Supported formats include:
            - DD/MM/YYYY HH:MM
            - YYYY-MM-DD HH:MM:SS
            - MM/DD/YYYY HH:MM
            - DD-MM-YYYY HH:MM
            Please check your date format and try again."""
        )

    df.set_index("arrival_datetime", inplace=True)
    df.index = pd.to_datetime(df.index, dayfirst=True)

    return df
