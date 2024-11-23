class HandlerPrompt:
    def __init__(self):
        self.history = []
        self.promptType = 0

    def PromptType(self):
        return self.promptType
    def PromptType(self, pt):
        self.promptType = pt

    def Execute(self):
        cmd = ""
        while cmd.lower() == "exit":
            cmd = str(input(f""))
            if cmd.lower() == "exit":
                if self.PromptType() == 0:
                    # Close Down Server
                    print("philler")
                else:
                    # Exit Session Prompt and Shift to C2 Prompt
                    self.PromptType(self.PromptType()-1)