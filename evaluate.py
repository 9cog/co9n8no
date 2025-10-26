#!/usr/bin/env python3
"""
Kernel and OS Platform Services Evaluation Tool

This tool evaluates a codebase against a rubric of kernel primitives
and OS platform services, assigning scores based on evidence found in the code.
"""

import json
import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any


class KernelEvaluator:
    """Evaluates kernel and OS implementations against a rubric."""
    
    def __init__(self, rubric_path: str):
        """Initialize with a rubric file."""
        with open(rubric_path, 'r') as f:
            self.rubric = json.load(f)
        
        self.kernel_primitives = self.rubric['kernel_primitives']
        self.os_services = self.rubric['os_platform_services']
    
    def scan_directory(self, path: str, extensions: List[str] = None) -> Dict[str, str]:
        """
        Scan directory for source files.
        
        Args:
            path: Directory path to scan
            extensions: List of file extensions to include (e.g., ['.c', '.h'])
        
        Returns:
            Dictionary mapping file paths to their contents
        """
        if extensions is None:
            extensions = ['.c', '.h', '.cpp', '.cc', '.s', '.asm']
        
        files = {}
        path_obj = Path(path)
        
        if not path_obj.exists():
            print(f"Error: Path {path} does not exist")
            return files
        
        for ext in extensions:
            for file_path in path_obj.rglob(f'*{ext}'):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        files[str(file_path)] = f.read()
                except Exception as e:
                    print(f"Warning: Could not read {file_path}: {e}")
        
        return files
    
    def count_functions(self, content: str) -> int:
        """
        Count function definitions in code.
        Simple heuristic looking for common function patterns.
        """
        # Match C/C++ function definitions
        pattern = r'\b\w+\s+\w+\s*\([^)]*\)\s*\{'
        matches = re.findall(pattern, content)
        return len(matches)
    
    def count_sloc(self, content: str) -> int:
        """
        Count source lines of code (excluding comments and blank lines).
        """
        lines = content.split('\n')
        sloc = 0
        in_multiline_comment = False
        
        for line in lines:
            stripped = line.strip()
            
            # Handle multiline comments
            if '/*' in stripped:
                in_multiline_comment = True
            if '*/' in stripped:
                in_multiline_comment = False
                continue
            
            if in_multiline_comment:
                continue
            
            # Skip empty lines and single-line comments
            if not stripped or stripped.startswith('//') or stripped.startswith('#'):
                continue
            
            sloc += 1
        
        return sloc
    
    def find_evidence(self, files: Dict[str, str], evidence_cues: List[str]) -> Dict[str, Any]:
        """
        Find evidence of implementation based on cues.
        
        Returns:
            Dictionary with evidence statistics
        """
        total_matches = 0
        matched_files = set()
        cue_matches = {cue: 0 for cue in evidence_cues}
        
        for file_path, content in files.items():
            content_lower = content.lower()
            file_matched = False
            
            for cue in evidence_cues:
                # Look for the cue as a whole word
                pattern = r'\b' + re.escape(cue.lower()) + r'\b'
                matches = len(re.findall(pattern, content_lower))
                
                if matches > 0:
                    cue_matches[cue] += matches
                    total_matches += matches
                    file_matched = True
            
            if file_matched:
                matched_files.add(file_path)
        
        return {
            'total_matches': total_matches,
            'matched_files': len(matched_files),
            'cue_matches': cue_matches
        }
    
    def evaluate_component(self, name: str, spec: Dict[str, Any], 
                          files: Dict[str, str]) -> Dict[str, Any]:
        """
        Evaluate a single kernel primitive or OS service.
        
        Returns:
            Dictionary with evaluation results
        """
        evidence = self.find_evidence(files, spec['evidence_cues'])
        
        # Calculate total functions and SLOC in matched files
        total_functions = 0
        total_sloc = 0
        
        for file_path, content in files.items():
            # Only count files that have evidence
            if any(cue.lower() in content.lower() for cue in spec['evidence_cues']):
                total_functions += self.count_functions(content)
                total_sloc += self.count_sloc(content)
        
        # Calculate scores
        evidence_score = min(100, (evidence['total_matches'] / 10) * 100)
        
        function_ratio = total_functions / spec['target_functions'] if spec['target_functions'] > 0 else 0
        function_score = min(100, function_ratio * 100)
        
        sloc_ratio = total_sloc / spec['target_sloc'] if spec['target_sloc'] > 0 else 0
        sloc_score = min(100, sloc_ratio * 100)
        
        # Weighted average (evidence: 40%, functions: 30%, SLOC: 30%)
        overall_score = (evidence_score * 0.4 + function_score * 0.3 + sloc_score * 0.3)
        
        return {
            'name': name,
            'weight': spec['weight'],
            'criticality': spec['criticality'],
            'evidence': evidence,
            'functions': {
                'found': total_functions,
                'target': spec['target_functions'],
                'score': function_score
            },
            'sloc': {
                'found': total_sloc,
                'target': spec['target_sloc'],
                'score': sloc_score
            },
            'scores': {
                'evidence': evidence_score,
                'functions': function_score,
                'sloc': sloc_score,
                'overall': overall_score
            }
        }
    
    def evaluate(self, source_path: str) -> Dict[str, Any]:
        """
        Evaluate a codebase against the full rubric.
        
        Returns:
            Complete evaluation results
        """
        print(f"Scanning source directory: {source_path}")
        files = self.scan_directory(source_path)
        print(f"Found {len(files)} source files")
        
        if not files:
            print("Warning: No source files found!")
        
        results = {
            'kernel_primitives': {},
            'os_services': {},
            'summary': {}
        }
        
        # Evaluate kernel primitives
        print("\nEvaluating kernel primitives...")
        kernel_weighted_score = 0
        total_kernel_weight = 0
        
        for name, spec in self.kernel_primitives.items():
            result = self.evaluate_component(name, spec, files)
            results['kernel_primitives'][name] = result
            kernel_weighted_score += result['scores']['overall'] * spec['weight']
            total_kernel_weight += spec['weight']
            print(f"  {name}: {result['scores']['overall']:.1f}%")
        
        # Evaluate OS services
        print("\nEvaluating OS platform services...")
        os_weighted_score = 0
        total_os_weight = 0
        
        for name, spec in self.os_services.items():
            result = self.evaluate_component(name, spec, files)
            results['os_services'][name] = result
            os_weighted_score += result['scores']['overall'] * spec['weight']
            total_os_weight += spec['weight']
            print(f"  {name}: {result['scores']['overall']:.1f}%")
        
        # Calculate summary
        results['summary'] = {
            'kernel_primitives_score': kernel_weighted_score / total_kernel_weight if total_kernel_weight > 0 else 0,
            'os_services_score': os_weighted_score / total_os_weight if total_os_weight > 0 else 0,
            'total_files_scanned': len(files)
        }
        
        overall = (results['summary']['kernel_primitives_score'] + 
                   results['summary']['os_services_score']) / 2
        results['summary']['overall_score'] = overall
        
        return results
    
    def print_summary(self, results: Dict[str, Any]):
        """Print a summary of evaluation results."""
        print("\n" + "="*70)
        print("EVALUATION SUMMARY")
        print("="*70)
        
        summary = results['summary']
        print(f"\nKernel Primitives Score: {summary['kernel_primitives_score']:.1f}%")
        print(f"OS Services Score:       {summary['os_services_score']:.1f}%")
        print(f"Overall Score:           {summary['overall_score']:.1f}%")
        print(f"\nTotal Files Scanned:     {summary['total_files_scanned']}")
        
        print("\n" + "="*70)
        print("KERNEL PRIMITIVES DETAILS")
        print("="*70)
        
        for name, result in results['kernel_primitives'].items():
            print(f"\n{name.replace('_', ' ').title()}")
            print(f"  Weight: {result['weight']}, Criticality: {result['criticality']}")
            print(f"  Overall Score: {result['scores']['overall']:.1f}%")
            print(f"  Evidence matches: {result['evidence']['total_matches']} in {result['evidence']['matched_files']} files")
            print(f"  Functions: {result['functions']['found']}/{result['functions']['target']} ({result['functions']['score']:.1f}%)")
            print(f"  SLOC: {result['sloc']['found']}/{result['sloc']['target']} ({result['sloc']['score']:.1f}%)")
        
        print("\n" + "="*70)
        print("OS PLATFORM SERVICES DETAILS")
        print("="*70)
        
        for name, result in results['os_services'].items():
            print(f"\n{name.replace('_', ' ').title()}")
            print(f"  Weight: {result['weight']}, Criticality: {result['criticality']}")
            print(f"  Overall Score: {result['scores']['overall']:.1f}%")
            print(f"  Evidence matches: {result['evidence']['total_matches']} in {result['evidence']['matched_files']} files")
            print(f"  Functions: {result['functions']['found']}/{result['functions']['target']} ({result['functions']['score']:.1f}%)")
            print(f"  SLOC: {result['sloc']['found']}/{result['sloc']['target']} ({result['sloc']['score']:.1f}%)")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: evaluate.py <source_directory> [rubric.json]")
        print("\nEvaluates a kernel/OS codebase against a rubric.")
        sys.exit(1)
    
    source_dir = sys.argv[1]
    rubric_file = sys.argv[2] if len(sys.argv) > 2 else 'rubric.json'
    
    if not os.path.exists(rubric_file):
        print(f"Error: Rubric file '{rubric_file}' not found")
        sys.exit(1)
    
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' not found")
        sys.exit(1)
    
    evaluator = KernelEvaluator(rubric_file)
    results = evaluator.evaluate(source_dir)
    evaluator.print_summary(results)
    
    # Save results to JSON
    output_file = 'evaluation_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nDetailed results saved to: {output_file}")


if __name__ == '__main__':
    main()
