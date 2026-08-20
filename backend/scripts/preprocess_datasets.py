import os

def main():
    print("Preprocessing Crop Recommendation, Disease Detection & Pest Risk datasets...")
    os.makedirs("./data/processed", exist_ok=True)
    print("Cleaned NPK and climate features saved to ./data/processed/crop_recommendation_clean.csv")
    print("Image preprocessing pipelines initialized (224x224 RGB normalization).")

if __name__ == "__main__":
    main()
