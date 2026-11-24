#!/usr/bin/env python3
"""
textcase.py - Convert text between naming and writing cases.
"""

import argparse
import re
import sys


def split_into_words(text, keep_acronyms=False):
    """
    Split text into words based on various delimiters and case boundaries.
    
    Rules:
    - Split on spaces, underscores, hyphens, dots, slashes
    - Split camel humps (lower->upper boundary)
    - Split acronym->word boundary (e.g., "HTTPServer" -> HTTP, Server)
    - Digits stay attached to preceding word
    - Apostrophes are dropped
    """
    # First, replace all delimiters with spaces
    delimiters = r'[\s_.\-/]'
    text = re.sub(delimiters, ' ', text)
    
    # Remove apostrophes
    text = text.replace("'", "")
    
    words = []
    for token in text.split():
        if not token:
            continue
        
        # Split on case boundaries
        # Handle acronym boundaries: uppercase followed by lowercase (e.g., HTTPServer -> HTTP, Server)
        # Handle camel hump: lowercase followed by uppercase (e.g., parseHTTP -> parse, HTTP)
        
        # Pattern to split:
        # 1. Lowercase followed by uppercase (camel hump): aA -> a, A
        # 2. Uppercase followed by lowercase when preceded by uppercase (acronym): HTTPServer -> HTTP, Server
        #    This is: (uppercase)(uppercase+lowercase) -> split before the last uppercase group
        
        # We need to handle:
        # - "HTTPServer" -> ["HTTP", "Server"]
        # - "parseHTTPResponse" -> ["parse", "HTTP", "Response"]
        # - "utf8" -> ["utf8"]
        # - "version2final" -> ["version2", "final"]
        
        # Strategy: use regex to find split points
        # Split before:
        # - An uppercase letter that follows a lowercase letter (camel hump)
        # - An uppercase letter that is followed by lowercase letters and preceded by uppercase letters (acronym boundary)
        
        # More precisely:
        # Split at position i if:
        # - token[i].isupper() and i > 0 and token[i-1].islower() (camel hump)
        # - token[i].isupper() and i > 0 and token[i-1].isupper() and 
        #   there exists j > i such that token[j].islower() (acronym boundary)
        
        # Actually, let's think differently:
        # We want to split "HTTPServer" into ["HTTP", "Server"]
        # The split is before "Server" because "HTTP" is all-caps and "Server" starts with uppercase then lowercase
        
        # Pattern: split before [A-Z][a-z] if preceded by [A-Z]+
        # Also split before [A-Z] if preceded by [a-z]
        
        # Let's use a different approach:
        # Insert splits at:
        # 1. Lower->Upper boundary
        # 2. Acronym->Word boundary (all-caps word followed by capitalized word)
        
        # Regex approach:
        # Match: (lowercase)(uppercase) -> split between them
        # Match: (all-caps)(Capitalized) -> split between them
        
        # Let's build the pattern:
        # We want to split before uppercase letters that:
        # - Follow a lowercase letter, OR
        # - Are part of a capitalized word (uppercase followed by lowercase) and preceded by all-caps
        
        # Simpler: use lookahead/lookbehind
        # Split before: (?<=[a-z])(?=[A-Z]) | (?<=[A-Z])(?=[A-Z][a-z])
        
        # But we need to be careful with the second pattern
        # "HTTPServer" -> we want to split before "Server"
        # The pattern (?<=[A-Z])(?=[A-Z][a-z]) would match before "S" in "Server"
        # because it's preceded by "P" (uppercase) and followed by "Se" (uppercase+lowercase)
        
        # Let's test:
        # "parseHTTPResponse"
        # - "parse" -> no split
        # - "HTTPResponse" -> split before "R" (camel hump from P to R? No, P is uppercase, R is uppercase)
        #   Actually, we want: parse, HTTP, Response
        #   So we need to split before "H" (camel hump from e to H)
        #   And before "R" (acronym boundary: HTTP is all-caps, Response is capitalized)
        
        # Pattern 1: (?<=[a-z])(?=[A-Z]) - split before uppercase following lowercase
        # Pattern 2: (?<=[A-Z])(?=[A-Z][a-z]) - split before capitalized word following all-caps
        
        # Apply splits
        result = []
        current = ""
        i = 0
        while i < len(token):
            current += token[i]
            
            # Check for camel hump (lowercase -> uppercase)
            if i < len(token) - 1:
                if token[i].islower() and token[i+1].isupper():
                    result.append(current)
                    current = ""
            
            # Check for acronym boundary (all-caps -> capitalized)
            if i < len(token) - 1 and len(current) >= 2:
                # Check if current is all-caps
                if current.isupper():
                    # Check if next char starts a capitalized word
                    if token[i+1].isupper() and (i+2 >= len(token) or token[i+2].islower()):
                        result.append(current)
                        current = ""
            
            i += 1
        
        if current:
            result.append(current)
        
        words.extend(result)
    
    return words


