from gemini_image_processor import GeminiImageProcessor
from gemini_transcription_model import GeminiTranscriptionModel
from gemini_image_description_model import GeminiImageDescriptionModel
from metadata_exporter import MetadataExporter
from metadata import Metadata
from extended_metadata import ExtendedMetadata
from transcription import Transcription
from token_tracker import TokenTracker
import time

def generate_metadata_single_image(image_front_path,image_processor,image_description_model,metadata_exporter,csv_file,token_tracker):
    image_front = image_processor.process_image(image_front_path)

    title = image_description_model.generate_title(image_front,"")
    abstract = image_description_model.generate_abstract(image_front,"")

    metadata = Metadata(image_front.display_name, title, abstract,token_tracker)
    metadata_exporter.write_to_csv(metadata, csv_file)

    #reset token counting mechanism after every metadata object generated
    token_tracker.reset()

def generate_metadata_front_and_back(image_front_path,image_back_path,image_processor,transcription_model,image_description_model,metadata_exporter,csv_file,token_tracker):
    image_front = image_processor.process_image(image_front_path)
    image_back = image_processor.process_image(image_back_path)

    transcription = transcription_model.generate_transcription(image_back)
    context = transcription.get_raw_transcription()
    total_token_count = transcription_model.get_total_tokens()
    total_input_token_count = transcription_model.get_input_tokens()
    total_output_token_count = transcription_model.get_output_tokens()

    title = image_description_model.generate_title(image_front,context)
    time.sleep(60) #To bypass the 2 requests per minute limitation set for the free tier of the Gemini API
    abstract = image_description_model.generate_abstract(image_front,context)

    total_token_count +=image_description_model.get_total_tokens()
    total_input_token_count +=image_description_model.get_total_input_tokens()
    total_output_token_count +=image_description_model.get_total_output_tokens()

    metadata = ExtendedMetadata(image_front.display_name,title,abstract,transcription,total_token_count,total_input_token_count,total_output_token_count)
    metadata_exporter.write_to_csv(metadata,csv_file)

    token_tracker.reset()

#Initialize image_processor
image_processor = GeminiImageProcessor()

#Initialize token tracker class
token_tracker = TokenTracker()

#Initialize transcription model
transcription_prompt_file= "Prompts/Transcription_Prompts/transcription_prompt.txt"
transcription_model = GeminiTranscriptionModel(transcription_prompt_file,token_tracker)
#Make sure in documentation relationship with transcription and photographer_name/date is clear


#Initialize image description model
title_prompt_file = "Prompts/Title_Prompts/title_prompt.txt"
abstract_prompt_file = "Prompts/Abstract_Prompts/abstract_prompt.txt"
image_description_model = GeminiImageDescriptionModel(title_prompt_file, abstract_prompt_file,token_tracker)

#Initialize metadata exporter class
metadata_exporter = MetadataExporter()

#ACTUAL PROCESSING CODE AFTER MODEL INSTANTIATION
image_front_path = "../Test_Images/portrait.tif"
image_back_path = "../Test_Images/portrait_back.tif"
result_double_csv = "CSV_files/double_image_results.csv"
result_single_csv = "CSV_files/single_image_results.csv"

#generate_metadata_front_and_back(image_front_path,image_back_path,image_processor,transcription_model,image_description_model,metadata_exporter,result_double_csv,token_tracker)
generate_metadata_single_image(image_front_path,image_processor,image_description_model,metadata_exporter,result_single_csv,token_tracker)


""" Be able to mix and match
Directory_Path = "Images"
with open("manifest.txt",'r') as manifest_file:
    file_name = manifest_file.read()
    image_front_path - f"{Directory_Path}{file_name}"
    generate_metadat


Directory:
for identifier in directory:
    generate_metadata_front_and_back(image):
"""