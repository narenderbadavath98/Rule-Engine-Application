import re

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):  # Double underscores
        self.node_type = node_type
        self.left = left
        self.right = right
        self.value = value

#API DESIGN FUNCTIONS


def create_rule(rule_string):
    print("Parsing rule:", rule_string)  # Debugging print
    tokens = re.findall(r'\(|\)|AND|OR|\w+\s*[<>!=]=?\s*\w+', rule_string)
    print("Tokens:", tokens)  # Debugging print
    stack = []
 
    precedence = {'OR': 1, 'AND': 2}
 
    def apply_operator(operator):
        if len(stack) < 2:
            raise ValueError("Invalid rule string: Not enough operands for operator") 
        right = stack.pop()
        left = stack.pop()
        stack.append(Node(node_type="operator", left=left, right=right, value=operator))

    for token in tokens:
        print("Processing token:", token)  # Debugging print
        if token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                operator = stack.pop()
                if operator in precedence:
                    apply_operator(operator)
                else:
                    raise ValueError("Invalid rule string: Unexpected token encountered")
            stack.pop()  # Pop the opening parenthesis
        elif token in precedence:
            while stack and stack[-1] in precedence and precedence[token] <= precedence[stack[-1]]:
                apply_operator(stack.pop())
            stack.append(token)
        else:  # token is an operand
            stack.append(Node(node_type="operand", value=token))
 
    while stack and stack[-1] in precedence:
        apply_operator(stack.pop())
 
    if len(stack) != 1:
        raise ValueError("Invalid rule string: Unbalanced parentheses or operators") 
 
    return stack[0]  # Return the root of the AST

#combine rules
def combine_rules(rules):
    if not rules:
        return None

    root = create_rule(rules[0])
    for rule in rules[1:]:
        new_root = create_rule(rule)
        root = Node(node_type="operator", left=root, right=new_root, value="OR")  # Combine using OR
    return root

#evaluation rule
def evaluate_rule(node, data):
    if node.node_type == "operand":
        # Evaluate the condition
        condition = node.value
        attribute, operator, value = re.split(r'\s*([<>!=]+)\s*', condition)
        attribute = attribute.strip()
        value = value.strip().strip("'")  # Remove quotes for string comparison

        if operator == '>':
            return data[attribute] > int(value)
        elif operator == '<':
            return data[attribute] < int(value)
        elif operator == '=':
            return data[attribute] == value
        elif operator == '!=':
            return data[attribute] != value
        # Add more operators as needed
    elif node.node_type == "operator":
        left_eval = evaluate_rule(node.left, data)
        right_eval = evaluate_rule(node.right, data)
        
        if node.value == "AND":
            return left_eval and right_eval
        elif node.value == "OR":
            return left_eval or right_eval

# Test case - Example output
if __name__ == "__main__":
    # Example rules and data
    rules = ["age > 30 AND income >= 50000", "department = 'IT'"]
    root = combine_rules(rules)
    
    # Example data
    data = {
        "age": 35,
        "income": 55000,
        "department": "IT"
    }
    
    # Evaluating the rules against the data
    result = evaluate_rule(root, data)
    print(result)  # Output: True (if the conditions are satisfied)