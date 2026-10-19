import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class PortfolioAcceptanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.projects = json.loads((ROOT / 'data' / 'projects.json').read_text(encoding='utf-8'))

    def test_four_distinct_projects_and_case_study_pages_exist(self):
        self.assertEqual(len(self.projects), 4)
        slugs = [p['slug'] for p in self.projects]
        self.assertEqual(len(set(slugs)), 4)
        for slug in slugs:
            self.assertTrue((ROOT / 'projects' / slug / 'index.html').is_file(), slug)

    def test_each_project_has_research_summary_and_local_chart_assets(self):
        for project in self.projects:
            with self.subTest(project=project['slug']):
                self.assertTrue(project.get('question'))
                self.assertTrue(project.get('method'))
                self.assertTrue(project.get('finding'))
                self.assertTrue(project.get('limitation'))
                self.assertTrue(project.get('charts'))
                for chart in project['charts']:
                    self.assertTrue((ROOT / chart['src']).is_file(), chart['src'])

    def test_clean_notebook_downloads_are_present_without_saved_outputs(self):
        paths = list((ROOT / 'notebooks').glob('*.ipynb'))
        self.assertEqual(len(paths), 4)
        for path in paths:
            notebook = json.loads(path.read_text(encoding='utf-8'))
            for cell in notebook.get('cells', []):
                if cell.get('cell_type') == 'code':
                    self.assertIsNone(cell.get('execution_count'))
                    self.assertEqual(cell.get('outputs', []), [])

    def test_home_and_case_studies_have_basic_accessible_structure(self):
        home = (ROOT / 'index.html').read_text(encoding='utf-8')
        self.assertIn('<main', home)
        self.assertIn('aria-label=', home)
        for project in self.projects:
            page = (ROOT / 'projects' / project['slug'] / 'index.html').read_text(encoding='utf-8')
            self.assertIn('<main', page)
            self.assertIn('<h1', page)
            self.assertIn('Download notebook', page)

if __name__ == '__main__':
    unittest.main()
