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
    
    
    def get_output(window, input: str, output: str, llm: PreTrainedLLM):
        
        print(f"Original Input: {input} \n Original Output: {output}")
        
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
        
        file.content += "\n\n---\nSynonyms"
        
        for i in synonsyms:
            if synonsyms[i] != []:
                file.content += f"\n\nOriginal Word: {i}"
                for j in synonsyms[i]:
                    num_of_items += 1
                    if j[1] == output:
                        num_of_matching_predictions += 1
                        file.content += f"\nReplaced with: \"{j[0]}\" \n└──>New Output: \"{j[1]}\""
                
        file.content += "\n\n---\nAntonyms"
        
        for i in antonyms:
            if antonyms[i] != []:
                file.content += f"\n\nOriginal Word: {i}"
                for j in antonyms[i]:
                    num_of_items += 1
                    if j[1] == output:
                        num_of_matching_predictions += 1
                        file.content += f"\nReplaced with: \"{j[0]}\" \n└──>New Output: \"{j[1]}\""
                    
        file.content += "\n\n---\nSummary"
        file.content += f"\n\nNumber of Counterfactuals: {num_of_items}"
        file.content += f"\nNumber of Matching Predictions: {num_of_matching_predictions}"
        file.content += f"\nPercentage of Matching Predictions: {num_of_matching_predictions / num_of_items * 100:.2f}%"
        file.content += f"\n\nNumber of Non-matching Predictions: {num_of_items - num_of_matching_predictions}"
        file.content += f"\nPercentage of Non-matching Predictions: {(num_of_items - num_of_matching_predictions) / num_of_items * 100:.2f}%"
        file.content += "\n\n---\nEnd of File"
        
        window.get_elem("LOADING_BAR_TEXT").update_text(window.win_dim, f"Generating Analysis...")
        window.events()
        window.draw()
        
        analysis_llm = PreTrainedLLM(model_type=PreTrainedLLM.QWEN)
        analysis_llm.set_model_folder_path(r"C:\Users\karki\Qwen2.5-3B")
        analysis_llm.max_input_length = 4000
        analysis_llm.max_output_length = 2000
        information = """
Scenario: A engineer / airline crew member has written a report detailing an airline incident. The report is fed into an Large Language Model, whereby the output is a prediction of the part failure. To explain the LLMs prediction, the LLM generates counterfactuals. This works by iterating through each word in the input and replacing it with a synonym or antonym and observing how the output has changed.
        
Task: You must provide a short 2 paragraph summary on what the counterfactuals can tell us about the prediction. Remember that not all synonym and antonym replacements are relevant to the scenario.
        
Information:"""
        analysis_llm.set_input_text(information + file.content)
        print("Analysis:", analysis_llm.get_output())
                
        file.save()
            