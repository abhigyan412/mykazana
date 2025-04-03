from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from PIL import Image
import pytesseract
from pdfminer.high_level import extract_text
import os
from io import BytesIO
import re

# Helper function for extracting text from file
def extract_text_from_file(file):
    file_extension = file.name.split('.')[-1].lower()
    
    if file_extension == 'pdf':
        return extract_text_from_pdf(file)
    elif file_extension in ['jpeg', 'jpg', 'png']:
        return extract_text_from_image(file)
    return None  # Return None instead of raising an error

# Extract text from PDF
def extract_text_from_pdf(file):
    file_content = file.read()
    file_like_object = BytesIO(file_content)
    return extract_text(file_like_object)

# Extract text from Image using OCR (Tesseract)
def extract_text_from_image(file):
    image = Image.open(file)
    return pytesseract.image_to_string(image)

# Improved Categorization function
def categorize_document(text):
    text = text.lower()
    
    # Keyword sets for categorization
    keywords = {
        'tax': ['tax', 'income tax', 'gst', 'irs'],
        'identity': ['passport', 'aadhar', 'ssn', 'identity'],
        'medical': ['hospital', 'prescription', 'diagnosis', 'medical'],
        'real_estate': ['property', 'real estate', 'mortgage', 'lease']
    }
    
    total_words = len(text.split()) if text.strip() else 1  # Avoid division by zero
    best_category = 'other'
    highest_confidence = 0.4  # Baseline confidence

    for category, words in keywords.items():
        match_count = sum(len(re.findall(r'\b' + word + r'\b', text)) for word in words)
        confidence = min(1.0, 0.4 + (match_count / total_words))  # Dynamic confidence score

        if match_count > 0 and confidence > highest_confidence:
            best_category = category
            highest_confidence = confidence
    
    return best_category, highest_confidence

class Document(models.Model):
    CATEGORY_CHOICES = [
        ('tax', 'Tax'),
        ('identity', 'Identity'),
        ('medical', 'Medical'),
        ('real_estate', 'Real Estate'),
        ('other', 'Other')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    extracted_text = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    confidence_score = models.FloatField(default=0.0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Check file size limit (10MB) before saving."""
        if self.file and self.file.size > 10 * 1024 * 1024:
            raise ValidationError("File size cannot exceed 10MB.")

    def save(self, *args, **kwargs):
        """Extract text and categorize the document on save."""
        if not self.extracted_text:
            extracted_text = extract_text_from_file(self.file)
            if extracted_text:
                self.extracted_text = extracted_text
                self.category, self.confidence_score = categorize_document(extracted_text)
        super().save(*args, **kwargs)
