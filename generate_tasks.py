#!/usr/bin/env python3
"""
Generate actionable tasks from evaluation results.

This script analyzes the evaluation results and generates a structured
report with feature-level tasks for implementing missing kernel/OS functionality.
"""

import json
import sys
from typing import Dict, List, Any


class TaskGenerator:
    """Generates actionable tasks from evaluation results."""
    
    def __init__(self, results_path: str, rubric_path: str):
        """Initialize with results and rubric."""
        with open(results_path, 'r') as f:
            self.results = json.load(f)
        
        with open(rubric_path, 'r') as f:
            self.rubric = json.load(f)
    
    def generate_tasks(self, threshold: float = 70.0) -> Dict[str, Any]:
        """
        Generate tasks for components scoring below threshold.
        
        Args:
            threshold: Score threshold below which to generate tasks (0-100)
        
        Returns:
            Dictionary with tasks organized by feature area
        """
        tasks = {
            'kernel_primitives': [],
            'os_services': []
        }
        
        # Process kernel primitives
        for name, result in self.results.get('kernel_primitives', {}).items():
            score = result.get('scores', {}).get('overall', 0)
            
            if score < threshold:
                spec = self.rubric['kernel_primitives'].get(name, {})
                task = self._generate_component_tasks(name, result, spec, 'kernel')
                tasks['kernel_primitives'].append(task)
        
        # Process OS services
        for name, result in self.results.get('os_services', {}).items():
            score = result.get('scores', {}).get('overall', 0)
            
            if score < threshold:
                spec = self.rubric['os_platform_services'].get(name, {})
                task = self._generate_component_tasks(name, result, spec, 'os_service')
                tasks['os_services'].append(task)
        
        return tasks
    
    def _generate_component_tasks(self, name: str, result: Dict[str, Any],
                                  spec: Dict[str, Any], component_type: str) -> Dict[str, Any]:
        """Generate tasks for a specific component."""
        score = result.get('scores', {}).get('overall', 0)
        functions_found = result.get('functions', {}).get('found', 0)
        functions_target = result.get('functions', {}).get('target', 1)
        sloc_found = result.get('sloc', {}).get('found', 0)
        sloc_target = result.get('sloc', {}).get('target', 1)
        
        # Calculate what's missing
        missing_functions = max(0, functions_target - functions_found)
        missing_sloc = max(0, sloc_target - sloc_found)
        
        # Get manifest functions if available
        manifest_functions = spec.get('manifest_functions', [])
        
        # Generate implementation tasks
        implementation_tasks = []
        
        # Core implementation task
        if missing_functions > 0:
            implementation_tasks.append({
                'task': f'Implement core {name.replace("_", " ")} functionality',
                'description': f'Implement {missing_functions} missing functions for {spec.get("description", name)}',
                'details': [
                    f'Target functions to implement: {functions_target}',
                    f'Currently implemented: {functions_found}',
                    f'Missing: {missing_functions}',
                    f'Target SLOC: {sloc_target}',
                    f'Current SLOC: {sloc_found}'
                ],
                'priority': spec.get('criticality', 'medium')
            })
        
        # Function-specific tasks
        if manifest_functions and len(manifest_functions) > 0:
            # Group functions into logical batches
            batch_size = max(3, len(manifest_functions) // 5)  # ~5 batches
            batches = [manifest_functions[i:i + batch_size] 
                      for i in range(0, len(manifest_functions), batch_size)]
            
            for i, batch in enumerate(batches, 1):
                implementation_tasks.append({
                    'task': f'Implement {name.replace("_", " ")} functions (batch {i}/{len(batches)})',
                    'description': f'Implement the following functions: {", ".join(batch[:5])}{"..." if len(batch) > 5 else ""}',
                    'functions': batch,
                    'priority': spec.get('criticality', 'medium')
                })
        
        # Testing task
        implementation_tasks.append({
            'task': f'Add tests for {name.replace("_", " ")}',
            'description': f'Create comprehensive tests for {name.replace("_", " ")} functionality',
            'details': [
                'Write unit tests for each function',
                'Add integration tests',
                'Ensure edge cases are covered',
                f'Target test coverage: 80%+'
            ],
            'priority': 'high'
        })
        
        # Documentation task
        implementation_tasks.append({
            'task': f'Document {name.replace("_", " ")} implementation',
            'description': f'Create documentation for {name.replace("_", " ")} module',
            'details': [
                'Document function APIs',
                'Add usage examples',
                'Describe architecture and design decisions',
                'Update README if needed'
            ],
            'priority': 'medium'
        })
        
        return {
            'component': name,
            'type': component_type,
            'current_score': score,
            'weight': spec.get('weight', 1),
            'criticality': spec.get('criticality', 'medium'),
            'description': spec.get('description', ''),
            'gap_analysis': {
                'functions_gap': missing_functions,
                'sloc_gap': missing_sloc,
                'functions_progress': f'{functions_found}/{functions_target}',
                'sloc_progress': f'{sloc_found}/{sloc_target}'
            },
            'tasks': implementation_tasks
        }
    
    def generate_report(self, output_path: str = 'implementation_tasks.json',
                       threshold: float = 70.0):
        """Generate and save task report."""
        tasks = self.generate_tasks(threshold)
        
        # Calculate summary statistics
        summary = self.results.get('summary', {})
        
        report = {
            'metadata': {
                'threshold': threshold,
                'kernel_score': summary.get('kernel_primitives_score', 0),
                'os_score': summary.get('os_services_score', 0),
                'overall_score': summary.get('overall_score', 0),
                'total_files_scanned': summary.get('total_files_scanned', 0)
            },
            'tasks': tasks,
            'summary': {
                'kernel_components_needing_work': len(tasks['kernel_primitives']),
                'os_components_needing_work': len(tasks['os_services']),
                'total_components': len(tasks['kernel_primitives']) + len(tasks['os_services'])
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def print_summary(self, tasks: Dict[str, Any]):
        """Print a summary of generated tasks."""
        print("\n" + "="*70)
        print("IMPLEMENTATION TASKS SUMMARY")
        print("="*70)
        
        kernel_tasks = tasks.get('kernel_primitives', [])
        os_tasks = tasks.get('os_services', [])
        
        print(f"\nKernel Primitives needing work: {len(kernel_tasks)}")
        for comp in sorted(kernel_tasks, key=lambda x: x['weight'], reverse=True):
            print(f"  - {comp['component'].replace('_', ' ').title()}")
            print(f"    Score: {comp['current_score']:.1f}% | "
                  f"Weight: {comp['weight']} | "
                  f"Criticality: {comp['criticality']}")
            print(f"    Gap: {comp['gap_analysis']['functions_gap']} functions, "
                  f"{comp['gap_analysis']['sloc_gap']} SLOC")
            print(f"    Tasks: {len(comp['tasks'])}")
        
        print(f"\nOS Services needing work: {len(os_tasks)}")
        for comp in sorted(os_tasks, key=lambda x: x['weight'], reverse=True):
            print(f"  - {comp['component'].replace('_', ' ').title()}")
            print(f"    Score: {comp['current_score']:.1f}% | "
                  f"Weight: {comp['weight']} | "
                  f"Criticality: {comp['criticality']}")
            print(f"    Gap: {comp['gap_analysis']['functions_gap']} functions, "
                  f"{comp['gap_analysis']['sloc_gap']} SLOC")
            print(f"    Tasks: {len(comp['tasks'])}")
        
        print("\n" + "="*70)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: generate_tasks.py <evaluation_results.json> [rubric.json] [threshold]")
        print("\nGenerates actionable implementation tasks from evaluation results.")
        print("\nArguments:")
        print("  evaluation_results.json - Path to evaluation results")
        print("  rubric.json            - Path to rubric file (default: rubric.json)")
        print("  threshold              - Score threshold for task generation (default: 70.0)")
        sys.exit(1)
    
    results_file = sys.argv[1]
    rubric_file = sys.argv[2] if len(sys.argv) > 2 else 'rubric.json'
    threshold = float(sys.argv[3]) if len(sys.argv) > 3 else 70.0
    
    generator = TaskGenerator(results_file, rubric_file)
    tasks = generator.generate_tasks(threshold)
    
    generator.print_summary(tasks)
    
    report = generator.generate_report('implementation_tasks.json', threshold)
    print(f"\nTask report saved to: implementation_tasks.json")
    print(f"Total components needing work: {report['summary']['total_components']}")


if __name__ == '__main__':
    main()
