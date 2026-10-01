from backend.ai_core.gemini_generator import GeminiDocumentGenerator

def generate_legal_document(document_type,parties,terms,dates):
    generator=GeminiDocumentGenerator()

    return generator.generate_document(
        document_type,
        parties,
        terms,
        dates
    )