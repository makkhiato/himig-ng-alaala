import pandas as pd
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler


def normalize():
    # 1. Get the absolute path to the directory where normalization.py lives
    # This points to: .../backend/utils/
    current_dir = Path(__file__).parent

    # 2. Go up one level to 'backend' and then down into 'data/processed'
    # .parent takes you to 'backend', then / 'data' / ... builds the rest
    file_path = current_dir.parent / 'data' / 'processed' / 'music_data_cleaned.json'

    # Check if the file actually exists before trying to read it
    if not file_path.exists():
        print(f"❌ Error: Could not find the file at {file_path}")
        return

    # 3. Load the data
    df = pd.read_json(file_path)
    print(f"✅ Loaded {len(df)} songs for normalization.")

    # ... [Rest of your MinMaxScaler logic here] ...
    scaler = MinMaxScaler()
    df['tempo_normalized'] = scaler.fit_transform(df[['tempo']]).round(2)

    # 4. Save to the same folder
    output_path = file_path.parent / 'music_data_normalized.json'
    df.to_json(output_path, orient='records', indent=4)
    print(f"🚀 Normalized data saved to: {output_path}")


if __name__ == "__main__":
    normalize()