# Example test cases split from test.py
# Add more files in this folder to extend test coverage

test_cases = {
    "multiline": "This is a multi-line command that should be treated as a single command",
    "multi.cmd1": "First command",
    "multi.cmd2": "Second command",
    "multi.cmd3": "^Third command with a continuation \(leading whitespace removed\) text from line 2 and line 3",
    "multi.cmd4": "Fourth command with a continuation text from line 2\nand line 3",
    "multi.cmd5": "0\n2\n4\n6\n8\n10\n12\n14\n16\n18\n20",
    "multi.cmd6": "Fifth command with a continuation\nand a comment line in between that should be ignored",

    "multi.heredoc": "^This is a heredoc test.  \nIt should be included in the value with line wraps\n    and indentation preserved.",
    
    "multi.heredoc-double": "^This is a heredoc test. It should be included in the value without line wraps nor indentation preserved.",
    
    "multi.heredoc-comment": "^This is a heredoc test. It should not include lines starting with #",

    
}
