import json
from typing import Any, Callable, Dict
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from web_data_scraping_system import DataScraper

# ---------------------------------
# Function Registry System
# ---------------------------------
class FunctionRegistry:
    """A simple registry to store and retrieve functions by name."""
    def __init__(self) -> None:
        self._functions: Dict[str, Callable[..., Any]] = {}
    
    def register(self, name: str, func: Callable[..., Any]) -> None:
        """Register a function with a given name."""
        self._functions[name] = func

    def get(self, name: str) -> Callable[..., Any]:
        """Retrieve a function by name (or None if not found)."""
        return self._functions.get(name)

# ---------------------------------
# Function Calling Agent
# ---------------------------------
class FunctionCallingAgent:
    def __init__(self, ai_name: str = "Function Calling Agent", user_name: str = "User", model_id: str = "qwen2:0.5b") -> None:
        """
        Initializes the FunctionCallingAgent.
        
        :param ai_name: Name of the function calling agent.
        :param user_name: Name of the user.
        :param model_id: The identifier for the language model to use.
        """
        self.ai_name = ai_name
        self.user_name = user_name
        self.model_id = model_id

        # Initialize DataScraper for real-time context (if needed)
        self.data_scraper = DataScraper()
        self.update_realtime_data()

        # Define a simple prompt template
        self.template = f"""
Context:
{{context}}

{self.user_name}: {{question}}

{self.ai_name}:"""
        self.prompt = ChatPromptTemplate.from_template(self.template)
        self.model = OllamaLLM(model=self.model_id)
        self.chain = self.prompt | self.model

        # Initialize the function registry
        self.function_registry = FunctionRegistry()

    def update_realtime_data(self):
        """Fetch updated real-time data from DataScraper."""
        self.current_time = self.data_scraper.getCurrentTime()
        self.current_date = self.data_scraper.getCurrentDate()
        self.current_location = self.data_scraper.getCurrentLocation()
        self.current_weather = self.data_scraper.getCurrentWeather()

        self.context = (
            f"Real-time Info:\n"
            f"- Time: {self.current_time}\n"
            f"- Date: {self.current_date}\n"
            f"- Location: {self.current_location}\n"
            f"- Weather: {self.current_weather}\n"
        )

    def register_function(self, name: str, func: Callable[..., Any]) -> None:
        """
        Registers a function so that the agent can call it.
        
        :param name: The function's name.
        :param func: The callable to register.
        """
        self.function_registry.register(name, func)

    def process_response(self, response: str) -> str:
        """
        Analyzes the model's response. If it appears to be a JSON-formatted function call,
        retrieves and calls the corresponding function from the registry. Otherwise, returns
        the original plain-text response.
        
        :param response: The raw response from the LLM.
        :return: The final processed response.
        """
        stripped = response.strip()
        # Check if the response is formatted as JSON (simple heuristic)
        if stripped.startswith("{") and stripped.endswith("}"):
            try:
                parsed = json.loads(stripped)
                if "function_call" in parsed:
                    func_call = parsed["function_call"]
                    func_name = func_call.get("name")
                    arguments = func_call.get("arguments", {})
                    func = self.function_registry.get(func_name)
                    if func:
                        func_result = func(**arguments)
                        enriched = {
                            "original_response": parsed,
                            "function_result": func_result
                        }
                        print(f"Function call '{func_name}' executed successfully.")
                        return json.dumps(enriched, indent=2)
                    else:
                        print(f"Function '{func_name}' not found in registry.")
                        return response
                else:
                    print("No function call detected in JSON response.")
                    return response
            except Exception as e:
                print(f"Error parsing JSON: {e}")
                return response
        else:
            print("No JSON response detected.")
            return response

    def get_response(self, question: str) -> str:
        """
        Generates the agent's response to a given question.
        It updates the context, invokes the model, then processes the response for any function calls.
        
        :param question: The user's query.
        :return: The final response.
        """
        self.update_realtime_data()
        raw_response = self.chain.invoke({
            "context": self.context,
            "question": question,
        })
        print("Raw response from model:" + raw_response)
        final_response = self.process_response(raw_response)
        return final_response

# ---------------------------------
# Example Usage
# ---------------------------------
if __name__ == "__main__":
    agent = FunctionCallingAgent(ai_name="Function Calling Agent", user_name="Gianne", model_id="qwen2:0.5b")

    # Register a sample function, for example: get_current_weather
    def get_current_weather(location: str) -> str:
        # Dummy implementation: In production, query an API here.
        return f"Sunny in {location} at 25 degrees Celcius."
    
    agent.register_function("get_current_weather", get_current_weather)
    
    # Simulate a model response instructing a function call
    simulated_response = json.dumps({
        "function_call": {
            "name": "get_current_weather",
            "arguments": {"location": "San Francisco"}
        }
    })
    processed = agent.process_response(simulated_response)
    print("Processed simulated response:")
    print(processed)
    
    # Ask the agent a question (this will invoke the model)
    user_query = "What's the current weather in San Francisco?"
    final_output = agent.get_response(user_query)
    print("\nFinal agent output:")
    print(final_output)


# Run Command: python function_calling_agent.py