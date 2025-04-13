from custom.scripts.pre_treained_llm import PreTrainedLLM
from scripts.utility.logger import Logger
from custom.scripts.file_handler import FileHandler
import re
from nltk.corpus import wordnet

class CounterfactualGenerator:
    
    MIN_WORD_LEN = 3
    INCLUDE_MULTI_WORD_SYNONYMS = False
    SYNONYM = 0
    ANTONYM = 1
    
    def __get_clean_string(value: str) -> str:
        return re.sub(r'[^A-Za-z ]', '', value)
    
    def __get_words(value: str) -> list[str]:
        return CounterfactualGenerator.__get_clean_string(value).split(" ")
    
    def __get_synonyms(word: str) -> list[str]:
        synonyms = set()
        
        for synset in wordnet.synsets(word):
            for lemma in synset.lemmas():
                synonym = lemma.name().replace("_", " ")  # Replace underscores with spaces
                if synonym.lower() != word.lower():  # Exclude the original word
                    synonyms.add(synonym)
                    
        return list(synonyms)
    
    def __get_antonyms(word: str) -> list[str]:
        antonyms = set()
        
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                if lemma.antonyms():  # Check if antonyms exist
                    for antonym in lemma.antonyms():
                        antonyms.add(antonym.name().replace("_", " "))  # Replace underscores with spaces
                        
        return list(antonyms)
        
        
    def __get_counterfactual_outputs(window,
                                     input: str, 
                                     llm: PreTrainedLLM, 
                                     mode = SYNONYM) -> dict[str, list[tuple[str, str]]]:
        
        counterfactuals: dict[str, list[tuple[str, str]]] = {}
        
        input_word_list = CounterfactualGenerator.__get_words(input)
        
        num_of_items = len(input_word_list)
        completed_num_items = 0
        
        for word in input_word_list:
            counterfactuals[word] = []
            
            if len(word) > 3:
                
                if mode == CounterfactualGenerator.SYNONYM:
                    new_words = CounterfactualGenerator.__get_synonyms(word)
                elif mode == CounterfactualGenerator.ANTONYM:
                    new_words = CounterfactualGenerator.__get_antonyms(word)
                else:
                    Logger.raise_exception("Invalid mode. Use SYNONYM or ANTONYM.")
                
                for new_word in new_words:
                    if " " not in new_word:
                        
                        new_input = input.replace(word, new_word)
                        
                        llm.set_input_text(new_input)
                        
                        counterfactuals[word].append((new_word, llm.get_output()))
            
            completed_num_items += 1
            percentage = int((completed_num_items / num_of_items) * 100)
              
            if mode == CounterfactualGenerator.SYNONYM:
                window.get_elem("LOADING_BAR_TEXT").update_text(window.win_dim, f"Generating Synonym Counterfactuals: {percentage}%")
                
            elif mode == CounterfactualGenerator.ANTONYM:
                window.get_elem("LOADING_BAR_TEXT").update_text(window.win_dim, f"Generating Antonym Counterfactuals: {percentage}%")
            
            window.events()
            window.draw()
                        
        return counterfactuals
    
    
    def get_output_str(original_output: str,
                       counterfactual_data: dict[str, list[tuple[str, str]]],
                       include_correct: bool = True,
                       include_incorrect: bool = True) -> str:
        
        output = ""
        
        for word in counterfactual_data:
            
            correct = False
            incorrect = False
            
            word_output = ""
            if counterfactual_data[word] != []:
                
                word_output += f"\n\nOriginal Word: {word}"
                
                for i in counterfactual_data[word]:
                    
                    replacement_text = f"\nReplaced with: \"{i[0]}\" \n└──>New Output: \"{i[1]}\""
                    
                    if i[1] == original_output:
                        if include_correct:
                            word_output += replacement_text
                            
                        correct = True
                        
                    else:
                        if include_incorrect:
                            word_output += replacement_text
                            
                        incorrect = True
                        
            
            if (correct and include_correct) or (incorrect and include_incorrect):
                output += word_output
                
        return output[2:] if output != "" else "None."
    
    
    def get_output(window, input: str, output: str, llm: PreTrainedLLM):
        
        Logger.log_info(f"Generating Counterfactuals for: {input} \n\nOutput: {output}")
        
        file = FileHandler("test.txt")
        
        file.content += f"Original Input {input}\n\nOriginal Output {output}"
        
        synonsyms = CounterfactualGenerator.__get_counterfactual_outputs(
            window,
            input,
            llm,
            CounterfactualGenerator.SYNONYM
        )
        
        antonyms = CounterfactualGenerator.__get_counterfactual_outputs(
            window,
            input,
            llm,
            CounterfactualGenerator.ANTONYM
        )
        
        num_of_items = 0
        num_of_matching_predictions = 0
        
        for word in synonsyms:
            num_of_items += len(synonsyms[word])
            
            for i in synonsyms[word]:
                if i[1] == output:
                    num_of_matching_predictions += 1
                    
        for word in antonyms:
            num_of_items += len(antonyms[word])
            
            for i in antonyms[word]:
                if i[1] == output:
                    num_of_matching_predictions += 1
        
        synonyms_text = CounterfactualGenerator.get_output_str(output, synonsyms, True, True)
        correct_synonyms = CounterfactualGenerator.get_output_str(output, synonsyms, True, False)
        incorrect_synonyms = CounterfactualGenerator.get_output_str(output, synonsyms, False, True)
        print(incorrect_synonyms)
           
        antonyms_text = CounterfactualGenerator.get_output_str(output, antonyms, True, True)
        correct_antonyms = CounterfactualGenerator.get_output_str(output, antonyms, True, False)
        incorrect_antonyms = CounterfactualGenerator.get_output_str(output, antonyms, False, True)
        
                    
        summary = f"Number of Counterfactuals: {num_of_items}"
        summary += f"\nNumber of Matching Predictions: {num_of_matching_predictions}"
        summary += f"\nPercentage of Matching Predictions: {num_of_matching_predictions / num_of_items * 100:.2f}%"
        summary += f"\n\nNumber of Non-matching Predictions: {num_of_items - num_of_matching_predictions}"
        summary += f"\nPercentage of Non-matching Predictions: {(num_of_items - num_of_matching_predictions) / num_of_items * 100:.2f}%"
        
        
        window.get_elem("LOADING_BAR_TEXT").update_text(window.win_dim, f"Generating Analysis...")
        window.events()
        window.draw()
        
