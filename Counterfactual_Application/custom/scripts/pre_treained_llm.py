import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, AutoTokenizer, AutoModelForCausalLM
from transformers import BatchEncoding

class PreTrainedLLM:
    
    BERT = 0
    QWEN = 1

    CPU_DEVICE_NAME = "cpu"
    GPU_DEVICE_NAME = "cuda"

    DEFAULT_MAX_INPUT_LENGTH = 512
    DEFAULT_MAX_OUTPUT_LENGTH = 128

    def __init__(self, model_type = BERT):
        self.__device = self.__setup_device()
        self.__model_folder_path = None
        self.__input_text = None

        self.tokenizer = None
        self.model = None
        self.tokenised_input = None
        
        self.max_input_length = self.DEFAULT_MAX_INPUT_LENGTH
        self.max_output_length = self.DEFAULT_MAX_OUTPUT_LENGTH
        
        self.model_type = model_type


    def __setup_device(self) -> str:
        if torch.cuda.is_available():

            torch.cuda.empty_cache()

            print("GPU processing enabled.")

            return self.GPU_DEVICE_NAME

        else:
            print("GPU processing not available.")
            return self.CPU_DEVICE_NAME


    def __load_model(self):

        print(f"Loading model:'{self.__model_folder_path}'")

        if self.__model_folder_path is None:
            raise Exception("Model folder path is empty.")

        if self.model_type == self.BERT:
            self.tokenizer = T5Tokenizer.from_pretrained(self.__model_folder_path)
            self.model = T5ForConditionalGeneration.from_pretrained(self.__model_folder_path).to(self.__device)
            
        elif self.model_type == self.QWEN:
            self.tokenizer = AutoTokenizer.from_pretrained(self.__model_folder_path)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.__model_folder_path,
                torch_dtype=torch.float16,
                device_map="auto"
            )


    def __tokenise_input(self):

        if self.__input_text is None:
            raise Exception("Input text is empty.")

        if self.model is None or self.tokenizer is None:
            print("Model or tokenizer is not loaded. Model and tokenizer will be loaded.")
            self.__load_model()

        self.tokenised_input = self.tokenizer(self.__input_text, return_tensors="pt", max_length=self.max_input_length, truncation=True).to(self.__device)

    def set_model_folder_path(self, model_folder_path: str):
        self.__model_folder_path = model_folder_path
        self.__load_model()

    def set_input_text(self, input_text: str):
        self.__input_text = input_text
        self.__tokenise_input()

    def get_output(self) -> str:
        if self.tokenised_input is None:
            raise Exception("Input has not been tokenised.")

        with torch.no_grad():
            output = self.model.generate(**self.tokenised_input, max_length=self.max_output_length)

        return self.tokenizer.decode(output[0], skip_special_tokens=True)