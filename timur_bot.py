from google.cloud import vision
import openai

def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient.from_service_account_json(GOOGLE_CLOUD_VISION_CREDENTIALS)

    with open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    result = []
    for text in texts:
        result.append(text.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return " ".join(result)


# Provide the path to the image file
mypromt = 'Старайся как можно лучше: выбери здесь информацию о составе крема и переведи каждый компонент на русский язык, и кратко опиши каждый компонент : ' + detect_text(
    "txtext2.jpg")

# Отправьте промпт для обработки моделью GPT-3
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=mypromt,
    max_tokens=2000
)

# Выведите полученный ответ
print(response.choices[0].text.strip())
