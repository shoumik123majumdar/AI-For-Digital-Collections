from image_description_model import ImageDescriptionModel
import google.generativeai as genai
import os

class GeminiImageDescriptionModel(ImageDescriptionModel):
    """
    Generates Image Descriptions (Titles, Abstracts) using Gemini
    """
    def __init__(self, title_prompt_file,abstract_prompt_file):
        super().__init__(title_prompt_file,abstract_prompt_file)
        goog_key = os.environ.get("GOOG_KEY")
        genai.configure(api_key=goog_key)
        generation_config = genai.GenerationConfig(temperature=0)
        self.__model = genai.GenerativeModel("gemini-1.5-pro", generation_config=generation_config)

    #LOTS OF REUSED CODE, HOW TO REFACTOR?
    def generate_title(self,image_file,context):
        title_prompt = self.title_prompt + context
        response = self.model.generate_content(contents=[title_prompt, image_file])
        self.title_token_data = response.usage_metadata()
        return response.text

    def generate_abstract(self,image_file,context):
        abstract_prompt = self.abstract_prompt + context
        response = self.model.generate_content(contents=[abstract_prompt, image_file])
        self.abstract_token_data = response.usage_metadata()
        return response.text

    def get_total_tokens(self):
        if self.abstract_token_data is None or self.title_token_data is None:
            return "abstract or title has not been generated yet, therefore no total token count can be returned"
        else:
            return self.title_token_data['total_tokens'] + self.abstract_token_data['total_tokens']

    def get_total_input_tokens(self):
        if self.abstract_token_data is None or self.title_token_data is None:
            return "abstract or title has not been generated yet, therefore no total token count can be returned"
        else:
            return self.title_token_data['prompt_tokens'] + self.abstract_token_data['prompt_tokens']

    def get_total_output_tokens(self):
        if self.abstract_token_data is None or self.title_token_data is None:
            return "abstract or title has not been generated yet, therefore no total token count can be returned"
        else:
            return self.title_token_data['completion_tokens'] + self.abstract_token_data['completion_tokens']