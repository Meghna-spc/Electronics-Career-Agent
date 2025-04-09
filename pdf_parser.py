from pdfminer.high_level import extract_text
import re

# Technical keywords for electronics engineering
TECHNICAL_KEYWORDS = [
    "Embedded Systems", "VLSI", "PCB Design", "IoT", "Arduino", "Raspberry Pi",
    "FPGA", "Verilog", "VHDL", "Circuit Design", "Power Electronics", "RF Engineering",
    "Signal Processing", "Microcontrollers", "MATLAB", "LabVIEW", "Altium Designer",
    "C/C++", "Python", "SPICE", "Oscilloscope", "Multisim", "CAD", "Schematic Design"
]

# Transferable skills
TRANSFERABLE_SKILLS = [
    "Problem Solving", "Teamwork", "Communication", "Project Management",
    "Critical Thinking", "Time Management", "Leadership", "Adaptability"
]

def parse_resume(pdf_path):
    try:
        text = extract_text(pdf_path)
        
        # Detect technical skills
        detected_tech = re.findall(r'\b(' + '|'.join(TECHNICAL_KEYWORDS) + r')\b', text, re.I)
        
        # Detect transferable skills
        detected_transferable = re.findall(r'\b(' + '|'.join(TRANSFERABLE_SKILLS) + r')\b', text, re.I)
        
        # Find missing technical keywords
        missing_tech = [kw for kw in TECHNICAL_KEYWORDS if kw.lower() not in text.lower()]
        
        # Extract sections
        experience = re.search(r'Experience(.+?)(Education|Skills)', text, re.DOTALL)
        education = re.search(r'Education(.+?)(Skills|Experience)', text, re.DOTALL)
        
        return {
            'technical_skills': list(set(detected_tech)) or ["No technical skills found"],
            'transferable_skills': list(set(detected_transferable)) or ["No transferable skills found"],
            'missing_keywords': missing_tech[:10],  # Show top 10 missing
            'experience': experience.group(1).strip()[:1000] if experience else "Experience section not found",
            'education': education.group(1).strip()[:1000] if education else "Education section not found",
            'raw_text': text[:2000] + "..."  # For AI analysis
        }
    except Exception as e:
        return {'error': f"Failed to parse PDF: {str(e)}"}
