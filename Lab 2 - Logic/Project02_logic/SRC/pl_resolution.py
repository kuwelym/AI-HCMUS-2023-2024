class PLResolution:
    """
    A class that implements the PL-Resolution algorithm for propositional logic.

    Attributes:
    - input_path (str): The path to the input file.
    - output_path (str): The path to the output file.
    - kb_clauses (list[list[str]]): The knowledge base clauses.
    - alpha_clause (list[str]): The alpha clause.
    - loops (list[list]): The list of loop(clauses generated from resolution rules).
    - entails (bool): Indicates whether the knowledge base clauses entails the alpha clause.

    Methods:
    - __init__(self, input_path:str, output_path:str): Initializes the PLResolution object.
    - custom_sort(self, literal:str): Custom sorting function for literals.
    - parse_clause(self, clause_str:str): Parses a clause string into a list of literals.
    - read_input(self): Reads the input file and returns the alpha clause and knowledge base clauses.
    - negate_literal(self, literal:str): Negates a literal by adding or removing the '-' character.
    - write_output(self): Writes the output data to the output file.
    - pl_resolution(self): Performs the PL-Resolution algorithm.
    """

    def __init__(self, input_path:str, output_path:str):
        """
        Initializes the PLResolution object.

        Args:
        - input_path (str): The path to the input file.
        - output_path (str): The path to the output file.
        """
        self.input_path = input_path
        self.output_path = output_path
        self.kb_clauses = []
        self.alpha_clause = []
        self.loops = []
        self.entails = False

    def custom_sort(self, literal:str):
        """
        Custom sorting function for literals.

        Args:
        - literal (str): The literal to be sorted.

        Returns:
        - str: The sorted literal.
        """
        # Ignore '-' character for sorting
        return literal.replace('-', '')

    def parse_clause(self, clause_str:str):
        """
        Parses a clause string into a list of literals.

        Args:
        - clause_str (str): The clause string to be parsed.

        Returns:
        - list[str]: The list of literals in the clause.
        """
        literals = [literal.strip() for literal in clause_str.split('OR')]
        sorted_literals = sorted(literals, key=self.custom_sort)
        return sorted_literals

    def read_input(self):
        """
        Reads the input file and returns the alpha clause and knowledge base clauses.

        Returns:
        - tuple[list[str], list[list[str]]]: The alpha clause and knowledge base clauses.
        """
        with open(self.input_path, 'r') as file:
            self.alpha_clause = self.parse_clause(file.readline().strip())
            num_clauses = int(file.readline().strip())
            self.kb_clauses = [self.parse_clause(file.readline()) for _ in range(num_clauses)]

    def negate_literal(self, literal:str):
        """
        Negates a literal by adding or removing the '-' character.

        Args:
        - literal (str): The literal to be negated.

        Returns:
        - list[str]: The negated literal.
        """
        if '-' in literal:
            return self.parse_clause(f"{literal[1:]}")
        return self.parse_clause(f"-{literal}")

    def write_output(self):
        """
        Writes the output data to the output file.
        """
        with open(self.output_path, 'w') as file:
            for loop in self.loops:
                file.write(f"{len(loop)}\n")
                for clause in loop:
                    file.write(f"{' OR '.join(clause)}\n")
            
            if self.entails:
                file.write("YES")
            else:
                file.write("0\n")
                file.write("NO")

    def pl_resolution(self):
        """
        Performs the PL-Resolution algorithm.

        Returns:
        - bool: True if the knowledge base clauses entails the alpha clause, False otherwise.
        """
        def is_valid_clause(clause: list):
            literals_set = set()
            for literal in clause:
                negated_literal = self.negate_literal(literal)[0]
                if negated_literal in literals_set or literal in literals_set:
                    return False
                literals_set.add(literal)
            return True
            
        def is_complementary_literals(literal_1: str, literal_2: str):
            return self.negate_literal(literal_1) == self.parse_clause(literal_2)
        
        def resolve(clause1: list[list], clause2: list[list]):
            new_clause = []
            clause1_length = len(clause1)
            clause2_length = len(clause2)
            for literal_1 in clause1:
                for literal_2 in clause2:
                    if (is_complementary_literals(literal_1, literal_2) 
                        and ((clause1_length == 1 or clause2_length == 1) or (clause1_length == 2 and clause2_length == 2 and literal_1 != literal_2))):

                        new_clause += [literal for literal in clause1 if literal != literal_1]
                        new_clause += [literal for literal in clause2 if literal != literal_2]
                        if not new_clause:
                            new_clause.append('{}')
                        break
            if not is_valid_clause(new_clause):
                return []
            return sorted(new_clause, key=self.custom_sort)
        
        clauses = self.kb_clauses.copy()
        for alpha_literal in self.alpha_clause:
            if(self.negate_literal(alpha_literal) not in clauses):
                clauses.append(self.negate_literal(alpha_literal))

        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    resolvents = resolve(clauses[i], clauses[j])
                    if resolvents not in new_clauses and resolvents not in clauses and resolvents != []: 
                        new_clauses.append(resolvents)

            if not new_clauses:
                return False

            clauses += new_clauses
            self.loops.append(new_clauses.copy())

            if ['{}'] in clauses:
                self.entails = True
                return self.entails
