"""
Topic Filter Module for Chatbot SI
-----------------------------------
Handles topic relevance checking and multi-intent detection.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Feature Flags
ENABLE_TOPIC_FILTERING = os.getenv('ENABLE_TOPIC_FILTERING', 'true').lower() == 'true'
ENABLE_MULTI_INTENT = os.getenv('ENABLE_MULTI_INTENT', 'true').lower() == 'true'
MULTI_INTENT_MAX_QUESTIONS = int(os.getenv('MULTI_INTENT_MAX_QUESTIONS', '5'))

def is_topic_relevant(user_input, groq_client, groq_model):
    """
    Check if user question is relevant to Sistem Informasi program.
    
    Args:
        user_input: User's question
        groq_client: Groq client instance
        groq_model: Groq model name
    
    Returns:
        tuple: (is_relevant: bool, reason: str)
    """
    if not ENABLE_TOPIC_FILTERING:
        return True, "filtering disabled"
    
    if not groq_client:
        # Fallback: accept all if Groq not available
        return True, "groq unavailable"
    
    try:
        # Define SI-related topics
        si_topics = [
            "Program Studi Sistem Informasi",
            "Mata kuliah SI",
            "Prospek kerja lulusan SI",
            "Dosen dan staff SI",
            "Akreditasi prodi SI",
            "Biaya kuliah SI",
            "Pendaftaran SI",
            "Kurikulum dan pembelajaran",
            "Fasilitas dan laboratorium",
            "Himpunan mahasiswa (HIMASIFOR)",
            "Karir di bidang teknologi informasi",
            "Perbedaan SI dengan prodi IT lainnya",
            "Institut Pendidikan Indonesia (IPI)",
            "Universitas/Kampus IPI Garut",
            "Lokasi kampus di Garut"
        ]
        
        system_prompt = f"""Kamu adalah filter topik untuk chatbot Program Studi Sistem Informasi Institut Pendidikan Indonesia (IPI) Garut.

Tugasmu: Tentukan apakah pertanyaan user RELEVAN dengan topik-topik berikut:
{chr(10).join([f"- {topic}" for topic in si_topics])}

Kriteria RELEVAN:
- Pertanyaan tentang kuliah, pendidikan, atau akademik di prodi SI
- Pertanyaan tentang teknologi informasi dalam konteks pendidikan/karir
- Pertanyaan umum tentang prodi (dosen, fasilitas, biaya, dll)
- Pertanyaan tentang IPI (Institut Pendidikan Indonesia) atau kampus
- Pertanyaan tentang lokasi kampus di Garut
- Sapaan atau percakapan pembuka (halo, hai, terima kasih)

Kriteria TIDAK RELEVAN:
- Pertanyaan umum yang tidak ada hubungannya dengan SI, IPI, atau pendidikan
- Pertanyaan tentang topik lain (politik, olahraga, hiburan, cuaca, dll)
- Pertanyaan pribadi yang tidak berhubungan dengan prodi atau kampus
- Permintaan untuk melakukan hal di luar konteks informasi SI/IPI

Jawab HANYA dengan format:
RELEVAN: [alasan singkat]
atau
TIDAK RELEVAN: [alasan singkat]

Contoh:
- "apa itu sistem informasi?" → RELEVAN: pertanyaan tentang definisi prodi SI
- "apa itu IPI?" → RELEVAN: pertanyaan tentang universitas tempat prodi SI berada
- "IPI di mana?" → RELEVAN: pertanyaan tentang lokasi kampus
- "siapa presiden indonesia?" → TIDAK RELEVAN: pertanyaan politik, bukan tentang SI/IPI
- "belajar python di si?" → RELEVAN: pertanyaan tentang mata kuliah SI
- "resep nasi goreng" → TIDAK RELEVAN: pertanyaan kuliner, tidak ada hubungan dengan SI/IPI
- "di garut dimana?" → RELEVAN: pertanyaan tentang lokasi kampus IPI"""
        
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            model=groq_model,
            temperature=0.3,  # Lower temperature for more consistent filtering
            max_tokens=100,
        )
        
        result = response.choices[0].message.content.strip()
        
        if result.startswith("RELEVAN"):
            reason = result.replace("RELEVAN:", "").strip()
            return True, reason
        elif result.startswith("TIDAK RELEVAN"):
            reason = result.replace("TIDAK RELEVAN:", "").strip()
            return False, reason
        else:
            # Fallback if response format unexpected
            return True, "uncertain format"
            
    except Exception as e:
        print(f"[ERROR] Topic filtering error: {e}")
        # Fallback: accept if filtering fails
        return True, "filtering error"

def detect_multi_intent(user_input, groq_client, groq_model):
    """
    Detect if user question contains multiple intents and extract sub-questions.
    
    Args:
        user_input: User's question
        groq_client: Groq client instance
        groq_model: Groq model name
    
    Returns:
        tuple: (is_multi_intent: bool, sub_questions: list)
    """
    if not ENABLE_MULTI_INTENT or not groq_client:
        return False, []
    
    try:
        system_prompt = """Kamu adalah detector pertanyaan majemuk untuk chatbot SI IPI Garut.

Tugasmu: Deteksi apakah pertanyaan user mengandung MULTIPLE INTENTS (lebih dari satu pertanyaan dalam satu kalimat).

Jika YA (multi-intent), ekstrak menjadi sub-pertanyaan yang lebih spesifik.
Jika TIDAK (single intent), return SINGLE.

Format output:
MULTIPLE:
1. [sub-pertanyaan 1]
2. [sub-pertanyaan 2]
3. [sub-pertanyaan 3]
...

atau

SINGLE

Contoh:

Input: "apa itu sistem informasi ipi garut dan siapa kaprodi nya"
Output:
MULTIPLE:
1. apa itu sistem informasi?
2. apa itu ipi garut?
3. siapa kaprodi sistem informasi?

Input: "biaya kuliah berapa dan dimana lokasi kampus?"
Output:
MULTIPLE:
1. biaya kuliah si berapa?
2. dimana lokasi kampus ipi?

Input: "apa itu sistem informasi?"
Output:
SINGLE

Input: "prospek kerja lulusan si apa saja dan berapa lama kuliah?"
Output:
MULTIPLE:
1. prospek kerja lulusan si apa saja?
2. berapa lama kuliah si?

Penting:
- Ekstrak pertanyaan yang jelas dan spesifik
- Jangan duplikasi konten yang sama
- Maksimal 5 sub-pertanyaan
- Pertahankan konteks SI/IPI jika relevan"""
        
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            model=groq_model,
            temperature=0.3,
            max_tokens=300,
        )
        
        result = response.choices[0].message.content.strip()
        
        if result.startswith("SINGLE"):
            return False, []
        elif result.startswith("MULTIPLE:"):
            lines = result.split('\n')[1:]  # Skip "MULTIPLE:" line
            sub_questions = []
            for line in lines:
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-')):
                    # Remove numbering (e.g., "1. ", "- ")
                    question = line.split('.', 1)[-1].strip() if '.' in line else line.lstrip('-').strip()
                    if question:
                        sub_questions.append(question)
            
            # Limit to max questions
            sub_questions = sub_questions[:MULTI_INTENT_MAX_QUESTIONS]
            
            if sub_questions:
                return True, sub_questions
        
        return False, []
        
    except Exception as e:
        print(f"[ERROR] Multi-intent detection error: {e}")
        return False, []
