import google.generativeai as genai

# Test API key
genai.configure(api_key="AIzaSyCfSLSqi8ZYPyyx26Zl30tYJDoR2zjNj08")
model = genai.GenerativeModel('gemini-2.0-flash-exp')

response = model.generate_content("Say hello")
print(response.text)