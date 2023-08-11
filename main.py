from google.cloud import texttospeech
import fitz

def synthesize_long_audio(project_id, location, output_gcs_uri):
    """
    Synthesizes long input, writing the resulting audio to `output_gcs_uri`.

    Example usage: synthesize_long_audio('12345', 'us-central1', 'gs://{BUCKET_NAME}/{OUTPUT_FILE_NAME}.wav')

    """
    pdf_path = "C:/Users/Pc/Downloads/2023_Information_for_Fresh_and_Returning_Sudents.pdf"
    text = ""

    pdf_document = fitz.open(pdf_path)
    num_pages = pdf_document.page_count

    for page_number in range(num_pages):
        page = pdf_document[page_number]
        text += page.get_text()

    pdf_document.close()
    project_id = project_id
    location = location
    output_gcs_uri = f'gs://ade-audio-bucket/{output_gcs_uri}'

    client = texttospeech.TextToSpeechLongAudioSynthesizeClient()

    input = texttospeech.SynthesisInput(
        text=text
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Standard-A"
    )

    parent = f"projects/{project_id}/locations/{location}"

    request = texttospeech.SynthesizeLongAudioRequest(
        parent=parent,
        input=input,
        audio_config=audio_config,
        voice=voice,
        output_gcs_uri=output_gcs_uri,
    )

    operation = client.synthesize_long_audio(request=request)
    # Set a deadline for your LRO to finish. 300 seconds is reasonable, but can be adjusted depending on the length of the input.
    # If the operation times out, that likely means there was an error. In that case, inspect the error, and try again.
    result = operation.result(timeout=300)
    print(
        "\nFinished processing, check your GCS bucket to find your audio file! Printing what should be an empty result: ",
        result,
    )


synthesize_long_audio(project_id='king-ade-texttospeech', location='europe-west1', output_gcs_uri='students_information.mp3')