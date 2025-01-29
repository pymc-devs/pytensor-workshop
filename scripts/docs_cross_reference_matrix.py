"""
Script to obtain the PyTensor docs cross reference matrix needed for the pagerank exercise.

Should be run in the root directory of the pytensor repository.
"""
import os
import re

from collections import defaultdict

import numpy as np

# Directory containing the rst files
docs_dir = 'doc'

def find_references(verbose=False) -> dict[str, set]:
    """Find sphinx referenced (:ref:`... <>`) in each page"""

    # Regular expression to match :ref: references
    ref_pattern = re.compile(r':ref:`(?:<([^`]+)>|([^`]+))`')

    brackets_pattern = re.compile(r'^(?:[^<]*<([^>]+)>|(.+))$')

    # Dictionary to store the tally of unique references for each page
    ref_tally = defaultdict(set)

    # Iterate over all files in the documentation directory
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.rst'):
                file_path = os.path.join(root, file)
                # print(file_path)
                with open(file_path, 'r', encoding='utf-8') as f:
                    ref_tally[file] = set()
                    content = f.read()
                    # Find all :ref: references in the file
                    refs = ref_pattern.findall(content)
                    # Add the unique references to the tally
                    for ref in refs:
                        result = ref[1]
                        match = brackets_pattern.match(result)
                        if match:
                            result = match.group(1) or match.group(2)
                        ref_tally[file].add(result)

    # Print the tally of unique references for each page
    if verbose:
        for file, refs in ref_tally.items():
            print(f'{file}: {sorted(refs)}')

    return ref_tally

def find_alias_definitions(verbose=False) -> dict[str, list[str]]:
    """Find what aliases are defined in each page"""

    # Regular expression to match reference aliases
    alias_pattern = re.compile(r'\.\. _([^:]+):')

    # Dictionary to store the aliases for each page
    alias_tally = defaultdict(list)

    # Iterate over all files in the documentation directory
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.rst'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Find all reference aliases in the file
                    aliases = alias_pattern.findall(content)
                    # Add the aliases to the tally
                    for alias in aliases:
                        alias_tally[file].append(alias)

    # Print the aliases for each page
    if verbose:
        for file, aliases in alias_tally.items():
            if aliases:
                print(f'{file}: {sorted(aliases)}')

    return alias_tally

def compute_cross_reference_count_matrix(verbose=False) -> tuple[list[str], np.ndarray]:
    """Define matrix of how many references exist from one page to another"""

    refs = find_references()
    alias = find_alias_definitions()

    rev_alias = {}
    for k in alias:
        for v in alias[k]:
            if v in rev_alias:
                if k != rev_alias[v]:
                    print(f'Warning: Alias {v} defined in {k} and {rev_alias[v]}')
            rev_alias[v] = k

    # Create a matrix M of size N x N, where N is the number of pages
    # Each row corresponds to a page, and each column corresponds to the number of references that that page has to the row page
    unique_sorted_refs = sorted(refs)
    M = {ref: {other_ref: 0 for other_ref in unique_sorted_refs} for ref in unique_sorted_refs}

    for from_page, to_pages_alias in refs.items():
        for to_page_alias in to_pages_alias:
            try:
                to_page = rev_alias[to_page_alias]
            except KeyError:
                raise ValueError(f'Alias {to_page_alias} not defined')
            if to_page not in unique_sorted_refs:
                raise ValueError(f'Reference page {to_page} not found')
            if from_page == to_page:
                continue
            M[from_page][to_page] += 1

    if verbose:
        for row, cols in M.items():
            print(row, list(cols.values()))

    N = np.array([list(row.values()) for row in M.values()])
    return list(M.keys()), N

if __name__ == '__main__':
    keys, M = compute_cross_reference_count_matrix(verbose=True)
    np.savetxt('docs_cros_reference_matrix.txt', M, fmt='%d', header=",".join(keys))