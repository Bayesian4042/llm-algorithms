import re
import os
import sys
import subprocess
import importlib
from openai import AzureOpenAI
from tavily import TavilyClient
from prompts import get_system_prompt
from opik import track

class CodingAgent:
    def __init__(self):
        self._load_credentials()
        
        self.openai_client = AzureOpenAI(
            api_key=self.openai_api_key,
            azure_endpoint=self.azure_endpoint,
            api_version=self.azure_api_version,
            azure_deployment=self.azure_deployment
        )
        
        self.tavily_client = TavilyClient(api_key=self.tavily_api_key)
        
        self.MAX_DEBUGGER_LIMIT = 3
        self.system_prompt = get_system_prompt()

    def _load_credentials(self):
        """Load API credentials from environment variables"""
        self.openai_api_key = os.getenv('AZURE_OPENAI_API_KEY')
        self.azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        self.azure_api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')
        self.azure_deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')
        
        self.tavily_api_key = os.getenv('TAVILY_API_KEY')
        
        missing_vars = []
        required_vars = [
            ('AZURE_OPENAI_API_KEY', self.openai_api_key),
            ('AZURE_OPENAI_ENDPOINT', self.azure_endpoint),
            ('AZURE_OPENAI_DEPLOYMENT', self.azure_deployment),
            ('TAVILY_API_KEY', self.tavily_api_key)
        ]
        
        for var_name, var_value in required_vars:
            if not var_value:
                missing_vars.append(var_name)
                
        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

    @track
    def tavily_search(self, query: str) -> dict:
        """Execute a Tavily search and return results"""
        try:
            response = self.tavily_client.search(query)
            print("Tavily search result:", response)
            return response
        except Exception as e:
            error_msg = f"Error performing search: {str(e)}"
            print(error_msg)
            return {"error": error_msg}

    def install_libraries(self, libraries: str) -> None:
        """Install required Python libraries"""
        libraries = re.findall(r'#\s*pip install\s+([\w-]+)', libraries)
        if not libraries:
            return

        print("Installing required libraries...")
        for lib in libraries:
            try:
                importlib.import_module(lib.replace('-', '_'))
                print(f"{lib} is already installed.")
            except ImportError:
                print(f"Installing {lib}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
        print("Libraries installed successfully.")

    def extract_action_details(self, text: str) -> tuple:
        """Extract action and action_input from text"""
        action = None
        action_input = None
        lines = text.splitlines()
        in_triple_quotes = False
        triple_quote_content = []

        for line in lines:
            line_stripped = line.strip()

            if line_stripped.startswith('action:'):
                action = line_stripped[7:].strip()
                continue

            if line_stripped.startswith('action_input:'):
                if '"""' in line_stripped:
                    in_triple_quotes = True
                    content_after_quotes = line_stripped[line_stripped.find('"""') + 3:]
                    if content_after_quotes:
                        triple_quote_content.append(content_after_quotes)
                    continue
                else:
                    action_input = line_stripped[12:].strip()
                    if action_input.startswith('"') and action_input.endswith('"'):
                        action_input = action_input[1:-1]
                    continue

            if in_triple_quotes:
                if '"""' in line_stripped:
                    content_before_quotes = line[:line.find('"""')]
                    if content_before_quotes:
                        triple_quote_content.append(content_before_quotes)
                    in_triple_quotes = False
                    action_input = '\n'.join(triple_quote_content)
                else:
                    triple_quote_content.append(line)

        return action, action_input

    @track
    def execute_code(self, code: str) -> tuple:
        """Execute Python code and return output and error"""
        print("Creating temp file:", code)
        with open('code.py', 'w') as f:
            f.write(code)

        try:
            result = subprocess.run(
                ['python', 'code.py'],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return "", "Execution timed out after 30 seconds."

    @track
    def run(self, prompt: str) -> None:
        """Main execution loop for the coding agent"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]

        debugger_limit = 0
        try:
            while True:
                print('Analyzing...')
                response = self.openai_client.chat.completions.create(
                    messages=messages,
                    model="gpt-4o-mini",
                    temperature=0,
                )

                response_message = response.choices[0].message.content
                print("Response message:", response_message)

                action, action_input = self.extract_action_details(response_message)

                if action == "tavily_search":
                    print("Searching for results...")
                    search_result = self.tavily_search(action_input)
                    messages.extend([
                        {"role": "system", "content": response_message},
                        {"role": "user", "content": f"Observation: {search_result}"},
                    ])

                elif action == "code":
                    output, error = self.execute_code(action_input)
                    if error and debugger_limit < self.MAX_DEBUGGER_LIMIT:
                        messages.extend([
                            {"role": "system", "content": response_message},
                            {"role": "user", "content": f"Observation: {error}"},
                        ])
                        debugger_limit += 1
                    else:
                        break

                elif action == "human":
                    print("Done")
                    break

        except Exception as e:
            print(f"Error in run: {str(e)}")