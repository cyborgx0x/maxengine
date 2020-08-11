import random
  

class Question:
    """
    Generate the question
    """
    def __init__(self, question, solution, *arg, hint, full_solution):
        self.question = question
        self.solution = solution
        self.other_answer = arg
        self.hint = hint
        self.full_solution = full_solution
        self.ans_bank = self.answer_sheet()
    def answer_question(self, choice):
        comparing_file = self.ans_bank
        key_to_compare = choice.upper()
        if key_to_compare in comparing_file and comparing_file[key_to_compare] == self.solution:
            print(self.full_solution)
        else: 
            print(self.hint)
            return True
    def question_for_user(self):
        "when user request training"
        print("Answer Following Question: \n" + self.question)
        
        for key in self.ans_bank:
            print (key + ":" + self.ans_bank[key])
    def answer_sheet(self):
        answer_bank = [self.solution, *self.other_answer]
        answer_bank = random.sample(answer_bank,4)
        key_answer = ["A","B","C","D"]
        user_to_choice = dict(zip(key_answer,answer_bank))
        return user_to_choice
    def loop_answer(self, choice):
        comparing_file=self.answer_sheet()
        key_to_compare = choice.upper()
        if key_to_compare in comparing_file and comparing_file[key_to_compare] == self.solution:
            pass
        else: 
            return True    
                
