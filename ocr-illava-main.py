import requests
import pandas as pd
import base64
import mimetypes
import os
import re
from Levenshtein import distance as levenshtein_distance

# === Konfigurasi LM Studio ===
LMSTUDIO_API_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_NAME = "llava-llama-3-8b-v1_1"

# === Normalisasi teks plat ===
def normalize_plate(text):
    """
    Bersihkan hasil: hapus spasi, ubah ke huruf besar, dan buang karakter non-alphanum
    """
    return re.sub(r'[^A-Z0-9]', '', text.upper())

# === Fungsi hitung CER ===
# Hitung dan evaluasi hasil prediksi menggunakan metrik:
# Character Error Rate (CER)
# Gunakan formula CER sebagai berikut:
# CER = (S + D + I) / N
# dengan:
# S = jumlah karakter salah substitusi
# D = jumlah karakter yang dihapus (deletion)
# I = jumlah karakter yang disisipkan (insertion)
# N = jumlah karakter pada ground truth (minimal 1 untuk menghindari pembagi nol)

# === Fungsi hitung CER ===
def calculate_cer(ground_truth, prediction):
    gt = normalize_plate(ground_truth)
    pred = normalize_plate(prediction)
    N = max(len(gt), 1)
    return levenshtein_distance(gt, pred) / N

# === Encode gambar ke base64 ===
def encode_image_to_base64(image_path):
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        mime_type = "image/jpeg"
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"

# === OCR ke LM Studio ===
def ocr_with_lmstudio(image_path):
    base64_image = encode_image_to_base64(image_path)
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": base64_image}},
                    {"type": "text", "text": "What is the license plate number shown in this image? Respond only with the plate number."}
                ]
            }
        ]
    }

    try:
        response = requests.post(LMSTUDIO_API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        error_text = response.text if 'response' in locals() else ''
        print(f"[ERROR] {image_path}: {e} | {error_text[:200]}")
        return ""

# === MAIN ===
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    csv_path = os.path.join(script_dir, "ground_truth_new.csv")
    df = pd.read_csv(csv_path, delimiter=";")

    image_dir = os.path.join(script_dir, "Indonesian_LPR_Dataset", "merged", "test")

    results = []

    for idx, row in df.iterrows():
        image_path = os.path.join(image_dir, row["image"])
        ground_truth = row["ground_truth"]

        print(f"[{idx+1}/{len(df)}] Proses OCR: {row['image']}")

        if not os.path.exists(image_path):
            print(f"⚠️  Gambar tidak ditemukan: {image_path}")
            prediction = ""
            cer = 1.0
        else:
            prediction = ocr_with_lmstudio(image_path)
            cer = calculate_cer(ground_truth, prediction)

        results.append({
            "image": row["image"],
            "ground_truth": normalize_plate(ground_truth),
            "prediction": normalize_plate(prediction),
            "CER_score": cer
        })

    result_df = pd.DataFrame(results)
    result_path = os.path.join(script_dir, "results.csv")
    result_df.to_csv(result_path, sep=";", index=False)

    avg_cer = result_df["CER_score"].mean()
    print("\n(ok) Proses selesai!")
    print(f"Rata-rata CER: {avg_cer:.4f}")
    print(f"Hasil tersimpan di: {result_path}")

if __name__ == "__main__":
    main()