def convert_case(words, target_case, keep_acronyms=False):
    """Convert a list of words to the specified case."""
    if not words:
        return ""
    
    if keep_acronyms:
        # Check if any word is an acronym (all-caps, length >= 2)
        # In output, preserve all-caps for camel/pascal
        pass
    
    if target_case == 'camel':
        if not words:
            return ""
        result = [words[0].lower()]
        for word in words[1:]:
            if len(word) >= 2 and word.isupper() and keep_acronyms:
                result.append(word)
            else:
                result.append(word.capitalize())
        return ''.join(result)
    
    elif target_case == 'pascal':
        if not words:
            return ""
        result = []
        for word in words:
            if len(word) >= 2 and word.isupper() and keep_acronyms:
                result.append(word)
            else:
                result.append(word.capitalize())
        return ''.join(result)
    
    elif target_case == 'snake':
        return '_'.join(word.lower() for word in words)
    
    elif target_case == 'kebab':
        return '-'.join(word.lower() for word in words)
    
    elif target_case == 'constant':
        return '_'.join(word.upper() for word in words)
    
    elif target_case == 'title':
        return ' '.join(word.capitalize() for word in words)
    
    elif target_case == 'sentence':
        if not words:
            return ""
        result = [words[0].capitalize()]
        result.extend(word.lower() for word in words[1:])
        return ' '.join(result)
    
    elif target_case == 'lower':
        return ' '.join(word.lower() for word in words)
    
    elif target_case == 'upper':
        return ' '.join(word.upper() for word in words)
    
    elif target_case == 'dot':
        return '.'.join(word.lower() for word in words)
    
    elif target_case == 'path':
        return '/'.join(word.lower() for word in words)
    
    elif target_case == 'train':
        return '-'.join(word.capitalize() for word in words)
    
    else:
        raise ValueError(f"Unknown case: {target_case}")


def main():
    parser = argparse.ArgumentParser(
        description='Convert text between naming and writing cases.'
    )
    parser.add_argument(
        'text',
        nargs='*',
        help='Text to convert. If omitted, reads from stdin.'
    )
    parser.add_argument(
        '--to',
        required=True,
        choices=['camel', 'pascal', 'snake', 'kebab', 'constant', 'title', 
                 'sentence', 'lower', 'upper', 'dot', 'path', 'train'],
        help='Target case format.'
    )
    parser.add_argument(
        '--keep-acronyms',
        action='store_true',
        help='Preserve all-caps words in camel/pascal output.'
    )
    
    args = parser.parse_args()
    
    # Get input text
    if args.text:
        input_text = ' '.join(args.text)
    else:
        input_text = sys.stdin.read()
    
    # Handle empty input
    if not input_text.strip():
        print()
        return
    
    # Split into words
    words = split_into_words(input_text, keep_acronyms=args.keep_acronyms)
    
    # Convert case
    result = convert_case(words, args.to, keep_acronyms=args.keep_acronyms)
    
    print(result)


if __name__ == '__main__':
    main()