#         analysis_llm = PreTrainedLLM(model_type=PreTrainedLLM.QWEN)
#         analysis_llm.set_model_folder_path(r"C:\Users\karki\Qwen2.5-3B")
#         analysis_llm.max_input_length = 4000
#         analysis_llm.max_output_length = 6000
#         information = """
# Scenario: A engineer / airline crew member has written a report detailing an airline incident. The report is fed into an Large Language Model, whereby the output is a prediction of the part failure. To explain the LLMs prediction, the LLM generates counterfactuals. This works by iterating through each word in the input and replacing it with a synonym or antonym and observing how the output has changed.
        
# Task: You must provide a short 2 paragraph summary on what the counterfactuals can tell us about the prediction. Remember that not all synonym and antonym replacements are relevant to the scenario.
        
# Information:"""
#         analysis_llm.set_input_text(information + file.content)
#         print("Analysis:", analysis_llm.get_output())
        
        file.content = summary + synonyms_text + antonyms_text
        print(file.content)
        
        file.save()
        
        all_outputs = {
        "DISPLAY_ALL": synonyms_text + antonyms_text,
        "DISPLAY_SYNONYMS": synonyms_text,
        "DISPLAY_CORRECT_SYNONYMS": correct_synonyms,
        "DISPLAY_INCORRECT_SYNONYMS": incorrect_synonyms,
        "DISPLAY_ANTONYMS": antonyms_text,
        "DISPLAY_CORRECT_ANTONYMS": correct_antonyms,
        "DISPLAY_INCORRECT_ANTONYMS": incorrect_antonyms
        }
        
        return summary, all_outputs
            