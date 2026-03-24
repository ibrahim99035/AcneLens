import express from 'express';
import multer from 'multer';
import { GoogleGenAI } from '@google/genai';
import cors from 'cors';

const app = express();
app.use(cors());
app.use(express.json());

// ✅ SECURE: Key is pulled from Vercel Environment Variables
const ai = new GoogleGenAI({ 
    apiKey: process.env.GEMINI_API_KEY 
});

// Use Memory Storage for Vercel (much faster than /tmp/)
const upload = multer({ storage: multer.memoryStorage() });

app.get('/', (req, res) => res.send('Acne AI Backend is Online 🚀'));

app.post('/api/analyze', upload.single('image'), async (req, res) => {
    try {
        if (!req.file) return res.status(400).json({ error: "No image uploaded" });

        const imageBase64 = req.file.buffer.toString("base64");
        const answers = JSON.parse(req.body.user_answers || "{}");

        const prompt = `
            Analyze this skin image for acne.
            Profile: ${answers.gender}, Age ${answers.age}, Skin Type: ${answers.skinType}.
            Symptoms: Painful? ${answers.painful}, Pus? ${answers.pus}, Redness? ${answers.redness}.
            
            1. Identify acne type.
            2. Evaluate suitability of 'Clarino' (Basil, Tea Tree, Thyme, Lavender).
            
            Return ONLY JSON: 
            {"diagnosis": "...", "suitability": "...", "reasoning": "...", "clinical_note": "..."}
        `;

        const response = await ai.models.generateContent({
            model: "gemini-3-flash-preview",
            contents: [{
                role: "user",
                parts: [
                    { text: prompt },
                    { inlineData: { data: imageBase64, mimeType: req.file.mimetype } }
                ]
            }],
            generationConfig: { media_resolution: "HIGH" }
        });

        // Clean and parse JSON response
        const text = response.text.replace(/```json|```/g, "").trim();
        res.json(JSON.parse(text));

    } catch (error) {
        console.error("AI Error:", error.message);
        res.status(500).json({ error: "AI Analysis failed. Check Vercel logs." });
    }
});

export default app;